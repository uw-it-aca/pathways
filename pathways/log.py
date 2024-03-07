# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from logging import Filter


class UserFilter(Filter):
    """ Add user information to each log entry. """

    def filter(self, record):
        from uw_saml.utils import get_user
        try:
            record.user = get_user() or "-"
        except Exception as ex:
            record.user = "-"

        return True
