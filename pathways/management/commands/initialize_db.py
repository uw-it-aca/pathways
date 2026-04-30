# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import connections
from django.apps import apps
import os


class Command(BaseCommand):

    def create_person_models(self):
        unmanaged_models = [m for m in apps.get_models() if (
            m._meta.app_label == 'uw_person_client' and
            m._meta.managed is False)]

        connection = connections['uw_person']
        existing_tables = connection.introspection.table_names()

        with connection.schema_editor() as schema_editor:
            for model in unmanaged_models:
                if model._meta.db_table not in existing_tables:
                    schema_editor.create_model(model)

    def handle(self, *args, **options):
        if os.getenv('ENV', '') != 'localdev':
            raise CommandError('Localdev only!')

        self.create_person_models()

        # Load uw_person data
        for fixture in [
                'person.json', 'employee.json', 'term.json', 'major.json',
                'student.json', 'adviser.json', 'transfer.json',
                'transcript.json', 'hold.json', 'degree.json', 'sport.json']:
            call_command('loaddata', fixture, '--database', 'uw_person',
                         '--app', 'uw_person_client')
