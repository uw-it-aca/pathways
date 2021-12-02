# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json

from django.test import TestCase
from pathways.data_import import import_major_data, import_level_coi
from pathways.models.major import Major
from pathways.models.course_level import CourseLevel


class ImportTest(TestCase):
    test_file_data = None

    def setUp(self):
        with open('pathways/tests/sample_major_import.json') as json_file:
            self.test_file_data = json.load(json_file)

    def test_major(self):
        majors = Major.objects.all()
        self.assertEqual(len(majors), 0)
        import_major_data(self.test_file_data)
        majors = Major.objects.all()
        self.assertEqual(len(majors), 1)

        self.assertEqual(majors[0].major_abbr, "TRAIN")
        url = "www.washington.edu/students/gencat/academic/rail_stud.html"
        self.assertEqual(majors[0].major_home_url, url)

    def test_import_level_coi(self):
        coi_data = [{"course_id": "CHEM 101", "coi_score": 2.1},
                    {"course_id": "BIO 199", "coi_score": -1},
                    {"course_id": "CHEM 201", "coi_score": 3.0},
                    {"course_id": "A A 201", "coi_score": 1.0},
                    {"course_id": "MATH 222", "coi_score": 2.0},
                    {"course_id": "CHEM 301", "coi_score": 3.5},
                    {"course_id": "CSE 301", "coi_score": -1},
                    {"course_id": "B BIO 301", "coi_score": 5.0},
                    {"course_id": "SPAN 301", "coi_score": 4.2},
                    {"course_id": "CSS 301", "coi_score": 1.9},
                    {"course_id": "CHEM 401", "coi_score": 2.1}]
        import_level_coi(coi_data)
        cl_1 = CourseLevel.objects.get(level=100)
        cl_2 = CourseLevel.objects.get(level=200)
        cl_3 = CourseLevel.objects.get(level=300)
        self.assertEqual(cl_1.coi_score, 2.1)
        self.assertEqual(cl_2.coi_score, 2)
        self.assertEqual(cl_3.coi_score, 3.6)
