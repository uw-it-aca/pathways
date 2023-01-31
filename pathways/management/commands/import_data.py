# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import json
import csv
from pathways.data_import import import_major_data, import_course_data, \
    import_curric_data, import_level_coi, import_coi_ranges, \
    import_gateway_courses, import_bottleneck_courses, \
    import_career_center_mapping
from logging import getLogger
import time
import hashlib
from pathways.models.data_import import DataImport


logger = getLogger(__name__)
COI_PATH = "pathways/data/coi_scores.csv"
MAJOR_PATH = "pathways/data/major_data.json"
COURSE_PATH = "pathways/data/course_data.json"
CURRIC_PATH = "pathways/data/curric_data.json"
BOTTLENECK_PATH = "pathways/data/bottleneck_courses.csv"
GATEWAY_PATH = "pathways/data/gateway_courses.csv"
CAREER_CENTER_PATH = "pathways/data/career_center_major_mapping.csv"


class Command(BaseCommand):
    help = 'Run all unit tests'

    def handle(self, *args, **options):
        start = time.time()
        if not self.data_needs_update():
            return
        with open(COI_PATH) as coi_file:
            reader = csv.reader(coi_file)
            # skip headers
            next(reader)
            coi_data = []
            for row in reader:
                coi_data.append({"course_id": row[0],
                                 "coi_score": float(row[1])})
            import_level_coi(coi_data)
            import_coi_ranges(coi_data)
            with open(MAJOR_PATH) as major_file:
                data = json.load(major_file)
                import_major_data(data)
            with open(COURSE_PATH) as course_file:
                data = json.load(course_file)
                import_course_data(data, coi_data)
            with open(CURRIC_PATH) as curric_file:
                data = json.load(curric_file)
                import_curric_data(data, coi_data)
            with open(GATEWAY_PATH) as gateway_file:
                data = csv.reader(gateway_file)
                import_gateway_courses(data)
            with open(BOTTLENECK_PATH) as bottleneck_file:
                data = csv.reader(bottleneck_file)
                import_bottleneck_courses(data)
            with open(CAREER_CENTER_PATH) as career_major_file:
                data = csv.reader(career_major_file)
                import_career_center_mapping(data)

        total_time = time.time() - start
        logger.info("Imported data in: %s" % total_time)

    def data_needs_update(self):
        needs_update = False
        coi_hash = self._get_hash_by_path(COI_PATH)
        if DataImport.needs_import('coi', coi_hash):
            needs_update = True
            DataImport.objects \
                .update_or_create(type='coi',
                                  defaults={'hash': coi_hash})
        major_hash = self._get_hash_by_path(MAJOR_PATH)
        if DataImport.needs_import('major', major_hash):
            needs_update = True
            DataImport.objects \
                .update_or_create(type='major',
                                  defaults={'hash': major_hash})
        course_hash = self._get_hash_by_path(COURSE_PATH)
        if DataImport.needs_import('course', course_hash):
            needs_update = True
            DataImport.objects \
                .update_or_create(type='course',
                                  defaults={'hash': course_hash})
        curric_hash = self._get_hash_by_path(CURRIC_PATH)
        if DataImport.needs_import('curric', curric_hash):
            needs_update = True
            DataImport.objects \
                .update_or_create(type='curric',
                                  defaults={'hash': curric_hash})
        gateway_hash = self._get_hash_by_path(GATEWAY_PATH)
        if DataImport.needs_import('gateway', gateway_hash):
            needs_update = True
            DataImport.objects \
                .update_or_create(type='gateway',
                                  defaults={'hash': gateway_hash})
        bottleneck_hash = self._get_hash_by_path(BOTTLENECK_PATH)
        if DataImport.needs_import('bottleneck', bottleneck_hash):
            needs_update = True
            DataImport.objects \
                .update_or_create(type='bottleneck',
                                  defaults={'hash': bottleneck_hash})
        career_hash = self._get_hash_by_path(CAREER_CENTER_PATH)
        if DataImport.needs_import('cc_major', career_hash):
            needs_update = True
            DataImport.objects \
                .update_or_create(type='cc_major',
                                  defaults={'hash': career_hash})
        return needs_update

    def _get_hash_by_path(self, path):
        return hashlib.md5(open(path, 'rb').read()).hexdigest()
