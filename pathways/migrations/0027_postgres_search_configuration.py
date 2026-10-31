# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations


def prepare_configuration(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    if schema_editor.connection.vendor != "postgresql":
        raise RuntimeError("Pathways search migrations require PostgreSQL.")
    schema_editor.execute(
        "CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public")
    schema_editor.execute(
        "CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public")
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_ts_config config JOIN pg_namespace namespace "
            "ON namespace.oid = config.cfgnamespace "
            "WHERE namespace.nspname = 'public' "
            "AND config.cfgname = 'pathways_english'")
        if cursor.fetchone() is None:
            cursor.execute(
                "CREATE TEXT SEARCH CONFIGURATION public.pathways_english "
                "(COPY = pg_catalog.english)")
            cursor.execute(
                "ALTER TEXT SEARCH CONFIGURATION public.pathways_english "
                "ALTER MAPPING FOR hword, hword_part, word "
                "WITH public.unaccent, pg_catalog.english_stem")


class Migration(migrations.Migration):
    dependencies = [("pathways", "0026_major_program_verind_id")]
    operations = [migrations.RunPython(
        prepare_configuration, migrations.RunPython.noop,
        hints={"model_name": "course"})]
