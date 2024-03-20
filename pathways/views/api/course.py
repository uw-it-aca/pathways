# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.course import Course
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
        except ObjectDoesNotExist as ex:
            return self.error_response(404,
                                       "Course %s not found" % course_abbr)
        return self.json_response(course)
