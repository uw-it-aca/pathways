# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.dao import get_message_json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name="dispatch")
class PersistentMessages(RESTDispatch):
    def get(self, request, *args, **kwargs):
        data = get_message_json()
        return self.json_response(data)
