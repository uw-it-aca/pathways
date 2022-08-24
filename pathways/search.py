# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from logging import getLogger
from whoosh.index import open_dir
from whoosh import qparser
from whoosh.query import *


logger = getLogger(__name__)


def search_courses(search_string, campus, is_bottleneck=None, is_gateway=None,
                   min_coi_score=None, max_coi_score=None):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        # test if matches a single course ID first, only return that if match
        parser = qparser.QueryParser('course_id', ix.schema)
        query = parser.parse(search_string)
        results = searcher.search(query)
        # If no course_id match, query contents
        if len(results) == 0:
            filter_queries = []
            if is_bottleneck is not None:
                filter_queries.append(Term('is_bottleneck', is_bottleneck))
            if is_gateway is not None:
                filter_queries.append(Term('is_gateway', is_gateway))

            if min_coi_score is not None or max_coi_score is not None:
                min_coi = 0
                max_coi = 5
                if min_coi_score is not None:
                    min_coi = min_coi_score
                if max_coi_score is not None:
                    max_coi = max_coi_score
                filter_queries.append(NumericRange('coi_score',
                                                   min_coi,
                                                   max_coi))

            filter_queries.append(Term('campus', campus))
            parser = qparser.MultifieldParser(["contents"],
                                              ix.schema,
                                              group=qparser.OrGroup)
            query = parser.parse(search_string)

            results = searcher.search(query,
                                      filter=And(filter_queries),
                                      limit=20)
        response = []
        for result in results:
            response.append({"id": result["course_id"],
                             "contents": result["contents"],
                             "score": result.score})
        return response
