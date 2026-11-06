import logging
import re
import tempfile
from pathlib import Path

from django.db import connection, transaction
from django.utils import timezone

from pathways.models.data_release_sync import DataReleaseSyncAttempt
from pathways.release_download import download_release
from pathways.release_import import import_release

logger = logging.getLogger(__name__)


class ReleaseSyncError(Exception):
    def __init__(self, attempt):
        self.attempt = attempt
        super().__init__(
            f"Release sync attempt {attempt.pk} failed ({attempt.error_code}). "
            "No catalog changes were committed by this attempt.")


def validate_sync_source(bucket, release_id, prefix, requested_by):
    if connection.in_atomic_block or not connection.get_autocommit():
        raise ValueError("Release sync must run outside an existing transaction.")
    if not isinstance(release_id, str) or not re.fullmatch(
            r"[A-Za-z0-9_-]{1,128}", release_id):
        raise ValueError("Invalid release ID.")
    for name, value, limit in (("bucket", bucket, 222), ("prefix", prefix, 512),
                               ("requested_by", requested_by, 150)):
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError(f"Invalid {name}.")
    if not bucket or bucket != bucket.strip():
        raise ValueError("A GCS bucket is required.")
    prefix = prefix.strip("/")
    if prefix and any(part in {"", ".", ".."} for part in prefix.split("/")):
        raise ValueError("Invalid GCS prefix.")
    return prefix


def sync_release(bucket, release_id, *, prefix="", requested_by="", temporary_root=None):
    prefix = validate_sync_source(bucket, release_id, prefix, requested_by)
    attempt = DataReleaseSyncAttempt.objects.create(
        release_id=release_id, bucket=bucket, prefix=prefix,
        requested_by=requested_by, status=DataReleaseSyncAttempt.Status.DOWNLOADING)
    return execute_sync_attempt(attempt, temporary_root=temporary_root)


def execute_sync_attempt(attempt, *, temporary_root=None, check_owner=None):
    try:
        with tempfile.TemporaryDirectory(
                prefix="pathways-release-sync-", dir=temporary_root) as temporary:
            release_dir = Path(temporary) / "release"
            download_release(attempt.bucket, attempt.release_id, release_dir,
                             prefix=attempt.prefix)
            if check_owner:
                check_owner()
            attempt.status = DataReleaseSyncAttempt.Status.IMPORTING
            attempt.save(update_fields=["status"])
            with transaction.atomic():
                if check_owner:
                    check_owner()
                changed = import_release(release_dir, release_id=attempt.release_id)
                attempt.status = (DataReleaseSyncAttempt.Status.SUCCEEDED if changed
                                  else DataReleaseSyncAttempt.Status.UNCHANGED)
                attempt.completed_on = timezone.now()
                attempt.save(update_fields=["status", "completed_on"])
    except Exception as exc:
        attempt.refresh_from_db()
        if attempt.status in {DataReleaseSyncAttempt.Status.SUCCEEDED,
                              DataReleaseSyncAttempt.Status.UNCHANGED}:
            logger.warning(
                "Release sync %s committed, but temporary cleanup failed (%s).",
                attempt.pk, type(exc).__name__)
            return attempt
        phase = attempt.status
        attempt.status = DataReleaseSyncAttempt.Status.FAILED
        attempt.completed_on = timezone.now()
        attempt.error_code = type(exc).__name__[:128]
        attempt.error_message = f"Release sync failed during {phase}."
        attempt.save(update_fields=[
            "status", "completed_on", "error_code", "error_message"])
        raise ReleaseSyncError(attempt) from exc
    return attempt
