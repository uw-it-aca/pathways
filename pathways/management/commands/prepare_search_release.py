# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from dawgpath_search import IndexValidationError
from django.core.management.base import BaseCommand, CommandError

from pathways.search_release import prepare_release


class Command(BaseCommand):
    help = (
        "Verify a trusted downloaded release and prepare a fresh search index. "
        "Does not download, import database data, or activate the index."
    )

    def add_arguments(self, parser):
        parser.add_argument("--release-dir", required=True)
        parser.add_argument("--output-dir", required=True)
        parser.add_argument("--release-id", required=True)

    def handle(self, *args, **options):
        try:
            manifest = prepare_release(
                options["release_dir"], options["output_dir"],
                release_id=options["release_id"])
        except (IndexValidationError, OSError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f"Prepared verified index for {manifest['release_id']}: "
            f"{manifest['search_index']['counts']}. "
            "No database data or active search index was changed."))
