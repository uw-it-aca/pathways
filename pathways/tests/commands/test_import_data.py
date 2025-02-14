# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch, mock_open

from pathways.management.commands.import_data import Command
from pathways.models.data_import import DataImport


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
        # call_command('import_data')
        pass


