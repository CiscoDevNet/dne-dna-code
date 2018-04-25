#!/usr/bin/env bash
# Clean the project directory.

set -e
cd "$(dirname "$0")/.."


# Script Arguments
for i in ${@}; do
    case ${i} in
        --all)
        deep_clean=true
        ;;

        *)
        echo "Unknown argument: $i"
        exit 1
        ;;
    esac
done


echo "==> Removing Python build artifacts..."
find . -name '*.pyc' -exec rm -f {} +
find . -name '*.pyo' -exec rm -f {} +
find . -name '*~' -exec rm -f {} +
find . -name '__pycache__' -exec rm -fr {} +
find . -name '*.egg-info' -exec rm -fr {} +
find . -name '*.egg' -exec rm -f {} +
rm -rf build/
rm -rf dist/
rm -rf .eggs/

echo "==> Removing test and coverage artifacts..."
rm -rf .cache/
rm -f  .coverage
rm -rf .tox/
rm -rf htmlcov/

echo "==> Cleaning docs directories..."
rm -rf docs/_build/*


if [[ $deep_clean == true ]]; then
    echo "==> Deep cleaning..."

    if [ -f "Pipfile" ] && [ -n "$(pipenv --version 2>/dev/null)" ]; then
        echo "==> Removing pipenv environment..."
        pipenv --rm || true
    fi

    if [ -d ".venv" ]; then
        echo "==> Removing project virtual environment '.venv'..."
        rm -rf .venv/
    fi

    if [ -d "venv" ]; then
        echo "==> Removing project virtual environment 'venv'..."
        rm -rf venv/
    fi
fi
