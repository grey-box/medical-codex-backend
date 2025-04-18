# Grey-Box | Project Codex Backend

Project Codex is a rapid medical translation API that aims to provide translations for medical terminology and medications. The need for an easy to use translation tool arose during the Ukraine War in 2022 to help with the influx of medical supplies in any language other than Ukrainian. The goal of Project Codex is to provide a tool that is more reliable and transparent than a simple Google Translate without the complexity of searching medical databases manually. Currently there is limited support for translating between Ukrainian, Russian, French and English, but the goal is to expand this to many more languages.

Along with this Backend API, there are plans for a Telegram AI chatbot that would integrate with this translation service.

## How to Get Involved
If you would like to help with development please reach out [here on the Grey-Box website](https://www.grey-box.ca/contact/).

## Documentation
- [Development Installation](/docs/DEV_INSTALL.md)
- [Azure Installation](/docs/AZURE_INSTALL.md)

## License
- [Apache License Version 2.0](/LICENSE)

## Overview

This service provides APIs for:
- Language detection and management
- Manual translation of medical codes
- Fallback translation mechanisms

## API Endpoints

### Languages API

- `GET /languages/`: Retrieves available languages
  - Returns: 200 OK with list of available languages
  - Error: 500 Internal Server Error

- `GET /languages/test`: Retrieves test languages
  - Returns: 200 OK with list of test languages
  - Error: 500 Internal Server Error

### Manual Translation API

- `POST /manual_translation/`: Performs manual translation of medical codes
  - Returns: 201 Created with translation results
  - Error: 500 Internal Server Error

### Fallback Translation API

- `POST /fallback_translation/`: Performs fallback translation when primary methods fail
  - Returns: 201 Created with fallback translation results
  - Error: 500 Internal Server Error

## HTTP Status Codes

The API consistently returns appropriate HTTP status codes:

- `200 OK`: Successful GET requests
- `201 Created`: Successful POST requests that create new resources
- `500 Internal Server Error`: Server-side errors

## Getting Started

### Prerequisites

- Docker
- Python 3.8+

### Running Locally

For macOS:
```bash
./docker-run-macos.sh
```

For Windows:
```bash
.\docker-run-windows.ps1
```

## Development

To build the application locally:

For macOS:

```bash
./build_local.sh
```
For Windows:

```bash
.\build_local.ps1
```