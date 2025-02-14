# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch, mock_open

from pathways.management.commands.import_data import Command
from pathways.models.data_import import DataImport
from pathways.models.coi_range import COIRange
from pathways.models.course_level import CourseLevel
from pathways.models.major import Major
from pathways.models.course import Course
from pathways.models.curriculum import Curriculum


class ImportTest(TestCase):
    def test_get_hash(self):
        file_data = "data".encode('utf-8')
        with patch("builtins.open",
                   mock_open(read_data=file_data)) as mock_file:
            hash = Command()._get_hash_by_path("/path/")
            self.assertEqual(hash, "8d777f385d3dfec8815d20f7496026dc")

    @patch('pathways.management.commands.import_data.Command'
           '._get_hash_by_path', return_value='123456')
    def test_needs_update_all(self, mock_data):
        Command().data_needs_update()
        di_objs = DataImport.objects.all()
        self.assertEqual(di_objs.count(), 7)

        coi_import = DataImport.objects.get(type='coi')
        coi_import.hash = 'newhash'
        coi_import.save()

        Command().data_needs_update()
        coi_import = DataImport.objects.get(type='coi')
        self.assertEqual(coi_import.hash, '123456')

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
           "pathways/tests/commands/mock_import_files/bottleneck_courses.csv")
    @patch('pathways.management.commands.import_data.GATEWAY_PATH',
           "pathways/tests/commands/mock_import_files/gateway_courses.csv")
    @patch('pathways.management.commands.import_data.CAREER_CENTER_PATH',
           "pathways/tests/commands/mock_import_files/admit_major_mapping.csv")
    def test_import(self, du):
        call_command('import_data')

        # Verify COI Import
        self.assertEqual(COIRange.objects.count(), 5)
        range_0 = COIRange.objects.get(coi_range=0).percent_in_range
        range_1 = COIRange.objects.get(coi_range=1).percent_in_range
        range_2 = COIRange.objects.get(coi_range=2).percent_in_range
        range_3 = COIRange.objects.get(coi_range=3).percent_in_range
        range_4 = COIRange.objects.get(coi_range=4).percent_in_range
        self.assertEqual(range_0, 0.125)
        self.assertEqual(range_1, 0.125)
        self.assertEqual(range_2, 0.25)
        self.assertEqual(range_3, 0.125)
        self.assertEqual(range_4, 0.375)

        self.assertEqual(CourseLevel.objects.count(), 4)
        level_100 = CourseLevel.objects.get(level=100).coi_score
        level_200 = CourseLevel.objects.get(level=200).coi_score
        level_300 = CourseLevel.objects.get(level=300).coi_score
        level_400 = CourseLevel.objects.get(level=400).coi_score
        self.assertEqual(level_100, 2.8)
        self.assertEqual(level_200, 0.1)
        self.assertEqual(level_300, 5)
        self.assertEqual(level_400, 1.2)

        # Verify Major Import
        self.assertEqual(Major.objects.count(), 1)
        major = Major.objects.get(program_code="UG-INFO-MAJOR")
        self.assertEqual(major.major_admission, "capacity-constrained")

        # Verify Course Import
        self.assertEqual(Course.objects.count(), 2)
        course = Course.objects.get(course_id="INFO 201")
        self.assertEqual(course.course_title,
                         "Foundational Skills for Data Science")
        # Verify Curric Import
        self.assertEqual(Curriculum.objects.count(), 2)
        curric = Curriculum.objects.get(abbrev="INFO")
        self.assertEqual(curric.curric_name, "INFORMATICS")

        info_201 = Course.objects.get(course_id="INFO 201")
        info_301 = Course.objects.get(course_id="INFO 301")

        # Verify Gateway Import
        self.assertTrue(info_201.is_gateway)
        self.assertFalse(info_301.is_gateway)

        # Verify Bottleneck Import
        self.assertTrue(info_301.is_bottleneck)
        self.assertFalse(info_201.is_bottleneck)

        # Verify Career Center Import
        self.assertEqual(major.career_center_major, "informatics")

    @patch('pathways.management.commands.'
           'import_data.Command.data_needs_update', return_value=False)
    @patch('pathways.management.commands.import_data.COI_PATH',
           "pathways/tests/commands/mock_import_files/coi_scores.csv")
    @patch('pathways.management.commands.import_data.MAJOR_PATH',
           "pathways/tests/commands/mock_import_files/major_data.json")
    @patch('pathways.management.commands.import_data.COURSE_PATH',
           "pathways/tests/commands/mock_import_files/course_data.json")
    @patch('pathways.management.commands.import_data.CURRIC_PATH',
           "pathways/tests/commands/mock_import_files/curric_data.json")
    @patch('pathways.management.commands.import_data.BOTTLENECK_PATH',
           "pathways/tests/commands/mock_import_files/bottleneck_courses.csv")
    @patch('pathways.management.commands.import_data.GATEWAY_PATH',
           "pathways/tests/commands/mock_import_files/gateway_courses.csv")
    @patch('pathways.management.commands.import_data.CAREER_CENTER_PATH',
           "pathways/tests/commands/mock_import_files/admit_major_mapping.csv")
    def test_noop_import(self, du):
        self.assertEqual(Course.objects.count(), 0)
        call_command('import_data')
        self.assertEqual(Course.objects.count(), 0)
