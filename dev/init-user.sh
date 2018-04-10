#!/usr/bin/env bash
# Install all dependencies that the project needs to run.

set -e
cd "$(dirname "$0")/.."


# Ensure that packages are only installed in an active virtual environment
export PIP_REQUIRE_VIRTUALENV=true


if [ -f "Pipfile" ] && [ -n "$(pipenv --version 2>/dev/null)" ]; then
    echo "==> Initializing pipenv environment and installing packages..."
    pipenv install

elif [ -f "requirements.txt" ]; then
    if [ -n "$(python -c 'import sys; print (sys.real_prefix)' 2>/dev/null)" ]; then
        echo "==> Installing requirements.txt packages in the active virtual environment..."

    else
        if [ ! -d "venv" ]; then
            echo "==> Creating a new virtual environment 'venv' for the project..."
            python -m venv venv
        else
            echo "==> Installing requirements.txt packages in the project's 'venv' virtual environment..."
            source venv/bin/activate
        fi
    fi

    pip install -r requirements.txt

else
    echo "No Python requirements found."
fi
