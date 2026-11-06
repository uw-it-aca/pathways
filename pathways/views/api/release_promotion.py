# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Views for data release promotion API endpoints."""

import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from pathways.release_promotion_api import (
    ReleaseLister,
    queue_release_for_promotion,
)
from pathways.views import support_group_required

logger = logging.getLogger(__name__)


@support_group_required(settings.ADMIN_USERS_GROUP)
@require_http_methods(["GET"])
def list_releases(request):
    """
    List all available data releases from GCS.

    Returns JSON with list of available releases.
    """
    try:
        lister = ReleaseLister()
        releases = lister.list_available_releases()
        return JsonResponse({
            "success": True,
            "releases": releases,
            "count": len(releases),
        })
    except ValueError as e:
        logger.error("Error listing releases: %s", e)
        return JsonResponse({
            "error": str(e),
            "error_code": "list_error"
        }, status=500)
    except Exception:
        logger.exception("Unexpected error listing releases")
        return JsonResponse({
            "error": "An unexpected error occurred",
            "error_code": "internal_error"
        }, status=500)


@support_group_required(settings.ADMIN_USERS_GROUP)
@require_http_methods(["GET"])
def get_release_manifest(request, release_id: str):
    """
    Fetch the manifest for a specific release.

    Args:
        release_id: The release ID

    Returns JSON with the release manifest.
    """
    try:
        lister = ReleaseLister()
        manifest = lister.get_release_manifest(release_id)
        return JsonResponse({
            "success": True,
            "release_id": release_id,
            "manifest": manifest,
        })
    except ValueError as e:
        logger.warning("Error fetching manifest for release %s: %s", release_id, e)
        return JsonResponse({
            "error": str(e),
            "error_code": "not_found"
        }, status=404)
    except Exception:
        logger.exception("Unexpected error fetching manifest for release %s", release_id)
        return JsonResponse({
            "error": "An unexpected error occurred",
            "error_code": "internal_error"
        }, status=500)


@support_group_required(settings.ADMIN_USERS_GROUP)
@require_http_methods(["POST"])
def promote_release(request):
    """
    Queue a release for promotion (import) into pathways.

    Expects JSON body with:
    - release_id: str (required)

    Returns JSON with queue status.
    """
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON",
            "error_code": "invalid_json"
        }, status=400)

    release_id = body.get("release_id", "").strip()
    if not release_id:
        return JsonResponse({
            "error": "release_id is required",
            "error_code": "missing_field"
        }, status=400)

    try:
        requested_by = request.user.get_username() if request.user else ""
        result = queue_release_for_promotion(release_id, requested_by=requested_by)
        return JsonResponse({
            "success": True,
            "data": result,
        })
    except ValueError as e:
        logger.warning("Error queuing release %s: %s", release_id, e)
        return JsonResponse({
            "error": str(e),
            "error_code": "queue_error"
        }, status=400)
    except Exception:
        logger.exception("Unexpected error queuing release %s", release_id)
        return JsonResponse({
            "error": "An unexpected error occurred",
            "error_code": "internal_error"
        }, status=500)
