# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class CourseLevel(models.Model):
    COURSE_LEVELS = [
        (100, '100'),
        (200, '200'),
        (300, '300'),
        (400, '400'),
    ]
    level = models.IntegerField(choices=COURSE_LEVELS)
    coi_score = models.FloatField(null=True)
