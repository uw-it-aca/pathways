# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import hashlib
import io
import json
import socket
import tempfile
from pathlib import Path
from unittest import skipUnless
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, connection
from django.test import SimpleTestCase, TestCase
from google.api_core.exceptions import Forbidden, PreconditionFailed

from pathways.models.course import Course
from pathways.models.data_import import DataImport
from pathways.models.data_release_import import DataReleaseImport
from pathways.models.major import Major, SimilarMajor
from pathways.release_download import download_release
from pathways.release_import import import_release
from pathways.search import search
from pathways.search_release import (
    RELEASE_FILES_BY_VERSION,
    ReleaseValidationError,
    verify_release,
)


def write_release(root, version="2.0"):
    release = root / "release"
    release.mkdir()
    fixtures = Path("pathways/tests/commands/mock_import_files")
    for name in RELEASE_FILES_BY_VERSION[version]:
        if name.endswith(".pkl"):
            content = b"never unpickle"
        elif name == "search-index.tar.gz":
            content = b"legacy archive bytes are never opened"
        elif name == "similar_majors.csv":
            content = (
                b"credential_code,STEM_ind,similar_credential_code,similar_STEM_ind,"
                b"similarity,similarity_group\n"
                b"INFO-40-1-6,1,INFO-40-1-6,1,0.8,High\n")
        else:
            content = (fixtures / name).read_bytes()
        (release / name).write_bytes(content)
    manifest = {
        "schema_version": version, "release_id": "test-release", "artifacts": {},
    }
    for path in release.iterdir():
        content = path.read_bytes()
        manifest["artifacts"][path.name] = {
            "version_path": f"releases/test-release/{path.name}",
            "size_bytes": len(content),
            "checksum_sha256": hashlib.sha256(content).hexdigest(),
        }
    (release / "manifest.json").write_text(json.dumps(manifest))
    return release, manifest


class DownloadReleaseTest(SimpleTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.release, self.manifest = write_release(self.root)
        self.output = self.root / "downloaded"
        self.client = self.enterContext(patch("pathways.release_download.storage.Client"))
        self.bucket = self.client.return_value.bucket.return_value
        self.blobs = {}
        for path in self.release.iterdir():
            content = path.read_bytes()
            blob = MagicMock(size=len(content), generation=123)
            blob.download_as_bytes.return_value = content
            self.blobs[f"releases/test-release/{path.name}"] = blob
        self.bucket.get_blob.side_effect = self.blobs.get

    def download(self, **kwargs):
        return download_release("test-bucket", "test-release", self.output, **kwargs)

    def assert_clean(self):
        self.assertFalse(self.output.exists())
        self.assertFalse(list(self.root.glob(".download-release-*")))

    def test_generation_pinned_download_verifies_every_file(self):
        self.assertEqual(self.download(), self.manifest)
        self.assertEqual(
            {path.name for path in self.output.iterdir()},
            {*RELEASE_FILES_BY_VERSION["2.0"], "manifest.json"})
        for key, blob in self.blobs.items():
            with self.subTest(key=key):
                blob.download_as_bytes.assert_called_once_with(if_generation_match=123)
        self.assertEqual(
            verify_release(self.output, release_id="test-release")[0], self.manifest)

    def test_prefix_and_command(self):
        self.bucket.get_blob.side_effect = lambda key: self.blobs.get(key.removeprefix("app/"))
        call_command(
            "download_data_release", bucket="bucket", prefix="app/",
            release_id="test-release", output_dir=str(self.output),
            stdout=io.StringIO())
        self.bucket.get_blob.assert_any_call("app/releases/test-release/manifest.json")

    def test_missing_or_changed_object_does_not_leave_partial_release(self):
        key = "releases/test-release/course_data.json"
        blob = self.blobs.pop(key)
        with self.assertRaises(FileNotFoundError):
            self.download()
        self.assert_clean()
        self.blobs[key] = blob
        blob.download_as_bytes.side_effect = PreconditionFailed("generation changed")
        with self.assertRaises(PreconditionFailed):
            self.download()
        self.assert_clean()

    def test_missing_generation_and_oversized_download_are_rejected(self):
        blob = self.blobs["releases/test-release/course_data.json"]
        blob.generation = None
        with self.assertRaisesRegex(ReleaseValidationError, "no generation"):
            self.download()
        blob.download_as_bytes.assert_not_called()
        self.assert_clean()
        blob.generation = 123
        blob.download_as_bytes.return_value = b"x" * (blob.size + 1)
        with self.assertRaisesRegex(ReleaseValidationError, "size limit"):
            self.download()
        self.assert_clean()

    def test_corrupt_object_fails_even_with_valid_outer_metadata(self):
        blob = self.blobs["releases/test-release/coi_scores.csv"]
        blob.download_as_bytes.return_value = b"x" * blob.size
        with self.assertRaisesRegex(ReleaseValidationError, "checksum"):
            self.download()
        self.assert_clean()

    def test_invalid_manifest_paths_and_versions_are_rejected_before_artifacts(self):
        manifest_blob = self.blobs["releases/test-release/manifest.json"]
        for kind in ("identity", "path", "version", "inventory"):
            manifest = json.loads(json.dumps(self.manifest))
            if kind == "identity":
                manifest["release_id"] = "other"
            elif kind == "path":
                manifest["artifacts"]["coi_scores.csv"]["version_path"] = "../escape"
            elif kind == "version":
                manifest["schema_version"] = "3.0"
            else:
                manifest["artifacts"].pop("similar_majors.csv")
            manifest_blob.download_as_bytes.return_value = json.dumps(manifest).encode()
            manifest_blob.size = len(manifest_blob.download_as_bytes.return_value)
            self.bucket.get_blob.reset_mock()
            with self.subTest(kind=kind), self.assertRaises(ReleaseValidationError):
                self.download()
            self.assertEqual(self.bucket.get_blob.call_count, 1)
            self.assert_clean()

    def test_size_limits_and_existing_output(self):
        manifest = self.blobs["releases/test-release/manifest.json"]
        manifest.size = 1024 * 1024 + 1
        with self.assertRaisesRegex(ReleaseValidationError, "size limit"):
            self.download()
        manifest.download_as_bytes.assert_not_called()
        self.assert_clean()
        self.output.mkdir()
        marker = self.output / "keep"
        marker.write_text("active")
        with self.assertRaises(FileExistsError):
            self.download()
        self.assertEqual(marker.read_text(), "active")

    def test_invalid_identity_prefix_and_auth_never_fall_back(self):
        for release_id, prefix in (("../escape", ""), ("test-release", "app/../bad")):
            with self.assertRaises(ValueError):
                download_release("bucket", release_id, self.output, prefix=prefix)
        self.client.assert_not_called()
        self.bucket.get_blob.side_effect = Forbidden("denied")
        with self.assertRaises(CommandError):
            call_command(
                "download_data_release", bucket="bucket",
                release_id="test-release", output_dir=str(self.output))
        self.assert_clean()

    def test_legacy_downloads_verify_archive_bytes_without_opening_them(self):
        content = b"opaque legacy archive"
        self.manifest["artifacts"]["search-index.tar.gz"] = {
            "version_path": "releases/test-release/search-index.tar.gz",
            "size_bytes": len(content),
            "checksum_sha256": hashlib.sha256(content).hexdigest(),
        }
        archive = MagicMock(size=len(content), generation=123)
        archive.download_as_bytes.return_value = content
        self.blobs["releases/test-release/search-index.tar.gz"] = archive
        for version in ("1.1", "1.0"):
            with self.subTest(version=version):
                self.output = self.root / version
                self.manifest["schema_version"] = version
                self.manifest["search_index"] = {"ignored": True}
                if version == "1.0":
                    self.manifest["artifacts"].pop("similar_majors.csv")
                    self.blobs.pop("releases/test-release/similar_majors.csv")
                blob = self.blobs["releases/test-release/manifest.json"]
                blob.download_as_bytes.return_value = json.dumps(self.manifest).encode()
                blob.size = len(blob.download_as_bytes.return_value)
                with patch("tarfile.open", side_effect=AssertionError("no extraction")):
                    self.assertEqual(self.download(), self.manifest)
                self.output = self.root / f"{version}-corrupt"
                archive.download_as_bytes.return_value = b"x" * len(content)
                with self.assertRaisesRegex(ReleaseValidationError, "checksum"):
                    self.download()
                self.assert_clean()
                archive.download_as_bytes.return_value = content


class ImportReleaseTest(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.release, self.manifest = write_release(self.root)

    def import_release(self):
        return import_release(self.release, release_id="test-release")

    @skipUnless(connection.vendor == "postgresql", "PostgreSQL search required")
    def test_imported_release_is_searchable_without_an_index_build(self):
        self.assertTrue(self.import_release())
        course = search("info201", types=["course"])
        self.assertEqual(course["course_matches"][0]["id"], "INFO 201")
        self.assertTrue(course["course_matches"][0]["is_course"])
        self.assertEqual(search("data science", types=["course"])[
            "text_matches"][0]["id"],
                         "INFO 201")
        majors = search("informatics", types=["major"])
        self.assertEqual(majors["major_matches"][0]["id"], "INFO-40-1-6")

    def test_legacy_1_1_import_uses_data_without_opening_archive_or_pickles(self):
        legacy = self.root / "legacy"
        legacy.mkdir()
        self.release, self.manifest = write_release(legacy, version="1.1")
        with patch("tarfile.open", side_effect=AssertionError("no extraction")), patch(
                "pickle.loads", side_effect=AssertionError("no unpickling")):
            self.assertTrue(self.import_release())
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(DataReleaseImport.objects.count(), 1)

    def test_legacy_archive_corruption_is_rejected_before_database_access(self):
        legacy = self.root / "legacy"
        legacy.mkdir()
        self.release, self.manifest = write_release(legacy, version="1.1")
        (self.release / "search-index.tar.gz").write_bytes(b"corrupt")
        with self.assertNumQueries(0), self.assertRaisesRegex(
                ReleaseValidationError, "checksum"):
            self.import_release()
        self.assertFalse(DataReleaseImport.objects.exists())

    def test_import_uses_verified_snapshot_not_reread_files(self):
        def verify_then_change_source(*args, **kwargs):
            verified = verify_release(*args, **kwargs)
            (self.release / "course_data.json").write_bytes(b"corrupt after verification")
            (self.release / "manifest.json").write_bytes(b"corrupt after verification")
            return verified

        with patch("pathways.release_import.verify_release",
                   side_effect=verify_then_change_source):
            self.assertTrue(self.import_release())
        self.assertEqual(Course.objects.count(), 2)
        expected = hashlib.sha256(json.dumps(
            self.manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(DataReleaseImport.objects.get().manifest_sha256, expected)

    def test_import_is_offline_idempotent_and_preserves_existing_semantics(self):
        with patch.object(socket, "socket", side_effect=AssertionError("network")):
            self.assertTrue(self.import_release())
        self.assertEqual(Course.objects.count(), 2)
        self.assertTrue(Course.objects.get(course_id="INFO 201").is_gateway)
        self.assertTrue(Course.objects.get(course_id="INFO 301").is_bottleneck)
        self.assertEqual(Course.objects.get(course_id="INFO 201").coi_score, 0.1)
        major = Major.objects.get()
        self.assertEqual(major.career_center_major, "informatics")
        self.assertTrue(major.is_stem)
        self.assertEqual(SimilarMajor.objects.count(), 1)
        self.assertEqual(DataReleaseImport.objects.count(), 1)
        self.assertEqual(DataImport.objects.count(), 9)
        timestamp = DataReleaseImport.objects.get().imported_on
        with patch(
            "pathways.data_import.import_course_data",
            side_effect=AssertionError("must be a no-op"),
        ):
            self.assertFalse(self.import_release())
        self.assertEqual(DataReleaseImport.objects.get().imported_on, timestamp)

    def test_late_failure_rolls_back_catalog_relationships_and_markers(self):
        self.import_release()
        before_courses = list(Course.objects.values())
        before_majors = list(Major.objects.values())
        before_similar = list(SimilarMajor.objects.values())
        before_markers = list(DataImport.objects.values())
        before_release = list(DataReleaseImport.objects.values())
        # Force an otherwise idempotent reimport after a legacy marker changes.
        DataImport.objects.filter(type="course").update(hash="changed")
        expected_markers = list(DataImport.objects.values())
        with patch(
            "pathways.data_import.import_stem_from_similar_majors",
            side_effect=IntegrityError("late failure"),
        ), self.assertRaises(IntegrityError):
            self.import_release()
        self.assertEqual(list(Course.objects.values()), before_courses)
        self.assertEqual(list(Major.objects.values()), before_majors)
        self.assertEqual(list(SimilarMajor.objects.values()), before_similar)
        self.assertNotEqual(expected_markers, before_markers)
        self.assertEqual(list(DataImport.objects.values()), expected_markers)
        self.assertEqual(list(DataReleaseImport.objects.values()), before_release)

    def test_first_import_failure_does_not_record_success(self):
        with patch(
            "pathways.data_import.import_stem_from_similar_majors",
            side_effect=IntegrityError("late failure"),
        ), self.assertRaises(IntegrityError):
            self.import_release()
        self.assertFalse(Course.objects.exists())
        self.assertFalse(Major.objects.exists())
        self.assertFalse(DataImport.objects.exists())
        self.assertFalse(DataReleaseImport.objects.exists())

    def test_corruption_or_legacy_release_fails_without_database_changes(self):
        data = (self.release / "curric_data.json").read_bytes()
        (self.release / "curric_data.json").write_bytes(b"corrupt")
        with self.assertRaises(ReleaseValidationError):
            self.import_release()
        self.assertFalse(DataImport.objects.exists())
        (self.release / "curric_data.json").write_bytes(data)
        self.manifest["schema_version"] = "1.0"
        self.manifest["artifacts"].pop("similar_majors.csv")
        content = b"opaque legacy archive"
        (self.release / "search-index.tar.gz").write_bytes(content)
        self.manifest["artifacts"]["search-index.tar.gz"] = {
            "version_path": "releases/test-release/search-index.tar.gz",
            "size_bytes": len(content),
            "checksum_sha256": hashlib.sha256(content).hexdigest(),
        }
        (self.release / "manifest.json").write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ReleaseValidationError, "1.1 or 2.0"):
            self.import_release()
        self.assertFalse(DataImport.objects.exists())

    def test_reused_release_id_with_different_manifest_is_rejected(self):
        self.import_release()
        self.manifest["unexpected_change"] = True
        (self.release / "manifest.json").write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ReleaseValidationError, "identity changed"):
            self.import_release()
        self.assertEqual(Course.objects.count(), 2)

    def test_confirmation_required_and_command_reports_committed_catalog(self):
        with self.assertRaisesRegex(CommandError, "confirm-replace-data"):
            call_command(
                "import_data_release", release_dir=str(self.release),
                release_id="test-release")
        self.assertFalse(DataImport.objects.exists())
        before_paths = set(self.root.rglob("*"))
        output = io.StringIO()
        with patch("tarfile.open", side_effect=AssertionError("no archive access")), patch(
            "pickle.loads", side_effect=AssertionError("no unpickling")):
            call_command(
                "import_data_release", release_dir=str(self.release),
                release_id="test-release", confirm_replace_data=True,
            stdout=output)
        self.assertEqual(set(self.root.rglob("*")), before_paths)
        self.assertIn("no index activation is needed", output.getvalue())

    def test_malformed_csvs_are_reported_before_table_replacement(self):
        for name, content in (
                ("similar_majors.csv", b"bad,header\n"),
                ("similar_majors.csv", (
                    b"credential_code,STEM_ind,similar_credential_code,similar_STEM_ind,"
                    b"similarity,similarity_group\n"
                    b"INFO-40-1-6,1,INFO-40-1-6,1,nan,High\n")),
                ("admit_major_mapping.csv", b"only-one-column\n")):
            original = (self.release / name).read_bytes()
            original_info = self.manifest["artifacts"][name]
            (self.release / name).write_bytes(content)
            self.manifest["artifacts"][name] = {
                **original_info, "size_bytes": len(content),
                "checksum_sha256": hashlib.sha256(content).hexdigest(),
            }
            (self.release / "manifest.json").write_text(json.dumps(self.manifest))
            with self.subTest(name=name), self.assertRaises(CommandError):
                call_command(
                    "import_data_release", release_dir=str(self.release),
                    release_id="test-release", confirm_replace_data=True,
                    stdout=io.StringIO())
            self.assertFalse(DataImport.objects.exists())
            self.assertFalse(Major.objects.exists())
            (self.release / name).write_bytes(original)
            self.manifest["artifacts"][name] = original_info
