# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from pathways.models.major import Major, SimilarMajor
from pathways.models.course import Course
from multiprocessing import Pool, cpu_count


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.validate_majors()
        self.validate_courses()

    def validate_majors(self):
        count_majors = Major.objects.count()
        count_gpa_2yr = 0
        count_gpa_5yr = 0
        count_common_courses = 0
        for major in Major.objects.all():
            cc = major.get_common_with_coi_and_flags()
            if cc and len(cc) > 0:
                count_common_courses += 1
            if major.gpa_2yr and sum(major.gpa_2yr.values()) > 0:
                count_gpa_2yr += 1
            if major.gpa_5yr and sum(major.gpa_5yr.values()) > 0:
                count_gpa_5yr += 1
        # count of distinct source_major in SimilarMajor
        count_similar_majors = SimilarMajor.objects.values('source_major')\
            .distinct().count()
        print(f"Total Majors: {count_majors}")
        print(f"Majors with GPA Distro (2, 5): {count_gpa_2yr} "
              f"({self.pct_str(count_gpa_2yr, count_majors)}), "
              f"{count_gpa_5yr} ({self.pct_str(count_gpa_5yr, count_majors)})")
        print(f"Majors with Common Courses: {count_common_courses} "
              f"({self.pct_str(count_common_courses, count_majors)})")
        print(f"Majors with Similar Majors: {count_similar_majors} "
              f"({self.pct_str(count_similar_majors, count_majors)})")

    def validate_courses(self):
        count_courses = Course.objects.count()
        count_with_grade_distro = \
            (Course.objects.filter(gpa_distro__isnull=False).count())
        count_with_prereq = (Course.objects.filter(prereq_graph__isnull=False))

        pool = Pool(processes=cpu_count()-1)
        results = pool.map(self._process_course, Course.objects.all())
        pool.close()
        pool.join()
        count_with_coi = len([r for r in results if r[1]])
        count_with_concurrent = len([r for r in results if r[2]])

        print(f"Total Courses: {count_courses}")
        print(f"Courses with Grade Distro: {count_with_grade_distro} "
              f"({self.pct_str(count_with_grade_distro, count_courses)})")
        print(f"Courses with Prereq Map: {count_with_prereq.count()} "
              f"({self.pct_str(count_with_prereq.count(), count_courses)})")
        print(f"Courses with COI: {count_with_coi} "
              f"({self.pct_str(count_with_coi, count_courses)})")
        print(f"Courses with Concurrent: {count_with_concurrent} "
              f"({self.pct_str(count_with_concurrent, count_courses)})")

    @staticmethod
    def _process_course(course):
        coi = course.get_coi_data()
        concurrent = course.get_concurrent_with_coi_and_flags()
        return (course.course_id, bool(coi), bool(concurrent))

    @staticmethod
    def pct_str(value, total):
        if value and total > 0:
            percent = (value/total)*100
            return f"{percent:.2f}%"
        else:
            return "0.00%"
