# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from pathways.dao.person import get_person_by_uwnetid


class TestPerson(TestCase):
    databases = "__all__"
    fixtures = ["person.json", "employee.json", "term.json", "major.json",
                "student.json", "adviser.json", "transfer.json",
                "transcript.json", "hold.json", "degree.json", "sport.json"]

    def test_get_person_by_uwnetid(self):
        person = get_person_by_uwnetid("javerage")
        self.assertEqual(person.uwnetid, "javerage")
        self.assertEqual(person.student.student_number, "1033334")

        # Advisers
        advisers = person.student.advisers.all()
        self.assertEqual(len(advisers), 1)
        self.assertEqual(advisers.first().employee.person.full_name,
                         "Jay Adviser")

        # Intended majors
        self.assertEqual(len(person.student.intended_majors), 2)

        # Majors
        self.assertEqual(len(person.student.majors), 2)
        self.assertEqual(person.student.majors[0].major_name,
                         "PRE SOCIAL SCIENCE")
        self.assertEqual(person.student.majors[1].major_name,
                         "INTERNATIONAL STUDIES")

        # Transcripts
        transcripts = person.student.transcripts.all()
        self.assertEqual(len(transcripts), 3)
        self.assertEqual(transcripts.last().cmp_cum_gpa, "2.00")
