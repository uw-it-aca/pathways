# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Explicit, generation-pinned downloads; no latest pointer or local fallback."""

import os
import re
import tempfile
from pathlib import Path

from dawgpath_search import IndexValidationError
from google.cloud import storage

from pathways.search_release import (
    _json,
    _verify,
    release_artifacts,
    verify_release,
    verify_release_index,
)

MAX_MANIFEST_BYTES = 1024 * 1024


def download_release(bucket_name, release_id, output_dir, *, prefix=""):
    if not bucket_name:
        raise ValueError("A GCS bucket is required.")
    if not isinstance(release_id, str) or not re.fullmatch(
            r"[A-Za-z0-9_-]+", release_id):
        raise ValueError("Invalid release ID.")
    prefix = prefix.strip("/")
    if prefix and any(part in {"", ".", ".."} for part in prefix.split("/")):
        raise ValueError("Invalid GCS prefix.")
    output = Path(output_dir)
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"Output directory already exists: {output}")
    bucket = storage.Client().bucket(bucket_name)

    def fetch(path, expected_size):
        key = f"{prefix}/{path}" if prefix else path
        blob = bucket.get_blob(key)
        if blob is None:
            raise FileNotFoundError(f"Missing GCS release object: {key}")
        if blob.generation is None:
            raise IndexValidationError(f"GCS object has no generation: {key}")
        if blob.size is None or blob.size > expected_size:
            raise IndexValidationError(f"GCS release object exceeds size limit: {key}")
        content = blob.download_as_bytes(if_generation_match=blob.generation)
        if len(content) > expected_size:
            raise IndexValidationError(f"GCS release object exceeds size limit: {key}")
        return content

    manifest_bytes = fetch(f"releases/{release_id}/manifest.json", MAX_MANIFEST_BYTES)
    manifest = _json(manifest_bytes, "manifest.json")
    artifacts = release_artifacts(manifest, release_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
            prefix=".download-release-", dir=output.parent) as temporary:
        staging = Path(temporary) / "release"
        staging.mkdir()
        for name, info in artifacts.items():
            content = fetch(info["version_path"], info["size_bytes"])
            _verify(content, info, name)
            (staging / name).write_bytes(content)
        (staging / "manifest.json").write_bytes(manifest_bytes)
        verified, contents = verify_release(staging, release_id=release_id)
        verify_release_index(verified, contents)
        output.mkdir()
        try:
            os.replace(staging, output)
        except OSError:
            output.rmdir()
            raise
    return manifest
