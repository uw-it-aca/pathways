# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from pathways.models.course import Course
from logging import getLogger
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer


logger = getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        stem_ana = StemmingAnalyzer()
        schema = Schema(course_id=ID(stored=True),
                        contents=TEXT(analyzer=stem_ana,
                                      stored=True))
        ix = create_in("indexdir", schema)
        writer = ix.writer()
        courses = Course.objects.all()

        for course in courses:
            writer.add_document(course_id=course.course_id,
                                contents=course.get_search_string())

        writer.commit()


