import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("pathways", "0030_datareleaseimport")]

    operations = [
        migrations.CreateModel(
            name="DataReleaseSyncAttempt",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False,
                                        primary_key=True, serialize=False)),
                ("release_id", models.CharField(max_length=128)),
                ("bucket", models.CharField(max_length=222)),
                ("prefix", models.CharField(blank=True, max_length=512)),
                ("requested_by", models.CharField(blank=True, max_length=150)),
                ("status", models.CharField(max_length=16, choices=[
                    ("downloading", "Downloading"), ("importing", "Importing"),
                    ("succeeded", "Succeeded"), ("unchanged", "Unchanged"),
                    ("failed", "Failed")])),
                ("started_on", models.DateTimeField(auto_now_add=True)),
                ("completed_on", models.DateTimeField(blank=True, null=True)),
                ("error_code", models.CharField(blank=True, max_length=128)),
                ("error_message", models.CharField(blank=True, max_length=255)),
            ],
            options={"ordering": ["-started_on"]},
        ),
        migrations.CreateModel(
            name="DataReleaseState",
            fields=[
                ("id", models.PositiveSmallIntegerField(default=1, editable=False,
                                                       primary_key=True, serialize=False)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("current_release", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to="pathways.datareleaseimport")),
            ],
            options={"constraints": [models.CheckConstraint(
                condition=models.Q(id=1), name="data_release_state_singleton")]},
        ),
    ]
