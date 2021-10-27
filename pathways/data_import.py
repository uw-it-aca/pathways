# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.models.major import Major
from pathways.models.course import Course


def import_major_data(data):
    Major.objects.all().delete()
    major_objs = []
    for major in data:
        major_objs.append(Major(
            major_abbr=data[major]['major_code'],
            gpa_2yr=data[major]['2_yr'],
            gpa_5yr=data[major]['5_yr'],
            major_title=data[major]['major_title'],
            major_school=data[major]['major_school'],
            major_campus=data[major]['major_campus'],
            major_description=data[major]['major_description'],
            major_admission=data[major]['major_admission'],
            program_code=data[major]['program_code'],
            major_home_url=data[major]['major_home_url'],
            common_course_decl=data[major]['common_course_decl']
        ))
    Major.objects.bulk_create(major_objs)


def import_course_data(data):
    Course.objects.all().delete()
    course_objs = []
    for course in data:
        course_objs.append(Course(
            course_id=course['course_id'],
            course_title=course['course_title'],
            course_credits=course['course_credits'],
            gpa_distro=course['gpa_distro'],
            concurrent_courses=course['concurrent_courses']
        ))
    Course.objects.bulk_create(course_objs)
