# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
from logging import getLogger
from whoosh.index import open_dir
from whoosh import qparser


logger = getLogger(__name__)


def search_courses(search_string):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        query = qparser.QueryParser("contents",
                                    ix.schema,
                                    group=qparser.OrGroup).parse(search_string)
        results = searcher.search(query)
        response = []
        for result in results:
            response.append({"id": result["course_id"],
                             "contents": result["contents"],
                             "score": result.score})
        return response
