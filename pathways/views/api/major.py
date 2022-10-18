# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.major import Major
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name="dispatch")
class MajorList(RESTDispatch):
    valid_campus = ['seattle', 'tacoma', 'bothell']

    def get(self, request, major_campus, *args, **kwargs):
        if major_campus in self.valid_campus:
            majors = Major.get_major_list_by_campus(major_campus)
            return self.json_response(majors)
        else:
            return self.error_response(status=400, message="Invalid campus")


@method_decorator(login_required, name="dispatch")
class MajorDetails(RESTDispatch):
    def get(self, request, credential_abbr, *args, **kwargs):
        try:
            major = Major.get_major_data(credential_abbr)
            return self.json_response(major)
        except ObjectDoesNotExist as ex:
            return self.error_response(404,
                                       "Major %s not found" % credential_abbr)
