# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import json
import csv
from pathways.models.course import Course
from logging import getLogger
import time
import hashlib
from pathways.models.data_import import DataImport
from whoosh.index import create_in
from whoosh.fields import *


logger = getLogger(__name__)



class Command(BaseCommand):

    def handle(self, *args, **options):
        schema = Schema(course_id=ID(stored=True), contents=TEXT(stored=True))
        ix = create_in("indexdir", schema)
        writer = ix.writer()
        courses = Course.objects.all()

        for course in courses:
            writer.add_document(course_id=course.course_id,
                                contents=course.get_search_string())

        writer.commit()


