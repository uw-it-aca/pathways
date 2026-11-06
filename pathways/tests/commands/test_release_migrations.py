from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class ReleaseMigrationUpgradeTest(TransactionTestCase):
    def test_queue_migration_preserves_existing_attempt_history(self):
        previous = [("pathways", "0031_data_release_sync")]
        current = [("pathways", "0032_release_sync_queue")]
        executor = MigrationExecutor(connection)
        self.addCleanup(lambda: MigrationExecutor(connection).migrate(current))
        executor.migrate(previous)
        historical_apps = executor.loader.project_state(previous).apps
        attempt_model = historical_apps.get_model("pathways", "DataReleaseSyncAttempt")
        attempt = attempt_model.objects.create(
            release_id="previous-release", bucket="trusted", status="succeeded",
            requested_by="operator")
        executor = MigrationExecutor(connection)
        executor.migrate(current)
        upgraded = executor.loader.project_state(current).apps.get_model(
            "pathways", "DataReleaseSyncAttempt").objects.get(pk=attempt.pk)
        self.assertEqual(upgraded.status, "succeeded")
        self.assertEqual(upgraded.requested_by, "operator")
        self.assertIsNone(upgraded.worker_id)
        self.assertIsNone(upgraded.claimed_on)

    def test_upgrade_from_deployed_search_graph_preserves_catalog(self):
        deployed = [("pathways", "0029_postgres_search_columns")]
        current = [("pathways", "0032_release_sync_queue")]
        executor = MigrationExecutor(connection)
        self.assertEqual(executor.loader.graph.leaf_nodes("pathways"), current)
        self.addCleanup(lambda: MigrationExecutor(connection).migrate(current))
        executor.migrate(deployed)
        historical_apps = executor.loader.project_state(deployed).apps
        course_model = historical_apps.get_model("pathways", "Course")
        course = course_model.objects.create(
            course_id="INFO 201", course_title="Existing deployed catalog",
            course_credits="5", course_campus="Seattle")
        marker_model = historical_apps.get_model("pathways", "DataImport")
        marker_model.objects.create(type="course", hash="deployed-hash")
        self.assertNotIn("pathways_datareleaseimport", connection.introspection.table_names())

        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(current)
        self.assertEqual([(migration.name, backwards) for migration, backwards in plan], [
            ("0030_datareleaseimport", False), ("0031_data_release_sync", False),
            ("0032_release_sync_queue", False)])
        executor.migrate(current)
        upgraded_apps = executor.loader.project_state(current).apps
        self.assertEqual(upgraded_apps.get_model("pathways", "Course").objects.get(
            pk=course.pk).course_title, "Existing deployed catalog")
        self.assertEqual(upgraded_apps.get_model("pathways", "DataImport").objects.get(
            type="course").hash, "deployed-hash")
        for model_name in ("DataReleaseImport", "DataReleaseState", "DataReleaseSyncAttempt"):
            self.assertFalse(upgraded_apps.get_model("pathways", model_name).objects.exists())
        self.assertEqual(MigrationExecutor(connection).migration_plan(current), [])
