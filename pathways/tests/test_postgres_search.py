# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from importlib import import_module
from io import StringIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError, connection
from django.db.migrations.executor import MigrationExecutor
from django.test import (
    RequestFactory,
    SimpleTestCase,
    TestCase,
    TransactionTestCase,
    override_settings,
)

from pathways.models.course import Course
from pathways.models.major import Major
from pathways.postgres_search import COURSE_TEXT, MAJOR_TEXT, search
from pathways.search import search as routed_search
from pathways.views.api.search import Search


class PostgresSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Course.objects.create(
            course_id="CSE 142", course_title="Computer Programming I",
            course_description="Introduction to programming and algorithms.",
            course_credits="5", course_campus="seattle", coi_score=1.5,
            is_gateway=True)
        Course.objects.create(
            course_id="B CSE 142", course_title="Computer Programming",
            course_description="Introduction to programming.",
            course_credits="5", course_campus="bothell", coi_score=4,
            is_bottleneck=True)
        Course.objects.create(
            course_id="FRENCH 101", course_title="French Studies",
            course_description="An introduction to caf\u00e9s.",
            course_credits="5", course_campus="seattle")
        Major.objects.create(
            major_abbr="CSE", major_title="Computer Science",
            credential_title="Computer Science", credential_code="CSE-0-1",
            credential_description="Programming and algorithms.",
            major_campus="Seattle", major_school="Engineering",
            program_code="CSE", program_verind_id="1")

    def test_exact_course_id_normalization(self):
        for query in ("cse142", "CSE 142", " cSe   142 "):
            with self.subTest(query=query):
                result = search(query)
                self.assertEqual(result["course_matches"][0]["id"], "CSE 142")
                self.assertEqual(result["text_matches"][0]["id"], "CSE 142")
                self.assertEqual(result["course_matches"][0]["url"],
                                 "/course?id=CSE+142")

    def test_campus_and_type_in_every_group(self):
        result = search("programming", campus_values=["bothell"],
                        types=["course"])
        self.assertEqual(result["major_matches"], [])
        self.assertTrue(result["text_matches"])
        for group in result.values():
            self.assertTrue(all(row["campus"].lower() == "bothell"
                                for row in group))

    def test_exact_course_precedes_loose_major(self):
        Major.objects.update(credential_title="CSE Computer Science")
        result = search("cse 142")
        self.assertEqual(result["major_matches"], [])
        self.assertEqual(result["course_matches"][0]["id"], "CSE 142")

    def test_major_identity_and_campus(self):
        result = search("computer science", campus_values=["seattle"],
                        types=["major"])
        major = result["major_matches"][0]
        self.assertEqual(major["id"], "CSE-0-1")
        self.assertTrue(major["is_major"])
        self.assertEqual(major["url"], "/major?id=CSE-0-1")

    def test_phrase_course_beats_partial_title_major(self):
        Major.objects.update(credential_title="Chemistry")
        Course.objects.filter(course_id="CSE 142").update(
            course_title="Organic Chemistry")
        result = search("organic chemistry")
        self.assertEqual(result["major_matches"], [])
        self.assertEqual(result["text_matches"][0]["id"], "CSE 142")

    def test_repeated_description_cannot_beat_title_phrase(self):
        Course.objects.filter(course_id="CSE 142").update(
            course_title="Organic Chemistry")
        Course.objects.filter(course_id="B CSE 142").update(
            course_title="Chemistry Topics",
            course_description="Organic chemistry. " * 20)
        result = search("organic chemistry", types=["course"])
        self.assertEqual(result["text_matches"][0]["id"], "CSE 142")

    def test_learn_prefers_explicit_introductory_instruction(self):
        Course.objects.filter(course_id="CSE 142").update(
            course_title="Introduction to Programming")
        Course.objects.filter(course_id="B CSE 142").update(
            course_title="Advanced Programming")
        result = search("learn programming", types=["course"])
        self.assertEqual(result["text_matches"][0]["id"], "CSE 142")

    def test_learn_ranks_majors_with_courses(self):
        Major.objects.update(credential_title="Programming")
        Course.objects.filter(course_id="CSE 142").update(
            course_title="Introduction to Programming")
        Course.objects.filter(course_id="B CSE 142").update(
            course_title="Advanced Programming")
        for query in ("learn programming", " LEARN   programming "):
            with self.subTest(query=query):
                result = search(query)
                displayed = (result["major_matches"]
                             + result["course_matches"]
                             + result["text_matches"])
                self.assertEqual(result["major_matches"], [])
                self.assertEqual(displayed[0]["id"], "CSE 142")
                self.assertTrue(any(row.get("is_major") for row in displayed))

    def test_ordinary_search_keeps_major_title_promotion(self):
        Major.objects.update(credential_title="Programming")
        result = search("programming")
        displayed = (result["major_matches"] + result["course_matches"]
                     + result["text_matches"])
        self.assertEqual(displayed[0]["id"], "CSE-0-1")
        self.assertTrue(any(row.get("is_course") for row in displayed))

    def test_metadata_downweighted_but_preserved(self):
        Course.objects.filter(course_id="B CSE 142").update(
            course_title="Molecular Structures",
            course_description="Study of organic chemistry.")
        for label in ("Prerequisite:", "Prerequisites:", "Offered:",
                      "offered :"):
            with self.subTest(label=label):
                description = f"Laboratory methods. {label} organic chemistry."
                Course.objects.filter(course_id="CSE 142").update(
                    course_title="Laboratory Methods",
                    course_description=description)
                result = search("organic chemistry", types=["course"])
                rows = result["text_matches"]
                self.assertEqual(rows[0]["id"], "B CSE 142")
                row = next(row for row in rows if row["id"] == "CSE 142")
                self.assertEqual(row["description"], description)
                self.assertLess(row["score"], rows[0]["score"])

    def test_ordinary_prerequisite_prose_keeps_topic_bonus(self):
        Course.objects.filter(course_id="CSE 142").update(
            course_title="Molecular Structures",
            course_description=(
                "Prerequisite knowledge in organic chemistry is developed."))
        result = search("organic chemistry", types=["course"])
        self.assertGreater(result["text_matches"][0]["score"], 8)

    def test_gateway_bottleneck_and_coi_apply_to_all_groups(self):
        for filters, expected in (
            ({"is_gateway": True}, ["CSE 142"]),
            ({"is_bottleneck": True}, ["B CSE 142"]),
            ({"min_coi_score": "3", "max_coi_score": "5"}, ["B CSE 142"]),
        ):
            with self.subTest(filters=filters):
                result = search("programming", **filters)
                self.assertEqual(
                    [row["id"] for row in result["text_matches"]], expected)
                self.assertEqual(result["major_matches"], [])
        self.assertEqual(search("cse142", is_bottleneck=True)[
            "course_matches"], [])

    def test_typo_fallback(self):
        result = search("progrmming", types=["course"])
        self.assertIn("CSE 142", [row["id"] for row in result["text_matches"]])

    def test_fuzzy_fallback_is_filter_scoped(self):
        Course.objects.filter(course_id="CSE 142").update(
            course_title="Microscopy", course_description="Imaging.")
        Course.objects.filter(course_id="B CSE 142").update(
            course_title="Microskopy", course_description="Imaging.")
        result = search("microscopy", types=["course"])
        self.assertNotIn("B CSE 142",
                         [row["id"] for row in result["text_matches"]])
        filtered = search("microscopy", types=["course"],
                          campus_values=["bothell"])
        self.assertIn("B CSE 142",
                      [row["id"] for row in filtered["text_matches"]])

    def test_unaccent_and_missing_descriptions(self):
        self.assertIn("FRENCH 101", [row["id"] for row in search("cafes")[
            "text_matches"]])
        Course.objects.filter(course_id="CSE 142").update(
            course_description=None)
        self.assertEqual(search("cse142")["course_matches"][0]["id"],
                         "CSE 142")

    def test_empty_punctuation_and_sql_input(self):
        for query in (None, "", "  ", "!!!"):
            self.assertTrue(all(not rows for rows in search(query).values()))
        search("'; DROP TABLE pathways_course; --")
        self.assertEqual(Course.objects.count(), 3)

    @override_settings(PATHWAYS_SEARCH_BACKEND="postgres")
    def test_real_api_response(self):
        request = RequestFactory().get("/api/v1/search/", {
            "search_string": "cse142", "campus[]": "seattle",
            "type[]": "course"})
        request.user = User()
        response = Search.as_view()(request)
        self.assertEqual(response.status_code, 200)
        payload = json.loads(response.content)
        self.assertEqual(set(payload), {
            "course_matches", "major_matches", "text_matches"})
        self.assertEqual(payload["course_matches"][0]["id"], "CSE 142")

    @override_settings(PATHWAYS_SEARCH_BACKEND="postgres")
    def test_api_gateway_and_bottleneck_are_not_swapped(self):
        for flag, expected in (("is_gateway", "CSE 142"),
                               ("is_bottleneck", "B CSE 142")):
            with self.subTest(flag=flag):
                request = RequestFactory().get("/api/v1/search/", {
                    "search_string": "programming", "type[]": "course",
                    flag: "true"})
                request.user = User()
                payload = json.loads(Search.as_view()(request).content)
                self.assertEqual(
                    [row["id"] for row in payload["text_matches"]], [expected])

    @override_settings(PATHWAYS_SEARCH_BACKEND="postgres")
    def test_post_migrate_check(self):
        output = StringIO()
        call_command("check_search_backend", stdout=output)
        self.assertIn("are ready", output.getvalue())


class SearchBackendTests(SimpleTestCase):
    @override_settings(PATHWAYS_SEARCH_BACKEND="postgres")
    @patch("pathways.postgres_search.search", return_value={"postgres": True})
    def test_postgres_opt_in(self, backend):
        self.assertEqual(routed_search("CSE142", [], []), {"postgres": True})
        backend.assert_called_once()

    @override_settings(PATHWAYS_SEARCH_BACKEND="whoosh")
    @patch("pathways.search.whoosh_search", return_value={"whoosh": True})
    def test_whoosh_rollback(self, backend):
        self.assertEqual(routed_search("CSE142", [], []), {"whoosh": True})
        output = StringIO()
        call_command("check_search_backend", stdout=output)
        self.assertIn("skipped", output.getvalue())

    @override_settings(PATHWAYS_SEARCH_BACKEND="invalid")
    def test_unknown_backend_fails_explicitly(self):
        with self.assertRaises(ImproperlyConfigured):
            routed_search("CSE142", [], [])
        with self.assertRaises(CommandError):
            call_command("check_search_backend")

    def test_migration_expressions_match_runtime_lookup(self):
        migration = import_module(
            "pathways.migrations.0028_postgres_search_indexes")
        self.assertEqual(migration.COURSE_TEXT, COURSE_TEXT)
        self.assertEqual(migration.MAJOR_TEXT, MAJOR_TEXT)
        self.assertFalse(migration.Migration.atomic)


class SearchMigrationTests(TransactionTestCase):
    @override_settings(PATHWAYS_SEARCH_BACKEND="postgres")
    def test_rollback_and_retry_preserve_catalog(self):
        Course.objects.create(
            course_id="CSE 142", course_title="Programming",
            course_credits="5", course_campus="seattle")
        Course.objects.create(
            course_id="CSE 143", course_title="Programming II",
            course_credits="5", course_campus="seattle")
        prior = [("pathways", "0027_postgres_search_configuration")]
        target = [("pathways", "0028_postgres_search_indexes")]
        executor = MigrationExecutor(connection)
        executor.migrate(prior)
        try:
            with self.assertRaises(CommandError):
                call_command("check_search_backend", stdout=StringIO())
            migration = import_module(
                "pathways.migrations.0028_postgres_search_indexes")
            name, table, method, expression = migration.INDEXES[0]
            with connection.cursor() as cursor:
                cursor.execute(
                    f'CREATE INDEX CONCURRENTLY "{name}" ON "{table}" '
                    f'USING {method} ({expression})')
                invalid_name = migration.INDEXES[1][0]
                with self.assertRaises(IntegrityError):
                    cursor.execute(
                        f'CREATE UNIQUE INDEX CONCURRENTLY "{invalid_name}" '
                        'ON pathways_course (course_campus)')
        finally:
            MigrationExecutor(connection).migrate(target)
        call_command("check_search_backend", stdout=StringIO())
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(search("cse142")["course_matches"][0]["id"],
                         "CSE 142")
