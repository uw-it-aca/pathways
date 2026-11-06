import uuid

from django.conf import settings
from django.db import connection, transaction
from django.utils import timezone

from pathways.models import DataReleaseSyncAttempt
from pathways.release_sync import (
    ReleaseSyncError,
    execute_sync_attempt,
    validate_sync_source,
)

QUEUE_LOCK = 742193620


def configured_source():
    if not getattr(settings, "RELEASE_SYNC_ENABLED", False):
        raise ValueError("Release sync queue is disabled.")
    bucket = getattr(settings, "RELEASE_SYNC_BUCKET", "")
    prefix = getattr(settings, "RELEASE_SYNC_PREFIX", "")
    return bucket, prefix


def enqueue_release_sync(release_id, *, requested_by=""):
    bucket, prefix = configured_source()
    prefix = validate_sync_source(bucket, release_id, prefix, requested_by)
    return DataReleaseSyncAttempt.objects.get_or_create(
        release_id=release_id, status=DataReleaseSyncAttempt.Status.QUEUED,
        defaults={"bucket": bucket, "prefix": prefix, "requested_by": requested_by})


def process_release_sync_queue(*, limit=1, temporary_root=None):
    bucket, prefix = configured_source()
    prefix = validate_sync_source(bucket, "configuration-check", prefix, "")
    if connection.vendor != "postgresql":
        raise ValueError("Release sync queue requires PostgreSQL.")
    if not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_try_advisory_lock(%s), pg_backend_pid()", [QUEUE_LOCK])
        acquired, backend_pid = cursor.fetchone()
    if not acquired:
        return []
    worker_id = uuid.uuid4()

    def check_owner():
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid()")
            if cursor.fetchone()[0] != backend_pid:
                raise ValueError("Release sync worker lost its database session.")

    try:
        check_owner()
        DataReleaseSyncAttempt.objects.filter(
            worker_id__isnull=False, status__in=["downloading", "importing"]
        ).update(status="failed", completed_on=timezone.now(),
                 error_code="WorkerInterrupted",
                 error_message="Previous queue worker exited before completing this attempt.")
        processed = []
        for _ in range(limit):
            check_owner()
            with transaction.atomic():
                attempt = DataReleaseSyncAttempt.objects.select_for_update().filter(
                    status="queued").order_by("started_on", "pk").first()
                if attempt is None:
                    break
                attempt.worker_id = worker_id
                attempt.claimed_on = timezone.now()
                attempt.status = "downloading"
                attempt.save(update_fields=["worker_id", "claimed_on", "status"])
            if (attempt.bucket, attempt.prefix) != (bucket, prefix):
                attempt.status = "failed"
                attempt.completed_on = timezone.now()
                attempt.error_code = "SourceConfigurationChanged"
                attempt.error_message = "Queued source no longer matches trusted configuration."
                attempt.save(update_fields=[
                    "status", "completed_on", "error_code", "error_message"])
            else:
                try:
                    execute_sync_attempt(attempt, temporary_root=temporary_root,
                                         check_owner=check_owner)
                except ReleaseSyncError as exc:
                    attempt = exc.attempt
            processed.append(attempt)
        return processed
    finally:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_unlock(%s)", [QUEUE_LOCK])