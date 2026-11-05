# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Verify immutable data release manifests and artifact bytes."""

import hashlib
import json
import re
from pathlib import Path


class ReleaseValidationError(ValueError):
    pass


RELEASE_FILES = {
    "course_data.json", "curric_data.json", "major_data.json",
    "course_prereq_data.pkl", "prereq_data.pkl", "bottleneck_courses.csv",
    "gateway_courses.csv", "coi_scores.csv", "admit_major_mapping.csv",
    "similar_majors.csv",
}
RELEASE_FILES_BY_VERSION = {
    "1.0": (RELEASE_FILES - {"similar_majors.csv"}) | {"search-index.tar.gz"},
    "1.1": RELEASE_FILES | {"search-index.tar.gz"},
    "2.0": RELEASE_FILES,
}


def _json(content, label):
    try:
        value = json.loads(content)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ReleaseValidationError(f"{label}: invalid JSON") from exc
    if not isinstance(value, dict):
        raise ReleaseValidationError(f"{label}: expected an object")
    return value


def _file_info(value):
    return (
        isinstance(value, dict)
        and type(value.get("size_bytes")) is int
        and value["size_bytes"] >= 0
        and isinstance(value.get("checksum_sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", value["checksum_sha256"]) is not None
    )


def _verify(content, info, label):
    if (
        not _file_info(info)
        or len(content) != info["size_bytes"]
        or hashlib.sha256(content).hexdigest() != info["checksum_sha256"]
    ):
        raise ReleaseValidationError(f"{label}: checksum/size mismatch")


def _plain_file(path):
    if path.is_symlink() or not path.is_file():
        raise ReleaseValidationError(
            f"Missing or non-regular release file: {path.name}")
    return path.read_bytes()


def release_artifacts(manifest, release_id):
    if not isinstance(release_id, str) or not re.fullmatch(
        r"[A-Za-z0-9_-]+", release_id
    ):
        raise ReleaseValidationError("Invalid release ID")
    version = manifest.get("schema_version")
    files = RELEASE_FILES_BY_VERSION.get(version) if isinstance(version, str) else None
    if files is None:
        raise ReleaseValidationError("Unsupported release manifest version")
    if version == "2.0" and "search_index" in manifest:
        raise ReleaseValidationError("Data-only release must not include search_index")
    if manifest.get("release_id") != release_id:
        raise ReleaseValidationError("Release identity mismatch")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != files:
        raise ReleaseValidationError("Release artifact inventory mismatch")
    for name, info in artifacts.items():
        if not _file_info(info) or info.get("version_path") != (
            f"releases/{release_id}/{name}"
        ):
            raise ReleaseValidationError(f"Invalid release artifact metadata: {name}")
    return artifacts


def verify_release(release_dir, *, release_id):
    """Read verified bytes once so import never rereads unverified source files."""
    root = Path(release_dir)
    manifest = _json(_plain_file(root / "manifest.json"), "manifest.json")
    artifacts = release_artifacts(manifest, release_id)
    contents = {}
    for name, info in artifacts.items():
        content = _plain_file(root / name)
        _verify(content, info, name)
        contents[name] = content
    return manifest, contents
