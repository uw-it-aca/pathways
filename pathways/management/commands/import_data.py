# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import json
from pathways.data_import import import_major_data, import_course_data, \
    import_curric_data, import_level_coi, import_coi_ranges


class Command(BaseCommand):
    help = 'Run all unit tests'

    def handle(self, *args, **options):
        with open('pathways/data/coi_scores.json') as coi_file:
            coi_data = json.load(coi_file)
            import_level_coi(coi_data)
            import_coi_ranges(coi_data)
            with open('pathways/data/major_data.json') as major_file:
                data = json.load(major_file)
                import_major_data(data)
            with open('pathways/data/course_data.json') as course_file:
                data = json.load(course_file)
                import_course_data(data, coi_data)
            with open('pathways/data/curric_data.json') as curric_file:
                data = json.load(curric_file)
                import_curric_data(data, coi_data)
