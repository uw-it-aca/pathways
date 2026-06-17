# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from pathways.views.pages import DefaultPageView
from userservice.user import UserService, UserServiceMiddleware
from importlib import reload
import mock
import sys


class PagesViewTest(TestCase):
    databases = "__all__"
    fixtures = ["person.json", "employee.json", "term.json", "major.json",
                "student.json", "adviser.json", "transfer.json",
                "transcript.json", "hold.json", "degree.json", "sport.json"]

    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.user = User()
        self.request.session = {}
        UserServiceMiddleware().process_request(self.request)
        get_response = mock.MagicMock()
        middleware = SessionMiddleware(get_response)
        response = middleware(self.request)
        self.request.session.save()

    @mock.patch.object(UserService, "get_user", return_value="javerage")
    def test_context(self, mock_get_user):
        with self.settings(GOOGLE_ANALYTICS_KEY=""):
            response = DefaultPageView.as_view()(self.request)
            self.assertIsInstance(response.context_data, dict)
            self.assertEqual(
                response.context_data["context_data"].get(
                    "googleAnalyticsKey"), "")
            self.assertEqual(
                response.context_data["context_data"].get("debugMode"), False
            )
            user_data = response.context_data["context_data"].get("personData")
            self.assertEqual(user_data.get("uwnetid"), "javerage")
            self.assertEqual(user_data.get("student_number"), "1033334")

    @mock.patch.object(UserService, "get_user", return_value="nobody")
    def test_context_unknown_user(self, mock_get_user):
        response = DefaultPageView.as_view()(self.request)
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(
            response.context_data["context_data"].get("personData"), {})

    def test_auth(self):
        with self.settings(LIMIT_USER_ACCESS=True):
            response = DefaultPageView.as_view()(self.request)
            self.assertEqual(response.status_code, 401)

    @mock.patch("pathways.views.is_member_of_group", return_value=True)
    def test_is_member(self, im):
        with self.settings(LIMIT_USER_ACCESS=True):
            response = DefaultPageView.as_view()(self.request)
            self.assertEqual(response.status_code, 200)

    def test_debug_urls(self):
        with self.settings(DEBUG=True):
            reload(sys.modules["pathways.urls"])
            reload(sys.modules["project.urls"])
            try:
                reverse("500_response")
            except NoReverseMatch:
                self.fail("500 reverse not found")
