from django.core.management.base import BaseCommand, CommandError

from pathways.release_sync_queue import enqueue_release_sync


class Command(BaseCommand):
    help = "Queue one explicit release from the configured trusted GCS source."

    def add_arguments(self, parser):
        parser.add_argument("--release-id", required=True)
        parser.add_argument("--requested-by", default="")
        parser.add_argument("--confirm-replace-data", action="store_true")

    def handle(self, *args, **options):
        if not options["confirm_replace_data"]:
            raise CommandError("Pass --confirm-replace-data to authorize catalog replacement.")
        try:
            attempt, created = enqueue_release_sync(
                options["release_id"], requested_by=options["requested_by"])
        except ValueError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(
            f"{'Queued' if created else 'Already queued'} release {attempt.release_id}. "
            f"Attempt {attempt.pk}.")