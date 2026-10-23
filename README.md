# pathways

[![Build Status](https://github.com/uw-it-aca/pathways/workflows/Build%2C%20Test%20and%20Deploy/badge.svg)](https://github.com/uw-it-aca/pathways/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/pathways/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/pathways?branch=main)

## System Requirements

- Python (3.12)
- Docker
- Node

## Development Stack

- Django (5.2)
- Vue (3.2)
- Vite (2.9)
- Vitest (0.10.2)

## Design Stack

- Bootstrap (5.1)
- Bootstrap Icons (1.9.0)

## Initial Setup

Clone this template repo as a new repo (command line)

        $ git clone git@github.com:uw-it-aca/pathways.git

Go to your repository

        $ cd pathways

Copy the sample .env file so that your environment can be run.

        $ cp .env.sample .env

Update any .env variables for local development purposes

## Development (using Docker)

Docker/Docker Compose is used to containerize your local build environment and deploy it to an 'app' container which is exposed to your localhost so you can view your application. Docker Compose creates a 'devtools' container - which is used for local development. Changes made locally are automatically syncd to the 'app' container.

### Search Index

The search index in `indexdir/` is automatically built when the docker container starts (via `docker/app_start.sh`). 

Note: `indexdir/` is ignored by Git. If Whoosh index files were previously tracked, they should be removed from the Git index using:
`git rm -r --cached indexdir`

        $ docker-compose up --build

View your application using your specified port number in the .env file

        Demo: http://localhost:800?/

#### Offline snapshot builds and downloaded-release verification

The shared `dawgpath-search` dependency is pinned to the same exact Git commit as
the pipeline. It pins Whoosh 2.7.4. Installing dependencies during the image build
needs GitHub access (and Git); building or preparing indexes does not use GCS,
credentials, or network access.

The existing no-argument `build_search_index` command and startup flow still
build from the local database, using the shared schema. Neither production
startup nor automatic refresh/activation changes in this increment.

To build directly from the checked-in offline snapshot without reading a
database, run inside the application environment:

```bash
python manage.py build_search_index \
  --input-root pathways/data \
  --output-dir indexdir/offline-check \
  --release-id local-snapshot
```

This uses the shared builder and the five local files `course_data.json`,
`major_data.json`, `coi_scores.csv`, `gateway_courses.csv`, and
`bottleneck_courses.csv`. It writes index metadata and never downloads data.
The output directory must be new; it does not overwrite the active index.

To test a complete, manually downloaded pipeline release:

```bash
python manage.py prepare_search_release \
  --release-dir /path/to/downloaded-release \
  --output-dir /path/to/new-prepared-index \
  --release-id <expected-release-id>
```

Use the directory containing `manifest.json` and all release artifacts
(ten for schema 1.0, eleven for schema 1.1),
not its parent download directory. Obtain it from a trusted source: manifest
checksums detect corruption but do not authenticate Whoosh's serialized schema.
The command verifies manifest version, release identity, all artifact hashes,
index source hashes, and the bundle's exact regular-file inventory. It rejects
symlinks, traversal paths, duplicate/missing archive members, metadata mismatches,
unsupported index contracts, and incompatible Whoosh versions. Legacy pickle
exports are only hashed, never deserialized. Pathways owns the full release
manifest and source-data consistency checks; `dawgpath-search` owns archive
validation, staged extraction, and index verification. The fresh output is
exposed only on success.

Preparation does not import JSON/CSV data into the database, change query/result
shapes, or select the new index for serving. Keep the downloaded release outside
the checked-in snapshot; local development does not need to pull from GCS.
Future production cutover/refresh must coordinate the database data and index
from the same release. That activation work is separate from these explicit,
offline preparation commands.

### Explicit GCS download and database import

These are operator commands, **not startup hooks or a live refresh workflow**.
Localdev still imports checked-in data at startup without contacting GCS.
Schedules, admin triggers, multi-pod readiness, and serving-index activation
are not implemented in this increment.

Download one completed, trusted release by its exact ID:

```bash
python manage.py download_data_release \
  --bucket <trusted-release-bucket> \
  --release-id <release-id> \
  --output-dir /path/to/new-local-release
```

Use `--prefix <object-prefix>` if releases are under a bucket prefix.
The command uses Google Application Default Credentials (workload identity in
GKE, or locally configured ADC), needs object **get** permission, and never
lists releases or follows `latest/`. It pins each read to its GCS generation,
checks every artifact's size/hash and the complete index, then exposes a fresh
local directory. Missing objects, authentication failures, generation changes,
or corruption fail without leaving a partial output or falling back to the
checked-in snapshot. Keep downloads outside the repository.

For an **isolated integration-test database or a database with serving traffic
stopped**, apply migrations and import the verified local release:

```bash
python manage.py migrate
python manage.py import_data_release \
  --release-dir /path/to/new-local-release \
  --release-id <release-id> \
  --confirm-replace-data
```

**Do not run this against a serving test/prod database yet.** Import replaces
catalog data, but deliberately does not change the active search index; serving
traffic could otherwise see a mismatched database and index. A coordinated
activation workflow is still required before resuming traffic.

Database imports require **schema 1.1** from the updated pipeline, including
`similar_majors.csv` fetched and frozen from Azure by the pipeline. There is no
supplemental CSV fallback and no Azure fetch during import. Existing schema-1.0
downloads can still be verified/prepared, but cannot be database-imported by
this command.

The importer verifies all files and the Whoosh bundle before mutation, uses
only those verified bytes, and reuses existing catalog/COI/flag/career/similar-
major/STEM import semantics. Pickle artifacts are only hashed, not unpickled.
Missing majors in similarity data retain the existing importer behavior:
unavailable pairs are skipped and logged, available majors still get STEM flags.
All table replacement, relationships, legacy file-hash markers, and the
`DataReleaseImport` success record commit in one transaction. A failure rolls
back all changes. A database row lock serializes these release imports on
PostgreSQL; do not run legacy import commands concurrently.

Repeating the currently imported release is a no-op when its manifest and
import markers still match. Reusing a previously imported release ID with a
different manifest is rejected. Import records describe database data only,
not which index is serving. The existing `import_data`, `build_search_index`,
startup script, and query code remain unchanged.

## Testing

### Front-end Testing (using Vitest)

Run Vitest test scripts and generate coverage report

        $ npm run test
        $ npm run coverage

### Linting (using ESLint and Stylelint)

Run ESLint for JS linting

        $ npm run eslint

Run Stylelint for CSS linting

         $ npm run stylelint

### Python Testing (using Django)

Run unittest

        $ docker-compose run --rm app bin/python manage.py test

## Authors

[Academic Experience Design & Delivery](https://github.com/uw-it-aca)

## License

Copyright 2022 UW Information Technology, University of Washington

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
