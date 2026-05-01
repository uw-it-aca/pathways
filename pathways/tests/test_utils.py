# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from pathways.utils import hash_netid


class UtilsTestClass(TestCase):
    def test_hash_netid(self):
        self.assertEqual(hash_netid(None), '')
        self.assertEqual(hash_netid('javerage'),
                         'c13c917a1822a8acd58c48d2c8c6880a')
