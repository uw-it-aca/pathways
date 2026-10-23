# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class DataReleaseImport(models.Model):
    """Successful database imports, not serving-index activation records."""

    release_id = models.CharField(max_length=128, primary_key=True)
    manifest_sha256 = models.CharField(max_length=64)
    imported_on = models.DateTimeField(auto_now=True)
