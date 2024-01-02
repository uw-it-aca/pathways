# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import csv
import json
from pathways.models.course import Course


class Command(BaseCommand):
    """
    format:
    course_id, course_title, gpa_level, gpa_count
    """
    def handle(self, *args, **options):
        with open('course_gpa_distro.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Course ID", "Course Title",
                             "GPA", "Count"])

            courses = Course.objects.all()
            print("found %s courses" % len(courses))
            write_count = 0
            row_count = 0
            for course in courses:
                course_data = [
                    course.course_id,
                    course.course_title
                ]
                if course.gpa_distro is not None:
                    write_count += 1
                    for gpa in course.gpa_distro.keys():
                        gpa_data = []
                        try:
                            gp = int(gpa)/10
                        except ValueError:
                            continue
                        gpa_data.append(gp)
                        gpa_data.append(course.gpa_distro[gpa])
                        writer.writerow(course_data + gpa_data)
                        row_count += 1
            print("wrote %s courses" % write_count)
            print("wrote %s rows" % row_count)




