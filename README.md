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

Local development uses the Compose PostgreSQL service for the Pathways catalog
and search. Startup applies Django migrations, checks PostgreSQL search
readiness, and imports the checked-in catalog without contacting GCS.
Search queries live PostgreSQL catalog tables; there is no Whoosh dependency,
filesystem search index, bundle preparation, or index activation step.

        $ docker-compose up --build

View your application using your specified port number in the .env file

        Demo: http://localhost:800?/

### Data Release Contract

New pipeline releases use **manifest schema 2.0** with exactly ten artifacts:
`course_data.json`, `curric_data.json`, `major_data.json`,
`course_prereq_data.pkl`, `prereq_data.pkl`, `bottleneck_courses.csv`,
`gateway_courses.csv`, `coi_scores.csv`, `admit_major_mapping.csv`, and
`similar_majors.csv`. There is no `search_index` metadata or search bundle.

The app validates release identity, exact artifact inventory, immutable
`releases/<release-id>/<filename>` references, file sizes, and SHA-256 checksums.
Local manifest/artifact symlinks are rejected. Only verified in-memory bytes are
used for import. Obtain releases from a trusted source: checksums detect
corruption but do not authenticate a manifest.

Legacy schemas **1.0 and 1.1 remain supported for read-only download and
verification** with their original exact inventories (ten and eleven artifacts,
respectively). Their `search-index.tar.gz` bytes are size/checksum verified but
never opened, extracted, validated as an index, built, or activated. Legacy
`search_index` metadata is not interpreted. Pickle exports are only hashed,
never deserialized. No `dawgpath_search` dependency is needed.

### Explicit GCS download and database import

These are explicit operator commands, **not automatic refresh hooks**.
Localdev still imports checked-in data at startup without contacting GCS.
Schedules and admin triggers are not provided by these commands.

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
checks every artifact's size/hash, then exposes a fresh
local directory. Missing objects, authentication failures, generation changes,
or corruption fail without leaving a partial output or falling back to the
checked-in snapshot. Keep downloads outside the repository.

For an **isolated integration-test database or an operator-controlled maintenance
window**, apply migrations and import the verified local release. Use the
directory containing `manifest.json` and its artifacts, not its parent:

```bash
python manage.py migrate
python manage.py import_data_release \
  --release-dir /path/to/new-local-release \
  --release-id <release-id> \
  --confirm-replace-data
```

Database imports accept **schema 2.0 and legacy schema 1.1**, including
`similar_majors.csv` fetched and frozen from Azure by the pipeline. There is no
supplemental CSV fallback and no Azure fetch during import. Existing schema-1.0
downloads can still be verified, but cannot be database-imported by
this command.

The importer verifies all artifact bytes before mutation, uses
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
different manifest is rejected. PostgreSQL search queries the committed catalog
directly, so imported data becomes searchable transactionally without preparing
or activating an external index. Multi-request workflows and operational
scheduling still need normal maintenance coordination; do not run legacy
imports concurrently with a release import.

## Testing

### Search Load Testing

See [Search Load Test](docs/search-load-test.md) for a local, authenticated k6
workload weighted by logged search frequency. It defaults to test; production
requires explicit opt-in and separate authentication headers.

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
