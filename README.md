# Medical Codex Backend

A FastAPI-based backend service for medical codex translation and language availability.

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