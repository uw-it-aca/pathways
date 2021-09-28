# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import json
from pathways.data_import import import_major_data
from pathways.data_import import import_course_data


class Command(BaseCommand):
    help = 'Run all unit tests'

    def handle(self, *args, **options):
        with open('pathways/data/major_gpa.json') as major_file:
            data = json.load(major_file)
            import_major_data(data)
        with open('pathways/data/course_data.json') as course_file:
            data = json.load(course_file)
            import_course_data(data)
