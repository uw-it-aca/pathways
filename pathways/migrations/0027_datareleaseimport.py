# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("pathways", "0026_major_program_verind_id")]

    operations = [
        migrations.CreateModel(
            name="DataReleaseImport",
            fields=[
                ("release_id", models.CharField(
                    max_length=128, primary_key=True, serialize=False)),
                ("manifest_sha256", models.CharField(max_length=64)),
                ("imported_on", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
