# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from pathways.views.pages import PageView
from pathways.views.api.major import MajorDetails, MajorList


urlpatterns = [
    re_path(
        r'^api/v1/majors/$',
        MajorList.as_view(), name='major-list'),
    re_path(
        r'^api/v1/majors/(?P<major_abbr>[^/]*)$',
        MajorDetails.as_view(), name='major-details'),
    re_path(r"^.*$", PageView.as_view(), name="index")
]
