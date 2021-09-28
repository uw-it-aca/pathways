# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, path, re_path
from pathways.views.pages import DefaultPageView
from pathways.views.api.major import MajorDetails, MajorList
from pathways.views.api.course import CourseList


urlpatterns = [
    re_path(
        r'^api/v1/majors/$',
        MajorList.as_view(), name='major-list'),
    re_path(
        r'^api/v1/majors/(?P<major_abbr>[^/]*)$',
        MajorDetails.as_view(), name='major-details'),
    re_path(
        r'^api/v1/courses/$',
        CourseList.as_view(), name='course-list'),
    re_path(r"^.*$", DefaultPageView.as_view(), name="index")
]
