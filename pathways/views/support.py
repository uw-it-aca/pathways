# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Views for data release promotion SPA tool."""

from django.conf import settings
from django.utils.decorators import method_decorator
from supporttools.views import SpaToolView

from pathways.views import support_group_required


@method_decorator(support_group_required(settings.ADMIN_USERS_GROUP), name="dispatch")
class DataReleaseSpaToolView(SpaToolView):
    """SPA view for data release promotion tool with same auth as supporttools."""

    def get_page_data(self):
        """Return bootstrap data for direct URL navigation."""
        return {
            "can_promote": True,  # Auth is enforced by decorator
            "username": self.request.user.get_username()
            if self.request.user.is_authenticated
            else None,
        }
