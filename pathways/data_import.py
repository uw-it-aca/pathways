# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from pathways.models.major import Major
from pathways.models.course import Course
from pathways.models.curriculum import Curriculum
from pathways.models.course_level import CourseLevel
from pathways.models.coi_range import COIRange
from django.core.exceptions import ObjectDoesNotExist
import statistics
import json


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
            common_course_decl=data[major]['common_course_decl'],
            credential_code=data[major]['credential_code'],
            credential_title=data[major]['credential_title'],
            credential_description=data[major]['credential_description']
        ))
    Major.objects.bulk_create(major_objs)


def import_course_data(data, coi_data):
    Course.objects.all().delete()
    course_objs = []
    for course in data:
        coi = _get_course_coi(course['course_id'], coi_data)
        course_objs.append(Course(
            course_id=course['course_id'],
            course_title=course['course_title'],
            course_credits=course['course_credits'],
            course_campus=course['course_campus'],
            gpa_distro=course['gpa_distro'],
            concurrent_courses=course['concurrent_courses'],
            prereq_graph=course['prereq_graph'],
            course_description=course['course_description'],
            course_offered=course['offered_string'],
            prereq_string=course['prereq_string'],
            coi_score=coi,
            department_abbrev=course['department_abbrev']
        ))
    Course.objects.bulk_create(course_objs)


def import_curric_data(data, coi_data):
    Curriculum.objects.all().delete()
    curric_coi = _get_curric_coi(coi_data)
    curric_objs = []
    for curric in data:
        coi = curric_coi.get(curric['curric_abbrev'])
        if coi is not None:
            coi = round(statistics.mean(coi), 1)
        try:
            pr_graph = json.loads(curric['prereq_graph'])
        except TypeError:
            pr_graph = None
        curric_objs.append(Curriculum(
            abbrev=curric['curric_abbrev'],
            prereq_graph=pr_graph,
            course_data=json.loads(curric['course_data']),
            average_coi_score=coi,
            curric_name=curric['curric_name']
        ))
    Curriculum.objects.bulk_create(curric_objs)


def import_level_coi(coi_data):
    CourseLevel.objects.all().delete()
    level_100 = []
    level_200 = []
    level_300 = []
    level_400 = []
    for course in coi_data:
        curric, num = _split_course_id(course['course_id'])
        if course['coi_score'] == -1:
            continue
        if 400 <= num < 500:
            level_400.append(course['coi_score'])
            continue
        if num >= 300:
            level_300.append(course['coi_score'])
            continue
        if num >= 200:
            level_200.append(course['coi_score'])
            continue
        if num >= 100:
            level_100.append(course['coi_score'])
            continue

    CourseLevel(level=100,
                coi_score=round(statistics.mean(level_100), 1)).save()
    CourseLevel(level=200,
                coi_score=round(statistics.mean(level_200), 1)).save()
    CourseLevel(level=300,
                coi_score=round(statistics.mean(level_300), 1)).save()
    CourseLevel(level=400,
                coi_score=round(statistics.mean(level_400), 1)).save()


def import_coi_ranges(coi_data):
    COIRange.objects.all().delete()
    course_count = len(coi_data)
    range_0 = 0
    range_1 = 0
    range_2 = 0
    range_3 = 0
    range_4 = 0
    for course in coi_data:
        if 0 <= course['coi_score'] <= 1:
            range_0 += 1
            continue
        if course['coi_score'] <= 2:
            range_1 += 1
            continue
        if course['coi_score'] <= 3:
            range_2 += 1
            continue
        if course['coi_score'] <= 4:
            range_3 += 1
            continue
        if course['coi_score'] <= 5:
            range_4 += 1
            continue

    COIRange(coi_range=0, percent_in_range=range_0 / course_count).save()
    COIRange(coi_range=1, percent_in_range=range_1 / course_count).save()
    COIRange(coi_range=2, percent_in_range=range_2 / course_count).save()
    COIRange(coi_range=3, percent_in_range=range_3 / course_count).save()
    COIRange(coi_range=4, percent_in_range=range_4 / course_count).save()


def _get_curric_coi(coi_data):
    currics = {}
    for course in coi_data:
        curric, num = _split_course_id(course['course_id'])
        if course['coi_score'] == -1:
            continue
        if curric in currics:
            currics[curric].append(course['coi_score'])
        else:
            currics[curric] = [course['coi_score']]
    return currics


def _get_course_coi(course, coi_data):
    for coi_course in coi_data:
        if coi_course['course_id'] == course and coi_course['coi_score'] != -1:
            return round(coi_course['coi_score'], 1)


def _split_course_id(course_id):
    curric, delim, num = course_id.rpartition(" ")
    return curric, int(num)


def import_gateway_courses(gateway_data):
    gateway_course_objs = []
    for row in gateway_data:
        course_id = row[1] + " " + row[2]
        try:
            course = Course.objects.get(course_id=course_id)
            course.is_gateway = True
            gateway_course_objs.append(course)
        except ObjectDoesNotExist:
            pass
        Course.objects.bulk_update(gateway_course_objs, ['is_gateway'])


def import_bottleneck_courses(bottleneck_data):
    bottleneck_course_objs = []
    for row in bottleneck_data:
        course_id = row[1] + " " + row[2]
        try:
            course = Course.objects.get(course_id=course_id)
            course.is_bottleneck = True
            bottleneck_course_objs.append(course)
        except ObjectDoesNotExist:
            pass
        Course.objects.bulk_update(bottleneck_course_objs, ['is_bottleneck'])


def import_career_center_mapping(career_major_data):
    majors_to_update = []
    for row in career_major_data:
        try:
            major = Major.objects.get(credential_code=row[0])
            major.career_center_major = row[1]
            majors_to_update.append(major)
        except ObjectDoesNotExist:
            pass
    Major.objects.bulk_update(majors_to_update, ['career_center_major'])
