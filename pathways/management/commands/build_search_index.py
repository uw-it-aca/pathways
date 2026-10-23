# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from logging import getLogger

from dawgpath_search import IndexValidationError, build_index, make_schema
from django.core.management.base import BaseCommand, CommandError
from whoosh.index import create_in

from pathways.models.course import Course
from pathways.models.major import Major

logger = getLogger(__name__)
INDEXDIR = "indexdir"


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "--input-root", help="Build offline from five local snapshot files.")
        parser.add_argument(
            "--output-dir", help="Fresh output directory for a snapshot build.")
        parser.add_argument(
            "--release-id", help="Release identity recorded in snapshot metadata.")

    def handle(self, *args, **options):
        if options.get("input_root"):
            if not options.get("output_dir") or not options.get("release_id"):
                raise CommandError(
                    "--input-root requires --output-dir and --release-id.")
            try:
                metadata = build_index(
                    options["input_root"], options["output_dir"],
                    release_id=options["release_id"])
            except (IndexValidationError, OSError) as exc:
                raise CommandError(str(exc)) from exc
            self.stdout.write(self.style.SUCCESS(
                f"Built snapshot index: {metadata['counts']}"))
            return
        if options.get("output_dir") or options.get("release_id"):
            raise CommandError("--output-dir/--release-id require --input-root.")
        if not os.path.exists(INDEXDIR):
            os.makedirs(INDEXDIR)
        schema = make_schema()
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
                                coi_score=course.coi_score,
                                course_title=course.course_title,
                                description=course.course_description)
        majors = Major.objects.all()
        for major in majors:
            writer.add_document(major_id=major.credential_code,
                                major_abbr=major.major_abbr,
                                major_title=major.credential_title,
                                type="major",
                                contents=major.get_search_string(),
                                campus=major.major_campus,
                                description=major.credential_description)

        writer.commit()
