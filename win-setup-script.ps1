# FastAPI Python Library Setup for Windows Environments
# author: Nicholas Nabours
# date: 2024-10-10
#
# This script works best when used with the PowerShell Extension in
# VSCode. There is no signed certificate associated with the script
# so you may encounter permissions issues running the script that 
# require you to temporarily change group permissions for executing
# powershell scripts.
#
# Run this script to install all the python libraries and build the
# database file for the Codex-Backend application.
#
# If you do not wish to run the app using Windows, utilize the docker
# commands located in the README_ASU_Branch.md file.
#


# Enable error handling and script execution
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$api_requirements= "fastapi_backend/requirements.txt"

# Check if we're in the git repo
try {
    git rev-parse --is-inside-work-tree > $null 2>&1
}
catch {
    Write-Output "Git version control system required."
    Write-Output "Please clone the git repository from the Grey-Box Github site."
    Write-Output "(https://github.com/grey-box/medical-codex-backend)"
    exit 1
}

# Get the root of the repository
$repo_root = & git rev-parse --show-toplevel

# Setup the Database
& $repo_root"\build-database.ps1"


# Check if the backend API requirements.txt file exists
if (Test-Path "$repo_root/$api_requirements") {
    Write-Output "Found requirements.txt file."
}
else {
    Write-Output "The python file for the database does not exist: $api_requirements"
    Write-Output "(Contains python libs needed to setup db)"
    exit 10
}


# Get the path to the pip executable
$pip_paths = & where.exe pip 2> $null
if ($pip_paths) {
    foreach ($pip_path in $pip_paths) {
        # Get the pip version for this executable
        $output = & $pip_path --version 2>&1

        # Check if the output contains "pip (python 3)"
        if ($output -match "pip.*\(python 3") {
            #Write-Output "Valid Pip installation found at $pip_path"
            $valid_pip_path = $pip_path
            #$pipfound = $true
            break
        }
    }
}

# Install the API requirements
Write-Output "Installing requirements..."
try {
    & $valid_pip_path install -r "$repo_root/$api_requirements"
}
catch {
    Write-Output "Error occurred running: pip install -r $repo_root/$api_requirements"
    exit 11
}

Write-Output @"

*** NEXT STEPS ***:
1. Setup your '.env' file according to the template in the Repo (.env.template)

2. Make sure you install Docker if you don't already have it installed.

3. Then run the 'starup.ps1' Powershell scripts to start the FastAPI app on windows.

4. Use the 'test.http' commands to make test requests to the API in the docker container.
"@



