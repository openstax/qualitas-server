#! /usr/bin/env bash

# Exit in case of error
set -e

TEST_RESULTS=${TEST_RESULTS-./junit.xml}

echo "Test results will be saved in: ${TEST_RESULTS}"

docker-compose -f circleci-compose.yml build
docker-compose -f circleci-compose.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f circleci-compose.yml up -d
docker-compose -f circleci-compose.yml exec web /bin/sh -c "pytest --cov=./qualitas --cov-report=xml:./cov.xml --junitxml="${TEST_RESULTS}" --cov-report=term"

# Comment this line out to leave the stack running. Useful for test development.
docker-compose -f circleci-compose.yml down -v --remove-orphans
