# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch, MagicMock
from pathways.models.major import Major
from pathways.models.course import Course


class ValidateDataTest(TestCase):
    def setUp(self):
        Major.objects.create(
            major_abbr="INFO",
            gpa_2yr={'a': 1},
            gpa_5yr={'b': 2}
        )
        Course.objects.create(
            course_id="INFO 201",
            course_title="Foundational Skills for Data Science"
        )

    @patch('pathways.management.commands.validate_data.Pool')
    @patch('pathways.management.commands.validate_data.cpu_count')
    def test_validate_data(self, mock_cpu_count, mock_pool):
        mock_cpu_count.return_value = 4
        mock_pool_instance = MagicMock()
        mock_pool.return_value = mock_pool_instance
        mock_pool_instance.map.return_value = [("INFO 201", False, False)]

        call_command('validate_data')

        self.assertTrue(mock_pool.called)
