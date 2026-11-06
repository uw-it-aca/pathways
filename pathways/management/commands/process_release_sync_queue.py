from django.core.management.base import BaseCommand, CommandError

from pathways.release_sync_queue import process_release_sync_queue


class Command(BaseCommand):
    help = "Process a bounded batch of authorized release requests; safe for daemon polling."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=1)
        parser.add_argument("--temporary-root")

    def handle(self, *args, **options):
        try:
            attempts = process_release_sync_queue(
                limit=options["limit"], temporary_root=options["temporary_root"])
        except ValueError as exc:
            raise CommandError(str(exc)) from exc
        for attempt in attempts:
            self.stdout.write(f"Attempt {attempt.pk}: {attempt.status}.")
