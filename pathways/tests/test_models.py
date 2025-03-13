# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json

from django.test import TestCase
from pathways.models.course import Course
from pathways.models.major import Major
from pathways.models.curriculum import Curriculum
from pathways.models.course_level import CourseLevel
from pathways.models.coi_range import COIRange
from pathways.models.user import User
from pathways.models.data_import import DataImport


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
            'course_campus': 'Bothell',
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
        Curriculum.objects.create(abbrev='TEST',
                                  prereq_graph=json.dumps(
                                      {'TEST 100': ['TEST 101']}),
                                  course_data=json.dumps(
                                      {'TEST 101': 'Test 101'}),
                                  average_coi_score=2.1,
                                  curric_name='Test Curriculum')

        CourseLevel.objects.create(level=100)

        COIRange.objects.create(coi_range=0, percent_in_range=0.11)
        COIRange.objects.create(coi_range=1, percent_in_range=0.12)
        COIRange.objects.create(coi_range=2, percent_in_range=0.13)
        COIRange.objects.create(coi_range=3, percent_in_range=0.14)
        COIRange.objects.create(coi_range=4, percent_in_range=0.15)

        Major.objects.create(major_abbr='CHEM',
                             major_title='Chemistry',
                             major_school='Arts and Sciences',
                             major_campus='Seattle',
                             major_description='This is a major in chemistry.',
                             major_admission='Open',
                             program_code='CHEM',
                             credential_title='Chemistry',
                             credential_description='This is chemistry.',
                             )
        Major.objects.create(major_abbr='TEST',
                             major_title='Test',
                             major_school='Test School',
                             major_campus='Test Campus',
                             program_code='TEST'
                             )

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
                          'percent_in_range': 13.0})
        self.assertEqual(json_data['is_bottleneck'], False)
        self.assertEqual(json_data['is_gateway'], False)

    def test_course_list(self):
        course_list = Course.get_course_list()
        self.assertEqual(course_list, [
            {'key': 'CHEM 101', 'value': 'CHEM 101: Chemistry 101'},
            {'key': 'CHEM 102', 'value': 'CHEM 102: Chemistry 102'},
            {'key': 'CHEM 103', 'value': 'CHEM 103: Chemistry 103'}
        ])

    def test_get_course_list_by_campus(self):
        course_list = Course.get_course_list_by_campus('Seattle')
        self.assertEqual(course_list, [
            {'key': 'CHEM 101', 'value': 'CHEM 101: Chemistry 101'},
            {'key': 'CHEM 102', 'value': 'CHEM 102: Chemistry 102'}
        ])

    def test_get_course_data(self):
        data = Course.get_course_data('CHEM 101')
        self.assertEqual(data['course_id'], 'CHEM 101')

    def test_course_concurrent_and_coi(self):
        bad_concurrent = {
            'course_id': 'TEST 101',
            'department_abbrev': 'TEST',
            'course_title': 'Testistry 101',
            'course_credits': '5',
            'course_campus': 'Seattle',
            'gpa_distro': {'A': 0.2, 'B': 0.3, 'C': 0.4},
            'concurrent_courses': {'MATH 102': 0.1,
                                   'CSE 103': 0.2},
            'prereq_graph': json.dumps({'CHEM 100': ['CHEM 101']}),
            'course_description': 'This is a course on test.',
            'course_offered': 'Autumn',
            'prereq_string': 'CHEM 100',
            'coi_score': 2.1,
            'is_bottleneck': False,
            'is_gateway': False
        }
        Course.objects.create(**bad_concurrent)

        course = Course.objects.get(course_id='TEST 101')
        concurrent = course.get_concurrent_with_coi_and_flags()
        self.assertEqual(concurrent, {})

    def test_course_fix_gpa(self):
        fixed = Course.fix_gpa_json("not a dict")
        self.assertEqual(fixed, [])

    def test_coi_percent(self):
        percent = COIRange.get_percent_by_score(None)
        self.assertEqual(percent, None)
        percent = COIRange.get_percent_by_score(0)
        self.assertEqual(percent, 11.0)
        percent = COIRange.get_percent_by_score(1.1)
        self.assertEqual(percent, 12.0)
        percent = COIRange.get_percent_by_score(2.1)
        self.assertEqual(percent, 13.0)
        percent = COIRange.get_percent_by_score(3.1)
        self.assertEqual(percent, 14.0)
        percent = COIRange.get_percent_by_score(4.1)
        self.assertEqual(percent, 15.0)

    def test_curric_prereq(self):
        prereq = Curriculum.get_prereq('TEST')
        self.assertEqual(prereq['prereq_graph'], '{"TEST 100": ["TEST 101"]}')
        self.assertEqual(prereq['course_data'], '{"TEST 101": "Test 101"}')

    def test_user_banner(self):
        User.objects.create(uwnetid='javerage', has_viewed_welcome=True)
        banners = User.show_banners('javerage')
        self.assertEqual(banners, ['bottleneck', 'outcomes', 'coi'])

        User.objects.create(uwnetid='all')
        banners = User.show_banners('all')
        self.assertEqual(banners, ['welcome', 'bottleneck', 'outcomes', 'coi'])

        new_banners = User.show_banners('newuser')
        self.assertEqual(new_banners, ['welcome',
                                       'bottleneck',
                                       'outcomes',
                                       'coi'])

    def test_import_model(self):
        DataImport.objects.create(type='course', hash='123abc')
        self.assertTrue(DataImport.needs_import('course',
                                                '456xyz'))
        self.assertFalse(DataImport.needs_import('course',
                                                 '123abc'))

    def test_major_search_string(self):
        major = Major.objects.get(major_abbr='CHEM')
        self.assertEqual(major.get_search_string(),
                         'CHEM Chemistry This is chemistry.')

    def test_major_search_results(self):
        major = Major.objects.get(major_abbr='CHEM')
        search_results = major.get_search_results_dict()
        self.assertEqual(search_results['id'], 'CHEM')
        self.assertEqual(search_results['url'], '/major?id=CHEM')

    def test_major_list(self):
        major_list = Major.get_major_list()
        self.assertEqual(major_list, [
            {'key': 'CHEM', 'value': 'Chemistry'},
            {'key': 'TEST', 'value': 'Test'}
        ])

    def test_major_fix_gpa(self):
        fixed = Major.fix_gpa_json({'A': 0.2, 'B': 0.3, 'C': 0.4})
        self.assertEqual(fixed, [
            {'gpa': 'A', 'count': 0.2},
            {'gpa': 'B', 'count': 0.3},
            {'gpa': 'C', 'count': 0.4}
        ])

        empty_fixed = Major.fix_gpa_json({})
        self.assertEqual(empty_fixed, [])

        bad_fixed = Major.fix_gpa_json("not a dict")
        self.assertEqual(bad_fixed, [])

    def test_major_coi(self):
        major = Major.objects.get(major_abbr='CHEM')
        response = major.get_common_with_coi_and_flags()
        self.assertEqual(response, {})
