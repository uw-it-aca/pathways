# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView
from supporttools.urls import get_registry_urlpatterns

from pathways.views.api.coi import CourseCOI, CurricCOI
from pathways.views.api.course import CourseDetails, CourseList
from pathways.views.api.curric import CurricPrereq
from pathways.views.api.major import MajorDetails, MajorList
from pathways.views.api.release_promotion import (
    get_release_manifest,
    list_releases,
    promote_release,
)
from pathways.views.api.search import Search
from pathways.views.api.user import UserPreference
from pathways.views.pages import DefaultPageView

# start with an empty url array
urlpatterns = []

# add debug routes for developing error pages
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^500$",
            TemplateView.as_view(template_name="500.html"),
            name="500_response"),
        re_path(r"^404$",
                TemplateView.as_view(template_name="404.html"),
                name="404_response")
    ]

urlpatterns += [
    re_path(
        r'^api/v1/user_pref/$',
        UserPreference.as_view(), name='user-pref'),
    re_path(
        r'^api/v1/majors/(?P<major_campus>[^/]*)$',
        MajorList.as_view(), name='major-list'),
    re_path(
        r'^api/v1/majors/details/(?P<credential_abbr>[^/]*)$',
        MajorDetails.as_view(), name='major-details'),
    re_path(
        r'^api/v1/courses/(?P<course_campus>[^/]*)$',
        CourseList.as_view(), name='course-list'),
    re_path(
        r'^api/v1/courses/details/(?P<course_abbr>[^/]*)$',
        CourseDetails.as_view(), name='course-details'),
    re_path(
        r'^api/v1/search/$',
        Search.as_view(), name='search'),
    re_path(
        r'^api/v1/curric_prereq/(?P<curric_abbr>[^/]*)$',
        CurricPrereq.as_view(), name='curric-prereq'),
    re_path(
        r'^api/v1/coi/course/(?P<department_abbrev>[^/]*)$',
        CourseCOI.as_view(), name='course-coi'),
    re_path(
        r'^api/v1/coi/curric/$',
        CurricCOI.as_view(), name='curric-coi'),
    re_path(
        r'^api/v1/admin/releases/$',
        list_releases, name='list-releases'),
    re_path(
        r'^api/v1/admin/releases/(?P<release_id>[A-Za-z0-9_-]+)/manifest/$',
        get_release_manifest, name='get-release-manifest'),
    re_path(
        r'^api/v1/admin/releases/promote/$',
        promote_release, name='promote-release'),

    # Include supporttools SPA registry URLs (must precede the catch-all)
    *get_registry_urlpatterns(),

    re_path(r'^(major|course|faq|search)$', DefaultPageView.as_view()),
    re_path(r'^$', DefaultPageView.as_view()),
]
