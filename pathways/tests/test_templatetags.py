# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from django.test import TestCase
from pathways.templatetags.vite import vite_styles, vite_scripts


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
