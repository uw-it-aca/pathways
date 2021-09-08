# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.major import Major


class MajorList(RESTDispatch):
    def get(self, request, *args, **kwargs):
        print('foo')
        majors = Major.get_major_list()
        print(majors)
        return self.json_response(majors)


class MajorDetails(RESTDispatch):
    def get(self, request, major_abbr, *args, **kwargs):
        major = Major.get_major_data(major_abbr)
        return self.json_response(major)
