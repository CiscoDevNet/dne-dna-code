#!/usr/bin/env bash
# Setup the project for use after cloning, or reset it back to the
# initial (unused) state.

set -e
cd "$(dirname "$0")/.."


echo "==> Setting up / resetting project for initial use..."
script/clean.sh --all
script/init-user.sh
script/init-dev.sh
