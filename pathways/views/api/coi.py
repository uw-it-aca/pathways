# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.course import Course
from pathways.models.course import Curriculum
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name="dispatch")
class CourseCOI(RESTDispatch):
    '''
    Takes a course abbr and fetches COI data for all courses in that
    course's curriculum.
    '''

    def get(self, request, department_abbrev, *args, **kwargs):
        dept_courses = Course.objects.filter(
            department_abbrev=department_abbrev)\
            .exclude(coi_score__isnull=True)
        course_cois = []
        for course in dept_courses:
            course_cois.append({'course_id': course.course_id,
                                'score': course.coi_score})
        return self.json_response(course_cois)


@method_decorator(login_required, name="dispatch")
class CurricCOI(RESTDispatch):
    '''
    Returns average COIs by curriculum for all curriculums.
    '''

    def get(self, request, *args, **kwargs):
        currics = Curriculum.objects.all()
        curric_scores = []
        for dept in currics:
            curric_scores.append({"curric_name": dept.curric_name,
                                  "curric": dept.abbrev,
                                  "score": dept.average_coi_score})
        return self.json_response(curric_scores)
