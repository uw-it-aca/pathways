# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.tests import ApiTest
from pathways.views.api.major import MajorDetails, MajorList
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
