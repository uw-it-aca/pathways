# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.apps import AppConfig
from django.contrib.staticfiles.apps import StaticFilesConfig


class ViteStaticFilesConfig(StaticFilesConfig):
    ignore_patterns = ['CVS', '*~']

class PathwaysConfig(AppConfig):
    name = 'pathways'
