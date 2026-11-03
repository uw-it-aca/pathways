# Search Load Test

This local k6 test calls the authenticated search API using the actual search
dispatcher, filters (when present in the request), ranking and serialization.
It does not run migrations, import data, or change the selected backend.

## Workload

Put the tab-separated log sample at repository-root `sample-searches`. Each row
must contain `type<TAB>query<TAB>positive integer count`, with no header. The
supplied sample has 2,000 rows representing 9,256 searches: 5,007 `course_id`
(54.1%) and 4,249 `free_text` (45.9%).

Each request independently selects a row with probability `count / 9256`.
The observed mix approaches those weights over longer runs; it is not an exact
ordered replay. Spaces, punctuation, capitalization and literal quotes are
preserved. Both logged types use `search_string`; the type is a reporting tag,
not an inferred `type[]=course` filter. The sample does not record campus/type
filters, timing, sessions or think time, so those are not invented.

The corpus, local header files and results are ignored by Git and excluded from
application Docker images. Keep any alternative corpus files outside the repo.

## Authentication

Log into test and capture the request headers of a successful search using browser
DevTools. Create `load-tests/search-headers.local.json` containing a JSON object:

```json
{
  "Cookie": "sessionid=REPLACE_WITH_LIVE_TEST_SESSION",
  "Accept": "application/json"
}
```

Include other application-required headers from the live request if necessary.
Do not include `Host`, `Content-Length`, `Connection`, `Accept-Encoding`, or HTTP/2
pseudo-headers such as `:authority`. Do not paste credentials into chat, commit
them, enable HTTP debug logs, or send this test to a hosted load-testing service.
Restrict the local file with `chmod 600 load-tests/search-headers.local.json`.

The preflight sends one request before starting load. It requires HTTP 200, JSON
content type and the three result arrays. Redirect following is disabled so an
expired session cannot silently benchmark the login page. Empty results are valid.

## Run Locally

Use an installed k6 CLI (see the [k6 installation guide](https://grafana.com/docs/k6/latest/set-up/install-k6/)):

```bash
k6 run load-tests/search.js
```

Alternatively, run the public k6 image locally, mounting only the test script and
inputs, not the whole application:

```bash
docker run --rm -i \
  --user "$(id -u):$(id -g)" \
  -v "$PWD/load-tests:/work:ro" \
  -v "$PWD/sample-searches:/sample-searches:ro" \
  -w /work grafana/k6:1.4.0 run search.js
```

The default is **1 request/sec for 1 minute**, plus a preflight and up to 10 seconds
for in-flight requests to finish. This is an arrival-rate test, not a simulated
user-count test. Obtain approval from the database owner before raising load on a
shared instance.

Take an idle database baseline, run the smoke test, then measure at progressively
higher rates, reviewing database health between runs:

```bash
k6 run -e RPS=2 -e DURATION=5m load-tests/search.js
k6 run -e RPS=5 -e DURATION=5m load-tests/search.js
```

For Docker, pass those same `-e` options **after `run`**, before `search.js`.
Stop with Ctrl-C if database health degrades. No test is started automatically by
application CI.

| Variable | Default | Purpose |
| --- | --- | --- |
| `RPS` | `1` | Requests started per second |
| `DURATION` | `1m` | Bounded run length, e.g. `30s` or `5m` |
| `PREALLOCATED_VUS` | `2` | Initially allocated workers |
| `MAX_VUS` | `10` | Maximum workers; increase deliberately if needed |
| `P95_MS` | `2000` | p95 latency pass/fail limit; choose your actual budget |
| `HEADERS_FILE` | `./search-headers.local.json` | Header file, relative to script |
| `SEARCHES_FILE` | `../sample-searches` | Corpus file, relative to script |
| `BASE_URL` | `https://test.dawgpath.uw.edu` | Test site, explicitly approved production site, or local HTTP mock |
| `ALLOW_PRODUCTION` | unset | Must be exactly `true` for production |

Run serially, not simultaneously, unless concurrent tests are intentional.
The thresholds fail if valid-search p95 exceeds the budget or iterations are
dropped. A failure rate of 1% or more automatically aborts the run at a threshold
evaluation after an initial 10-second delay (not an exact 10-second cutoff).
Requests time out at 10 seconds. These limits do not
monitor database CPU or protect other tenants; continue watching infrastructure.

## Production Whoosh Comparison

Production load requires approval, `BASE_URL=https://dawgpath.uw.edu`,
`ALLOW_PRODUCTION=true`, and a separate explicit header file. The default test
header filename is rejected for production. Log into production and save headers
from a successful production search to
`load-tests/prod-search-headers.local.json`, using the same JSON format above.
Run `chmod 600 load-tests/prod-search-headers.local.json`. Do not copy test cookies
to that file. The runner cannot determine which environment a cookie came from;
the successful authenticated preflight is still required.

After the current test run finishes, take an idle production baseline and run
these commands from the repository root, **one at a time**:

```bash
docker run --rm -i \
  --user "$(id -u):$(id -g)" \
  -v "$PWD/load-tests:/work:ro" \
  -v "$PWD/sample-searches:/sample-searches:ro" \
  -w /work grafana/k6:1.4.0 run \
  -e BASE_URL=https://dawgpath.uw.edu \
  -e ALLOW_PRODUCTION=true \
  -e HEADERS_FILE=./prod-search-headers.local.json \
  -e RPS=2 -e DURATION=5m \
  -e PREALLOCATED_VUS=20 -e MAX_VUS=20 search.js
```

Review latency, errors, pod health and live-user impact before repeating the
command with `-e RPS=5`. Use the same 20-worker settings for the test comparison
runs too; worker count changes generator capacity, not the requested rate.
Stop with Ctrl-C if service health degrades.

Verify the backend on each environment rather than assuming it from the hostname.
For this trial, test selects PostgreSQL and production retains Whoosh. Whoosh
search primarily consumes app-pod CPU and index/filesystem resources rather than
database CPU, although authentication and other application activity still use
the database. Record app CPU/memory, replica counts and latency for both backends.

This compares deployed environments, not an isolated backend benchmark:
production traffic, pod sizes/counts, catalog/index contents, caching and cluster
conditions may differ. Report those differences with the latency results; do not
attribute every difference to the search backend.

## Measurements

The console reports valid-search latency overall and by `query_type`, with median,
p90, p95, p99 and maximum. `search_failures` includes non-200 responses, login
redirects, invalid JSON and missing result arrays; failed responses are excluded
from `search_latency`, so inspect both metrics. Generic HTTP metrics include the
single preflight; search-specific metrics do not. `dropped_iterations` means the
requested rate was not achieved with the available workers.

For a longer run, optional local outputs allow time-window analysis:

```bash
mkdir -p load-tests/results
k6 run -e RPS=2 -e DURATION=5m \
  --summary-export=load-tests/results/summary.json \
  --out json=load-tests/results/metrics.json load-tests/search.js
```

Query strings are omitted from metric tags; grouping uses only the two logged
types. Keep result files local. This setup intentionally repeats the frequency
distribution and includes cache effects rather than forcing cold database caches.

Watch Cloud SQL CPU, read I/O/latency, connections, active queries and lock waits,
alongside pod CPU/memory, restarts and worker saturation. Correlate the run's time
window with Query Insights or existing `pg_stat_statements` statistics. Do not
reset shared database statistics. Check achieved rate and dropped iterations
before calling a latency result acceptable. Use the same workload and rates when
comparing backends, keeping deployment and database conditions comparable.

## Validate Without Live Traffic

The parser/sampler/header/response checks use Node's built-in test runner:

```bash
node --test load-tests/search-workload.test.js
```

When the supplied corpus is present, the test verifies all 9,256 weighted ticket
positions against the exact per-type counts. No credentials or live service are
needed for these tests.

With Docker and the k6 image available, run the integration checks too:

```bash
docker pull grafana/k6:1.4.0
node --test load-tests/search-workload.test.js load-tests/search-integration.test.js
```

The integration checks use a temporary localhost server and dummy credentials,
verify the requests and metrics, reject a login redirect before load starts,
and fail a run if the response shape changes after preflight. They require Linux
Docker host networking and never contact the test site.
