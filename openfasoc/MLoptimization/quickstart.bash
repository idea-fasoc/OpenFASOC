#!/bin/bash

# this script produces an example RL optimization run

# =====================================================================
# Check if Python 3.10 is installed
if command -v python3.10 &>/dev/null; then
    echo "Python 3.10 is installed."
else
    echo "Error: Python 3.10 is not installed."
    exit 1
fi
PY_RUN="python3.10"

# =====================================================================
# Check if ngspice is installed
if command -v ngspice &>/dev/null; then
    echo "ngspice is installed."
else
    echo "Error: ngspice is not installed."
    exit 1
fi

# =====================================================================
# check that ngspice>40 is installed
ngspice --version > test_ngspice_version.txt
version_line=$(sed -n '2p' test_ngspice_version.txt)
version_number=$(echo "$version_line" | grep -oP '(?<=ngspice-)\d+')
required_version=40

if [[ "$version_number" -ge "$required_version" ]]; then
    echo "Correct ngspice version ($version_line) is installed."
else
    echo "Error: Incorrect ngspice version. Expected version >= $required_version but found:"
    echo "$version_line"
    exit 1
fi

# =====================================================================
# ensure all python depedencies are installed
# File containing the list of python dependencies
requirements_file="requirements.txt"

# Function to check if a Python package is installed
is_installed() {
    $PY_RUN -m pip show "$1" &> /dev/null
}

# Read the dependencies from requirements.txt and process each line
# while IFS= read -r package || [ -n "$package" ]; do
#     # Remove leading/trailing whitespace
#     package=$(echo "$package" | xargs)
#     # Skip empty lines and comments
#     if [[ -z "$package" || "$package" == \#* ]]; then
#         continue
#     fi
#     # Extract the package name without extras and version specifiers for checking
#     package_name=$(echo "$package" | sed 's/\[.*\]//;s/[<>=].*//')
#     echo "Checking if $package is installed..."
#     if is_installed "$package_name"; then
#         echo "$package is already installed."
#     else
#         echo "$package is not installed. Installing..."
#         $PY_RUN -m pip install "$package"
#         # Check if the installation was successful
#         if is_installed "$package_name"; then
#             echo "$package installed successfully."
#         else
#             echo "Failed to install $package."
#         fi
#     fi
#     echo
# done < "$requirements_file"
echo "Dependency check and package installations complete."



# =====================================================================
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

