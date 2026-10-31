# PostgreSQL Search Trial

## Scope

This is a Pathways-only trial based on `origin/develop` at `02b1c4c`. It does
not include pipeline changes, release download/import commands, shared-chart
changes, experimental benchmark tooling, or private query/judgment artifacts.
It searches the existing Course and Major rows already in the application DB.
No new catalog release is required. Description completeness affects relevance
but is not a prerequisite for enabling the backend.

`PATHWAYS_SEARCH_BACKEND` accepts `whoosh` or `postgres`, defaulting to `whoosh`.
Test values explicitly select `postgres`; production values explicitly retain
`whoosh`. The API still returns `course_matches`, `major_matches`, and
`text_matches`. The search API's previously crossed gateway/bottleneck arguments
are corrected and covered by an integration test.

Whoosh dependency installation, index building, imports, and existing scheduled
jobs remain unchanged. This branch does not retire Whoosh or any pipeline bundle.

## Deployment Integration

The existing deployment chart runs the shared image's `/scripts/deploy.sh`, which
calls Django `migrate` and then sources `/scripts/app_deploy.sh`. This image now
installs that application hook. It runs `manage.py check_search_backend` after
migrations and exits nonzero if PostgreSQL search is selected but not ready.
The hook uses fail-fast shell behavior; it does not swallow prerequisite errors.

Migrations extend the current develop graph after `0026_major_program_verind_id`:

1. `0027_postgres_search_configuration` installs `pg_trgm` and `unaccent` in
   `public`, then creates the English/unaccent text search configuration
   `public.pathways_english`. It does not import current application SQL into
   migration history. Shared extensions/configuration are deliberately retained
   on reverse migration rather than risking removal of other consumers.
2. `0028_postgres_search_indexes` is non-atomic and builds six expression indexes
   with `CREATE INDEX CONCURRENTLY`. It skips valid existing named indexes and
   drops/rebuilds invalid indexes left by an interrupted build. Reverse migration
   drops only these application-owned indexes, also concurrently.

All operations are limited to the `default` database, not the person datastore.
No data rows or Django model fields are changed. Index expressions are frozen
inside the migration and tested against the runtime matching expressions.

The deploy gate checks PostgreSQL 12+, both public extensions, the text-search
configuration's usability, and the existence/validity/readiness of all six indexes.
It does not issue sample user searches or change catalog rows. Whoosh selection
skips the PostgreSQL gate so flag rollback does not depend on these indexes.

## Before Merging To Develop

1. Confirm the test database version is PostgreSQL 12 or later and approve the
   database changes with its owner. Local validation used PostgreSQL 17.
2. Confirm the migration role can create extensions, objects in `public`, and
   indexes on the Course and Major tables. On managed PostgreSQL an administrator
   may need to preinstall the extensions; do not grant broad privileges merely
   for search. The actual test/prod role permissions are not yet verified.
3. If preinstallation is necessary, an authorized administrator can run:

   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;
   CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;
   ```

   Existing extensions in another schema are not automatically moved. Coordinate
   that situation with the database owner instead of relocating shared objects.
4. Ensure the role owns the two catalog tables or can create their indexes, and
   can create the text-search configuration. An existing configuration created by
   another role is not overwritten by this migration.
5. Budget deploy-job time for concurrent index construction on the actual catalog.
   It avoids the normal index-build writer lock, but still consumes CPU/I/O and
   may wait for long transactions. Run only one migration job at a time.
6. Open a PR targeting develop and run the existing CI. This feature branch is
   not a new deployment target; merge to develop uses the existing test release.
   No manual cluster changes or automatic push are part of this implementation.

Before enabling on another environment, do the same preparation there. Migrations
are additive and apply when the code is deployed even when Whoosh is selected;
the feature flag changes serving behavior, not migration history.

## Verify The Trial

After the deploy job succeeds, run inside a new application pod:

```bash
/app/bin/python manage.py check_search_backend
```

Exercise exact IDs (`CSE142`), multiword topics (`organic chemistry`), typos,
campus/type filters, and gateway/bottleneck/COI filters through the normal API.
Confirm result links and descriptions still render correctly. Verify HTTP errors,
database CPU, slow queries, and p95 search latency under representative traffic.

Ranking prioritizes exact IDs, title phrases, all-word title coverage, and topic
prose over partial matches. Majors require all meaningful title words to enter
the promoted group. Trigram fallback is scoped to the selected type and filters.
Labeled prerequisite/offering suffixes remain searchable but have lower weight
and do not earn strong topic bonuses. Original descriptions are unchanged.

The local judged pilot supported the lexical ranking changes, but is small.
Some new results remain unjudged and the original holdout has already been used.
Median latency was competitive locally; broad-query p95 remained worse than
Whoosh. This is a develop trial, not a production cutover or a performance SLA.

Indexes maintain themselves transactionally when the existing importer changes
catalog rows. No new per-pod index watcher or background reindex task is needed
for PostgreSQL search. The retained Whoosh workflow still runs for rollback.

## Rollback

Set `PATHWAYS_SEARCH_BACKEND=whoosh` in test values and redeploy. Check that the
retained Whoosh index matches the catalog and that a search succeeds. The existing
Whoosh build path has not been disabled. A flag rollback needs no DB downgrade.

Leave the additive extensions/config/indexes installed for immediate rollback.
Only remove indexes during a separately approved cleanup after no pods use the
PostgreSQL backend. If reverting the migration, stop/select away from PostgreSQL
search first, then migrate to `0027_postgres_search_configuration`. That removes
the six search indexes, not catalog rows or shared extensions/configuration.
Do not roll back schema underneath running PostgreSQL search pods.

## Validation

Focused database tests:

```bash
python manage.py test pathways.tests.test_postgres_search --noinput
python manage.py makemigrations pathways --check --dry-run
```

The tests cover actual API routing, filters, exact IDs, title phrases, accents,
typos, metadata weighting, malicious input parameterization, deploy readiness,
and rollback/reapplication on a real PostgreSQL database. They also create a real
failed concurrent index and verify that the migration repairs it while preserving
catalog rows. No prototype preparation command is needed to run the tests.

The focused suite currently passes 22 tests. Full application validation ran
89 tests with one failure in `TestCoiApi.test_course` (expected first score 2.1,
received 0.3). The untouched develop baseline reproduces the same full-suite
failure in its 67 tests, while that test passes in isolation on both versions.
The COI endpoint uses no explicit ordering; this existing failure is not repaired
as part of the search trial.

CI's pycodestyle check passes for touched Python modules. Ruff was also run using
the user's repository skill, excluding migrations and applying no automatic
fixes. The new modules pass Ruff. A path-matched comparison finds 95 existing
tracked-file findings on this branch versus 97 on develop, with no new findings.
Repository-wide Ruff is therefore not clean; unrelated warnings are left alone.

The local test harness used an existing Python 3.12 application image with this
worktree's source/settings mounted read-only and separate disposable PostgreSQL
database names. The real shared `/scripts/deploy.sh`, with the new application
hook mounted at its installed path, also ran successfully twice against a fresh
local database: initial migration/provisioning and an idempotent second deploy.
Pathways model state matches its migrations. The installed person-client package
reports separate model-options drift under localdev; the Pathways-scoped check
does not hide or modify that upstream dependency warning.

A fresh image build and target-cluster role verification remain
deployment prerequisites, not claims made by these source-level tests.