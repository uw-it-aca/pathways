import io
import json
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest import skipUnless
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, connection, connections, transaction
from django.test import TransactionTestCase

from pathways.models import DataReleaseState, DataReleaseSyncAttempt
from pathways.models.course import Course
from pathways.models.data_import import DataImport
from pathways.release_sync import ReleaseSyncError, sync_release
from pathways.tests.commands.test_data_release import write_release


class ReleaseSyncTest(TransactionTestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.release, _ = write_release(self.root)
        self.staging = self.root / "staging"
        self.staging.mkdir()
        self.download = self.enterContext(patch(
            "pathways.release_sync.download_release", side_effect=self.copy_release))

    def copy_release(self, bucket, release_id, output, **kwargs):
        self.assertEqual(DataReleaseSyncAttempt.objects.first().status, "downloading")
        shutil.copytree(self.release, output)

    def sync(self):
        return sync_release("trusted-bucket", "test-release", prefix="app/",
                            requested_by="operator", temporary_root=self.staging)

    def test_success_repeat_and_cleanup(self):
        attempt = self.sync()
        self.assertEqual(attempt.status, "succeeded")
        self.assertEqual(attempt.requested_by, "operator")
        self.assertEqual(attempt.prefix, "app")
        self.assertIsNotNone(attempt.completed_on)
        self.assertEqual(DataReleaseState.objects.get().current_release_id, "test-release")
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(list(self.staging.iterdir()), [])
        repeat = self.sync()
        self.assertEqual(repeat.status, "unchanged")
        self.assertEqual(DataReleaseSyncAttempt.objects.count(), 2)
        self.assertEqual(list(self.staging.iterdir()), [])

    def test_download_failure_is_recorded_without_secrets(self):
        self.download.side_effect = OSError("secret signed URL credential")
        with self.assertRaises(ReleaseSyncError) as raised:
            self.sync()
        attempt = raised.exception.attempt
        self.assertEqual(attempt.status, "failed")
        self.assertEqual(attempt.error_code, "OSError")
        self.assertNotIn("secret", str(raised.exception))
        self.assertNotIn("secret", attempt.error_message)
        self.assertIsNotNone(attempt.completed_on)
        self.assertFalse(DataReleaseState.objects.exists())
        self.assertFalse(Course.objects.exists())
        self.assertEqual(list(self.staging.iterdir()), [])

    def test_import_failure_preserves_catalog_and_current_release(self):
        self.sync()
        before = list(Course.objects.values())
        with patch("pathways.data_import.import_stem_from_similar_majors",
                   side_effect=IntegrityError("late failure")):
            DataImport.objects.filter(type="course").update(hash="changed")
            with self.assertRaises(ReleaseSyncError) as raised:
                self.sync()
        self.assertEqual(raised.exception.attempt.status, "failed")
        self.assertIn("importing", raised.exception.attempt.error_message)
        self.assertEqual(list(Course.objects.values()), before)
        self.assertEqual(DataReleaseState.objects.get().current_release_id, "test-release")
        self.assertEqual(list(self.staging.iterdir()), [])

    def copy_with_identity(self, bucket, release_id, output, **kwargs):
        shutil.copytree(self.release, output)
        manifest_path = output / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        manifest["release_id"] = release_id
        for name, artifact in manifest["artifacts"].items():
            artifact["version_path"] = f"releases/{release_id}/{name}"
        manifest_path.write_text(json.dumps(manifest))

    def test_switch_and_restore_previous_release(self):
        self.sync()
        self.download.side_effect = self.copy_with_identity
        attempt = sync_release("trusted-bucket", "second-release",
                               temporary_root=self.staging)
        self.assertEqual(attempt.status, "succeeded")
        self.assertEqual(DataReleaseState.objects.get().current_release_id, "second-release")
        restored = self.sync()
        self.assertEqual(restored.status, "succeeded")
        self.assertEqual(DataReleaseState.objects.get().current_release_id, "test-release")
        self.assertEqual(list(self.staging.iterdir()), [])

    def test_success_record_failure_rolls_back_import_and_current_state(self):
        original_save = DataReleaseSyncAttempt.save

        def fail_success(attempt, *args, **kwargs):
            if attempt.status == "succeeded":
                raise IntegrityError("cannot record success")
            return original_save(attempt, *args, **kwargs)

        with patch.object(DataReleaseSyncAttempt, "save", new=fail_success), \
                self.assertRaises(ReleaseSyncError):
            self.sync()
        self.assertEqual(DataReleaseSyncAttempt.objects.get().status, "failed")
        self.assertFalse(Course.objects.exists())
        self.assertFalse(DataReleaseState.objects.exists())

    @skipUnless(connection.vendor == "postgresql", "PostgreSQL row locking required")
    def test_concurrent_syncs_serialize_import_and_record_both_outcomes(self):
        barrier = Barrier(2)

        def concurrent_download(*args, **kwargs):
            self.copy_with_identity(*args, **kwargs)
            barrier.wait(timeout=10)

        def run_sync(release_id):
            try:
                return sync_release("trusted-bucket", release_id,
                                    temporary_root=self.staging)
            finally:
                connections.close_all()

        self.download.side_effect = concurrent_download
        with ThreadPoolExecutor(max_workers=2) as executor:
            attempts = list(executor.map(run_sync, ["first-release", "second-release"]))
        self.assertEqual([attempt.status for attempt in attempts], ["succeeded"] * 2)
        last = DataReleaseSyncAttempt.objects.latest("completed_on")
        self.assertEqual(DataReleaseState.objects.get().current_release_id, last.release_id)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(list(self.staging.iterdir()), [])

    def test_invalid_input_and_nested_transaction_do_not_start_attempt(self):
        for release_id, prefix in (("../bad", ""), ("x" * 129, ""),
                                   ("test-release", "a/../b")):
            with self.assertRaises(ValueError):
                sync_release("bucket", release_id, prefix=prefix)
        with transaction.atomic(), self.assertRaises(ValueError):
            self.sync()
        self.assertFalse(DataReleaseSyncAttempt.objects.exists())
        self.download.assert_not_called()

    def test_command_confirmation_and_result(self):
        options = {"bucket": "trusted-bucket", "release_id": "test-release",
                   "temporary_root": str(self.staging)}
        with self.assertRaises(CommandError):
            call_command("sync_data_release", **options)
        self.assertFalse(DataReleaseSyncAttempt.objects.exists())
        output = io.StringIO()
        call_command("sync_data_release", confirm_replace_data=True,
                     stdout=output, **options)
        self.assertIn("succeeded", output.getvalue())
        self.assertIn(str(DataReleaseSyncAttempt.objects.get().pk), output.getvalue())

    def test_status_command_reports_unknown_current_and_recent_attempts(self):
        output = io.StringIO()
        call_command("data_release_status", stdout=output)
        self.assertEqual(json.loads(output.getvalue()), {
            "current_release": None, "attempts": []})
        self.sync()
        self.sync()
        output = io.StringIO()
        call_command("data_release_status", limit=1, stdout=output)
        result = json.loads(output.getvalue())
        self.assertEqual(result["current_release"]["release_id"], "test-release")
        self.assertEqual(len(result["attempts"]), 1)
        self.assertEqual(result["attempts"][0]["status"], "unchanged")
        for limit in (0, 101):
            with self.assertRaises(CommandError):
                call_command("data_release_status", limit=limit)