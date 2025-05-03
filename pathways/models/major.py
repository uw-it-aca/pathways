# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from pathways.models.course import Course
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import urlencode


class Major(models.Model):
    major_abbr = models.CharField(max_length=12)
    major_title = models.TextField()
    major_school = models.TextField()
    major_campus = models.TextField()
    major_description = models.TextField(null=True)
    major_admission = models.TextField(null=True)
    major_home_url = models.URLField(null=True)
    program_code = models.CharField(max_length=25)
    program_verind_id = models.CharField(max_length=50)
    common_course_decl = models.JSONField(null=True)
    gpa_2yr = models.JSONField(null=True)
    gpa_5yr = models.JSONField(null=True)
    credential_title = models.TextField(null=True)
    credential_code = models.CharField(max_length=25, null=True)
    credential_description = models.TextField(null=True)
    career_center_major = models.TextField(null=True)
    is_stem = models.BooleanField(default=False)

    def is_parent_major(self):
        """
        Check if the major is a parent major (deg_major_pathway == 0).
        """
        return self.credential_code.split("-")[1] == "0"

    def get_search_string(self):
        string = "{abbr} {title} {description}"
        return string.format(abbr=self.major_abbr,
                             title=self.credential_title,
                             description=self.credential_description)

    def get_search_results_dict(self):
        url = urlencode({"id": self.major_abbr})
        return {"id": self.major_abbr,
                "contents": self.get_search_string(),
                "title": self.credential_title,
                "description": self.credential_description,
                "abbr": self.major_abbr,
                "score": 100,
                "campus": self.major_campus,
                "url": "/major?" + url}

    @staticmethod
    def get_major_list():
        majors = Major.objects.only("major_abbr", "major_title")
        major_json = []
        for major in majors:
            major_json.append({"key": major.major_abbr,
                               "value": major.major_title})
        return major_json

    @staticmethod
    def get_major_list_by_campus(major_campus):
        majors = Major.objects\
            .filter(major_campus=major_campus.capitalize())\
            .only("major_abbr", "major_title")
        major_json = []
        for major in majors:
            major_json.append({"key": major.credential_code,
                               "value": major.credential_title})
        return major_json

    @staticmethod
    def get_major_data(credential_abbr):
        return Major.objects.get(credential_code=credential_abbr).json_data()

    def json_data(self):
        return {"major_abbr": self.major_abbr,
                "major_title": self.major_title,
                "major_school": self.major_school,
                "major_campus": self.major_campus,
                "major_description": self.major_description,
                "major_admission": self.major_admission,
                "program_code": self.program_code,
                "program_verind_id": self.program_verind_id,
                "major_home_url": Major.get_major_url(self.major_home_url),
                "common_course_decl": self.get_common_with_coi_and_flags(),
                "gpa_2yr": Major.fix_gpa_json(self.gpa_2yr),
                "gpa_5yr": Major.fix_gpa_json(self.gpa_5yr),
                "credential_description": self.credential_description,
                "credential_title": self.credential_title,
                "credential_code": self.credential_code,
                "career_center_major": self.career_center_major,
                "is_stem": self.is_stem,
                "similar_majors": SimilarMajor.json_data_by_major(self)}

    def similar_major_json(self):
        return {"credential_code": self.credential_code,
                "credential_title": self.credential_title,
                "major_school": self.major_school,
                "campus": self.major_campus,
                "is_stem": self.is_stem,
                "major_admission": self.major_admission}

    @staticmethod
    def fix_gpa_json(json):
        fixed = []
        try:
            for key in json:
                fixed.append({"gpa": key, "count": json[key]})
        except TypeError:
            # No GPA data
            pass
        return fixed

    @staticmethod
    def get_major_url(url):
        if url is not None:
            return "http:\\\\%s" % url

    def get_common_with_coi_and_flags(self):
        common_with_coi = {}
        try:
            courses = self.common_course_decl.keys()
            coi_scores = Course.objects.filter(course_id__in=courses)
            for course in courses:
                try:
                    course_obj = Course.objects.get(course_id=course)
                    percent = self.common_course_decl[course]['percent']
                    title = self.common_course_decl[course]['title']
                    coi = coi_scores.get(course_id=course).coi_score
                    bottleneck = course_obj.is_bottleneck
                    gateway = course_obj.is_gateway
                    common_with_coi[course] = {"percent": percent,
                                               "title": title,
                                               "coi_score": coi,
                                               "is_bottleneck": bottleneck,
                                               "is_gateway": gateway}
                except ObjectDoesNotExist:
                    pass
        except AttributeError:
            # No common courses
            pass
        return common_with_coi


class SimilarMajor(models.Model):
    class Description(models.TextChoices):
        VERY_LOW = "VL", "Very Low"
        LOW = "L", "Low"
        MID = "M", "Mid"
        HIGH = "H", "High"
    source_major = models.ForeignKey(Major,
                                     on_delete=models.CASCADE,
                                     related_name='source_major')
    similar_major = models.ForeignKey(Major,
                                      on_delete=models.CASCADE,
                                      related_name='similar_major')
    similarity_score = models.FloatField()
    similarity_description = models.TextField(choices=Description.choices)

    @classmethod
    def json_data_by_major(cls, major):
        """
        Get similar majors for a given major in hierarchical format.
        """
        similar_majors = (cls.objects.filter(source_major=major)
                          .select_related('similar_major'))
        # Group similar majors by program code
        majors_by_program = {}
        for sm in similar_majors:
            program_id = sm.similar_major.program_verind_id
            (majors_by_program.setdefault(program_id, [])
             .append(sm.similar_major))

        major_data = []
        for pc, majors in majors_by_program.items():
            # If multiple majors in program group by parent
            if len(majors) > 1:
                program_majors = \
                    [major.similar_major_json() for major in majors]
                program_json = {
                    'program_code': majors[0].program_code,
                    'program_verind_id': majors[0].program_verind_id,
                    'program_title': majors[0].major_title,
                    'program_school': majors[0].major_school,
                    'program_campus': majors[0].major_campus,
                    'program_majors': program_majors
                }
                major_data.append(program_json)
            else:
                major_data.append(majors[0].similar_major_json())
        return major_data

    @classmethod
    def get_similarity_from_string(cls, similarity_string):
        similarity_map = {
            "Very Low": cls.Description.VERY_LOW,
            "Low": cls.Description.LOW,
            "Mid": cls.Description.MID,
            "High": cls.Description.HIGH
        }
        return similarity_map.get(similarity_string)
