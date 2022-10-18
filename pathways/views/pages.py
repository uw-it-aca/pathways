# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from uw_saml.utils import get_user
from pathways.views import eval_group_required
from pathways.models.user import User

ALLOWED_USERS_GROUP = getattr(settings, "ALLOWED_USERS_GROUP", None)


@method_decorator(login_required, name="dispatch")
@method_decorator(eval_group_required(ALLOWED_USERS_GROUP),
                  name='dispatch')
class PageView(TemplateView):
    template_name = "index.html"

    """
    Superclass for all page views.
    """
    def get_context_data(self, **kwargs):
        uwnetid = get_user(self.request)
        context = super().get_context_data(**kwargs)
        context["ga_key"] = getattr(settings, "GOOGLE_ANALYTICS_KEY", " ")
        context["google_feedback_form"] = \
            getattr(settings, "GOOGLE_FEEDBACK_FORM", "")
        context['user'] = uwnetid
        banners = User.show_banners(uwnetid)
        context['show_welcome'] = "welcome" in banners
        context['show_bottleneck'] = "bottleneck" in banners
        context['show_outcomes'] = "outcomes" in banners

        context["django_debug"] = getattr(settings, "DEBUG", False)
        return context


class DefaultPageView(PageView):
    template_name = "index.html"
