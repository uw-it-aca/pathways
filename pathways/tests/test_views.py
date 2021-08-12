# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from pathways.views import PageView


class PagesViewTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.user = User()
        SessionMiddleware().process_request(self.request)
        self.request.session.save()

    def test_context(self):
        response = PageView.as_view()(self.request)
        self.assertIsInstance(response.context_data, dict)
        # Add tests for context values
