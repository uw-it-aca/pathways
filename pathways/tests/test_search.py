# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from pkg_resources import resource_listdir

from pathways.search import (format_course_id,
                             _get_major_dict,
                             _get_course_dict,
                             _get_campus_filters,
                             _get_type_filters,
                             course_id_search,
                             course_id_direct_match,
                             major_name_direct_match,
                             text_search, major_title_search
                             )
from pathways.tests import SearchIndexTest
from unittest.mock import patch
from whoosh.index import open_dir
from whoosh import qparser
from whoosh.query import Term
from django.core.management import call_command


class TestSearch(SearchIndexTest):
    @patch('pathways.management.commands.build_search_index.INDEXDIR',
           SearchIndexTest.TEST_INDEX_DIR)
    def setUp(self):
        super().setUp()
        call_command('build_search_index')

    def test_format_course_id(self):
        self.assertEqual(format_course_id("TRAIN 1"),
                         "TRAIN 1")
        self.assertEqual(format_course_id("B TRAIN 1"),
                         "B TRAIN 1")
        self.assertEqual(format_course_id("TRAIN1"),
                         "TRAIN 1")
        self.assertEqual(format_course_id("B TRAIN1"),
                         "B TRAIN 1")

    def test_major_dict(self):
        ix = open_dir(self.TEST_INDEX_DIR)
        with ix.searcher() as searcher:
            parser = qparser.QueryParser('major_title', ix.schema)
            major_query = parser.parse("Informatics")
            results = searcher.search(major_query)
            response = []
            for result in results:
                response.append(_get_major_dict(result))
            self.assertEqual(len(response), 1)
            self.assertEqual(response[0]['id'], 'INFO-40-1-6')

    def test_course_dict(self):
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

    def test_campus_filters(self):
        filters = _get_campus_filters(['seattle', 'bothell'])
        self.assertEqual(len(filters), 2)
        self.assertEqual(filters[0], Term('campus', 'seattle'))
        self.assertEqual(filters[1], Term('campus', 'bothell'))

    def test_get_type_filters(self):
        filters = _get_type_filters(['course', 'major'])
        self.assertEqual(len(filters), 2)
        self.assertEqual(filters[0], Term('type', 'course'))
        self.assertEqual(filters[1], Term('type', 'major'))

    @patch('pathways.search.SEARCH_INDEX_DIR', SearchIndexTest.TEST_INDEX_DIR)
    def test_major_title_search(self):
        results = major_title_search("Informatics")
        self.assertEqual(len(results), 1)

    @patch('pathways.search.SEARCH_INDEX_DIR', SearchIndexTest.TEST_INDEX_DIR)
    def test_course_id_search(self):
        results = course_id_search("INFO 201")
        self.assertEqual(len(results), 1)

    def test_course_id_direct(self):
        results = course_id_direct_match("INFO 201")
        self.assertEqual(len(results), 1)

        bot_results = course_id_direct_match("INFO 201", "bothell")
        self.assertEqual(len(bot_results), 0)

    def test_major_name_direct(self):
        results = major_name_direct_match("Informatics")
        self.assertEqual(len(results), 1)

        bot_results = major_name_direct_match("Informatics", "bothell")
        self.assertEqual(len(bot_results), 0)

    @patch('pathways.search.SEARCH_INDEX_DIR', SearchIndexTest.TEST_INDEX_DIR)
    def test_text_search(self):
        results = text_search("INFO 201")
        self.assertEqual(len(results), 3)

        results = text_search("Informatics")
        self.assertEqual(len(results), 1)

        results = text_search("INFO 201", "bothell")
        self.assertEqual(len(results), 0)

        results = text_search("info", is_bottleneck=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 'INFO 301')

        results = text_search("info", is_gateway=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 'INFO 201')

        results = text_search("info",
                              max_coi_score=1,
                              min_coi_score=0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 'INFO 201')
