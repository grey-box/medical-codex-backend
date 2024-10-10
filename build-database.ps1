# Enable error handling and script execution
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# List of Python scripts to run
$scripts = @(
    "data_manipulation\conn.py",
    "data_manipulation\read_compendium.py",
    "data_manipulation\read_who_essentials.py",
    "data_manipulation\read_wikidata.py",
    "data_manipulation\read_drugbank.py",
    "data_manipulation\read_fda_product_code_classification.py",
    "data_manipulation\read_fip.py",
    "data_manipulation\read_rxterms.py",
    "data_manipulation\read_utis_in_ua.py"
)

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

# Check if the `data_manipulation` directory exists
if (Test-Path "$repo_root\data_manipulation") {
    Write-Output "The data_manipulation subdirectory exists."
}
else {
    Write-Output "The data_manipulation subdirectory does not exist."
    exit 2
}

# Check for python requirements to setup db
$requirements = "$repo_root\data_manipulation\requirements.txt"
if (Test-Path $requirements) {
    Write-Output "Found requirements.txt file."
}
else {
    Write-Output "The python requirements.txt file for the database does not exist."
    Write-Output "(Contains python libs needed to setup db)"
    exit 3
}

# Check if Python is installed and find Pip installation
$valid_pip_path = ""
$pipfound = $false
$output = ""

$pip_paths = & where.exe pip 2> $null
if ($pip_paths) {
    foreach ($pip_path in $pip_paths) {
        # Get the pip version for this executable
        $output = & $pip_path --version 2>&1

        # Check if the output contains "pip (python 3)"
        if ($output -match "pip.*\(python 3") {
            Write-Output "Valid Pip installation found at $pip_path"
            $valid_pip_path = $pip_path
            $pipfound = $true
            break
        }
    }
}

# Check if Python is installed and find the Python executable
$valid_python_path = ""
$pyfound = $false
$output = ""

$python_paths = & where.exe python 2> $null
if ($python_paths) {
    foreach ($python_path in $python_paths) {
        # Get the Python version for this executable
        $output = & $python_path --version 2>&1

        # Check if the output contains "Python 3"
        if ($output -match "^Python 3") {
            Write-Output "Valid Python 3 installation found at $python_path"
            $valid_python_path = $python_path
            $pyfound = $true
            break
        }
    }
}


# If Python or Pip not installed, provide instructions and exit
if (-not $pipfound) {
    Write-Output "Pip is not installed."
    if (-not $pyfound) {
        Write-Output "Python is not installed."
        Write-Output "Please install the latest version of Python from the official website:"
        Write-Output "(https://www.python.org/downloads/)"
        Write-Output "After installation, please run this script again."
        exit 5
    }
    else {
        Write-Output "Python was found without Pip installed."
        Write-Output "Please install the latest version of Pip from the official website or reinstall Python:"
        Write-Output "(https://pip.pypa.io/en/stable/installation/)"
        exit 4
    }
}

if (-not $pyfound) {
    Write-Output "Python is not installed."
    Write-Output "Please install the latest version of Python from the official website:"
    Write-Output "(https://www.python.org/downloads/)"
    Write-Output "After installation, please run this script again."
    exit 5
}

# Display Python and Pip versions
Write-Output "Python version:"
& $valid_python_path --version
Write-Output "Pip version:"
& $valid_pip_path --version
Write-Output ""

# Check if all the required files are present
$file_not_found = $false
foreach ($script in $scripts) {
    if (-not (Test-Path "$repo_root\$script")) {
        Write-Output "File not found: $script"
        $file_not_found = $true
    }
}

# If files not found, exit with error code
if ($file_not_found) {
    exit 6
}

Write-Output "All DB files found for creating database..."
Write-Output ""

Write-Output "Installing requirements..."
try {
    & $valid_pip_path install -r $requirements
}
catch {
    Write-Output "Error occurred running: pip install -r \data_manipulation\requirements.txt"
    exit 7
}

Write-Output ""
Write-Output "DB requirements installed Successfully."

Write-Output "Setting up database..."
# Loop through the list of scripts and execute each one
foreach ($script in $scripts) {
    Write-Output "Running $script..."
    try {
        & $valid_python_path "$repo_root\$script"
    }
    catch {
        Write-Output "Error occurred running: $script"
        exit 8
    }
}

Write-Output ""
Write-Output "All scripts executed successfully. Check for Codex DB in \fastapi_backend\codex.db"

Write-Output "Database will now be available in fastapi_backend\codex.db"

# Database will now be available in fastapi_backend\codex.db