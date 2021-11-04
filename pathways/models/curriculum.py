# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Curriculum(models.Model):
    abbrev = models.CharField(max_length=10)
    prereq_graph = models.JSONField(null=True)
    prereq_list = models.JSONField(null=True)
    postreq_list = models.JSONField(null=True)

    @staticmethod
    def get_prereq(abbrev):
        curric = Curriculum.objects.get(abbrev=abbrev)
        response = {"prereq_grap": curric.prereq_graph,
                    "prereq_list": curric.prereq_list,
                    "postreq_list": curric.postreq_list}
        return response
