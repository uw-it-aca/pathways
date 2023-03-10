# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Curriculum(models.Model):
    abbrev = models.CharField(max_length=10)
    prereq_graph = models.JSONField(null=True)
    course_data = models.JSONField(null=True)
    average_coi_score = models.FloatField(null=True)
    curric_name = models.TextField(null=True)

    @staticmethod
    def get_prereq(abbrev):
        curric = Curriculum.objects.get(abbrev=abbrev)
        response = {"prereq_graph": curric.prereq_graph,
                    "course_data": curric.course_data}
        return response
