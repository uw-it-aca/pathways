# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.management import call_command
from pathways.data_import import (
    import_major_data, import_course_data, import_curric_data)
import mock
import json
import csv
from unittest.mock import patch
import shutil


class ApiTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')
        self.request.user = User()
        get_response = mock.MagicMock()
        middleware = SessionMiddleware(get_response)
        response = middleware(self.request)
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


class SearchIndexTest(TestCase):
    TEST_INDEX_DIR = 'test_index_dir'

    def setUp(self):
        try:
            shutil.rmtree(self.TEST_INDEX_DIR)
        except FileNotFoundError:
            pass

        @patch('pathways.management.commands.'
               'import_data.Command.data_needs_update', return_value=True)
        @patch('pathways.management.commands.import_data.COI_PATH',
               "pathways/tests/commands/mock_import_files/coi_scores.csv")
        @patch('pathways.management.commands.import_data.MAJOR_PATH',
               "pathways/tests/commands/mock_import_files/major_data.json")
        @patch('pathways.management.commands.import_data.COURSE_PATH',
               "pathways/tests/commands/mock_import_files/course_data.json")
        @patch('pathways.management.commands.import_data.CURRIC_PATH',
               "pathways/tests/commands/mock_import_files/curric_data.json")
        @patch('pathways.management.commands.import_data.BOTTLENECK_PATH',
               "pathways/tests/commands/"
               "mock_import_files/bottleneck_courses.csv")
        @patch('pathways.management.commands.import_data.GATEWAY_PATH',
               "pathways/tests/commands/mock_import_files/gateway_courses.csv")
        @patch('pathways.management.commands.import_data.CAREER_CENTER_PATH',
               "pathways/tests/commands/"
               "mock_import_files/admit_major_mapping.csv")
        def import_test_data(du):
            call_command('import_data')

        import_test_data()

    def tearDown(self):
        try:
            shutil.rmtree(self.TEST_INDEX_DIR)
        except FileNotFoundError:
            pass
