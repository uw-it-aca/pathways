# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError

from pathways.release_import import import_release


class Command(BaseCommand):
    help = (
        "Transactionally replace catalog data from a verified "
        "local schema-1.1 or schema-2.0 release. PostgreSQL "
        "search uses the imported data directly."
    )

    def add_arguments(self, parser):
        parser.add_argument("--release-dir", required=True)
        parser.add_argument("--release-id", required=True)
        parser.add_argument("--confirm-replace-data",
                            action="store_true")

    def handle(self, *args, **options):
        if not options["confirm_replace_data"]:
            msg = (
                "This transactionally replaces catalog data and "
                "relationships. "
                "Use an isolated database or an "
                "operator-controlled maintenance window. "
                "Pass --confirm-replace-data to proceed.")
            raise CommandError(msg)
        try:
            changed = import_release(
                options["release_dir"],
                release_id=options["release_id"])
        except (ValueError, KeyError, TypeError, IndexError, OSError,
                DatabaseError) as exc:
            msg = (f"Release import failed; database changes "
                   f"rolled back: {exc}")
            raise CommandError(msg) from exc
        status = 'Imported' if changed else 'Already imported'
        self.stdout.write(self.style.SUCCESS(
            f"{status} release {options['release_id']}. "
            "PostgreSQL search queries the committed catalog; "
            "no index activation is needed."))
