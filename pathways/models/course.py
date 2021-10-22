# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=10)
    course_title = models.CharField(max_length=120)
    course_credits = models.CharField(max_length=12)
    gpa_distro = models.JSONField(null=True)

    @staticmethod
    def get_course_list():
        courses = Course.objects.only("course_id", "course_title")
        course_json = []
        for course in courses:
            course_text = "%s: %s" % (course.course_id, course.course_title)
            course_json.append({"key": course.course_id,
                               "value": course_text})
        return course_json

    @staticmethod
    def get_course_data(course_id):
        return Course.objects.get(course_id=course_id).json_data()

    def json_data(self):
        return {"course_id": self.course_id,
                "course_title": self.course_title,
                "course_credits": self.course_credits,
                "gpa_distro": self.fix_gpa_json(self.gpa_distro)}

    @staticmethod
    def fix_gpa_json(json):
        fixed = []
        for key in json:
            if key != "null":
                fixed.append({"gpa": key, "count": json[key]})
        return fixed
