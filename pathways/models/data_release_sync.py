import uuid
from typing import ClassVar

from django.db import models


class DataReleaseSyncAttempt(models.Model):
    class Status(models.TextChoices):
        DOWNLOADING = "downloading"
        IMPORTING = "importing"
        SUCCEEDED = "succeeded"
        UNCHANGED = "unchanged"
        FAILED = "failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    release_id = models.CharField(max_length=128)
    bucket = models.CharField(max_length=222)
    prefix = models.CharField(max_length=512, blank=True)
    requested_by = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices)
    started_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    error_code = models.CharField(max_length=128, blank=True)
    error_message = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-started_on"]


class DataReleaseState(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    current_release = models.ForeignKey(
        "DataReleaseImport", on_delete=models.PROTECT)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints: ClassVar[list[models.CheckConstraint]] = [models.CheckConstraint(
            condition=models.Q(id=1), name="data_release_state_singleton")]