#!/usr/bin/env bash
# Install all the development dependencies for this project.

set -e
cd "$(dirname "$0")/.."


# Ensure that packages are only installed in an active virtual environment
export PIP_REQUIRE_VIRTUALENV=true


if [ -f "Pipfile" ] && [ -n "$(pipenv --version 2>/dev/null)" ]; then
    echo "==> Installing Pipfile development dependencies..."
    pipenv install --dev

elif [ -f "dev-requirements.txt" ]; then
    if [ -n "$(python -c 'import sys; print (sys.real_prefix)' 2>/dev/null)" ]; then
        echo "==> Installing dev-requirements.txt packages in the active virtual environment..."
    else
        echo "==> Installing dev-requirements.txt packages in the project's 'venv' virtual environment..."
        source venv/bin/activate
    fi

    pip install -r requirements-dev.txt

else
    echo "No Python dev requirements found."
fi
