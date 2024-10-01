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
