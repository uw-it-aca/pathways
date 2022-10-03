# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import reverse
#from uw_saml.utils import get_user
#from userservice.user import UserService


def auth_user(request):
    return {
        # 'username': get_user(request),  # Basic SAML auth
        # 'username': UserService().get_user(),  # With UserService override
        # 'signout_url': reverse('saml_logout'),
    }


def google_analytics(request):
    return {"google_analytics": getattr(settings, "GOOGLE_ANALYTICS_KEY", " ")}


def django_debug(request):
    return {"django_debug": getattr(settings, "DEBUG", False)}
