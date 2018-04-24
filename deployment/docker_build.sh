#!/bin/bash

set -eu -o pipefail
set -x

IMAGE=${1:-jumpcut}

# Ensure we are in the right (root) directory
cd "${0%/*}"
cd ..

# Build frontend distribution
docker build -t frontend frontend
mkdir -p deployment/frontend_out
docker run --rm -v "$(pwd)/deployment/frontend_out:/code/dist" frontend gulp deploy

# Build production image
docker build --pull -t production -f deployment/Dockerfile .
