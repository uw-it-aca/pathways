# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations


COURSE_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_id, '') || ' ' || coalesce(course_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_description, '')), 'B')"
)
COURSE_TOPIC_DESCRIPTION = (
    "regexp_replace(coalesce(course_description, ''), "
    "'\\m(Prerequisites?|Offered)[[:space:]]*:[\\s\\S]*$', '', 'i')"
)
COURSE_TOPIC_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_id, '') || ' ' || coalesce(course_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    f"{COURSE_TOPIC_DESCRIPTION}), 'B')"
)
COURSE_RANK_TEXT = (
    f"({COURSE_TOPIC_TEXT}) || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "substr(coalesce(course_description, ''), "
    f"length({COURSE_TOPIC_DESCRIPTION}) + 1)), 'D')"
)
MAJOR_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(major_abbr, '') || ' ' || coalesce(credential_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(credential_description, '')), 'B')"
)
COURSE_TITLE_TEXT = (
    "to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_title, ''))"
)
MAJOR_TITLE_TEXT = (
    "to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(credential_title, ''))"
)
# PostgreSQL computes these on every insert or update, so data imports keep
# them current without any application-side indexing step.
COLUMNS = {
    "pathways_course": (
        ("search_document", COURSE_TEXT),
        ("search_rank_document", COURSE_RANK_TEXT),
        ("search_title_document", COURSE_TITLE_TEXT),
    ),
    "pathways_major": (
        ("search_document", MAJOR_TEXT),
        ("search_title_document", MAJOR_TITLE_TEXT),
    ),
}
COLUMN_INDEXES = (
    ("pathways_search_course_document", "pathways_course", "gin",
     "search_document"),
    ("pathways_search_major_document", "pathways_major", "gin",
     "search_document"),
)
EXPRESSION_INDEXES = (
    ("pathways_search_course_text", "pathways_course", "gin",
     f"({COURSE_TEXT})"),
    ("pathways_search_major_text", "pathways_major", "gin",
     f"({MAJOR_TEXT})"),
)


def _applies(schema_editor):
    return (schema_editor.connection.alias == "default"
            and schema_editor.connection.vendor == "postgresql")


def _create_indexes(cursor, indexes):
    for name, table, method, expression in indexes:
        cursor.execute(
            "SELECT index.indisvalid FROM pg_index index "
            "WHERE index.indexrelid = to_regclass(%s)", [f"public.{name}"])
        existing = cursor.fetchone()
        if existing is not None and not existing[0]:
            cursor.execute(f'DROP INDEX CONCURRENTLY public."{name}"')
        cursor.execute(
            f'CREATE INDEX CONCURRENTLY IF NOT EXISTS "{name}" '
            f'ON public."{table}" USING {method} ({expression})')


def _drop_indexes(cursor, indexes):
    for name, table, method, expression in indexes:
        cursor.execute(f'DROP INDEX CONCURRENTLY IF EXISTS public."{name}"')


def add_columns(apps, schema_editor):
    if not _applies(schema_editor):
        return
    with schema_editor.connection.cursor() as cursor:
        for table, columns in COLUMNS.items():
            additions = ", ".join(
                f'ADD COLUMN IF NOT EXISTS "{name}" tsvector '
                f"GENERATED ALWAYS AS ({expression}) STORED"
                for name, expression in columns)
            cursor.execute(f'ALTER TABLE public."{table}" {additions}')
        _create_indexes(cursor, COLUMN_INDEXES)
        _drop_indexes(cursor, EXPRESSION_INDEXES)


def drop_columns(apps, schema_editor):
    if not _applies(schema_editor):
        return
    with schema_editor.connection.cursor() as cursor:
        _create_indexes(cursor, EXPRESSION_INDEXES)
        _drop_indexes(cursor, COLUMN_INDEXES)
        for table, columns in COLUMNS.items():
            drops = ", ".join(
                f'DROP COLUMN IF EXISTS "{name}"' for name, _ in columns)
            cursor.execute(f'ALTER TABLE public."{table}" {drops}')


class Migration(migrations.Migration):
    atomic = False
    dependencies = [("pathways", "0028_postgres_search_indexes")]
    operations = [migrations.RunPython(
        add_columns, drop_columns, atomic=False,
        hints={"model_name": "course"})]
