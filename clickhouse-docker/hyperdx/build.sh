#!/bin/bash
# Meant to be run from the root of the repo

# No Auth
docker build --squash . -f ./clickhouse-docker/hyperdx/Dockerfile \
    --build-context clickhouse=./clickhouse-docker/clickhouse \
    --build-context otel-collector=./clickhouse-docker/otel-collector \
    --build-context hyperdx=./clickhouse-docker/hyperdx \
    --build-context api=./packages/api \
    --build-context app=./packages/app \
    --target all-in-one-noauth -t hyperdx/dev-all-in-one-noauth
