# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views import View


class RESTDispatch(View):
    @staticmethod
    def json_response(content=None, status=200):
        if content is None:
            content = {}
        try:
            data = json.dumps(content,
                              sort_keys=True,
                              cls=DjangoJSONEncoder)
            return HttpResponse(data,
                                status=status,
                                content_type='application/json')
        except TypeError:
            return RESTDispatch().error_response(400)

    @staticmethod
    def error_response(status, message='', content=None):
        if content is None:
            content = {}
        content['error'] = str(message)
        return HttpResponse(json.dumps(content),
                            status=status,
                            content_type='application/json',
                            )
