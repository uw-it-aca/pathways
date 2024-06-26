# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json

from django.test import TestCase
from pathways.data_import import (
    import_major_data, import_level_coi, import_coi_ranges, _get_course_coi,
    _get_curric_coi)
from pathways.models.major import Major
from pathways.models.course_level import CourseLevel
from pathways.models.coi_range import COIRange


class ImportTest(TestCase):
    test_file_data = None
    coi_data = [{"course_id": "CHEM 101", "coi_score": 2.1},
                {"course_id": "BIO 199", "coi_score": -1},
                {"course_id": "CHEM 201", "coi_score": 3.0},
                {"course_id": "A A 201", "coi_score": 1.1},
                {"course_id": "MATH 222", "coi_score": 2.0},
                {"course_id": "CHEM 301", "coi_score": 3.5},
                {"course_id": "CSE 301", "coi_score": -1},
                {"course_id": "B BIO 301", "coi_score": 5.0},
                {"course_id": "SPAN 301", "coi_score": 4.2},
                {"course_id": "CSS 301", "coi_score": 1.9},
                {"course_id": "CHEM 401", "coi_score": 2.1}]

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
        import_level_coi(self.coi_data)
        cl_1 = CourseLevel.objects.get(level=100)
        cl_2 = CourseLevel.objects.get(level=200)
        cl_3 = CourseLevel.objects.get(level=300)
        self.assertEqual(cl_1.coi_score, 2.1)
        self.assertEqual(cl_2.coi_score, 2)
        self.assertEqual(cl_3.coi_score, 3.6)

    def test_import_coi_ranges(self):
        import_coi_ranges(self.coi_data)
        cr_0 = COIRange.objects.get(coi_range=0)
        cr_2 = COIRange.objects.get(coi_range=2)
        cr_4 = COIRange.objects.get(coi_range=4)

        self.assertEqual(cr_0.percent_in_range, 0)
        self.assertEqual(cr_2.percent_in_range, 0.2727272727272727)
        self.assertEqual(cr_4.percent_in_range, 0.18181818181818182)

    def test_course_coi(self):
        coi = _get_course_coi("B BIO 301", self.coi_data)
        self.assertEqual(coi, 5.0)

    def test_curric_coi(self):
        curric_coi = _get_curric_coi(self.coi_data)
        self.assertEqual(curric_coi.get("A A"), [1.1])
        self.assertEqual(curric_coi.get("CHEM"), [2.1, 3.0, 3.5, 2.1])
