# PostgreSQL Search Rollout

## Scope

This document covers the Pathways PostgreSQL-only search rollout. It does not
cover pipeline changes, release download/import commands, shared-chart changes,
experimental benchmark tooling, or private query/judgment artifacts.
It searches the existing Course and Major rows already in the application DB.
No new catalog release is required. Description completeness affects relevance
but is not a prerequisite for deploying search.

PostgreSQL is the sole search backend in local, test, and production deployments.
There is no backend environment selector. The API still returns
`course_matches`, `major_matches`, and
`text_matches`. The search API's previously crossed gateway/bottleneck arguments
are corrected and covered by an integration test.

The Whoosh dependency, startup index builder, CI index-build step, and local
index volume are removed. Legacy local index files are excluded from the image
build context. Existing catalog imports and scheduled jobs continue to run;
search indexes are maintained by PostgreSQL rather than filesystem artifacts.

## Deployment Integration

The existing deployment chart runs the shared image's `/scripts/deploy.sh`, which
calls Django `migrate` and then sources `/scripts/app_deploy.sh`. This image now
installs that application hook. It runs `manage.py check_search_backend` after
migrations and exits nonzero if PostgreSQL search is not ready.
The hook uses fail-fast shell behavior; it does not swallow prerequisite errors.

Local startup runs `migrate`, then `check_search_backend`, then `import_data`,
stopping on failure. PostgreSQL CI runs `migrate --noinput` and
`check_search_backend` before the focused database tests. No flow builds a
filesystem search index.

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
3. `0029_postgres_search_columns` is non-atomic and adds stored generated
   `tsvector` columns (`search_document`, `search_title_document`, and for
   courses `search_rank_document`) to the Course and Major tables. It replaces
   the two full-text expression indexes with GIN indexes on `search_document`.
   PostgreSQL computes these columns on every insert and update, so searches no
   longer rebuild text vectors per candidate row. The importer needs no changes.
   Adding the columns rewrites each table under an `ACCESS EXCLUSIVE` lock. That
   took about 3.5 seconds locally on the full catalog. Reads of these tables
   block briefly, and this happens on every environment that deploys the
   migration, including production. Reverse migration restores the
   expression indexes before dropping the columns.

All operations are limited to the `default` database, not the person datastore.
No data rows or Django model fields are changed; the generated columns are
database-only and invisible to the ORM. Expressions are frozen inside the
migrations and tested against each other and against the stored column values.

The deploy gate checks PostgreSQL 12+, both public extensions, the text-search
configuration's usability, the existence/validity/readiness of all six indexes,
and the presence of the generated search columns.
It does not issue sample user searches or change catalog rows. All deployments
must pass this gate; there is no alternate-backend bypass.

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

Before deploying to another environment, do the same preparation there.
Migrations apply when the code is deployed, and search requires the resulting
database objects in every environment.

## Verify The Rollout

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
Trigram fallback runs only when no full-text or ID-prefix match exists.

The local judged pilot supported the lexical ranking changes, but is small.
Some new results remain unjudged and the original holdout has already been used.
Median latency was competitive locally; broad-query p95 still needs validation
under representative load. Pilot results are not a production performance SLA.

Generated columns and indexes maintain themselves transactionally when the
existing importer changes catalog rows. No new per-pod index watcher or
background reindex task is needed for PostgreSQL search.

## Rollback

There is no backend-switch rollback. Roll back application code only to a
compatible PostgreSQL-search release, leaving extensions, configuration, generated
columns, and indexes installed. If no compatible release exists, stop the rollout
and coordinate recovery with the database owner before changing schema.

Schema reversal is a separately approved maintenance operation. Stop all search
pods and jobs that depend on the generated columns or indexes before reversing
their migrations. Shared extensions/configuration are deliberately retained.
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
as part of the search rollout.

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
