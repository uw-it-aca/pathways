# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.curriculum import Curriculum
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name="dispatch")
class CurricPrereq(RESTDispatch):
    def get(self, request, curric_abbr, *args, **kwargs):
        try:
            curric = Curriculum.get_prereq(curric_abbr)
            return self.json_response(curric)
        except ObjectDoesNotExist as ex:
            return self.error_response(404,
                                       "Curric %s not found" % curric_abbr)
