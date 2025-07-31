# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.tests import ApiTest
from pathways.views.api import RESTDispatch
from pathways.views.api.major import MajorDetails, MajorList
from pathways.views.api.coi import CurricCOI, CourseCOI
from pathways.views.api.user import UserPreference
from pathways.views.api.search import Search
from pathways.views.api.curric import CurricPrereq
from pathways.views.api.course import CourseList, CourseDetails
from pathways.models.curriculum import Curriculum
from django.test import RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch
import json


class TestApi(ApiTest):
    def setUp(self):
        super(TestApi, self).setUp()

    def test_json_response(self):
        json_resp = RESTDispatch().json_response()
        self.assertEqual(json_resp.status_code, 200)

        json_resp = RESTDispatch().json_response(object)
        self.assertEqual(json_resp.status_code, 400)


class TestMajorApi(ApiTest):
    def setUp(self):
        super(TestMajorApi, self).setUp()

    def test_list(self):
        response = MajorList.as_view()(self.request, major_campus="seattle")
        major_list = json.loads(response.content)
        self.assertEqual(len(major_list), 3)
        self.assertEqual(major_list[0]['key'], "TRAIN-2-1-0")
        self.assertEqual(major_list[0]['value'],
                         "Railroad Studies degree in switching")

    def test_details(self):
        response = MajorDetails.as_view()(self.request,
                                          credential_abbr="TRAIN-2-1-0",
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


class TestSearchApi(ApiTest):
    def setUp(self):
        super(TestSearchApi, self).setUp()

    def _get_response(self, request_data):
        request = RequestFactory().get('/', data=request_data)
        request.user = User()
        return json.loads(Search.as_view()(request).content)

    def test_search(self):
        request_data = {
            'search_string': "transgenic bacterial",
        }
        search = self._get_response(request_data)
        self.assertEqual(len(search['text_matches']), 8)

    def test_no_results(self):
        request_data = {
            'search_string': "efg34",
        }
        search = self._get_response(request_data)
        self.assertEqual(len(search['text_matches']), 0)


class TestCurricApi(ApiTest):
    def setUp(self):
        super(TestCurricApi, self).setUp()
        Curriculum.objects.create(abbrev="CSE")

    def test_get_curric(self):
        response = CurricPrereq.as_view()(self.request, 'CSE')
        self.assertEqual(response.status_code, 200)

        response = CurricPrereq.as_view()(self.request, 'FAKE')
        self.assertEqual(response.status_code, 404)


class TestCourseApi(ApiTest):
    def setUp(self):
        super(TestCourseApi, self).setUp()

    def test_get_course_list(self):
        response = CourseList.as_view()(self.request, course_campus="seattle")
        course_list = json.loads(response.content)
        self.assertEqual(len(course_list), 33)

        response = CourseList.as_view()(self.request, course_campus="tacoma")
        course_list = json.loads(response.content)
        self.assertEqual(len(course_list), 0)

        response = CourseList.as_view()(self.request,
                                        course_campus="FakeCampus101")
        course_list = json.loads(response.content)
        self.assertEqual(len(course_list), 0)

    def test_get_course_details(self):
        response = CourseDetails.as_view()(self.request, course_abbr="TRAIN 9")
        details = json.loads(response.content)
        self.assertEqual(details['course_title'], 'Southwestern Pottery')
        self.assertEqual(response.status_code, 200)

        response = CourseDetails.as_view()(self.request,
                                           course_abbr="FOOBAR 121")
        self.assertEqual(response.status_code, 404)
