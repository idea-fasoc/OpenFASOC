#!/bin/bash

# this script will recreate the ICCAD paper RL results (using the default seed)
echo "This script has been verified to run with python3.11 and package versions provided"



# =====================================================================
#
# find most recent version of python
#
# Find all installed Python 3 versions and sort them in descending order
#PYTHON_VERSIONS=$(compgen -c | grep -E '^python3\.[0-9]+$' | sort -V | tail -n 1)
# Extract the most recent version
#MOST_RECENT_PYTHON=$(echo "$PYTHON_VERSIONS" | tail -n 1)
# Check if a Python version was found
#if [ -z "$MOST_RECENT_PYTHON" ]; then
#    echo "No Python 3 versions found."
#    exit 1
#fi
# Print the most recent Python version
#echo
#echo "Currently using Python version: $MOST_RECENT_PYTHON"
#echo
# Check if the most recent version is at least 3.10
#MINIMUM_VERSION="3.10"
#if [[ "$(echo $MOST_RECENT_PYTHON | cut -d '.' -f2)" -lt "$(echo $MINIMUM_VERSION | cut -d '.' -f2)" ]]; then
#    echo "The most recent Python version ($MOST_RECENT_PYTHON) is less than $MINIMUM_VERSION. Please update your Python installation."
#    echo
#    exit 1
#fi
# Save the command to run the most recent Python version into a variable
#PY_RUN=$MOST_RECENT_PYTHON
PY_RUN="python3.11"




# =====================================================================
#
# ensure all python depedencies are installed
#

# File containing the list of python dependencies
requirements_file="requirements.txt"
#requirements_file="donotdothischeck.txt"

# Function to check if a Python package is installed
is_installed() {
    $PY_RUN -m pip show "$1" &> /dev/null
}

# Read the dependencies from requirements.txt and process each line
while IFS= read -r package || [ -n "$package" ]; do
    # Remove leading/trailing whitespace
    package=$(echo "$package" | xargs)
    # Skip empty lines and comments
    if [[ -z "$package" || "$package" == \#* ]]; then
        continue
    fi
    # Extract the package name without extras and version specifiers for checking
    package_name=$(echo "$package" | sed 's/\[.*\]//;s/[<>=].*//')
    echo "Checking if $package is installed..."
    if is_installed "$package_name"; then
        echo "$package is already installed."
    else
        echo "$package is not installed. Installing..."
        $PY_RUN -m pip install "$package"
        # Check if the installation was successful
        if is_installed "$package_name"; then
            echo "$package installed successfully."
        else
            echo "Failed to install $package."
        fi
    fi
    echo
done < "$requirements_file"
echo "Dependency check and package installations complete."



# =====================================================================
#
# setup and run the RL code
#

# clean old files
#rm -rf *checkpoint
#rm record*.txt
#rm train.yaml
#rm eval.yaml
#rm eval*.txt

# NOTE: this is done automatically when you specify "first_run" flag
# open gen_spec.py line 39, change the name of yaml file to train.yaml
$PY_RUN gen_spec.py --first_run
$PY_RUN model.py
# NOTE: this is done automatically when you do NOT specify "first_run" flag
# open gen_spec.py line 36, change the name of yaml file, and put the same name into eval.py line 16
$PY_RUN gen_spec.py
$PY_RUN eval.py
# eval.py creates eval*.txt which shows how many specifications are reached
