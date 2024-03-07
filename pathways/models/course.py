# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
import json
from pathways.models.course_level import CourseLevel
from pathways.models.curriculum import Curriculum
from pathways.models.coi_range import COIRange
from django.core.exceptions import ObjectDoesNotExist


class Course(models.Model):
    course_id = models.CharField(max_length=10)
    department_abbrev = models.CharField(max_length=6, null=True)
    course_title = models.CharField(max_length=120)
    course_credits = models.CharField(max_length=12)
    course_campus = models.CharField(max_length=7)
    gpa_distro = models.JSONField(null=True)
    concurrent_courses = models.JSONField(null=True)
    prereq_graph = models.JSONField(null=True)
    course_description = models.TextField(null=True)
    course_offered = models.TextField(null=True)
    prereq_string = models.TextField(null=True)
    coi_score = models.FloatField(null=True)
    is_bottleneck = models.BooleanField(default=False)
    is_gateway = models.BooleanField(default=False)

    def get_search_string(self):
        string = "{id} {title} {description}"
        return string.format(id=self.course_id,
                             title=self.course_title,
                             description=self.course_description)

    @staticmethod
    def get_course_list():
        courses = Course.objects.only("course_id", "course_title")
        return Course._get_course_list_json(courses)

    @staticmethod
    def get_course_list_by_campus(campus):
        courses = Course.objects\
            .filter(course_campus=campus)\
            .only("course_id", "course_title")
        return Course._get_course_list_json(courses)

    @staticmethod
    def _get_course_list_json(course_list):
        course_json = []
        for course in course_list:
            course_text = "%s: %s" % (course.course_id, course.course_title)
            course_json.append({"key": course.course_id,
                                "value": course_text})
        return course_json

    @staticmethod
    def get_course_data(course_id):
        return Course.objects.get(course_id=course_id).json_data()

    @staticmethod
    def get_course_data_by_campus(campus, course_id):
        return Course.objects.get(course_campus=campus,
                                  course_id=course_id).json_data()

    def json_data(self):
        graph = None
        if self.prereq_graph:
            graph = json.loads(self.prereq_graph)
        concurrrent = self.get_concurrent_with_coi_and_flags()
        return {"course_id": self.course_id,
                "department_abbrev": self.department_abbrev,
                "course_title": self.course_title,
                "course_credits": self.course_credits,
                "course_campus": self.course_campus,
                "gpa_distro": self.fix_gpa_json(self.gpa_distro),
                "concurrent_courses": concurrrent,
                "prereq_graph": graph,
                "prereq_string": self.prereq_string,
                "course_description": self.course_description,
                "course_offered": self.course_offered,
                "coi_data": self.get_coi_data(),
                "is_bottleneck": self.is_bottleneck,
                "is_gateway": self.is_gateway}

    @staticmethod
    def fix_gpa_json(json):
        fixed = []
        try:
            for key in json:
                if key != "null":
                    fixed.append({"gpa": key, "count": json[key]})
        except TypeError:
            # No GPA distro for course
            pass
        return fixed

    def get_coi_data(self):
        curric, delim, num = self.course_id.rpartition(" ")
        curric_score = Curriculum.objects.get(abbrev=curric).average_coi_score
        course_level = int(num)//100*100
        level_score = CourseLevel.objects.get(level=course_level).coi_score
        percent_in_range = COIRange.get_percent_by_score(self.coi_score)

        return {"course_coi": self.coi_score,
                "curric_coi": curric_score,
                "course_level_coi": level_score,
                "percent_in_range": percent_in_range}

    def get_concurrent_with_coi_and_flags(self):
        if self.concurrent_courses is not None:
            courses = self.concurrent_courses.keys()
            course_objs = Course.objects.filter(course_id__in=courses)
            concurrent_with_coi = {}
            for course in courses:
                try:
                    course_obj = course_objs.get(course_id=course)
                    percent = self.concurrent_courses[course]
                    title = course_obj.course_title
                    coi = course_obj.coi_score
                    bottleneck = course_obj.is_bottleneck
                    gateway = course_obj.is_gateway
                    concurrent_with_coi[course] = {"percent": percent,
                                                   "title": title,
                                                   "coi_score": coi,
                                                   "is_bottleneck": bottleneck,
                                                   "is_gateway": gateway}
                except ObjectDoesNotExist:
                    pass
            return concurrent_with_coi
