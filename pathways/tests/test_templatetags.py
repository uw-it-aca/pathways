# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
import json
from unittest.mock import patch, mock_open
from django.test import TestCase
from pathways.templatetags.vite import vite_styles, vite_scripts


class ViteTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.mock_manifest_data = json.dumps({
            "pathways_vue/main.js": {
                "file": "assets/main-123.js",
                "css": ["assets/main-123.css"]
            }
        })

    def tearDown(self):
        # Clean up run after every test method.
        pass

    @patch("builtins.open", new_callable=mock_open)
    def test_vite_styles(self, mock_file):
        mock_file.return_value.read.return_value = self.mock_manifest_data
        entries = ("pathways_vue/main.js",)
        link = vite_styles(*entries)
        pattern = re.compile(r'<link\s+[^>]*href="[^"]*main-[^"]*"[^>]*>')
        self.assertTrue(pattern.search(link))

    @patch("builtins.open", new_callable=mock_open)
    def test_vite_scripts(self, mock_file):
        mock_file.return_value.read.return_value = self.mock_manifest_data
        entries = ("pathways_vue/main.js",)
        script = vite_scripts(*entries)
        pattern = re.compile(
            r'<script\s+[^>]*src="[^"]*main-[^"]*"[^>]*></script>'
        )
        self.assertTrue(pattern.search(script))
