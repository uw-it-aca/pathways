# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

from pathways.models.course import Course
from pathways.views.api import RESTDispatch


@method_decorator(login_required, name="dispatch")
class CourseList(RESTDispatch):
    def get(self, request, course_campus, *args, **kwargs):
        courses = Course.get_course_list_by_campus(course_campus)
        return self.json_response(courses)


@method_decorator(login_required, name="dispatch")
class CourseDetails(RESTDispatch):
    def get(self, request, course_abbr, *args, **kwargs):
        try:
            course = Course.get_course_data(course_abbr)
        except ObjectDoesNotExist:
            return self.error_response(404,
                                       f"Course {course_abbr} not found")
        return self.json_response(course)
