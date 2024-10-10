# Enable error handling and script execution
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$api_requirements= "fastapi_backend\requirements.txt"

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
if (Test-Path "$repo_root\$api_requirements") {
    Write-Output "Found requirements.txt file."
}
else {
    Write-Output "The python file for the database does not exist: $api_requirements"
    Write-Output "(Contains python libs needed to setup db)"
    exit 10
}

# Install the API requirements
Write-Output "Installing requirements..."
try {
    & $valid_pip_path install -r "$repo_root\$api_requirements"
}
catch {
    Write-Output "Error occurred running: pip install -r $api_requirements"
    exit 11
}

Write-Output @"
Setup your '.env' file according to the template in the Repo (.env.template)

Make sure you install Docker if you don't already have it installed.

Then run the 'build_local.ps1' and 'docker-run-windows.ps1' Powershell scripts.
These will build you docker container and then start the container.

Use the 'test.http' commands to make test requests to the API in the docker container.
"@



