# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from django.test import TestCase
from pathways.templatetags.vite import vite_styles, vite_scripts
from pathways.templatetags.hashing_tag import hash_netid


class ViteTestClass(TestCase):
    def test_vite_styles(self):
        entries = ("pathways_vue/main.js",)
        link = vite_styles(*entries)
        pattern = re.compile(
            '<link rel="[\\w]*" href="[\\w\\D]*main.[\\d\\w]*.css" />'
        )
        self.assertTrue(pattern.match(link))

    def test_vite_scripts(self):
        entries = ("pathways_vue/main.js",)
        script = vite_scripts(*entries)
        pattern = re.compile(
            '<script type="[\\w]*" src="[\\w\\D]*main.[\\d\\w]*.js"></script>'
        )
        self.assertTrue(pattern.match(script))

    def test_manifest_names(self):
        entries = ("pathways_vue/main.js", "pathways_vue/main.js")
        try:
            vite_scripts(*entries)
        except Exception:
            self.fail("Didn't ignore duplicate entry")


class HashTestClass(TestCase):
    def test_hash_netid(self):
        self.assertEqual(hash_netid(None), '')
        self.assertEqual(hash_netid('javerage'),
                         'c13c917a1822a8acd58c48d2c8c6880a')
