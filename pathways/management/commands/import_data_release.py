# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError

from pathways.release_import import import_release


class Command(BaseCommand):
    help = (
        "Replace database data from a verified local schema-1.1 release. "
        "Does not activate its index. Stop serving traffic before use."
    )

    def add_arguments(self, parser):
        parser.add_argument("--release-dir", required=True)
        parser.add_argument("--release-id", required=True)
        parser.add_argument("--confirm-replace-data", action="store_true")

    def handle(self, *args, **options):
        if not options["confirm_replace_data"]:
            raise CommandError(
                "This replaces catalog data without switching the serving index. "
                "Use only on an isolated database or with traffic stopped. "
                "Pass --confirm-replace-data to proceed.")
        try:
            changed = import_release(
                options["release_dir"], release_id=options["release_id"])
        except (ValueError, KeyError, TypeError, IndexError, OSError,
                DatabaseError) as exc:
            raise CommandError(f"Release import failed; database changes rolled back: {exc}") from exc
        self.stdout.write(self.style.SUCCESS(
            f"{'Imported' if changed else 'Already imported'} release "
            f"{options['release_id']}. Active search index unchanged; "
            "do not resume traffic until a coordinated activation is completed."))
