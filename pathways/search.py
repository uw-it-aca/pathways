# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from logging import getLogger
from whoosh.index import open_dir
from whoosh import qparser
from whoosh.query import *
from urllib.parse import urlencode
from pathways.models.course import Course
from pathways.models.major import Major
import re


logger = getLogger(__name__)


def search(search_string, campus_values=None, types=None, is_bottleneck=None,
           is_gateway=None, min_coi_score=None, max_coi_score=None):
    course_results = \
        course_id_direct_match(search_string.upper(),
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
            "abbr": result["major_abbr"],
            "title": result["major_title"],
            "description": result["description"],
            "score": result.score,
            "campus": result["campus"],
            "is_major": True,
            "url": "/major?" + url}


def _get_course_dict(result):
    url = urlencode({"id": result["course_id"]})
    return {"id": result["course_id"],
            "title": result["course_title"],
            "description": result.get("description"),
            "score": result.score,
            "campus": result["campus"],
            "is_course": True,
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


def course_id_direct_match(course_id, campus=None):
    course_match = Course.objects.filter(course_id=format_course_id(course_id))
    if campus:
        course_match = course_match.filter(course_campus=campus)

    response = []
    for course in course_match:
        response.append(course.get_search_results_dict())
    return response


def format_course_id(course_id):
    return re.sub(r"([a-zA-Z]+)(\d+)", r"\1 \2", course_id)


def major_name_direct_match(major_name, campus=None):
    major_match = Major.objects.filter(credential_title__icontains=major_name)
    if campus:
        major_match = major_match.filter(major_campus=campus)

    response = []
    for major in major_match:
        response.append(major.get_search_results_dict())
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
                                  limit=2000)
        phrase_parser = qparser.MultifieldParser(["contents"],
                                                 ix.schema)
        phrase_parser.add_plugin(qparser.SequencePlugin())
        phrase_quyery = phrase_parser.parse("\"%s\"" % search_string)
        phrase_results = searcher.search(phrase_quyery,
                                         limit=2000)
        results.upgrade(phrase_results)
        response = []
        for result in results:
            if 'major_id' in result:
                response.append(_get_major_dict(result))
            else:
                response.append(_get_course_dict(result))
        return response
