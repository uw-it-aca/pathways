# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from google.api_core.exceptions import GoogleAPIError
from google.auth.exceptions import GoogleAuthError

from pathways.release_download import download_release


class Command(BaseCommand):
    help = "Download and verify one explicit GCS release. Does not import or activate."

    def add_arguments(self, parser):
        parser.add_argument("--bucket", required=True)
        parser.add_argument("--release-id", required=True)
        parser.add_argument("--output-dir", required=True)
        parser.add_argument("--prefix", default="")

    def handle(self, *args, **options):
        try:
            manifest = download_release(
                options["bucket"], options["release_id"], options["output_dir"],
                prefix=options["prefix"])
        except (ValueError, OSError,
                GoogleAPIError, GoogleAuthError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f"Downloaded verified release {manifest['release_id']}. "
            "No database or active index was changed."))
