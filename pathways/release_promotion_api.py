# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""API for discovering and promoting data releases from GCS to pathways."""

import json
import logging
import re

from django.conf import settings
from google.api_core.exceptions import GoogleAPIError
from google.cloud import storage

logger = logging.getLogger(__name__)


class ReleaseLister:
    """Discover finalized data releases from GCS bucket."""

    def __init__(self, bucket_name: str | None = None, prefix: str = ""):
        self.bucket_name = bucket_name or getattr(settings, "RELEASE_SYNC_BUCKET", None)
        if not self.bucket_name:
            raise ValueError("RELEASE_SYNC_BUCKET must be configured")
        self.prefix = prefix.strip("/")
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def list_available_releases(self) -> list:
        """
        List all finalized releases available in the bucket.

        Returns:
            List of dicts with release metadata:
            - release_id: str
            - manifest_path: str (GCS path)
            - manifest_size: int
            - manifest_checksum: str
        """
        releases = []
        try:
            # List all manifest.json files in the releases/ prefix
            prefix = f"{self.prefix}/releases" if self.prefix else "releases"
            prefix = prefix.strip("/")

            iterator = self.bucket.list_blobs(prefix=prefix, delimiter="/")
            # Get the sub-prefixes (release IDs)
            for page in iterator.pages:
                for prefix_item in page.prefixes:
                    # Extract release ID from path like "releases/release-id/"
                    parts = prefix_item.rstrip("/").split("/")
                    if len(parts) >= 2:
                        release_id = parts[-1]
                        manifest_blob_path = f"{prefix_item}manifest.json"
                        try:
                            manifest_blob = self.bucket.get_blob(manifest_blob_path)
                            if manifest_blob and manifest_blob.exists():
                                releases.append({
                                    "release_id": release_id,
                                    "manifest_path": manifest_blob_path,
                                    "manifest_size": manifest_blob.size,
                                    "manifest_checksum": manifest_blob.md5_hash,
                                    "updated": manifest_blob.updated.isoformat()
                                    if manifest_blob.updated else None,
                                })
                        except GoogleAPIError as e:
                            logger.warning(
                                "Error checking manifest for release %s: %s",
                                release_id, e)

            # Sort by most recent first
            releases.sort(key=lambda r: r.get("updated") or "", reverse=True)
            return releases

        except GoogleAPIError as e:
            logger.error("Error listing releases from GCS: %s", e)
            raise ValueError("Failed to list available releases from storage") from e

    def get_release_manifest(self, release_id: str) -> dict:
        """
        Fetch and parse the manifest for a specific release.

        Args:
            release_id: The release ID to fetch

        Returns:
            Parsed manifest dict

        Raises:
            ValueError: If release ID is invalid or manifest cannot be found/parsed
        """
        if not re.fullmatch(r"[A-Za-z0-9_-]+", release_id):
            raise ValueError("Invalid release ID")

        try:
            manifest_path = (
                f"{self.prefix}/releases/{release_id}/manifest.json"
                if self.prefix
                else f"releases/{release_id}/manifest.json"
            )
            manifest_path = manifest_path.lstrip("/")

            blob = self.bucket.get_blob(manifest_path)
            if not blob or not blob.exists():
                raise ValueError(f"Release not found: {release_id}")

            manifest_json = blob.download_as_text()
            manifest = json.loads(manifest_json)

            # Validate manifest structure
            if not isinstance(manifest, dict):
                raise ValueError("Invalid manifest format")  # noqa: TRY004

            return manifest

        except json.JSONDecodeError as e:
            logger.error("Failed to parse manifest for release %s: %s", release_id, e)
            raise ValueError(f"Invalid manifest for release {release_id}") from e
        except GoogleAPIError as e:
            logger.error("Error fetching manifest for release %s: %s", release_id, e)
            raise ValueError("Failed to fetch release manifest from storage") from e


def queue_release_for_promotion(release_id: str, requested_by: str = "") -> dict:
    """
    Queue a release for import into the pathways database.

    Args:
        release_id: The release to promote
        requested_by: Username requesting the promotion (optional)

    Returns:
        Dict with queue status:
        - success: bool
        - message: str
        - queue_attempt_id: int (if successful)

    Raises:
        ValueError: If validation fails
    """
    from pathways.release_sync_queue import enqueue_release_sync

    if not re.fullmatch(r"[A-Za-z0-9_-]+", release_id):
        raise ValueError("Invalid release ID")

    try:
        # Validate the release exists and is properly formed
        lister = ReleaseLister()
        manifest = lister.get_release_manifest(release_id)

        # Verify manifest has required fields
        if "release_id" not in manifest or manifest["release_id"] != release_id:
            raise ValueError("Release ID mismatch in manifest")

        # Queue the release for sync/import
        # The bucket and prefix are managed by the release_sync_queue module
        attempt, created = enqueue_release_sync(
            release_id, requested_by=requested_by)

        return {
            "success": True,
            "message": (
                f"Release {release_id} queued for import (attempt {attempt.pk})"
                if created
                else f"Release {release_id} already queued (attempt {attempt.pk})"
            ),
            "queue_attempt_id": attempt.pk,
            "release_id": release_id,
        }

    except Exception as e:
        logger.error("Failed to queue release %s: %s", release_id, e)
        raise ValueError(f"Failed to queue release: {e!s}") from e
