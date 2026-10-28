# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from re import T

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from userservice.user import UserService

from pathways.dao.person import PersonNotFoundException, get_person_by_uwnetid
from pathways.models.user import User
from pathways.utils import hash_netid
from pathways.views import eval_group_required

ALLOWED_USERS_GROUP = getattr(settings, "ALLOWED_USERS_GROUP", None)


@method_decorator(login_required, name="dispatch")
@method_decorator(eval_group_required(ALLOWED_USERS_GROUP), name="dispatch")
class PageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response({**context, "context_data": context})

    def get_context_data(self, **kwargs):

        user_service = UserService()
        user = user_service.get_user()

        banners = User.show_banners(user)
        context = {}
        context["googleAnalyticsKey"] = settings.GOOGLE_ANALYTICS_KEY
        context["googleFeedbackForm"] = settings.GOOGLE_FEEDBACK_FORM
        context["clarityProjectId"] = settings.CLARITY_PROJECT_ID

        # Dawgpath customization
        context["show_welcome"] = True if "welcome" in banners else False
        context["show_bottleneck"] = True if "bottleneck" in banners else False
        context["show_outcomes"] = True if "outcomes" in banners else False
        context["show_coi"] = True if "coi" in banners else False

        # User context
        context["user"] = user
        context["hashedNetid"] = hash_netid(user)
        context["login_user"] = user_service.get_original_user()
        context["override_user"] = user_service.get_override_user()
        # context["user_fullname"] = person_display_name(person)
        context["signout_url"] = reverse("saml_logout")
        context["debug_mode"] = settings.DEBUG

        try:
            context["personData"] = get_person_by_uwnetid(user)
        except PersonNotFoundException:
            context["personData"] = {}

        return context


class DefaultPageView(PageView):
    template_name = "index.html"
