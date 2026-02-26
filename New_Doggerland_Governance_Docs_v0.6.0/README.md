# New Doggerland — Governance Docs v0.6.0

This repository contains the **New Doggerland v0.6.0 governance and operations document stack**, written in LaTeX.

The stack is designed to be **mission-locked, capture-resistant, audit-native, and legible to external reviewers** (e.g., donors, DAFs, auditors), while clearly separating **binding authority** from **non-binding explanatory materials**.

## Start here

- Canonical map: MANIFEST.md
- Latest published snapshot: v0.6.0 (see Releases)

## How to read this repo

- **Authority comes only from the binding governance layer** (the Consolidated Governance Document and binding schedules/policies adopted under it).
- **Companion / vision / summaries are non-binding** and exist to improve clarity, orientation, and external legibility.
- **Operational manuals are execution documents** and must remain subordinate to the binding governance layer.
- If any conflict exists, **higher-order documents govern** (see the Consolidated Governance Document's hierarchy and derivation rules).

## Repository layout

### `00 summary/`
External-facing overview material intended to help readers understand the system quickly.

### `05 external assurance/`
DAF- and donor-facing assurance materials. Explanatory and packaging-oriented; **not** a source of authority.

### `10 governance/` (binding)
The constitutional core and binding schedules/policies that operationalize thresholds and controls.

### `15 governance companion/`
Non-binding explanatory companions, including the **Founder Vision** (non-binding; derived; confers no authority).

### `20 operational manual/`
Execution manual(s), written in IF/THEN/ELSE style and subordinate to governance.

### `25 o_m companion/`
Non-binding companion/explanation for the operational manual.

### `30 board vetting/`
Board selection / vetting process materials (binding only if explicitly adopted under governance).

> Note: Each folder includes its own `ndstyle.sty` for portability. Compiling from **inside** a folder is the simplest approach.

## How to compile

Compile any `.tex` file from within its folder.

### Option A: `latexmk` (recommended)
```bash
latexmk -pdf -interaction=nonstopmode "<filename>.tex"
```

### Option B: `pdflatex`
```bash
pdflatex -interaction=nonstopmode "<filename>.tex"
pdflatex -interaction=nonstopmode "<filename>.tex"
```

## Suggested reading order

1. `00 summary/` — External Summary
2. `10 governance/` — Consolidated Governance Document, then Schedules A–D
3. `15 governance companion/` — Governance Companion, then Founder Vision
4. `20 operational manual/` — Operational Manual, then OM Companion
5. `05 external assurance/` — DAF Safety & Accountability + Grant Menu

## Licensing

- **Current license (pre-operational):** CC BY-NC 4.0 (Attribution–NonCommercial).
- **Planned relicensing (post-operational):** Once New Doggerland is operational, this repository is intended to be relicensed under **CC BY 4.0** to maximize adoption and reuse.

### Name & branding
"New Doggerland" and any associated names/logos/marks are **not** licensed for reuse. Forks and derivatives must not represent themselves as New Doggerland or imply endorsement.

### Contributions
This repository is not accepting external contributions at this time.
