# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Tests for data release promotion feature."""

import json
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from google.api_core.exceptions import ServiceUnavailable

from pathways.data_release import RELEASE_FILES, release_artifacts
from pathways.models import DataReleaseImport, DataReleaseState
from pathways.release_promotion_api import (
    ReleaseLister,
    queue_release_for_promotion,
)
from pathways.views.api.release_promotion import (
    get_release_manifest,
    list_releases,
)
from pathways.views.support import DataReleaseSpaToolView


class ReleaseListerTestCase(TestCase):
    """Test ReleaseLister with mocked GCS."""

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_promotion_api.storage.Client")
    def test_list_available_releases(self, mock_client_class):
        """Test listing releases with mocked GCS."""
        # Setup mock GCS client
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket

        # Mock list_blobs to return manifests alongside release artifacts.
        mock_blob1 = MagicMock()
        mock_blob1.name = "releases/release-001/manifest.json"
        mock_blob1.size = 1024
        mock_blob1.md5_hash = "abc123"
        mock_blob1.updated.isoformat.return_value = "2026-11-06T10:00:00"

        mock_artifact = MagicMock()
        mock_artifact.name = "releases/release-001/course_data.json"

        mock_nested_manifest = MagicMock()
        mock_nested_manifest.name = (
            "releases/release-001/archive/manifest.json")

        mock_blob2 = MagicMock()
        mock_blob2.name = "releases/release-002/manifest.json"
        mock_blob2.size = 2048
        mock_blob2.md5_hash = "def456"
        mock_blob2.updated.isoformat.return_value = "2026-11-05T10:00:00"

        mock_bucket.list_blobs.return_value = [
            mock_blob1, mock_artifact, mock_nested_manifest, mock_blob2]

        # Test
        lister = ReleaseLister()
        releases = lister.list_available_releases()

        # Verify
        mock_bucket.list_blobs.assert_called_once_with(prefix="releases/")
        mock_bucket.get_blob.assert_not_called()
        self.assertEqual(len(releases), 2)
        self.assertEqual(releases[0]["release_id"], "release-001")
        self.assertEqual(releases[0]["manifest_size"], 1024)
        # Most recent first
        self.assertEqual(releases[0]["updated"], "2026-11-06T10:00:00")

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket",
    RELEASE_SYNC_PREFIX="catalog")
    @patch("pathways.release_promotion_api.storage.Client")
    def test_configured_prefix_is_used_for_listing_and_manifest(self,
    mock_client_class):
        bucket = mock_client_class.return_value.bucket.return_value
        bucket.list_blobs.return_value = []
        blob = bucket.get_blob.return_value
        blob.exists.return_value = True
        blob.download_as_text.return_value = '{"release_id": "release-001"}'

        lister = ReleaseLister()
        self.assertEqual(lister.list_available_releases(), [])
        self.assertEqual(
            lister.get_release_manifest("release-001")["release_id"],
            "release-001")
        bucket.list_blobs.assert_called_once_with(
            prefix="catalog/releases/")
        bucket.get_blob.assert_called_once_with(
            "catalog/releases/release-001/manifest.json")

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_promotion_api.storage.Client")
    def test_get_release_manifest(self, mock_client_class):
        """Test fetching release manifest with mocked GCS."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket

        manifest_data = {
            "release_id": "test-release-001",
            "version": "1.0",
            "tables": ["courses", "majors"],
            "created": "2026-11-06T00:00:00Z",
        }

        mock_blob = MagicMock()
        mock_blob.exists.return_value = True
        mock_blob.download_as_text.return_value = json.dumps(manifest_data)
        mock_bucket.get_blob.return_value = mock_blob

        # Test
        lister = ReleaseLister()
        manifest = lister.get_release_manifest("test-release-001")

        # Verify
        self.assertEqual(manifest["release_id"], "test-release-001")
        self.assertEqual(manifest["version"], "1.0")
        self.assertIn("courses", manifest["tables"])

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_promotion_api.storage.Client")
    def test_release_id_validation(self, mock_client_class):
        """Test that invalid release IDs are rejected."""
        # Setup mock
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket
        mock_bucket.get_blob.return_value = None

        lister = ReleaseLister()

        # Invalid IDs - should raise ValueError with "Invalid release ID"
        invalid_ids = [
            "release/001",  # path traversal
            "release 001",  # space
            "release@001",  # special char
            "../../etc/passwd",  # path traversal
        ]

        for release_id in invalid_ids:
            with self.assertRaises(ValueError) as cm:
                lister.get_release_manifest(release_id)
            self.assertIn("Invalid release ID", str(cm.exception))

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_promotion_api.storage.Client")
    def test_storage_and_manifest_errors(self, mock_client_class):
        bucket = mock_client_class.return_value.bucket.return_value
        lister = ReleaseLister()

        bucket.list_blobs.side_effect = ServiceUnavailable("down")
        with self.assertRaisesRegex(ValueError, "Failed to list"):
            lister.list_available_releases()

        bucket.get_blob.return_value = None
        with self.assertRaisesRegex(ValueError, "Release not found"):
            lister.get_release_manifest("release-001")

        blob = bucket.get_blob.return_value = MagicMock()
        blob.download_as_text.return_value = "not json"
        with self.assertRaisesRegex(ValueError, "Invalid manifest"):
            lister.get_release_manifest("release-001")

        blob.download_as_text.return_value = "[]"
        with self.assertRaisesRegex(TypeError, "Invalid manifest format"):
            lister.get_release_manifest("release-001")

        blob.download_as_text.side_effect = ServiceUnavailable("down")
        with self.assertRaisesRegex(ValueError, "Failed to fetch"):
            lister.get_release_manifest("release-001")


@override_settings(RELEASE_PROMOTION_MOCK=False)
class ReleasePromotionAPITestCase(TestCase):
    """Test release promotion API endpoints."""

    def setUp(self):
        self.factory = RequestFactory()
        patcher = patch("pathways.views.is_member_of_group", return_value=True)
        self.mock_is_member = patcher.start()
        self.addCleanup(patcher.stop)

    def _login_non_member(self):
        user = get_user_model().objects.create_user(username="javerage")
        self.client.force_login(user)
        self.mock_is_member.return_value = False

    def test_list_releases_denied_for_non_member(self):
        self._login_non_member()
        response = self.client.get("/api/v1/admin/releases/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            self.mock_is_member.call_args.args[1], settings.ADMIN_USERS_GROUP)

    def test_promote_release_denied_for_non_member(self):
        self._login_non_member()
        response = self.client.post(
            "/api/v1/admin/releases/promote/",
            data=json.dumps({"release_id": "release-001"}),
            content_type="application/json")
        self.assertEqual(response.status_code, 401)

    @patch("pathways.views.api.release_promotion.queue_release_for_promotion")
    def test_promote_release_uses_real_queue_when_mock_disabled(self,
    mock_queue):
        mock_queue.return_value = {"success": True, "queue_attempt_id": 42}
        admin_user = get_user_model().objects.create_user(username="admin")
        self.client.force_login(admin_user)
        response = self.client.post(
            "/api/v1/admin/releases/promote/",
            data=json.dumps({"release_id": "release-001"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_queue.assert_called_once_with("release-001", requested_by="admin")
        self.assertEqual(response.json()["data"]["queue_attempt_id"], 42)

    @patch("pathways.views.api.release_promotion.queue_release_for_promotion")
    def test_promote_release_rejects_malformed_body(self, mock_queue):
        admin_user = get_user_model().objects.create_user(username="admin")
        self.client.force_login(admin_user)
        cases = (
            (b"\xff", "invalid_json"),
            (b"[]", "invalid_body"),
            (b"null", "invalid_body"),
            (b'{"release_id": 42}', "invalid_field"),
            (b'{"release_id": null}', "invalid_field"),
        )
        for body, error_code in cases:
            with self.subTest(body=body):
                response = self.client.post(
                    "/api/v1/admin/releases/promote/",
                    data=body, content_type="application/json")
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()["error_code"], error_code)
        mock_queue.assert_not_called()

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.views.api.release_promotion.ReleaseLister")
    def test_list_releases_endpoint(self, mock_lister_class):
        """Test list_releases API endpoint."""
        mock_lister = MagicMock()
        mock_lister_class.return_value = mock_lister

        mock_releases = [
            {
                "release_id": "release-001",
                "manifest_size": 1024,
                "updated": "2026-11-06T10:00:00",
            },
            {
                "release_id": "release-002",
                "manifest_size": 2048,
                "updated": "2026-11-05T10:00:00",
            },
        ]
        mock_lister.list_available_releases.return_value = mock_releases

        # Create request with mock user
        request = self.factory.get("/api/v1/admin/releases/")
        request.user = MagicMock()
        request.user.is_authenticated = True
        request.user.groups.filter.return_value.exists.return_value = True

        # Test
        response = list_releases(request)
        response_data = json.loads(response.content)

        # Verify
        self.assertTrue(response_data["success"])
        self.assertEqual(len(response_data["releases"]), 2)
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["current_release_id"])

    @patch("pathways.views.api.release_promotion.ReleaseLister")
    def test_list_releases_returns_tracked_current_release(self, mock_lister):
        mock_lister.return_value.list_available_releases.return_value = []
        release = DataReleaseImport.objects.create(
            release_id="current-release", manifest_sha256="a" * 64)
        DataReleaseState.objects.create(current_release=release)
        admin_user = get_user_model().objects.create_user(username="admin")
        self.client.force_login(admin_user)

        response = self.client.get("/api/v1/admin/releases/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["current_release_id"],
            "current-release")

    @override_settings(RELEASE_SYNC_BUCKET=None)
    def test_list_releases_missing_bucket_config(self):
        """Test list_releases with missing RELEASE_SYNC_BUCKET."""
        request = self.factory.get("/api/v1/admin/releases/")
        request.user = MagicMock()
        request.user.is_authenticated = True
        request.user.groups.filter.return_value.exists.return_value = True

        response = list_releases(request)
        response_data = json.loads(response.content)

        # Should return error (no "success" key, has "error" key)
        self.assertNotIn("success", response_data)
        self.assertIn("error", response_data)
        self.assertEqual(response.status_code, 500)

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.views.api.release_promotion.ReleaseLister")
    def test_get_release_manifest_endpoint(self, mock_lister_class):
        """Test get_release_manifest API endpoint."""
        mock_lister = MagicMock()
        mock_lister_class.return_value = mock_lister

        manifest_data = {
            "release_id": "test-release",
            "version": "1.0",
            "tables": ["courses", "majors"],
        }
        mock_lister.get_release_manifest.return_value = manifest_data

        # Create request
        request = self.factory.get(
            "/api/v1/admin/releases/test-release/manifest/"
        )
        request.user = MagicMock()
        request.user.is_authenticated = True
        request.user.groups.filter.return_value.exists.return_value = True

        # Test
        response = get_release_manifest(request, release_id="test-release")
        response_data = json.loads(response.content)

        # Verify
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["manifest"]["release_id"],
        "test-release")

    def _admin_login(self):
        admin_user = get_user_model().objects.create_user(username="admin")
        self.client.force_login(admin_user)

    @patch("pathways.views.api.release_promotion.ReleaseLister")
    def test_unexpected_errors_return_internal_error(self, mock_lister):
        self._admin_login()
        lister = mock_lister.return_value
        lister.list_available_releases.side_effect = RuntimeError("boom")
        lister.get_release_manifest.side_effect = RuntimeError("boom")

        responses = (
            self.client.get("/api/v1/admin/releases/"),
            self.client.get("/api/v1/admin/releases/release-001/manifest/"),
        )
        with patch("pathways.views.api.release_promotion."
                   "queue_release_for_promotion",
                   side_effect=RuntimeError("boom")):
            responses += (self.client.post(
                "/api/v1/admin/releases/promote/",
                data=json.dumps({"release_id": "release-001"}),
                content_type="application/json"),)

        for response in responses:
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()["error_code"], "internal_error")
            self.assertNotIn("boom", response.json()["error"])

    @patch("pathways.views.api.release_promotion.ReleaseLister")
    def test_missing_manifest_returns_not_found(self, mock_lister):
        self._admin_login()
        mock_lister.return_value.get_release_manifest.side_effect = (
            ValueError("Release not found: release-001"))
        response = self.client.get(
            "/api/v1/admin/releases/release-001/manifest/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error_code"], "not_found")

    @patch("pathways.views.api.release_promotion.queue_release_for_promotion")
    def test_promote_release_requires_release_id(self, mock_queue):
        self._admin_login()
        for body in ({}, {"release_id": "  "}):
            with self.subTest(body=body):
                response = self.client.post(
                    "/api/v1/admin/releases/promote/",
                    data=json.dumps(body), content_type="application/json")
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()["error_code"],
                                 "missing_field")
        mock_queue.assert_not_called()


@override_settings(RELEASE_PROMOTION_MOCK=True)
class MockReleasePromotionAPITestCase(TestCase):
    def setUp(self):
        admin_user = get_user_model().objects.create_user(username="admin")
        self.client.force_login(admin_user)
        group_patcher = patch(
            "pathways.views.is_member_of_group", return_value=True)
        group_patcher.start()
        self.addCleanup(group_patcher.stop)

    @patch("pathways.release_promotion_api.storage.Client")
    @patch("pathways.views.api.release_promotion.queue_release_for_promotion")
    def test_local_release_workflow_never_contacts_storage_or_queues(
        self, mock_queue, mock_storage
    ):
        response = self.client.get("/api/v1/admin/releases/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["mock"])
        releases = response.json()["releases"]
        self.assertGreaterEqual(len(releases), 2)
        self.assertEqual(response.json()["current_release_id"],
        releases[1]["release_id"])
        release_id = releases[0]["release_id"]

        url = f"/api/v1/admin/releases/{release_id}/manifest/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        manifest = response.json()["manifest"]
        self.assertEqual(manifest["release_id"], release_id)
        self.assertEqual(set(manifest["artifacts"]), RELEASE_FILES)
        self.assertEqual(release_artifacts(manifest, release_id),
        manifest["artifacts"])

        response = self.client.post(
            "/api/v1/admin/releases/promote/",
            data=json.dumps({"release_id": release_id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["data"]["mock"])
        response = self.client.get("/api/v1/admin/releases/")
        self.assertEqual(response.json()["current_release_id"],
        releases[1]["release_id"])
        mock_storage.assert_not_called()
        mock_queue.assert_not_called()

    @patch("pathways.views.api.release_promotion.queue_release_for_promotion")
    def test_unknown_release_cannot_be_simulated(self, mock_queue):
        response = self.client.post(
            "/api/v1/admin/releases/promote/",
            data=json.dumps({"release_id": "unknown"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        mock_queue.assert_not_called()

    @patch("pathways.views.is_member_of_group", return_value=False)
    def test_mock_endpoints_still_require_admin_access(self, mock_is_member):
        response = self.client.get("/api/v1/admin/releases/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            self.client.post(
                "/api/v1/admin/releases/promote/",
                data=json.dumps({"release_id": "local-sample-20261116"}),
                content_type="application/json",
            ).status_code,
            401,
        )
        self.assertEqual(mock_is_member.call_args.args[1],
        settings.ADMIN_USERS_GROUP)


class QueueReleaseTestCase(TestCase):
    """Test queuing releases for promotion."""

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_sync_queue.enqueue_release_sync")
    @patch("pathways.release_promotion_api.ReleaseLister")
    def test_queue_release_for_promotion(self, mock_lister_class,
    mock_enqueue):
        """Test queue_release_for_promotion function."""
        # Setup mocks
        mock_lister = MagicMock()
        mock_lister_class.return_value = mock_lister

        manifest_data = {
            "release_id": "test-release",
            "schema_version": "2.0",
            "version": "1.0",
        }
        mock_lister.get_release_manifest.return_value = manifest_data

        mock_attempt = MagicMock()
        mock_attempt.pk = 123
        mock_enqueue.return_value = (mock_attempt, True)

        # Test
        result = queue_release_for_promotion(
            "test-release", requested_by="testuser"
        )

        # Verify
        self.assertTrue(result["success"])
        self.assertEqual(result["queue_attempt_id"], 123)
        self.assertEqual(result["release_id"], "test-release")

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    def test_queue_release_invalid_id(self):
        """Test that queue_release rejects invalid release IDs."""
        with self.assertRaises(ValueError) as cm:
            queue_release_for_promotion("../../etc/passwd")

        self.assertIn("Invalid release ID", str(cm.exception))

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_sync_queue.enqueue_release_sync")
    @patch("pathways.release_promotion_api.ReleaseLister")
    def test_queue_release_rejects_incompatible_manifest(self, mock_lister,
                                                         mock_enqueue):
        for manifest, message in (
                ({"release_id": "other", "schema_version": "2.0"},
                 "Release ID mismatch"),
                ({"release_id": "test-release", "schema_version": "1.0"},
                 "requires release schema")):
            mock_lister.return_value.get_release_manifest.return_value = (
                manifest)
            with self.subTest(message=message), \
                    self.assertRaisesRegex(ValueError, message):
                queue_release_for_promotion("test-release")
        mock_enqueue.assert_not_called()

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_sync_queue.enqueue_release_sync")
    @patch("pathways.release_promotion_api.ReleaseLister")
    def test_queue_release_reports_existing_attempt(self, mock_lister,
                                                    mock_enqueue):
        mock_lister.return_value.get_release_manifest.return_value = {
            "release_id": "test-release", "schema_version": "1.1"}
        mock_enqueue.return_value = (MagicMock(pk=7), False)
        result = queue_release_for_promotion("test-release")
        self.assertEqual(result["message"],
                         "Release test-release already queued (attempt 7)")


class DataReleaseSpaToolViewTestCase(TestCase):
    """Test the SPA tool view."""

    @patch("pathways.views.is_member_of_group", return_value=True)
    @patch("supporttools.templatetags.vite._load_manifest")
    def test_registered_spa_page(self, mock_manifest, mock_is_member):
        mock_manifest.return_value = {
            "pathways_vue/support/data-release-promotion.js": {
                "file": "pathways/assets/release.js",
                "css": ["pathways/assets/release.css"],
            },
        }
        user = get_user_model().objects.create_user(username="testuser")
        self.client.force_login(user)

        response = self.client.get("/support/data_release_promotion/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="supporttools-vue-nav"')
        self.assertContains(response, 'id="spa-tool-app"')
        self.assertContains(response, "/static/supporttools/js/main.js")
        self.assertContains(response, "/static/pathways/assets/release.js")
        self.assertContains(response, "/static/pathways/assets/release.css")
        self.assertContains(response, '"username": "testuser"')
        self.assertEqual(mock_is_member.call_args.args[1],
        settings.ADMIN_USERS_GROUP)

    @patch("pathways.views.is_member_of_group", return_value=False)
    def test_registered_spa_page_denied_for_non_member(self, mock_is_member):
        user = get_user_model().objects.create_user(username="nonmember")
        self.client.force_login(user)

        response = self.client.get("/support/data_release_promotion/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(mock_is_member.call_args.args[1],
        settings.ADMIN_USERS_GROUP)

    def test_spa_tool_view_get_page_data(self):
        """Test SPA tool view returns proper page data."""
        view = DataReleaseSpaToolView()

        # Create mock request with authenticated user
        mock_request = MagicMock()
        mock_request.user.is_authenticated = True
        mock_request.user.get_username.return_value = "testuser"
        view.request = mock_request

        page_data = view.get_page_data()

        # Verify
        self.assertTrue(page_data["can_promote"])
        self.assertEqual(page_data["username"], "testuser")

    def test_spa_tool_view_unauthenticated(self):
        """Test SPA tool view with unauthenticated user."""
        view = DataReleaseSpaToolView()

        # Create mock request with unauthenticated user
        mock_request = MagicMock()
        mock_request.user.is_authenticated = False
        view.request = mock_request

        page_data = view.get_page_data()

        # Verify
        self.assertTrue(page_data["can_promote"])  # Auth checked by decorator
        self.assertIsNone(page_data["username"])
