# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Tests for data release promotion feature."""

import json
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings

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

        # Mock list_blobs to return paginated results
        mock_blob1 = MagicMock()
        mock_blob1.size = 1024
        mock_blob1.md5_hash = "abc123"
        mock_blob1.updated.isoformat.return_value = "2026-11-06T10:00:00"

        mock_blob2 = MagicMock()
        mock_blob2.size = 2048
        mock_blob2.md5_hash = "def456"
        mock_blob2.updated.isoformat.return_value = "2026-11-05T10:00:00"

        mock_bucket.get_blob.side_effect = lambda path: (
            mock_blob1 if "release-001" in path else
            mock_blob2 if "release-002" in path else
            None
        )

        # Mock iterator pages
        mock_page = MagicMock()
        mock_page.prefixes = ["releases/release-001/", "releases/release-002/"]
        mock_iterator = MagicMock()
        mock_iterator.pages = [mock_page]
        mock_bucket.list_blobs.return_value = mock_iterator

        # Test
        lister = ReleaseLister()
        releases = lister.list_available_releases()

        # Verify
        self.assertEqual(len(releases), 2)
        self.assertEqual(releases[0]["release_id"], "release-001")
        self.assertEqual(releases[0]["manifest_size"], 1024)
        # Most recent first
        self.assertEqual(releases[0]["updated"], "2026-11-06T10:00:00")

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
        self.assertEqual(response_data["manifest"]["release_id"], "test-release")


class QueueReleaseTestCase(TestCase):
    """Test queuing releases for promotion."""

    @override_settings(RELEASE_SYNC_BUCKET="test-bucket")
    @patch("pathways.release_sync_queue.enqueue_release_sync")
    @patch("pathways.release_promotion_api.ReleaseLister")
    def test_queue_release_for_promotion(self, mock_lister_class, mock_enqueue):
        """Test queue_release_for_promotion function."""
        # Setup mocks
        mock_lister = MagicMock()
        mock_lister_class.return_value = mock_lister

        manifest_data = {
            "release_id": "test-release",
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


class DataReleaseSpaToolViewTestCase(TestCase):
    """Test the SPA tool view."""

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
