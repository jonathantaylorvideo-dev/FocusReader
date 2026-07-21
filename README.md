# File Processing Pipeline

A small pipeline that validates JSON payload files and routes them into
processed or quarantined folders.

## Project structure

```
.
├── orchestrator.py       # process_inbox(): moves files from Inbox/ to Processed/ or Quarantine/
├── schema_validator.py   # validate_payload(): checks a JSON payload against the required schema
├── requirements.txt      # Python dependencies (pytest)
└── tests/
    └── test_pipeline.py  # tests for orchestrator.py and schema_validator.py
```

`orchestrator.py` expects three directories to exist at runtime, relative to
the working directory: `Inbox/`, `Processed/`, and `Quarantine/`. They are
not part of the repo (create them before running the pipeline).

## How it works

1. `schema_validator.validate_payload()` parses a payload string as JSON and
   checks it contains the required keys: `id`, `content_type`, `payload`.
2. `orchestrator.process_inbox()` reads every file in `Inbox/`, validates it,
   and moves it to `Processed/` on success (unless the payload sets
   `escalate`) or to `Quarantine/` otherwise.

## Running tests

```
pip install -r requirements.txt
pytest
```
