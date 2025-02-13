# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.tests import ApiTest
from pathways.views.api.major import MajorDetails, MajorList
from pathways.views.api.coi import CurricCOI, CourseCOI
from pathways.views.api.user import UserPreference
from django.test import RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch
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

    def test_errors(self):
        response = MajorList.as_view()(self.request, major_campus="pluto")
        self.assertEqual(response.status_code, 400)
        response = MajorDetails.as_view()(self.request,
                                          credential_abbr="Fake-Cred")
        self.assertEqual(response.status_code, 404)


class TestCoiApi(ApiTest):
    def setUp(self):
        super(TestCoiApi, self).setUp()

    def test_curric(self):
        response = CurricCOI.as_view()(self.request)
        curric_coi = json.loads(response.content)
        self.assertEqual(len(curric_coi), 1)
        self.assertEqual(curric_coi[0]['curric_name'], "TRAINING")
        self.assertEqual(curric_coi[0]['score'], 1.9)

    def test_course(self):
        response = CourseCOI.as_view()(self.request,
                                       department_abbrev='TRAIN')
        course_coi = json.loads(response.content)
        self.assertEqual(len(course_coi), 19)
        self.assertEqual(course_coi[0]['score'], 2.1)
        self.assertEqual(course_coi[0]['course_id'], "TRAIN 1")


class TestUserApi(ApiTest):
    def setUp(self):
        super(TestUserApi, self).setUp()

    @patch('pathways.views.api.user.get_user', return_value='javerage')
    def test_user(self, mock_get_user):
        request = RequestFactory().post('/',
                                        data={
                                            'viewed_welcome_display': True,
                                            'viewed_bottleneck_banner': True,
                                            'viewed_outcomes_banner': True,
                                            'viewed_coi_banner': True
                                        },
                                        content_type='application/json')
        request.user = User()
        response = UserPreference.as_view()(request)
        self.assertEqual(response.status_code, 200)

        response = UserPreference.as_view()(request)
        self.assertEqual(response.status_code, 304)
