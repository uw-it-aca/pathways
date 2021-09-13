# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class Major(models.Model):
    major_abbr = models.CharField(max_length=12)
    major_title = models.TextField()
    gpa_2yr = models.JSONField(null=True)
    gpa_5yr = models.JSONField(null=True)

    @staticmethod
    def get_major_list():
        majors = Major.objects.only("major_abbr", "major_title")
        major_json = []
        for major in majors:
            major_json.append({"key": major.major_abbr,
                               "value": major.major_title})
        return major_json

    @staticmethod
    def get_major_data(major_abbr):
        return Major.objects.get(major_abbr=major_abbr).json_data()

    def json_data(self):
        return {"major_abbr": self.major_abbr,
                "major_title": self.major_title,
                "gpa_2yr": Major.fix_gpa_json(self.gpa_2yr),
                "gpa_5yr": Major.fix_gpa_json(self.gpa_5yr)}

    @staticmethod
    def fix_gpa_json(json):
        fixed = []
        for key in json:
            fixed.append({"gpa": key, "count": json[key]})
        return fixed

