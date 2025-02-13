# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json

from django.test import TestCase
from pathways.models.course import Course
from pathways.models.major import Major
from pathways.models.curriculum import Curriculum
from pathways.models.course_level import CourseLevel
from pathways.models.coi_range import COIRange


class ImportTest(TestCase):

    def setUp(self):
        course_1 = {
            'course_id': 'CHEM 101',
            'department_abbrev': 'CHEM',
            'course_title': 'Chemistry 101',
            'course_credits': '5',
            'course_campus': 'Seattle',
            'gpa_distro': {'A': 0.2, 'B': 0.3, 'C': 0.4},
            'concurrent_courses': {'CHEM 102': 0.1,
                                   'CHEM 103': 0.2},
            'prereq_graph': json.dumps({'CHEM 100': ['CHEM 101']}),
            'course_description': 'This is a course on chemistry.',
            'course_offered': 'Autumn',
            'prereq_string': 'CHEM 100',
            'coi_score': 2.1,
            'is_bottleneck': False,
            'is_gateway': False
        }
        course_2 = {
            'course_id': 'CHEM 102',
            'department_abbrev': 'CHEM',
            'course_title': 'Chemistry 102',
            'course_credits': '5',
            'course_campus': 'Seattle',
            'gpa_distro': {'A': 0.2, 'B': 0.3, 'C': 0.4},
            'concurrent_courses': ['CHEM 101', 'CHEM 103'],
            'prereq_graph': json.dumps({'CHEM 101': ['CHEM 102']}),
            'course_description': 'This is a course on chemistry.',
            'course_offered': 'Autumn',
            'prereq_string': 'CHEM 101',
            'coi_score': 2.1,
            'is_bottleneck': False,
            'is_gateway': False
        }
        course_3 = {
            'course_id': 'CHEM 103',
            'department_abbrev': 'CHEM',
            'course_title': 'Chemistry 103',
            'course_credits': '5',
            'course_campus': 'Seattle',
            'gpa_distro': {'A': 0.2, 'B': 0.3, 'C': 0.4},
            'concurrent_courses': ['CHEM 101', 'CHEM 102'],
            'prereq_graph': json.dumps({'CHEM 102': ['CHEM 103']}),
            'course_description': 'This is a course on chemistry.',
            'course_offered': 'Autumn',
            'prereq_string': 'CHEM 102',
            'coi_score': 2.1,
            'is_bottleneck': False,
            'is_gateway': False
        }
        Course.objects.create(**course_1)
        Course.objects.create(**course_2)
        Course.objects.create(**course_3)

        Curriculum.objects.create(abbrev='CHEM')
        CourseLevel.objects.create(level=100)
        COIRange.objects.create(coi_range=2, percent_in_range=0.5)

    def test_search_string(self):
        course = Course.objects.get(course_id='CHEM 101')
        self.assertEqual(course.get_search_string(),
                         'CHEM 101 Chemistry 101'
                         ' This is a course on chemistry.')

    def test_search_results(self):
        course = Course.objects.get(course_id='CHEM 101')
        search_results = course.get_search_results_dict()
        self.assertEqual(search_results['id'], 'CHEM 101')
        self.assertEqual(search_results['url'], '/course?id=CHEM+101')

    def test_json_data(self):
        course = Course.objects.get(course_id='CHEM 101')
        json_data = course.json_data()
        self.assertEqual(json_data['course_id'], 'CHEM 101')
        self.assertEqual(json_data['course_title'], 'Chemistry 101')
        self.assertEqual(json_data['course_credits'], '5')
        self.assertEqual(json_data['course_campus'], 'Seattle')
        self.assertEqual(json_data['gpa_distro'],
                         [
                             {'gpa': 'A', 'count': 0.2},
                             {'gpa': 'B', 'count': 0.3},
                             {'gpa': 'C', 'count': 0.4}
                         ])
        self.assertEqual(json_data['concurrent_courses'],
                         {
                             'CHEM 102': {
                                 'percent': 0.1,
                                 'title': 'Chemistry 102',
                                 'coi_score': 2.1,
                                 'is_bottleneck': False,
                                 'is_gateway': False
                             },
                             'CHEM 103': {
                                 'percent': 0.2,
                                 'title': 'Chemistry 103',
                                 'coi_score': 2.1,
                                 'is_bottleneck': False,
                                 'is_gateway': False
                             }
                         }
                         )
        self.assertEqual(json_data['prereq_graph'],
                         {'CHEM 100': ['CHEM 101']})
        self.assertEqual(json_data['course_description'],
                         'This is a course on chemistry.')
        self.assertEqual(json_data['course_offered'], 'Autumn')
        self.assertEqual(json_data['prereq_string'], 'CHEM 100')
        self.assertEqual(json_data['coi_data'],
                         {'course_coi': 2.1,
                          'curric_coi': None,
                          'course_level_coi': None,
                          'percent_in_range': 50.0})
        self.assertEqual(json_data['is_bottleneck'], False)
        self.assertEqual(json_data['is_gateway'], False)
