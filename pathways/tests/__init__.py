# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
import json
from pathways.data_import import import_major_data


class ApiTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.user = User()
        SessionMiddleware().process_request(self.request)
        self.request.session.save()
        with open('pathways/tests/sample_major_import.json') as json_file:
            test_file_data = json.load(json_file)
            import_major_data(test_file_data)
