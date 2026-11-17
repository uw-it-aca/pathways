"""Local-only sample data for the release promotion interface."""

import copy

RELEASES = [
    {
        "release_id": "local-sample-20261116",
        "manifest_size": 2468,
        "updated": "2026-11-16T12:00:00Z",
    },
    {
        "release_id": "local-sample-20261109",
        "manifest_size": 2351,
        "updated": "2026-11-09T12:00:00Z",
    },
]

CURRENT_RELEASE_ID = "local-sample-20261109"

ARTIFACTS = {
    "course_data.json": {"size_bytes": 12582912, "checksum_sha256": "a" * 64},
    "curric_data.json": {"size_bytes": 1048576, "checksum_sha256": "b" * 64},
    "major_data.json": {"size_bytes": 524288, "checksum_sha256": "c" * 64},
    "course_prereq_data.pkl": {"size_bytes": 8388608, "checksum_sha256": "d" * 64},
    "prereq_data.pkl": {"size_bytes": 4194304, "checksum_sha256": "e" * 64},
    "bottleneck_courses.csv": {"size_bytes": 32768, "checksum_sha256": "f" * 64},
    "gateway_courses.csv": {"size_bytes": 16384, "checksum_sha256": "0" * 64},
    "coi_scores.csv": {"size_bytes": 262144, "checksum_sha256": "1" * 64},
    "admit_major_mapping.csv": {"size_bytes": 65536, "checksum_sha256": "2" * 64},
    "similar_majors.csv": {"size_bytes": 131072, "checksum_sha256": "3" * 64},
}


class MockReleaseLister:
    def list_available_releases(self):
        return copy.deepcopy(RELEASES)

    def get_release_manifest(self, release_id):
        if not any(release["release_id"] == release_id for release in RELEASES):
            raise ValueError(f"Release not found: {release_id}")
        return {
            "release_id": release_id,
            "schema_version": "2.0",
            "artifacts": {
                name: {**info, "version_path": f"releases/{release_id}/{name}"}
                for name, info in ARTIFACTS.items()
            },
        }
