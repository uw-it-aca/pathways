# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from logging import getLogger
from whoosh.index import open_dir
from whoosh import qparser
from whoosh.query import *
from urllib.parse import urlencode


logger = getLogger(__name__)


def search(search_string, campus_values=None, types=None, is_bottleneck=None,
                   is_gateway=None, min_coi_score=None, max_coi_score=None):
    course_results = course_id_search(search_string,
                                      campus_values) if "course" in types or \
                                                        not types else []
    major_results = major_title_search(search_string,
                                       campus_values) if "major" in types or \
                                                         not types else []

    text_results = text_search(search_string, campus_values, types,
                               is_bottleneck, is_gateway, min_coi_score,
                               max_coi_score)

    return {"course_matches": course_results,
            "major_matches": major_results,
            "text_matches": text_results}


def _get_major_dict(result):
    url = urlencode({"id": result["major_id"]})
    return {"id": result["major_id"],
            "contents": result["contents"],
            "abbr": result["major_abbr"],
            "score": result.score,
            "campus": result["campus"],
            "url": "/major?" + url}


def _get_course_dict(result):
    url = urlencode({"id": result["course_id"]})
    return {"id": result["course_id"],
            "contents": result["contents"],
            "score": result.score,
            "campus": result["campus"],
            "url": "/course?" + url}


def _get_campus_filters(campus_values):
    campus_filter = []
    if campus_values:
        campus_queries = [Term('campus', campus) for campus in campus_values]
        campus_filter = Or(campus_queries)
    return campus_filter


def _get_type_filters(types):
    type_filter = []
    if types:
        type_queries = [Term('type', type) for type in types]
        type_filter = Or(type_queries)
    return type_filter


def major_title_search(major_title, campus=None):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        parser = qparser.QueryParser('major_title', ix.schema)
        campus_query = _get_campus_filters(campus)
        major_query = parser.parse(major_title)
        results = searcher.search(major_query, filter=campus_query, limit=200)
        response = []
        for result in results:
            response.append(_get_major_dict(result))
        return response


def course_id_search(course_id, campus=None):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        parser = qparser.QueryParser('course_id', ix.schema)
        campus_query = _get_campus_filters(campus)
        course_query = parser.parse(course_id)
        results = searcher.search(course_query, filter=campus_query, limit=200)
        response = []
        for result in results:
            response.append(_get_course_dict(result))
        return response


def text_search(search_string, campus_values=None, types=None,
                is_bottleneck=None, is_gateway=None, min_coi_score=None,
                max_coi_score=None):
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
        if campus_values is not None:
            filter_queries += _get_campus_filters(campus_values)
        if types is not None:
            filter_queries += _get_type_filters(types)
        parser = qparser.MultifieldParser(["contents"],
                                          ix.schema,
                                          group=qparser.OrGroup)
        query = parser.parse(search_string)

        results = searcher.search(query,
                                  filter=And(filter_queries),
                                  limit=200)
        response = []
        for result in results:
            try:
                response.append(_get_course_dict(result))
            except KeyError:
                response.append(_get_major_dict(result))
        return response
