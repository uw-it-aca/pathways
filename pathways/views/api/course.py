# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.course import Course
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# @method_decorator(login_required, name="dispatch")
class CourseList(RESTDispatch):
    def get(self, request, *args, **kwargs):
        courses = Course.get_course_list()
        return self.json_response(courses)
