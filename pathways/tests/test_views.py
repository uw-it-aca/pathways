# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from pathways.views.pages import DefaultPageView
from importlib import reload
import mock
import sys


class PagesViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.user = User()
        get_response = mock.MagicMock()
        middleware = SessionMiddleware(get_response)
        response = middleware(self.request)
        self.request.session.save()

    def test_context(self):
        with self.settings(GOOGLE_ANALYTICS_KEY=" "):
            response = DefaultPageView.as_view()(self.request)
            self.assertIsInstance(response.context_data, dict)
            self.assertEqual(response.context_data.get('ga_key'), ' ')
            self.assertEqual(response.context_data.get('django_debug'), False)

    def test_auth(self):
        with self.settings(LIMIT_USER_ACCESS=True):
            response = DefaultPageView.as_view()(self.request)
            self.assertEqual(response.status_code, 401)

    @mock.patch('pathways.views.is_member_of_group', return_value=True)
    def test_is_member(self, im):
        with self.settings(LIMIT_USER_ACCESS=True):
            response = DefaultPageView.as_view()(self.request)
            self.assertEqual(response.status_code, 200)

    def test_debug_urls(self):
        with self.settings(DEBUG=True):
            reload(sys.modules['pathways.urls'])
            reload(sys.modules['project.urls'])
            try:
                reverse('500_response')
            except NoReverseMatch:
                self.fail('500 reverse not found')
