from pathways import postgres_search


def search(search_string, campus_values=None, types=None, is_bottleneck=None,
           is_gateway=None, min_coi_score=None, max_coi_score=None):
    return postgres_search.search(
        search_string, campus_values, types, is_bottleneck, is_gateway,
        min_coi_score, max_coi_score)
