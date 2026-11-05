from django.core.management.base import BaseCommand, CommandError

from pathways.release_sync import ReleaseSyncError, sync_release


class Command(BaseCommand):
    help = "Download, verify and transactionally import one explicit GCS release."

    def add_arguments(self, parser):
        parser.add_argument("--bucket", required=True)
        parser.add_argument("--release-id", required=True)
        parser.add_argument("--prefix", default="")
        parser.add_argument("--requested-by", default="")
        parser.add_argument("--temporary-root")
        parser.add_argument("--confirm-replace-data", action="store_true")

    def handle(self, *args, **options):
        if not options["confirm_replace_data"]:
            raise CommandError(
                "Use an isolated database or an operator-controlled maintenance window. "
                "Pass --confirm-replace-data to replace catalog data and relationships.")
        try:
            attempt = sync_release(
                options["bucket"], options["release_id"], prefix=options["prefix"],
                requested_by=options["requested_by"],
                temporary_root=options["temporary_root"])
        except (ReleaseSyncError, ValueError) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f"Release {attempt.release_id}: {attempt.status}. Attempt {attempt.pk}."))