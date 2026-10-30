# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, connection

from pathways.postgres_search import CONFIG, SEARCH_INDEXES


class Command(BaseCommand):
    help = "Verify the selected search backend after database migrations."

    def handle(self, *args, **options):
        backend = getattr(settings, "PATHWAYS_SEARCH_BACKEND", "whoosh")
        if backend == "whoosh":
            self.stdout.write("Whoosh selected; PostgreSQL checks skipped.")
            return
        if backend != "postgres":
            raise CommandError(f"Unknown search backend: {backend}")
        if connection.vendor != "postgresql" or connection.pg_version < 120000:
            raise CommandError("PostgreSQL search requires PostgreSQL 12+.")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT extname FROM pg_extension extension "
                    "JOIN pg_namespace namespace "
                    "ON namespace.oid = extension.extnamespace "
                    "WHERE namespace.nspname = 'public' "
                    "AND extname IN ('pg_trgm', 'unaccent')")
                if {row[0] for row in cursor.fetchall()} != {
                        "pg_trgm", "unaccent"}:
                    raise CommandError(
                        "Missing public search extensions; run migrations.")
                cursor.execute("SELECT to_tsvector(%s::regconfig, %s)",
                               [CONFIG, "search verification"])
                cursor.execute(
                    "SELECT name.relname FROM pg_index index "
                    "JOIN pg_class name ON name.oid = index.indexrelid "
                    "JOIN pg_namespace namespace "
                    "ON namespace.oid = name.relnamespace "
                    "WHERE namespace.nspname = 'public' "
                    "AND name.relname = ANY(%s) "
                    "AND index.indisvalid AND index.indisready",
                    [list(SEARCH_INDEXES)])
                missing = set(SEARCH_INDEXES) - {
                    row[0] for row in cursor.fetchall()}
                if missing:
                    raise CommandError(
                        "Missing or invalid search indexes: "
                        + ", ".join(sorted(missing)))
        except DatabaseError as error:
            raise CommandError(
                "PostgreSQL search prerequisites are unavailable; "
                "run migrations and check database privileges.") from error
        self.stdout.write(self.style.SUCCESS(
            "PostgreSQL search configuration and indexes are ready."))
