# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Prepare a trusted, already-downloaded release without network or activation."""

import hashlib
import json
import re
import tempfile
from pathlib import Path

from dawgpath_search import IndexValidationError, prepare_bundle
from dawgpath_search.builder import INPUT_FILES

RELEASE_FILES = {
    *INPUT_FILES, "curric_data.json", "admit_major_mapping.csv",
    "course_prereq_data.pkl", "prereq_data.pkl", "search-index.tar.gz",
}
RELEASE_FILES_BY_VERSION = {
    "1.0": RELEASE_FILES,
    "1.1": RELEASE_FILES | {"similar_majors.csv"},
}


def _json(content, label):
    try:
        value = json.loads(content)
    except (ValueError, UnicodeDecodeError) as exc:
        raise IndexValidationError(f"{label}: invalid JSON") from exc
    if not isinstance(value, dict):
        raise IndexValidationError(f"{label}: expected an object")
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
        raise IndexValidationError(f"{label}: checksum/size mismatch")


def _plain_file(path):
    if path.is_symlink() or not path.is_file():
        raise IndexValidationError(f"Missing or non-regular release file: {path.name}")
    return path.read_bytes()


def release_artifacts(manifest, release_id):
    if not isinstance(release_id, str) or not re.fullmatch(
        r"[A-Za-z0-9_-]+", release_id
    ):
        raise IndexValidationError("Invalid release ID")
    version = manifest.get("schema_version")
    files = RELEASE_FILES_BY_VERSION.get(version) if isinstance(version, str) else None
    if files is None:
        raise IndexValidationError("Unsupported release manifest version")
    if manifest.get("release_id") != release_id:
        raise IndexValidationError("Release identity mismatch")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != files:
        raise IndexValidationError("Release artifact inventory mismatch")
    for name, info in artifacts.items():
        if not _file_info(info) or info.get("version_path") != (
            f"releases/{release_id}/{name}"
        ):
            raise IndexValidationError(f"Invalid release artifact metadata: {name}")
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
    index_metadata = manifest.get("search_index")
    if (
        not isinstance(index_metadata, dict)
        or index_metadata.get("release_id") != release_id
        or not isinstance(index_metadata.get("inputs"), dict)
        or set(index_metadata["inputs"]) != set(INPUT_FILES)
    ):
        raise IndexValidationError("Invalid search index metadata")
    for name, info in index_metadata["inputs"].items():
        if not _file_info(info) or any(
            artifacts[name][key] != info[key]
            for key in ("size_bytes", "checksum_sha256")
        ):
            raise IndexValidationError(f"Index input does not match release: {name}")
    return manifest, contents


def prepare_release(release_dir, output_dir, *, release_id):
    """Verify trusted local release bytes and prepare a fresh index."""
    output = Path(output_dir)
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output directory already exists: {output}")
    manifest, contents = verify_release(release_dir, release_id=release_id)
    prepare_bundle(
        contents["search-index.tar.gz"], output,
        metadata=manifest["search_index"], release_id=release_id)
    return manifest


def verify_release_index(manifest, contents):
    """Check a trusted bundle without retaining or activating an index."""
    with tempfile.TemporaryDirectory(prefix="verify-release-") as temporary:
        prepare_bundle(
            contents["search-index.tar.gz"], Path(temporary) / "index",
            metadata=manifest["search_index"], release_id=manifest["release_id"])
