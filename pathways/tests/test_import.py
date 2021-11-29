# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json

from django.test import TestCase
from pathways.data_import import import_major_data
from pathways.models.major import Major


class ImportTest(TestCase):
    test_file_data = None

    def setUp(self):
        with open('pathways/tests/sample_major_import.json') as json_file:
            self.test_file_data = json.load(json_file)

    def test_context(self):
        majors = Major.objects.all()
        self.assertEqual(len(majors), 0)
        import_major_data(self.test_file_data)
        majors = Major.objects.all()
        self.assertEqual(len(majors), 1)

        self.assertEqual(majors[0].major_abbr, "TRAIN")
        url = "www.washington.edu/students/gencat/academic/rail_stud.html"
        self.assertEqual(majors[0].major_home_url, url)
