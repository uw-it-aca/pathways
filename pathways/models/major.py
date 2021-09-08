# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Major(models.Model):
    major_abbr = models.CharField(max_length=12)
    gpa_2yr = models.JSONField()
    gpa_5yr = models.JSONField()

    @staticmethod
    def get_major_list():
        return list(Major.objects.values_list("major_abbr", flat=True))

    @staticmethod
    def get_major_data(major_abbr):
        return Major.objects.get(major_abbr=major_abbr).json_data()

    def json_data(self):
        return {"major_abbr": self.major_abbr,
                "gpa_2yr": self.gpa_2yr,
                "gpa_5yr": self.gpa_5yr}
