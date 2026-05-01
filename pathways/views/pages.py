# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from re import T
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from uw_saml.utils import get_user
from pathways.views import eval_group_required
from pathways.models.user import User
from pathways.utils import hash_netid
from pathways.dao.person import get_person_by_uwnetid, PersonNotFoundException


ALLOWED_USERS_GROUP = getattr(settings, "ALLOWED_USERS_GROUP", None)


@method_decorator(login_required, name="dispatch")
@method_decorator(eval_group_required(ALLOWED_USERS_GROUP),
                  name='dispatch')
class PageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response({**context, "context_data": context})

    def get_context_data(self, **kwargs):
        uwnetid = get_user(self.request)
        banners = User.show_banners(uwnetid)
        context = {}
        context["googleAnalyticsKey"] = settings.GOOGLE_ANALYTICS_KEY
        context["googleFeedbackForm"] = settings.GOOGLE_FEEDBACK_FORM
        context["clarityProjectId"] = settings.CLARITY_PROJECT_ID
        context['user'] = uwnetid
        context['hashedNetid'] = hash_netid(uwnetid)
        context['show_welcome'] = True if "welcome" in banners else False
        context['show_bottleneck'] = True if "bottleneck" in banners else False
        context['show_outcomes'] = True if "outcomes" in banners else False
        context['show_coi'] = True if "coi" in banners else False
        context["debugMode"] = getattr(settings, "DEBUG", False)

        try:
            context['personData'] = get_person_by_uwnetid(uwnetid)
        except PersonNotFoundException:
            context['personData'] = {}

        return context


class DefaultPageView(PageView):
    template_name = "index.html"
