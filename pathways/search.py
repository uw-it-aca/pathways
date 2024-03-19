# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from logging import getLogger
from whoosh.index import open_dir
from whoosh import qparser
from whoosh.query import *


logger = getLogger(__name__)


def search_courses(search_string, campus=None, is_bottleneck=None,
                   is_gateway=None, min_coi_score=None, max_coi_score=None):
    if len(campus) == 0:
        campus = None
    course_results = course_id_search(search_string, campus)
    major_results = major_title_search(search_string, campus)
    text_results = text_search(search_string, campus, is_bottleneck,
                               is_gateway, min_coi_score, max_coi_score)

    return {"course_matches": course_results,
            "major_matches": major_results,
            "text_matches": text_results}


def major_title_search(major_title, campus=None):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        parser = qparser.QueryParser('major_title', ix.schema)
        campus_query = Term('campus', campus) if campus else None
        major_query = parser.parse(major_title)
        results = searcher.search(major_query, filter=campus_query)
        response = []
        for result in results:
            response.append({"id": result["major_id"],
                             "contents": result["contents"],
                             "score": result.score})
        return response


def course_id_search(course_id, campus=None):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        parser = qparser.QueryParser('course_id', ix.schema)
        campus_query = Term('campus', campus) if campus else None
        course_query = parser.parse(course_id)
        results = searcher.search(course_query, filter=campus_query)
        response = []
        for result in results:
            response.append({"id": result["course_id"],
                             "contents": result["contents"],
                             "score": result.score})
        return response


def text_search(search_string, campus=None, is_bottleneck=None,
                is_gateway=None, min_coi_score=None, max_coi_score=None):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        filter_queries = []
        if is_bottleneck:
            filter_queries.append(Term('is_bottleneck', is_bottleneck))
        if is_gateway:
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
        if campus is not None:
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
