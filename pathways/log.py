# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from logging import Filter
from asgiref.local import Local

_local = Local()


class UserFilter(Filter):
    """ Add user information to each log entry. """

    def filter(self, record):
        record.user = getattr(_local, "user", "-") or "-"
        record.actas = (getattr(_local, "actas", "-") or "-").lower()
        return True


class UserLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            from userservice.user import UserService
            user_service = UserService()
            setattr(_local, "user", user_service.get_original_user())
            setattr(_local, "actas", user_service.get_user())
        except Exception as ex:
            pass

        response = self.get_response(request)
        return response
