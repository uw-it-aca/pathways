# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from pathways.views.pages import DefaultPageView


urlpatterns = [re_path(r"^.*$", DefaultPageView.as_view(), name="index")]
