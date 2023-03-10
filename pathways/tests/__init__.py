# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
import json
from pathways.data_import import import_major_data, import_course_data, \
    import_curric_data
import csv


class ApiTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.user = User()
        SessionMiddleware().process_request(self.request)
        self.request.session.save()
        with open('pathways/tests/sample_coi_import.json') as coi_file:
            reader = csv.reader(coi_file)
            # skip headers
            next(reader)
            coi_data = []
            for row in reader:
                coi_data.append({"course_id": row[0],
                                 "coi_score": float(row[1])})
            with open('pathways/tests/sample_major_import.json') as json_file:
                test_file_data = json.load(json_file)
                import_major_data(test_file_data)
            with open('pathways/tests/sample_course_import.json') as json_file:
                test_file_data = json.load(json_file)
                import_course_data(test_file_data, coi_data)
            with open('pathways/tests/sample_curric_import.json') as json_file:
                test_file_data = json.load(json_file)
                import_curric_data(test_file_data, coi_data)
