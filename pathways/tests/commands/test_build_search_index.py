# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from django.core.management import call_command
from whoosh.index import open_dir
from whoosh import qparser
from pathways.search import _get_course_dict
from pathways.tests import SearchIndexTest
from unittest.mock import patch


class BuildSearchIndexTest(SearchIndexTest):
    @patch('pathways.management.commands.build_search_index.INDEXDIR',
           SearchIndexTest.TEST_INDEX_DIR)
    def test_build_search_index(self):
        call_command('build_search_index')
        self.assertEqual(len(os.listdir(self.TEST_INDEX_DIR)), 3)

        ix = open_dir(self.TEST_INDEX_DIR)
        with ix.searcher() as searcher:
            parser = qparser.QueryParser('course_id', ix.schema)
            course_query = parser.parse("INFO 201")
            results = searcher.search(course_query)
            response = []
            for result in results:
                response.append(_get_course_dict(result))
            self.assertEqual(len(response), 1)
            self.assertEqual(response[0]['id'], 'INFO 201')
