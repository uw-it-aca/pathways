# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator

from pathways.models.curriculum import Curriculum
from pathways.views.api import RESTDispatch


@method_decorator(login_required, name="dispatch")
class CurricPrereq(RESTDispatch):
    def get(self, request, curric_abbr, *args, **kwargs):
        try:
            curric = Curriculum.get_prereq(curric_abbr)
            return self.json_response(curric)
        except ObjectDoesNotExist:
            return self.error_response(404,
                                       f"Curric {curric_abbr} not found")
