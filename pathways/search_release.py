# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Prepare a trusted, already-downloaded release without network or activation."""

import hashlib
import json
import re
from pathlib import Path

from dawgpath_search import IndexValidationError, prepare_bundle
from dawgpath_search.builder import INPUT_FILES

RELEASE_FILES = {
    *INPUT_FILES, "curric_data.json", "admit_major_mapping.csv",
    "course_prereq_data.pkl", "prereq_data.pkl", "search-index.tar.gz",
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


def prepare_release(release_dir, output_dir, *, release_id):
    """Verify all release files and extract only listed regular index files.

    Caller must trust the manifest's origin; checksums do not authenticate
    Whoosh's serialized schema. Never unpickle the legacy data exports here.
    """
    if not isinstance(release_id, str) or not re.fullmatch(
        r"[A-Za-z0-9_-]+", release_id
    ):
        raise IndexValidationError("Invalid release ID")
    root = Path(release_dir)
    output = Path(output_dir)
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output directory already exists: {output}")
    manifest = _json(_plain_file(root / "manifest.json"), "manifest.json")
    if manifest.get("schema_version") != "1.0":
        raise IndexValidationError("Unsupported release manifest version")
    if manifest.get("release_id") != release_id:
        raise IndexValidationError("Release identity mismatch")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != RELEASE_FILES:
        raise IndexValidationError("Release must contain all ten artifact entries")
    bundle = None
    for name, info in artifacts.items():
        if not _file_info(info) or info.get("version_path") != (
            f"releases/{release_id}/{name}"
        ):
            raise IndexValidationError(f"Invalid release artifact metadata: {name}")
        content = _plain_file(root / name)
        _verify(content, info, name)
        if name == "search-index.tar.gz":
            bundle = content
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
    assert bundle is not None
    prepare_bundle(bundle, output, metadata=index_metadata, release_id=release_id)
    return manifest
