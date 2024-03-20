# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from pathways.models.course import Course
from pathways.models.major import Major
from logging import getLogger
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
import os


logger = getLogger(__name__)
INDEXDIR = "indexdir"


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not os.path.exists(INDEXDIR):
            os.makedirs(INDEXDIR)
        stem_ana = StemmingAnalyzer()
        schema = Schema(course_id=TEXT(stored=True),
                        major_id=TEXT(stored=True),
                        major_title=TEXT(stored=True),
                        type=TEXT(stored=True),
                        contents=TEXT(analyzer=stem_ana,
                                      stored=True),
                        campus=TEXT(),
                        is_gateway=BOOLEAN(),
                        is_bottleneck=BOOLEAN(),
                        coi_score=NUMERIC()
                        )
        ix = create_in(INDEXDIR, schema)
        writer = ix.writer()

        courses = Course.objects.all()
        for course in courses:
            writer.add_document(course_id=course.course_id,
                                type="course",
                                contents=course.get_search_string(),
                                campus=course.course_campus,
                                is_gateway=course.is_gateway,
                                is_bottleneck=course.is_bottleneck,
                                coi_score=course.coi_score)
        majors = Major.objects.all()
        for major in majors:
            writer.add_document(major_id=major.major_abbr,
                                major_title=major.credential_title,
                                type="major",
                                contents=major.get_search_string(),
                                campus=major.major_campus)

        writer.commit()
