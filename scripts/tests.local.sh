#! /usr/bin/env bash

# Exit in case of error
set -e

if [ "$(uname -s)" = "Linux" ]; then
    echo "Remove __pycache__ files"
    sudo find . -type d -name __pycache__ -exec rm -r {} \+
fi

docker-compose \
    -f docker-compose.tests.yml \
    -f docker-compose.yml \
    config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
sleep 5
docker-compose -f docker-stack.yml exec db psql -h db -d postgres -U postgres -c "DROP DATABASE IF EXISTS tests"
docker-compose -f docker-stack.yml exec web /bin/sh -c "pytest --cov=./qualitas --cov-report=xml:./cov.xml --junitxml="${TEST_RESULTS}" --cov-report=term"
