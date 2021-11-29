# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from uw_saml.utils import get_user
from pathways.models.user import User


@method_decorator(login_required, name="dispatch")
class PageView(TemplateView):
    """
    Superclass for all page views.
    """
    def get_context_data(self, **kwargs):
        uwnetid = get_user(self.request)
        context = super().get_context_data(**kwargs)
        context["ga_key"] = getattr(settings, "GOOGLE_ANALYTICS_KEY", " ")
        context['user'] = uwnetid
        context['show_welcome'] = User.show_welcome(uwnetid)
        context["django_debug"] = getattr(settings, "DEBUG", False)
        return context


class DefaultPageView(PageView):
    template_name = "index.html"
