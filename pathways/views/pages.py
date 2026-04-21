# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from uw_saml.utils import get_user

from pathways.models.user import User
from pathways.views import eval_group_required

ALLOWED_USERS_GROUP = getattr(settings, "ALLOWED_USERS_GROUP", None)


@method_decorator(login_required, name="dispatch")
@method_decorator(eval_group_required(ALLOWED_USERS_GROUP), name="dispatch")
class PageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response({"context_data": context})

    def get_context_data(self, **kwargs):
        uwnetid = get_user(self.request)
        context = {}
        context["debugMode"] = settings.DEBUG
        context["googleAnalyticsKey"] = settings.GOOGLE_ANALYTICS_KEY
        context["googleFeedbackForm"] = settings.GOOGLE_FEEDBACK_FORM
        context["clarityProjectId"] = settings.CLARITY_PROJECT_ID
        context["user"] = uwnetid
        banners = User.show_banners(uwnetid)
        context["show_welcome"] = "welcome" in banners
        context["show_bottleneck"] = "bottleneck" in banners
        context["show_outcomes"] = "outcomes" in banners
        context["show_coi"] = "coi" in banners

        context["django_debug"] = getattr(settings, "DEBUG", False)
        return context


class DefaultPageView(PageView):
    template_name = "index.html"
