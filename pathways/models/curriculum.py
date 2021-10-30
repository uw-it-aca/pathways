# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Curriculum(models.Model):
    abbrev = models.CharField(max_length=10)
    prereq_graph = models.JSONField(null=True)

    @staticmethod
    def get_prereq(abbrev):
        print(Curriculum.objects.all())
        return Curriculum.objects.get(abbrev=abbrev).prereq_graph
