# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch, MagicMock
from pathways.models.major import Major, SimilarMajor


class ImportSimilarMajorsTest(TestCase):
    def setUp(self):
        Major.objects.create(
            major_abbr="INFO",
            credential_code="0-INFO-10",
            is_stem=False
        )
        Major.objects.create(
            major_abbr="CSE",
            credential_code="0-CSE-10",
            is_stem=False
        )

    @patch('pathways.management.commands.import_similar_majors.AzureStorageDAO')
    def test_import_similar_majors(self, mock_azure):
        # Mock the CSV data returned from Azure
        # Format based on code:
        # Source Cred Code, Source Stem, Sim Cred Code, Sim Stem, Score, Desc
        csv_content = (
            "source_cred,source_stem,sim_cred,sim_stem,score,desc\n"
            "0-INFO-10,0,0-CSE-10,1,0.8,High\n"
        )

        mock_client = MagicMock()
        mock_azure.return_value = mock_client
        mock_client.get_most_recent_blob.return_value = csv_content

        call_command('import_similar_majors')

        # Check SimilarMajor created
        self.assertEqual(SimilarMajor.objects.count(), 1)
        sim_major = SimilarMajor.objects.first()
        self.assertEqual(sim_major.source_major.major_abbr, "INFO")
        self.assertEqual(sim_major.similar_major.major_abbr, "CSE")
        self.assertEqual(sim_major.similarity_score, 0.8)
        self.assertEqual(sim_major.similarity_description, "H")

        # Check STEM update
        cse = Major.objects.get(major_abbr="CSE")
        self.assertTrue(cse.is_stem)
        info = Major.objects.get(major_abbr="INFO")
        self.assertFalse(info.is_stem)
