# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from django.test import TestCase
from pathways.templatetags.vite import vite_styles, vite_scripts
from pathways.templatetags.hashing_tag import hash_netid


class ViteTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_vite_styles(self):
        entries = ("pathways_vue/main.js",)
        link = vite_styles(*entries)
        pattern = re.compile(r'<link\s+[^>]*href="[^"]*main-[^"]*"[^>]*>')
        self.assertTrue(pattern.search(link))

    def test_vite_scripts(self):
        entries = ("pathways_vue/main.js",)
        script = vite_scripts(*entries)
        pattern = re.compile(
            r'<script\s+[^>]*src="[^"]*main-[^"]*"[^>]*></script>'
        )
        self.assertTrue(pattern.search(script))


class HashTestClass(TestCase):
    def test_hash_netid(self):
        self.assertEqual(hash_netid(None), '')
        self.assertEqual(hash_netid('javerage'),
                         'c13c917a1822a8acd58c48d2c8c6880a')
