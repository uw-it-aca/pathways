# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from pathways.models.major import Major
import json


class Command(BaseCommand):
    help = 'Run all unit tests'

    def handle(self, *args, **options):
        with open('pathways/data/major_gpa.json') as json_file:
            data = json.load(json_file)
            for major in data:
                gpa_data = {"gpa_2yr": data[major]['2_yr'],
                            "gpa_5yr": data[major]['5_yr'],
                            "major_title": data[major]['major_title'],
                            "major_school": data[major]['major_school'],
                            "major_campus": data[major]['major_campus'],
                            "major_description":
                                data[major]['major_description'],
                            "major_admission": data[major]['major_admission'],
                            "program_code": data[major]['program_code'],
                            "major_home_url": data[major]['major_home_url'],
                            }
                Major.objects.update_or_create(major_abbr=major,
                                               defaults=gpa_data)
