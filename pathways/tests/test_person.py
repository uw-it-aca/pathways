# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from pathways.dao.person import (
    get_person_by_uwnetid, valid_uwnetid, PersonNotFoundException)


class TestPerson(TestCase):
    databases = "__all__"
    fixtures = ["person.json", "employee.json", "term.json", "major.json",
                "student.json", "adviser.json", "transfer.json",
                "transcript.json", "hold.json", "degree.json", "sport.json"]

    def test_get_person_by_uwnetid(self):
        person = get_person_by_uwnetid("javerage")

        self.assertEqual(person.get("student_number"), "1033334")
        self.assertEqual(person.get("class_desc"), "Sophomore")
        self.assertEqual(person.get("total_credits"), "79.00")
        self.assertEqual(person.get("quarters_completed"), 3)
        self.assertEqual(person.get("cumulative_gpa"), "3.84")

        # Advisers
        self.assertEqual(len(person.get("advisers")), 1)
        self.assertEqual(person.get("advisers")[0].get("display_name"),
                         "Jay Adviser")

        # Majors
        self.assertEqual(len(person.get("majors")), 2)
        self.assertEqual(person.get("majors")[0].get("major_name"),
                         "PRE SOCIAL SCIENCE")
        self.assertEqual(person.get("majors")[1].get("major_name"),
                         "INTERNATIONAL STUDIES")

        # Not a student
        person = get_person_by_uwnetid("jadviser")
        self.assertEqual(person, {
            "display_name": "Jay Adviser", "uwnetid": "jadviser"})

        # Not a person
        self.assertRaises(PersonNotFoundException,
                          get_person_by_uwnetid, "xxxxxxx")

    def test_valid_netid(self):
        self.assertEqual(valid_uwnetid("javerage"), None)
        self.assertEqual(valid_uwnetid("jadviser"), None)
        self.assertEqual(valid_uwnetid("xxxxxx"), "Not a valid UWNetID: ")
        self.assertEqual(valid_uwnetid(None),
                         "No override user supplied, please enter a UWNetID")
        self.assertEqual(valid_uwnetid(""),
                         "No override user supplied, please enter a UWNetID")
