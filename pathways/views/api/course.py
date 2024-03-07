# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.course import Course
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pathways.search import search_courses


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


@method_decorator(login_required, name="dispatch")
class CourseSearch(RESTDispatch):
    def get(self, request, *args, **kwargs):
        search_string = request.GET.get("search_string")
        is_bottleneck = False

        def to_bool(value):
            return value is not None and value == "true"

        is_gateway = to_bool(request.GET.get("is_gateway"))
        is_bottleneck = to_bool(request.GET.get("is_bottleneck"))
        min_coi_score = request.GET.get("min_coi_score")
        max_coi_score = request.GET.get("max_coi_score")
        campus = request.GET.get("campus")

        courses = search_courses(search_string, campus,
                                 is_gateway=is_bottleneck,
                                 is_bottleneck=is_gateway,
                                 min_coi_score=min_coi_score,
                                 max_coi_score=max_coi_score)
        return self.json_response(courses)
