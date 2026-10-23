# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""Explicit transactional catalog replacement from verified local release bytes."""

import csv
import hashlib
import io
import json
import math
import re

from dawgpath_search import IndexValidationError
from django.db import transaction

from pathways import data_import
from pathways.models.data_import import DataImport
from pathways.models.data_release_import import DataReleaseImport
from pathways.search_release import verify_release, verify_release_index

IMPORT_FILES = {
    "coi": "coi_scores.csv", "major": "major_data.json",
    "course": "course_data.json", "curric": "curric_data.json",
    "gateway": "gateway_courses.csv", "bottleneck": "bottleneck_courses.csv",
    "cc_major": "admit_major_mapping.csv", "similar": "similar_majors.csv",
}
SIMILAR_HEADER = [
    "credential_code", "STEM_ind", "similar_credential_code",
    "similar_STEM_ind", "similarity", "similarity_group",
]


def _csv(content, name, width, header=None):
    try:
        rows = list(csv.reader(
            io.StringIO(content.decode("utf-8-sig"), newline=""), strict=True))
    except (UnicodeDecodeError, csv.Error) as exc:
        raise IndexValidationError(f"{name}: invalid UTF-8 CSV") from exc
    if header is not None and (not rows or rows.pop(0) != header):
        raise IndexValidationError(f"{name}: invalid header")
    if any(len(row) != width or any(
            not value or value != value.strip() for value in row) for row in rows):
        raise IndexValidationError(f"{name}: invalid row")
    return rows


def _parse(contents):
    coi_rows = _csv(contents["coi_scores.csv"], "coi_scores.csv", 2,
                    ["course_id", "score"])
    coi = []
    levels = set()
    for course_id, value in coi_rows:
        if not re.fullmatch(r"[A-Z][A-Z &/+]* [1-9][0-9]{0,2}", course_id):
            raise IndexValidationError("Invalid COI course ID")
        score = float(value)
        if not math.isfinite(score) or not -5 <= score <= 5:
            raise IndexValidationError("Invalid COI score")
        coi.append({"course_id": course_id, "coi_score": score})
        number = int(course_id.rsplit(" ", 1)[1])
        if score != -1 and number >= 100:
            levels.add(400 if 400 <= number < 500 else
                       300 if number >= 300 else 200 if number >= 200 else 100)
    if levels != {100, 200, 300, 400}:
        raise IndexValidationError("COI needs scores for all four course levels")
    parsed = {}
    for name, expected in (
            ("major_data.json", dict), ("course_data.json", list),
            ("curric_data.json", list)):
        data = json.loads(contents[name])
        if not isinstance(data, expected) or not data:
            raise IndexValidationError(f"{name}: expected nonempty {expected.__name__}")
        parsed[name] = data
    flags = {}
    for name in ("gateway_courses.csv", "bottleneck_courses.csv"):
        rows = _csv(contents[name], name, 3)
        valid_headers = [["course", "dept_abbr", "course_no"]]
        if name == "bottleneck_courses.csv":
            valid_headers.append(["course", "dept_abbv", "course_no"])
        if not rows or rows.pop(0) not in valid_headers:
            raise IndexValidationError(f"{name}: invalid header")
        flags[name] = rows
    career = _csv(contents["admit_major_mapping.csv"], "admit_major_mapping.csv", 2)
    similar = _csv(contents["similar_majors.csv"], "similar_majors.csv", 6,
                   SIMILAR_HEADER)
    if not similar:
        raise IndexValidationError("Similar majors CSV must not be empty")
    seen = set()
    stem = {}
    for row in similar:
        score = float(row[4])
        if (not math.isfinite(score) or not -1 <= score <= 1
                or row[5] not in {"Very Low", "Low", "Mid", "High"}):
            raise IndexValidationError("Invalid similar-major similarity")
        for code, flag in ((row[0], row[1]), (row[2], row[3])):
            if (len(code) > 25 or not re.fullmatch(
                    r"[A-Z][A-Z0-9 &/+.-]*-\d+-\d+-\d+", code)
                    or flag not in {"0", "1"} or (
                        code in stem and stem[code] != flag)):
                raise IndexValidationError("Invalid similar-major credential/STEM flag")
            stem[code] = flag
        pair = (row[0], row[2])
        if pair in seen:
            raise IndexValidationError("Duplicate similar-major pair")
        seen.add(pair)
    return coi, parsed, flags, career, similar


def import_release(release_dir, *, release_id):
    """Replace database data atomically; caller must keep serving traffic stopped."""
    manifest, contents = verify_release(release_dir, release_id=release_id)
    if manifest["schema_version"] != "1.1":
        raise IndexValidationError(
            "Database import requires release schema 1.1 with similar_majors.csv")
    if len(release_id) > 128:
        raise IndexValidationError("Release ID exceeds 128 characters")
    verify_release_index(manifest, contents)
    coi, parsed, flags, career, similar = _parse(contents)
    manifest_bytes = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    # Keep legacy import_data's MD5 markers compatible, but only write on success.
    hashes = {kind: hashlib.md5(contents[name]).hexdigest()
              for kind, name in IMPORT_FILES.items()}
    marker_hash = hashlib.md5(manifest_bytes).hexdigest()
    with transaction.atomic():
        DataImport.objects.get_or_create(type="release", defaults={"hash": ""})
        marker = DataImport.objects.select_for_update().get(type="release")
        previous = DataReleaseImport.objects.filter(release_id=release_id).first()
        if previous and previous.manifest_sha256 != manifest_hash:
            raise IndexValidationError("Previously imported release identity changed")
        if (previous and marker.hash == marker_hash and all(
                DataImport.objects.filter(type=kind, hash=value).exists()
                for kind, value in hashes.items())):
            return False
        data_import.import_level_coi(coi)
        data_import.import_coi_ranges(coi)
        data_import.import_major_data(parsed["major_data.json"])
        data_import.import_course_data(parsed["course_data.json"], coi)
        data_import.import_curric_data(parsed["curric_data.json"], coi)
        data_import.import_gateway_courses(flags["gateway_courses.csv"])
        data_import.import_bottleneck_courses(flags["bottleneck_courses.csv"])
        data_import.import_career_center_mapping(career)
        data_import.import_similar_majors(similar)
        data_import.import_stem_from_similar_majors(similar)
        for kind, value in hashes.items():
            DataImport.objects.update_or_create(type=kind, defaults={"hash": value})
        DataReleaseImport.objects.update_or_create(
            release_id=release_id, defaults={"manifest_sha256": manifest_hash})
        marker.hash = marker_hash
        marker.save()
    return True
