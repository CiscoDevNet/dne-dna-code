#! /bin/bash

# This bash script is downloaded and ran on the dCloud DevBox for the DevNet
# Express DNAv3 Pod automatically when a terminal starts.  It's purpose is to
# allow the DevBox to get updates and changes applied between formal pod
# refreshes.

# The "SYNC_VERSION" is used to determine whether any pod updates are needed
SYNC_VERSION=1

# Step 1. Check to see if script needs to run.  If not, exit.
CURRENT_VERSION=$(<~/sync_version)
echo "Current SYNC_VERSION ${CURRENT_VERSION}"

if [ "$CURRENT_VERSION" -eq "$SYNC_VERSION" ];
  then
    echo "Pod up to date."
    exit
fi

echo "Pod configuration needs updates."

# Step 2. Run Updates
# Example Update
    # Download updated Python requirements
    curl https://raw.githubusercontent.com/CiscoDevNet/dne-dna-code/master/requirements.txt -o sync_requirements.txt
    # Create a Virtual Environment
    python3.6 -m venv sync_venv
    source sync_venv/bin/activate
    # Install updated requirements
    pip install -r sync_requirements.txt
    # Deactivate and delete venv
    deactivate
    rm -Rf sync_venv >> sync_log.txt 2>&1
    # Delete downloaded Python requirements file
    rm sync_requirements.txt

# Step 3. Update Pod Version
echo "Updating SYNC_VERSION to ${SYNC_VERSION}"
echo ${SYNC_VERSION} > ~/sync_version
