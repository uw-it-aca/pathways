# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from uw_saml.utils import is_member_of_group
from django.conf import settings


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
