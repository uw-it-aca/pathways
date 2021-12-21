# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, path, re_path
from pathways.views.pages import DefaultPageView
from pathways.views.api.major import MajorDetails, MajorList
from pathways.views.api.course import CourseList, CourseDetails
from pathways.views.api.curric import CurricPrereq
from pathways.views.api.user import UserPreference


urlpatterns = [
    re_path(
        r'^api/v1/user_pref/$',
        UserPreference.as_view(), name='user-pref'),
    re_path(
        r'^api/v1/majors/(?P<major_campus>[^/]*)$',
        MajorList.as_view(), name='major-list'),
    re_path(
        r'^api/v1/majors/(?P<major_campus>[^/]+)/(?P<credential_abbr>[^/]*)$',
        MajorDetails.as_view(), name='major-details'),
    re_path(
        r'^api/v1/courses/(?P<course_campus>[^/]*)$',
        CourseList.as_view(), name='course-list'),
    re_path(
        r'^api/v1/courses/details/(?P<course_abbr>[^/]*)$',
        CourseDetails.as_view(), name='course-details'),
    re_path(
        r'^api/v1/curric_prereq/(?P<curric_abbr>[^/]*)$',
        CurricPrereq.as_view(), name='curric-prereq'),
    re_path(r"^.*$", DefaultPageView.as_view(), name="index")
]
