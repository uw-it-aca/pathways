# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from uw_saml.utils import is_member_of_group


def eval_group_required(group_id):
    """
    Similar to UW_SAML's group_required but only applies for specific env
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if settings.LIMIT_USER_ACCESS:
                if is_member_of_group(request, group_id):
                    return view_func(request, *args, **kwargs)

                return render(request,
                              'uw_saml/access_denied.html',
                              status=401)
            return view_func(request, *args, **kwargs)

        return login_required(function=wrapper)

    return decorator


def can_override_user(request):
    return is_member_of_group(request, settings.ADMIN_USERS_GROUP)


def can_manage_persistent_message(request):
    return is_member_of_group(request, settings.ADMIN_USERS_GROUP)
