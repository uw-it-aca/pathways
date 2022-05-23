# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class DataImport(models.Model):
    type = models.CharField(max_length=10, unique=True)
    hash = models.CharField(max_length=32)
    imported_on = models.DateTimeField(auto_now=True)

    @staticmethod
    def needs_import(type, hash):
        imp = DataImport.objects.filter(type=type,
                                        hash=hash).count()
        return imp == 0
