#!/usr/bin/env bash
# Update the root requirements.txt and requirements-dev.txt
#
# Use pipenv to manage the user vs. dev requirements and to create full
# "frozen" requirements.txt files in the repository root.



set -e
cd "$(dirname "$0")/.."


# Ensure that packages are only installed in an active virtual environment
export PIP_REQUIRE_VIRTUALENV=true


# Reset the current environment remove requirements files
pipenv --rm 1>/dev/null 2>/dev/null || true
rm -f Pipfile
rm -f Pipfile.lock
rm -f requirements.txt
rm -f requirements-dev.txt


echo Update the User Requirements
for requirement_file in $( find */requirements.txt ); do
    if [[ ! $requirement_file == dev/* ]]; then
        echo "Installing requirements from $requirement_file"
        pipenv install -r $requirement_file
    fi
done
pipenv run pip freeze > requirements.txt


echo Update the Dev Requirements
echo "Installing dev requirements from dev/requirements.txt"
pipenv install --dev -r dev/requirements.txt
pipenv run pip freeze > requirements-dev.txt
