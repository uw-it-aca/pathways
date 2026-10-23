# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import hashlib
import io
import json
import socket
import tarfile
import tempfile
from pathlib import Path
from unittest.mock import patch

from dawgpath_search import IndexValidationError, build_index, open_index
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase

from pathways.search import course_id_search, major_title_search, text_search
from pathways.search_release import RELEASE_FILES, prepare_release


class PrepareSearchReleaseTest(SimpleTestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.release = self.root / "release"
        self.release.mkdir()
        self.output = self.root / "prepared"
        files = {
            "course_data.json": json.dumps([{
                "course_id": "INFO 201", "course_title": "Data Science",
                "course_description": "Analyzing information",
                "course_campus": "seattle",
            }]).encode(),
            "major_data.json": json.dumps({"INFO": {
                "credential_code": "INFO-0-1-6", "major_code": "INFO",
                "credential_title": "Informatics",
                "credential_description": "Information studies",
                "major_campus": "Seattle",
            }}).encode(),
            "coi_scores.csv": b"course_id,score\nINFO 201,0.12\n",
            "gateway_courses.csv": b"course,dept_abbr,course_no\nINFO201,INFO,201\n",
            "bottleneck_courses.csv": b"course,dept_abbv,course_no\n",
            "curric_data.json": b"[]",
            "admit_major_mapping.csv": b"INFO-0-1-6,informatics\n",
            "course_prereq_data.pkl": b"never unpickle",
            "prereq_data.pkl": b"never unpickle",
        }
        for name, content in files.items():
            (self.release / name).write_bytes(content)
        self.index_dir = self.root / "built"
        metadata = build_index(
            self.release, self.index_dir, release_id="test-release")
        with tarfile.open(self.release / "search-index.tar.gz", "w:gz") as archive:
            for name in [*metadata["files"], "index-metadata.json"]:
                archive.add(self.index_dir / name, arcname=name)
        self.manifest = {
            "schema_version": "1.0", "release_id": "test-release",
            "search_index": metadata, "artifacts": {},
        }
        for name in RELEASE_FILES:
            self.rehash(name)
        self.save_manifest()

    def rehash(self, name):
        content = (self.release / name).read_bytes()
        self.manifest["artifacts"][name] = {
            "version_path": f"releases/test-release/{name}",
            "size_bytes": len(content),
            "checksum_sha256": hashlib.sha256(content).hexdigest(),
        }

    def save_manifest(self):
        (self.release / "manifest.json").write_text(json.dumps(self.manifest))

    def prepare(self):
        return prepare_release(
            self.release, self.output, release_id="test-release")

    def test_prepare_is_offline_and_preserves_query_results(self):
        with patch.object(socket, "socket", side_effect=AssertionError("network")):
            self.assertEqual(self.prepare(), self.manifest)
        index = open_index(self.output, release_id="test-release")
        index.close()
        for function, args, kwargs in (
            (course_id_search, ("INFO 201",), {}),
            (major_title_search, ("Informatics",), {}),
            (text_search, ("info",), {"is_gateway": True}),
            (text_search, ("info",), {"min_coi_score": 0, "max_coi_score": 1}),
            (text_search, ("information",), {}),
        ):
            with patch("pathways.search.SEARCH_INDEX_DIR", str(self.index_dir)):
                expected = function(*args, **kwargs)
            with patch("pathways.search.SEARCH_INDEX_DIR", str(self.output)):
                self.assertEqual(function(*args, **kwargs), expected)

    def test_existing_output_is_not_changed(self):
        self.output.mkdir()
        marker = self.output / "active"
        marker.write_text("keep")
        with self.assertRaises(FileExistsError):
            self.prepare()
        self.assertEqual(marker.read_text(), "keep")

    def test_corrupt_release_file_is_rejected_before_preparation(self):
        (self.release / "curric_data.json").write_bytes(b"corrupt")
        with self.assertRaisesRegex(IndexValidationError, "checksum"):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_missing_release_file_is_rejected(self):
        (self.release / "prereq_data.pkl").unlink()
        with self.assertRaises(IndexValidationError):
            self.prepare()

    def test_invalid_manifest_json_and_shapes_are_rejected(self):
        for content in (b"{invalid", b"[]", b"\xff", b"null"):
            with self.subTest(content=content):
                (self.release / "manifest.json").write_bytes(content)
                with self.assertRaises(IndexValidationError):
                    self.prepare()
                self.assertFalse(self.output.exists())

    def test_invalid_archive_is_rejected_even_with_updated_checksum(self):
        (self.release / "search-index.tar.gz").write_bytes(b"not gzip")
        self.rehash("search-index.tar.gz")
        self.save_manifest()
        with self.assertRaises(IndexValidationError):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_symlinked_release_file_is_rejected(self):
        path = self.release / "coi_scores.csv"
        path.rename(self.root / "coi.csv")
        path.symlink_to(self.root / "coi.csv")
        with self.assertRaises(IndexValidationError):
            self.prepare()

    def test_manifest_identity_shape_and_index_inputs(self):
        original = json.dumps(self.manifest)
        for change in ("version", "identity", "missing", "input", "path", "files"):
            self.manifest = json.loads(original)
            with self.subTest(change=change):
                if change == "version":
                    self.manifest["schema_version"] = "2.0"
                elif change == "identity":
                    self.manifest["release_id"] = "other"
                elif change == "missing":
                    self.manifest["artifacts"].pop("curric_data.json")
                elif change == "input":
                    self.manifest["search_index"]["inputs"]["coi_scores.csv"][
                        "checksum_sha256"] = "0" * 64
                elif change == "path":
                    self.manifest["artifacts"]["coi_scores.csv"][
                        "version_path"] = "latest/coi_scores.csv"
                else:
                    self.manifest["search_index"]["files"] = {"../escape": {}}
                self.save_manifest()
                with self.assertRaises(IndexValidationError):
                    self.prepare()
                self.assertFalse(self.output.exists())

    def test_unsafe_or_incomplete_archive_is_never_extracted(self):
        for kind in ("traversal", "symlink", "duplicate", "missing", "oversized"):
            with self.subTest(kind=kind):
                with tarfile.open(
                    self.release / "search-index.tar.gz", "w:gz"
                ) as archive:
                    if kind != "missing":
                        name = next(iter(self.manifest["search_index"]["files"]))
                        member = tarfile.TarInfo(
                            "../escape" if kind == "traversal" else name)
                        if kind == "symlink":
                            member.type = tarfile.SYMTYPE
                            member.linkname = "/tmp/escape"
                        content = (self.index_dir / name).read_bytes()
                        if kind == "oversized":
                            content += b"extra"
                        member.size = len(content)
                        archive.addfile(member, io.BytesIO(content))
                        if kind == "duplicate":
                            archive.addfile(member, io.BytesIO(content))
                self.rehash("search-index.tar.gz")
                self.save_manifest()
                with self.assertRaises(IndexValidationError):
                    self.prepare()
                self.assertFalse(self.output.exists())
                self.assertFalse((self.root / "escape").exists())
                self.assertFalse(list(self.root.glob(".prepare-index-*")))

    def test_bundle_metadata_must_match_manifest(self):
        self.manifest["search_index"]["builder_version"] = "different"
        self.save_manifest()
        with self.assertRaisesRegex(IndexValidationError, "differs"):
            self.prepare()
        self.assertFalse(self.output.exists())

    def test_prepare_command(self):
        call_command(
            "prepare_search_release", release_dir=str(self.release),
            output_dir=str(self.output), release_id="test-release",
            stdout=io.StringIO())
        self.assertTrue((self.output / "index-metadata.json").is_file())
        with self.assertRaises(CommandError):
            call_command(
                "prepare_search_release", release_dir=str(self.release),
                output_dir=str(self.output), release_id="test-release")

    def test_shared_snapshot_command_requires_no_database(self):
        with patch.object(socket, "socket", side_effect=AssertionError("network")):
            call_command(
                "build_search_index", input_root=str(self.release),
                output_dir=str(self.output), release_id="offline-snapshot",
                stdout=io.StringIO())
        index = open_index(self.output, release_id="offline-snapshot")
        index.close()
        for options in (
            {"input_root": str(self.release)},
            {"release_id": "missing-inputs"},
            {"input_root": str(self.release), "output_dir": str(self.output),
             "release_id": "existing-output"},
        ):
            with self.subTest(options=options), self.assertRaises(CommandError):
                call_command("build_search_index", **options)
