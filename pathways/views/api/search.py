# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pathways.search import search


@method_decorator(login_required, name="dispatch")
class Search(RESTDispatch):
    def get(self, request, *args, **kwargs):
        search_string = request.GET.get("search_string")
        is_bottleneck = False

        def to_bool(value):
            return value is not None and value == "true"

        is_gateway = to_bool(request.GET.get("is_gateway"))
        is_bottleneck = to_bool(request.GET.get("is_bottleneck"))
        min_coi_score = request.GET.get("min_coi_score")
        max_coi_score = request.GET.get("max_coi_score")
        campus_values = request.GET.getlist("campus[]")
        types = request.GET.getlist("type[]")

        courses = search(search_string, campus_values, types,
                         is_gateway=is_bottleneck,
                         is_bottleneck=is_gateway,
                         min_coi_score=min_coi_score,
                         max_coi_score=max_coi_score)
        return self.json_response(courses)
