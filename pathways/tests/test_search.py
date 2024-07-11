from pathways.search import format_course_id
from django.test import TestCase


class TestSearchApi(TestCase):

    def test_format_course_id(self):
        self.assertEqual(format_course_id("TRAIN 1"),
                         "TRAIN 1")
        self.assertEqual(format_course_id("B TRAIN 1"),
                         "B TRAIN 1")
        self.assertEqual(format_course_id("TRAIN1"),
                         "TRAIN 1")
        self.assertEqual(format_course_id("B TRAIN1"),
                         "B TRAIN 1")
