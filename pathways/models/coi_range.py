# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class COIRange(models.Model):
    RANGES = [
        (0, '0-1'),
        (1, '1-2'),
        (2, '2-3'),
        (3, '3-4'),
        (4, '4-5')
    ]
    coi_range = models.IntegerField(choices=RANGES)
    percent_in_range = models.FloatField(null=True)

    @staticmethod
    def get_percent_by_score(score):
        if score <= 1:
            return COIRange.objects.get(coi_range=0)
        if score <= 2:
            return COIRange.objects.get(coi_range=1)
        if score <= 3:
            return COIRange.objects.get(coi_range=2)
        if score <= 4:
            return COIRange.objects.get(coi_range=3)
        if score <= 5:
            return COIRange.objects.get(coi_range=4)
