#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
source ./bin/activate

tests=(
    pathways.tests.test_postgres_search
    pathways.tests.test_api.TestSearchApi
    pathways.tests.commands.test_data_release_verification
    pathways.tests.commands.test_data_release
    pathways.tests.commands.test_release_sync
    pathways.tests.commands.test_release_sync_queue
    pathways.tests.commands.test_release_migrations
)

if (( $# > 0 )); then
    tests=("$@")
fi

python manage.py migrate --noinput
python manage.py check_search_backend
python -Wd -m coverage run --source=pathways manage.py test "${tests[@]}" --noinput

# put generated coverage result where CI will combine it with the SQLite run
if [ -d /coverage ]; then
    cp .coverage.* /coverage
fi