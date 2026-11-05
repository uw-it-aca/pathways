# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import hashlib
import json
import socket
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from pathways.data_release import (
    RELEASE_FILES,
    RELEASE_FILES_BY_VERSION,
    ReleaseValidationError,
    verify_release,
)


class ReleaseVerificationTest(TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.make_release("2.0")

    def make_release(self, version):
        self.manifest = {
            "schema_version": version, "release_id": "test-release",
            "artifacts": {},
        }
        for name in RELEASE_FILES_BY_VERSION[version]:
            content = b"opaque verified bytes"
            (self.root / name).write_bytes(content)
            self.manifest["artifacts"][name] = {
                "version_path": f"releases/test-release/{name}",
                "size_bytes": len(content),
                "checksum_sha256": hashlib.sha256(content).hexdigest(),
            }
        self.save_manifest()

    def save_manifest(self):
        (self.root / "manifest.json").write_text(json.dumps(self.manifest))

    def verify(self):
        return verify_release(self.root, release_id="test-release")

    def test_data_only_inventory_and_offline_verified_snapshot(self):
        self.assertEqual(RELEASE_FILES, {
            "course_data.json", "curric_data.json", "major_data.json",
            "course_prereq_data.pkl", "prereq_data.pkl", "bottleneck_courses.csv",
            "gateway_courses.csv", "coi_scores.csv", "admit_major_mapping.csv",
            "similar_majors.csv",
        })
        with patch.object(socket, "socket", side_effect=AssertionError("network")):
            manifest, contents = self.verify()
        self.assertEqual(manifest, self.manifest)
        self.assertEqual(set(contents), RELEASE_FILES)
        (self.root / "course_data.json").write_bytes(b"changed")
        self.assertEqual(contents["course_data.json"], b"opaque verified bytes")

    def test_legacy_archive_is_opaque_but_checksum_verified(self):
        for version in ("1.0", "1.1"):
            with self.subTest(version=version):
                self.make_release(version)
                self.manifest["search_index"] = {"legacy": "not inspected"}
                self.save_manifest()
                with patch("tarfile.open", side_effect=AssertionError("no extraction")):
                    self.assertEqual(self.verify()[0], self.manifest)
                (self.root / "search-index.tar.gz").write_bytes(b"tampered")
                with self.assertRaisesRegex(ReleaseValidationError, "checksum"):
                    self.verify()

    def test_missing_corrupt_and_symlinked_artifacts_are_rejected(self):
        path = self.root / "course_data.json"
        for kind in ("missing", "corrupt", "symlink"):
            with self.subTest(kind=kind):
                self.make_release("2.0")
                if kind == "corrupt":
                    path.write_bytes(b"corrupt")
                else:
                    path.unlink()
                    if kind == "symlink":
                        path.symlink_to(self.root / "major_data.json")
                with self.assertRaises(ReleaseValidationError):
                    self.verify()

    def test_invalid_manifest_json_and_shapes_are_rejected(self):
        for content in (b"{invalid", b"[]", b"\xff", b"null"):
            with self.subTest(content=content):
                (self.root / "manifest.json").write_bytes(content)
                with self.assertRaises(ReleaseValidationError):
                    self.verify()

    def test_identity_inventory_paths_and_metadata_are_strict(self):
        original = json.dumps(self.manifest)
        for kind in ("version", "identity", "missing", "extra", "path",
                     "checksum", "size", "index", "archive"):
            with self.subTest(kind=kind):
                self.manifest = json.loads(original)
                artifacts = self.manifest["artifacts"]
                info = artifacts["course_data.json"]
                if kind == "version":
                    self.manifest["schema_version"] = "3.0"
                elif kind == "identity":
                    self.manifest["release_id"] = "other"
                elif kind == "missing":
                    artifacts.pop("course_data.json")
                elif kind in ("extra", "archive"):
                    artifacts["../escape" if kind == "extra" else
                              "search-index.tar.gz"] = info
                elif kind == "path":
                    info["version_path"] = "latest/course_data.json"
                elif kind == "checksum":
                    info["checksum_sha256"] = "invalid"
                elif kind == "size":
                    info["size_bytes"] = True
                else:
                    self.manifest["search_index"] = {}
                self.save_manifest()
                with self.assertRaises(ReleaseValidationError):
                    self.verify()

    def test_unsafe_release_ids_are_rejected(self):
        for release_id in ("../escape", "", "a/b", None):
            with self.subTest(release_id=release_id), self.assertRaisesRegex(
                    ReleaseValidationError, "release ID"):
                verify_release(self.root, release_id=release_id)

    def test_symlinked_manifest_is_rejected(self):
        path = self.root / "manifest.json"
        path.rename(self.root / "other.json")
        path.symlink_to(self.root / "other.json")
        with self.assertRaises(ReleaseValidationError):
            self.verify()
