# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
from io import StringIO
from logging import getLogger

from django.core.management.base import BaseCommand

from pathways.dao.azure_storage import AzureStorageDAO
from pathways.data_import import (
    import_similar_majors,
    import_stem_from_similar_majors,
)

logger = getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        azure_client = AzureStorageDAO()
        similar_major_string = azure_client.get_most_recent_blob()

        f = StringIO(similar_major_string)
        csv_data = csv.reader(f)
        # skip headers
        next(csv_data)
        similar_major_data = list(csv_data)
        import_similar_majors(similar_major_data)
        import_stem_from_similar_majors(similar_major_data)
