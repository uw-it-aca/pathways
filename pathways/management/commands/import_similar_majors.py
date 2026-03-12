# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import csv
from pathways.data_import import import_similar_majors, \
    import_stem_from_similar_majors
from pathways.dao.azure_storage import AzureStorageDAO
from logging import getLogger
from io import StringIO

logger = getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        azure_client = AzureStorageDAO()
        similar_major_string = azure_client.get_most_recent_blob()

        f = StringIO(similar_major_string)
        csv_data = csv.reader(f)
        # skip headers
        next(csv_data)
        similar_major_data = []
        for line in csv_data:
            similar_major_data.append(line)
        import_similar_majors(similar_major_data)
        import_stem_from_similar_majors(similar_major_data)
