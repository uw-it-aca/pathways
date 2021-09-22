# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.major import Major
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name="dispatch")
class MajorList(RESTDispatch):
    def get(self, request, *args, **kwargs):
        majors = Major.get_major_list()
        return self.json_response(majors)


@method_decorator(login_required, name="dispatch")
class MajorDetails(RESTDispatch):
    def get(self, request, major_abbr, *args, **kwargs):
        try:
            major = Major.get_major_data(major_abbr)
            return self.json_response(major)
        except ObjectDoesNotExist as ex:
            return self.error_response(404, "Major %s not found" % major_abbr)
