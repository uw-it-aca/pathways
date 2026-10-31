# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations


COURSE_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_id, '') || ' ' || coalesce(course_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_description, '')), 'B')"
)
MAJOR_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(major_abbr, '') || ' ' || coalesce(credential_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(credential_description, '')), 'B')"
)
INDEXES = (
    ("pathways_search_course_text", "pathways_course", "gin",
     f"({COURSE_TEXT})"),
    ("pathways_search_major_text", "pathways_major", "gin",
     f"({MAJOR_TEXT})"),
    ("pathways_search_course_title", "pathways_course", "gin",
     "lower(course_title) gin_trgm_ops"),
    ("pathways_search_major_title", "pathways_major", "gin",
     "lower(credential_title) gin_trgm_ops"),
    ("pathways_search_course_id", "pathways_course", "btree",
     "(regexp_replace(lower(course_id), '\\s+', '', 'g')) text_pattern_ops"),
    ("pathways_search_major_abbr", "pathways_major", "btree",
     "(regexp_replace(lower(major_abbr), '\\s+', '', 'g')) text_pattern_ops"),
)


def create_indexes(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    with schema_editor.connection.cursor() as cursor:
        for name, table, method, expression in INDEXES:
            cursor.execute(
                "SELECT index.indisvalid FROM pg_index index "
                "WHERE index.indexrelid = to_regclass(%s)",
                [f"public.{name}"])
            existing = cursor.fetchone()
            if existing is not None and not existing[0]:
                cursor.execute(f'DROP INDEX CONCURRENTLY public."{name}"')
            cursor.execute(
                f'CREATE INDEX CONCURRENTLY IF NOT EXISTS "{name}" '
                f'ON public."{table}" USING {method} ({expression})')


def drop_indexes(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    with schema_editor.connection.cursor() as cursor:
        for name, table, method, expression in reversed(INDEXES):
            cursor.execute(
                f'DROP INDEX CONCURRENTLY IF EXISTS public."{name}"')


class Migration(migrations.Migration):
    atomic = False
    dependencies = [("pathways", "0027_postgres_search_configuration")]
    operations = [migrations.RunPython(
        create_indexes, drop_indexes, atomic=False,
        hints={"model_name": "course"})]
