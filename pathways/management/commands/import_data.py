# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import json
from pathways.data_import import import_major_data


class Command(BaseCommand):
    help = 'Run all unit tests'

    def handle(self, *args, **options):
        with open('pathways/data/major_gpa.json') as json_file:
            data = json.load(json_file)
            import_major_data(data)
