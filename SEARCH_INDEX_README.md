# search_index.json

This file is auto-generated. Do not edit it manually.

It is a plain-text extraction of all governance documents in this repository, used by the [Governance Discovery](https://newdoggerland.org/governance) page to power full-text search of the governance stack.

## How to update

Run this before publishing each new release:

```
python build_search_index.py
```

The script lives in the repo root. It reads all `.tex` files from `New_Doggerland_Governance_Docs_vX.X/`, strips LaTeX markup, and writes a fresh `search_index.json`.

Then upload the new `search_index.json` to the repo root (overwriting this file) and commit to `main`. The discovery page updates itself automatically.

## What it contains

- All governance documents, schedules, operational manuals, companion documents, and board vetting materials
- Extracted as plain-text paragraphs, one entry per passage
- Version and generation date recorded in the `meta` block at the top of the file

## Current version

v0.5.2 — 924 indexed passages across 15 documents.

Update this line when you publish a new release.
