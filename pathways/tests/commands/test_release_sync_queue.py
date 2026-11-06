import io
import json
import shutil
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event
from unittest import skipUnless
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection, connections
from django.test import TransactionTestCase, override_settings

from pathways.models import DataReleaseState, DataReleaseSyncAttempt
from pathways.release_sync_queue import enqueue_release_sync, process_release_sync_queue
from pathways.tests.commands.test_data_release import write_release


@skipUnless(connection.vendor == "postgresql", "PostgreSQL queue locking required")
@override_settings(RELEASE_SYNC_ENABLED=True, RELEASE_SYNC_BUCKET="trusted",
                   RELEASE_SYNC_PREFIX="app")
class ReleaseSyncQueueTest(TransactionTestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.release, _ = write_release(self.root)
        self.download = self.enterContext(patch(
            "pathways.release_sync.download_release", side_effect=self.copy_release))

    def copy_release(self, bucket, release_id, output, **kwargs):
        shutil.copytree(self.release, output)
        manifest_path = output / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["release_id"] = release_id
        for name, artifact in manifest["artifacts"].items():
            artifact["version_path"] = f"releases/{release_id}/{name}"
        manifest_path.write_text(json.dumps(manifest))

    def test_queue_deduplicates_and_worker_reuses_attempt(self):
        attempt, created = enqueue_release_sync("test-release", requested_by="operator")
        duplicate, repeated = enqueue_release_sync("test-release")
        self.assertTrue(created)
        self.assertFalse(repeated)
        self.assertEqual(attempt.pk, duplicate.pk)
        self.assertEqual(attempt.status, "queued")
        processed = process_release_sync_queue()
        self.assertEqual(processed[0].pk, attempt.pk)
        self.assertEqual(processed[0].status, "succeeded")
        self.assertIsNotNone(processed[0].claimed_on)
        self.assertIsNotNone(processed[0].worker_id)
        self.assertEqual(DataReleaseState.objects.get().current_release_id, "test-release")
        self.assertEqual(process_release_sync_queue(), [])

    def test_disabled_and_changed_configuration_fail_closed(self):
        with override_settings(RELEASE_SYNC_ENABLED=False), self.assertRaises(ValueError):
            enqueue_release_sync("test-release")
        attempt, _ = enqueue_release_sync("test-release")
        with override_settings(RELEASE_SYNC_BUCKET="different"):
            processed = process_release_sync_queue()
        self.assertEqual(processed[0].error_code, "SourceConfigurationChanged")
        attempt.refresh_from_db()
        self.assertEqual(attempt.status, "failed")
        self.download.assert_not_called()

    def test_interrupted_claim_is_failed_but_direct_attempt_is_untouched(self):
        abandoned = DataReleaseSyncAttempt.objects.create(
            release_id="old", bucket="trusted", status="importing", worker_id=uuid.uuid4())
        direct = DataReleaseSyncAttempt.objects.create(
            release_id="direct", bucket="trusted", status="downloading")
        process_release_sync_queue()
        abandoned.refresh_from_db()
        direct.refresh_from_db()
        self.assertEqual(abandoned.error_code, "WorkerInterrupted")
        self.assertEqual(abandoned.status, "failed")
        self.assertEqual(direct.status, "downloading")

    def test_failure_does_not_block_next_queued_request(self):
        enqueue_release_sync("bad-release")
        enqueue_release_sync("good-release")

        def download(bucket, release_id, output, **kwargs):
            if release_id == "bad-release":
                raise OSError("secret")
            self.copy_release(bucket, release_id, output, **kwargs)

        self.download.side_effect = download
        processed = process_release_sync_queue(limit=2)
        self.assertEqual([attempt.status for attempt in processed], ["failed", "succeeded"])

    def test_worker_session_loss_prevents_import(self):
        enqueue_release_sync("test-release")

        def disconnect(*args, **kwargs):
            self.copy_release(*args, **kwargs)
            connection.close()

        self.download.side_effect = disconnect
        processed = process_release_sync_queue()
        self.assertEqual(processed[0].status, "failed")
        self.assertFalse(DataReleaseState.objects.exists())

    def test_command_confirmation_limits_and_results(self):
        with self.assertRaises(CommandError):
            call_command("queue_data_release", release_id="test-release")
        self.assertFalse(DataReleaseSyncAttempt.objects.exists())
        output = io.StringIO()
        call_command("queue_data_release", release_id="test-release",
                     requested_by="operator", confirm_replace_data=True, stdout=output)
        self.assertIn("Queued", output.getvalue())
        for limit in (0, 101):
            with self.assertRaises(CommandError):
                call_command("process_release_sync_queue", limit=limit)
        output = io.StringIO()
        call_command("process_release_sync_queue", stdout=output)
        self.assertIn("succeeded", output.getvalue())

    def test_overlapping_worker_does_not_claim_or_recover_live_attempt(self):
        entered = Event()
        release_worker = Event()
        enqueue_release_sync("test-release")

        def download(*args, **kwargs):
            entered.set()
            if not release_worker.wait(timeout=10):
                raise RuntimeError("Worker test timed out")
            self.copy_release(*args, **kwargs)

        def worker():
            try:
                return process_release_sync_queue()
            finally:
                connections.close_all()

        self.download.side_effect = download
        with ThreadPoolExecutor(max_workers=1) as executor:
            running = executor.submit(worker)
            try:
                self.assertTrue(entered.wait(timeout=10))
                self.assertEqual(process_release_sync_queue(), [])
                self.assertEqual(DataReleaseSyncAttempt.objects.get().status, "downloading")
            finally:
                release_worker.set()
            self.assertEqual(running.result()[0].status, "succeeded")