# medical-codex-backend

Medical codex backend

## Major Backlog Items

1. Define an API that is agnostic of the cloud service utilized.
2. Implement /translate endpoint.
    - Translate text selected by user.
    - Add 'Last Resort' translate from approved source (google, LLM, etc.).
3. Define and implement a reference table for translation.
4. Review SQLAlchemy ORM usage.
5. Set default vlaues for fuzzy-matching in a config file.
6. Define more precisely the conversion setps from raw, intermediate, to API ready data.
7. Update existing data sources.
8. Define and implement a reference table for fuzzy matching.
9. Configure DB so it is easy to add languages in the future.
10. Receive and log translations that need to be manually evaluated later.
11. Implement available langauges API enpoints.
12. Look for near matches using fuzzy-match algorithm.

## Running the App with Docker

### For Development
**Run these scripts from the root of the repo where the `compose.yaml` file is located.**

To start the app for development run:

`docker compose up --build --watch`

This will build the container according to the `Dockerfile` and then start the container. The `--watch` option watches the source code for changes and rebuilds/refreshes containers when files are updated. It doesn't seem to update files as described in the documentation without rebuilding the image first but you can see output from the FastAPI app without opening docker desktop.

Alternatively, you can run the two commands separately to achieve the same result:

`docker compose up --build -d`  
`docker compose watch`

The `-d` option starts the container in the background.

<hr>



