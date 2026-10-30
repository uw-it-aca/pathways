# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from urllib.parse import urlencode

from django.db import connection

CONFIG = "public.pathways_english"
SEARCH_INDEXES = (
    "pathways_search_course_text", "pathways_search_major_text",
    "pathways_search_course_title", "pathways_search_major_title",
    "pathways_search_course_id", "pathways_search_major_abbr",
)
COURSE_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_id, '') || ' ' || coalesce(course_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_description, '')), 'B')"
)
COURSE_TOPIC_DESCRIPTION = (
    "regexp_replace(coalesce(course_description, ''), "
    "'\\m(Prerequisites?|Offered)[[:space:]]*:[\\s\\S]*$', '', 'i')"
)
COURSE_TOPIC_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(course_id, '') || ' ' || coalesce(course_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    f"{COURSE_TOPIC_DESCRIPTION}), 'B')"
)
COURSE_RANK_TEXT = (
    f"({COURSE_TOPIC_TEXT}) || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "substr(coalesce(course_description, ''), "
    f"length({COURSE_TOPIC_DESCRIPTION}) + 1)), 'D')"
)
MAJOR_TEXT = (
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(major_abbr, '') || ' ' || "
    "coalesce(credential_title, '')), 'A') || "
    "setweight(to_tsvector('public.pathways_english'::regconfig, "
    "coalesce(credential_description, '')), 'B')"
)


def _rows(kind, query, campuses, is_bottleneck, is_gateway, minimum, maximum,
          introductory=False):
    course = kind == "course"
    table = "pathways_course" if course else "pathways_major"
    identifier = "course_id" if course else "credential_code"
    title = "course_title" if course else "credential_title"
    description = "course_description" if course else "credential_description"
    campus = "course_campus" if course else "major_campus"
    abbreviation = "course_id" if course else "major_abbr"
    vector = COURSE_TEXT if course else MAJOR_TEXT
    ranking_vector = COURSE_RANK_TEXT if course else MAJOR_TEXT
    title_vector = (
        f"to_tsvector('{CONFIG}'::regconfig, coalesce({title}, ''))")
    normalized_id = (
        f"regexp_replace(lower({abbreviation}), '\\s+', '', 'g')")
    conditions = []
    parameters = [introductory, query, " OR ".join(re.findall(r"\w+", query)),
                  query, query, re.sub(r"\s+", "", query.lower())]
    filter_parameters = []
    if campuses:
        conditions.append(f"lower({campus}) = ANY(%s)")
        filter_parameters.append([value.lower() for value in campuses])
    if (is_bottleneck or is_gateway
            or minimum is not None or maximum is not None):
        if not course:
            return []
        if is_bottleneck:
            conditions.append("is_bottleneck")
        if is_gateway:
            conditions.append("is_gateway")
        if minimum is not None:
            conditions.append("coi_score >= %s")
            filter_parameters.append(float(minimum))
        if maximum is not None:
            conditions.append("coi_score <= %s")
            filter_parameters.append(float(maximum))
    filters = " AND ".join(conditions) or "TRUE"
    parameters.extend(filter_parameters + filter_parameters)
    conditions.append(
        f"(({vector}) @@ terms OR {normalized_id} LIKE escaped_id || '%%' "
        f"OR (NOT EXISTS (SELECT 1 FROM {table} "
        f"WHERE ({filters}) AND (({vector}) @@ terms "
        f"OR {normalized_id} LIKE escaped_id || '%%')) "
        f"AND (lower({title}) %% raw_query OR raw_query <%% lower({title}))))")
    sql = f"""
        WITH input AS (
                 SELECT %s::boolean AS introductory,
                     lower(unaccent(%s)) AS raw_query,
                   websearch_to_tsquery('{CONFIG}'::regconfig, %s) AS terms,
                   plainto_tsquery('{CONFIG}'::regconfig, %s) AS all_terms,
                   phraseto_tsquery('{CONFIG}'::regconfig, %s) AS phrase,
                   %s AS compact_id
        ), query AS NOT MATERIALIZED (
            SELECT *, replace(replace(replace(compact_id, '\\', '\\\\'),
                      '%%', '\\%%'), '_', '\\_') AS escaped_id FROM input
        ), candidates AS MATERIALIZED (
            SELECT {identifier} AS result_id, {title} AS result_title,
                   {description} AS result_description,
                   {campus} AS result_campus, {abbreviation} AS result_abbr,
                   ({normalized_id} = compact_id) AS exact_id,
                   ({title_vector}) AS title_document,
                   ({ranking_vector}) AS document
            FROM {table} CROSS JOIN query
            WHERE {' AND '.join(conditions)}
        )
        SELECT result_id, result_title, result_description, result_campus,
               result_abbr, exact_id,
               (title_document @@ all_terms) AS title_match,
               CASE WHEN exact_id THEN 100.0 ELSE 0 END
                   + CASE WHEN introductory AND title_document @@ all_terms
                       AND (lower(result_title) ~
                            '(introduction|introductory|beginning|fundamentals|basic)'
                            OR lower(coalesce(result_description, '')) ~
                            '(no prior|without prior|no previous)')
                       THEN 30.0 ELSE 0 END
                   + CASE WHEN title_document @@ phrase THEN 50.0 ELSE 0 END
                   + CASE WHEN title_document @@ all_terms THEN 20.0 ELSE 0 END
                   + CASE WHEN ts_filter(document, '{{A,B}}'::"char"[])
                       @@ phrase THEN 5.0 ELSE 0 END
                   + CASE WHEN ts_filter(document, '{{A,B}}'::"char"[])
                       @@ all_terms THEN 3.0 ELSE 0 END
                   + ts_rank_cd(document, terms, 32)
                   + word_similarity(raw_query, lower(result_title)) AS score
        FROM candidates CROSS JOIN query
        ORDER BY exact_id DESC, score DESC, result_id, result_campus
        LIMIT 2000
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, parameters)
        results = []
        for row in cursor.fetchall():
            (identifier_value, title_value, description_value, campus_value,
             abbr, exact, title_match, score) = row
            result = {
                "id": identifier_value, "title": title_value,
                "description": description_value, "campus": campus_value,
                "score": float(score), f"is_{kind}": True,
                "url": f"/{kind}?" + urlencode({"id": identifier_value}),
            }
            if not course:
                result["abbr"] = abbr
            results.append((result, exact, title_match))
        return results


def search(search_string, campus_values=None, types=None, is_bottleneck=None,
           is_gateway=None, min_coi_score=None, max_coi_score=None):
    response = {"course_matches": [], "major_matches": [], "text_matches": []}
    query = (search_string or "").strip()
    if not query or not re.search(r"\w", query):
        return response
    introductory = bool(re.match(r"^learn\s+\S", query, flags=re.IGNORECASE))
    matching_query = (
        re.sub(r"^learn\s+", "", query, flags=re.IGNORECASE)
        if introductory else query)
    text_results = []
    for kind in ("course", "major"):
        if types and kind not in types:
            continue
        rows = _rows(kind, matching_query, campus_values, is_bottleneck,
                     is_gateway, min_coi_score, max_coi_score, introductory)
        for result, exact, title_match in rows:
            if kind == "course" and exact:
                response["course_matches"].append(result)
            if kind == "major" and title_match:
                response["major_matches"].append(result)
            text_results.append(result)
    response["major_matches"] = (
        [] if response["course_matches"] else response["major_matches"][:200])
    response["text_matches"] = sorted(
        text_results, key=lambda result: (
            -result["score"], result["id"], result["campus"]))[:2000]
    return response
