import json

from django.core.management.base import BaseCommand, CommandError
from django.core.serializers.json import DjangoJSONEncoder

from pathways.models import DataReleaseState, DataReleaseSyncAttempt


class Command(BaseCommand):
    help = "Show the tracked current release and recent sync attempts as JSON."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=10)

    def handle(self, *args, **options):
        limit = options["limit"]
        if not 1 <= limit <= 100:
            raise CommandError("Limit must be between 1 and 100.")
        state = DataReleaseState.objects.select_related("current_release").first()
        current = None
        if state:
            current = {
                "release_id": state.current_release_id,
                "manifest_sha256": state.current_release.manifest_sha256,
                "imported_on": state.current_release.imported_on,
                "updated_on": state.updated_on,
            }
        attempts = list(DataReleaseSyncAttempt.objects.values()[:limit])
        self.stdout.write(json.dumps(
            {"current_release": current, "attempts": attempts},
            cls=DjangoJSONEncoder, indent=2))
