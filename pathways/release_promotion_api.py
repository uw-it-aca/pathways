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

    def __init__(self, bucket_name: str | None = None,
                 prefix: str | None = None):
        self.bucket_name = (bucket_name or
                            getattr(settings, "RELEASE_SYNC_BUCKET",
                                    None))
        if not self.bucket_name:
            raise ValueError("RELEASE_SYNC_BUCKET must be configured")
        self.prefix = (
            getattr(settings, "RELEASE_SYNC_PREFIX", "")
            if prefix is None else prefix
        ).strip("/")
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
            prefix = f"{self.prefix}/releases/" if self.prefix else "releases/"

            for blob in self.bucket.list_blobs(prefix=prefix):
                parts = blob.name[len(prefix):].split("/")
                if (len(parts) != 2 or not parts[0] or
                        parts[1] != "manifest.json"):
                    continue

                updated = blob.updated.isoformat() if blob.updated else None
                releases.append({
                    "release_id": parts[0],
                    "manifest_path": blob.name,
                    "manifest_size": blob.size,
                    "manifest_checksum": blob.md5_hash,
                    "updated": updated,
                })

            # Sort by most recent first
            releases.sort(key=lambda r: r.get("updated") or "", reverse=True)
            return releases

        except GoogleAPIError as e:
            logger.error("Error listing releases from GCS: %s", e)
            msg = "Failed to list available releases from storage"
            raise ValueError(msg) from e

    def get_release_manifest(self, release_id: str) -> dict:
        """Fetch and parse the manifest for a specific release.

        Args:
            release_id: The release ID to fetch

        Returns:
            Parsed manifest dict

        Raises:
            ValueError: If release ID is invalid or manifest
                cannot be found/parsed
        """
        if not re.fullmatch(r"[A-Za-z0-9_-]+", release_id):
            raise ValueError("Invalid release ID")

        try:
            if self.prefix:
                manifest_path = (
                    f"{self.prefix}/releases/{release_id}"
                    "/manifest.json")
            else:
                manifest_path = (
                    f"releases/{release_id}/manifest.json")
            manifest_path = manifest_path.lstrip("/")

            blob = self.bucket.get_blob(manifest_path)
            if not blob or not blob.exists():
                raise ValueError(f"Release not found: {release_id}")

            manifest_json = blob.download_as_text()
            manifest = json.loads(manifest_json)

            # Validate manifest structure
            if not isinstance(manifest, dict):
                raise TypeError("Invalid manifest format")

            return manifest

        except json.JSONDecodeError as e:
            logger.error(
                "Failed to parse manifest for release %s: %s",
                release_id, e)
            msg = f"Invalid manifest for release {release_id}"
            raise ValueError(msg) from e
        except GoogleAPIError as e:
            logger.error(
                "Error fetching manifest for release %s: %s",
                release_id, e)
            msg = "Failed to fetch release manifest from storage"
            raise ValueError(msg) from e


def queue_release_for_promotion(release_id: str,
                                requested_by: str = "") -> dict:
    """Queue a release for import into the pathways database.

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

        # Verify manifest identity and import compatibility before queueing.
        if ("release_id" not in manifest or
                manifest["release_id"] != release_id):
            raise ValueError("Release ID mismatch in manifest")
        if manifest.get("schema_version") not in ("1.1", "2.0"):
            raise ValueError(
                "Database import requires release schema 1.1 or 2.0")

        # Queue the release for sync/import
        # The bucket and prefix are managed by the
        # release_sync_queue module
        attempt, created = enqueue_release_sync(
            release_id, requested_by=requested_by)

        return {
            "success": True,
            "message": (
                f"Release {release_id} queued for import "
                f"(attempt {attempt.pk})"
                if created
                else f"Release {release_id} already queued "
                f"(attempt {attempt.pk})"
            ),
            "queue_attempt_id": attempt.pk,
            "release_id": release_id,
        }

    except Exception as e:
        logger.error("Failed to queue release %s: %s", release_id, e)
        raise ValueError(f"Failed to queue release: {e!s}") from e
