# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=10)
    course_title = models.CharField(max_length=120)

    @staticmethod
    def get_course_list():
        courses = Course.objects.only("course_id", "course_title")
        course_json = []
        for course in courses:
            course_json.append({"key": course.major_abbr,
                               "value": course.major_title})
        return course_json
