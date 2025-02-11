# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class User(models.Model):
    uwnetid = models.CharField(max_length=32)
    has_viewed_welcome = models.BooleanField(default=False)
    has_viewed_bottleneck_banner = models.BooleanField(default=False)
    has_viewed_outcomes_banner = models.BooleanField(default=False)
    has_viewed_coi_banner = models.BooleanField(default=False)
    first_login = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def show_banners(uwnetid):
        try:
            user = User.objects.get(uwnetid=uwnetid)
            banners = []
            if not user.has_viewed_welcome:
                banners.append("welcome")
            if not user.has_viewed_bottleneck_banner:
                banners.append("bottleneck")
            if not user.has_viewed_outcomes_banner:
                banners.append("outcomes")
            if not user.has_viewed_coi_banner:
                banners.append("coi")
            return banners
        except ObjectDoesNotExist:
            return ["welcome", "bottleneck", "outcomes", "coi"]
