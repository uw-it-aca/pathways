# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.views.api import RESTDispatch
from pathways.models.user import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from uw_saml.utils import get_user
import json


@method_decorator(login_required, name="dispatch")
class UserPreference(RESTDispatch):
    def post(self, request, *args, **kwargs):
        uwnetid = get_user(self.request)
        request_params = json.loads(request.body)
        welcome_display = request_params.get("viewed_welcome_display")
        bottleneck_display = request_params.get("viewed_bottleneck_banner")

        user, created = \
            User.objects.get_or_create(uwnetid=uwnetid)
        user_updated = False
        if welcome_display is not None:
            if welcome_display != user.has_viewed_welcome:
                user_updated = True
                user.has_viewed_welcome = welcome_display
        if bottleneck_display is not None:
            if bottleneck_display != user.has_viewed_bottleneck_banner:
                user_updated = True
                user.has_viewed_bottleneck_banner = bottleneck_display
        if user_updated:
            user.save()
            return self.json_response(status=200)
        else:
            return self.json_response(status=304)
