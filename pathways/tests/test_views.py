# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import RequestFactory, TestCase
from pathways.views import PageView


class PagesViewTest(TestCase):
    def test_context(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = PageView.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        # Add tests for context values
