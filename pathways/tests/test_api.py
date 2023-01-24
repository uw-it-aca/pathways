# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.tests import ApiTest
from pathways.views.api.major import MajorDetails, MajorList
from pathways.views.api.coi import CurricCOI, CourseCOI
import json


class TestMajorApi(ApiTest):
    def setUp(self):
        super(TestMajorApi, self).setUp()

    def test_list(self):
        response = MajorList.as_view()(self.request, major_campus="seattle")
        major_list = json.loads(response.content)
        self.assertEqual(len(major_list), 1)
        self.assertEqual(major_list[0]['key'], "TRAIN-2-1_0")
        self.assertEqual(major_list[0]['value'],
                         "Railroad Studies degree in switching")

    def test_details(self):
        response = MajorDetails.as_view()(self.request,
                                          credential_abbr="TRAIN-2-1_0",
                                          major_campus="seattle")
        major_details = json.loads(response.content)
        self.assertIn("http", major_details['major_home_url'])
        self.assertEqual(major_details['gpa_2yr'][0]['count'], 0)

class TestCoiApi(ApiTest):
    def setUp(self):
        super(TestCoiApi, self).setUp()

    def test_curric(self):
        response = CurricCOI.as_view()(self.request)
        curric_coi = json.loads(response.content)
        self.assertEqual(len(curric_coi), 1)
        self.assertEqual(curric_coi[0]['curric_name'], "TRAINING")
        self.assertEqual(curric_coi[0]['coi'], 1.9)

    def test_course(self):
        response = CourseCOI.as_view()(self.request,
                                       department_abbrev='TRAIN')
        course_coi = json.loads(response.content)
        self.assertEqual(len(course_coi), 33)
        self.assertEqual(course_coi[0]['coi'], 2.1)
        self.assertEqual(course_coi[0]['course_id'], "TRAIN 1")
