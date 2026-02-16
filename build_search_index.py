#!/usr/bin/env python3
"""
New Doggerland — Governance Search Index Builder
=================================================
Run this script before publishing a GitHub release.
It extracts all .tex files from the governance stack,
strips LaTeX markup, and produces search_index.json
to attach as a release asset.

Usage:
    python build_search_index.py [--root PATH] [--version TAG] [--out FILE]

Defaults:
    --root     ./New_Doggerland_Governance_Docs_v0.5   (auto-detected)
    --version  auto-detected from folder name
    --out      ./search_index.json

Then attach to release:
    gh release upload v0.5.2 search_index.json --repo NewDoggerland/Core-Documents
"""

import re
import os
import json
import argparse
from datetime import date
from pathlib import Path


# ─── Document registry ───────────────────────────────────────────────────────
# Maps the 5-char file prefix (e.g. "10.00") to a human-readable label.
# Add new entries here as the stack grows.

FILE_LABELS = {
    "00.00": "External Summary",
    "05.20": "DAF Safety & Accountability",
    "05.50": "Grant Menu Appendix",
    "10.00": "Consolidated Governance Document",
    "10.10": "Schedule A — Material Action Thresholds",
    "10.20": "Schedule B — Emergency Scope Registry",
    "10.30": "Schedule C — Delegation & Approval Matrix",
    "10.40": "Schedule D — Logging & Audit Integrity Policy",
    "10.90": "Governance Schedule Index",
    "15.00": "Founder Vision",
    "15.50": "Governance Companion",
    "20.00": "Operational Manual",
    "20.50": "Operational Manual Companion",
    "30.10": "Board Vetting Process",
    "30.20": "Board Vetting Checklist",
}

CATEGORIES = {
    "Summary & Assurance":  ["00.00", "05.20", "05.50"],
    "Governance":           ["10.00", "10.10", "10.20", "10.30", "10.40", "10.90"],
    "Vision & Companions":  ["15.00", "15.50"],
    "Operations":           ["20.00", "20.50"],
    "Board Vetting":        ["30.10", "30.20"],
}

MIN_PARAGRAPH_LENGTH = 50


# ─── LaTeX stripping ─────────────────────────────────────────────────────────

def strip_latex(text: str) -> str:
    """Convert LaTeX source to plain searchable text."""
    # Remove comments
    text = re.sub(r'%.*', '', text)
    # Remove document structure
    text = re.sub(r'\\begin\{[^}]+\}', '', text)
    text = re.sub(r'\\end\{[^}]+\}', '', text)
    text = re.sub(r'\\documentclass.*', '', text)
    text = re.sub(r'\\usepackage.*', '', text)
    text = re.sub(r'\\maketitle', '', text)
    # Section headings -> readable markers
    text = re.sub(r'\\section\*?\{([^}]+)\}',       r'\n## \1\n', text)
    text = re.sub(r'\\subsection\*?\{([^}]+)\}',    r'\n### \1\n', text)
    text = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'\n#### \1\n', text)
    text = re.sub(r'\\paragraph\*?\{([^}]+)\}',     r'\n##### \1\n', text)
    # Unwrap formatting — keep content
    text = re.sub(r'\\textbf\{([^}]+)\}',    r'\1', text)
    text = re.sub(r'\\textit\{([^}]+)\}',    r'\1', text)
    text = re.sub(r'\\emph\{([^}]+)\}',      r'\1', text)
    text = re.sub(r'\\underline\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\texttt\{([^}]+)\}',    r'\1', text)
    # List items
    text = re.sub(r'\\item\s*', '• ', text)
    # Preserve hrefs
    text = re.sub(r'\\href\{[^}]+\}\{([^}]+)\}', r'\1', text)
    # Remove title/author/date blocks
    text = re.sub(r'\\title\{[^}]*\}', '', text)
    text = re.sub(r'\\author\{[^}]*\}', '', text)
    text = re.sub(r'\\date\{[^}]*\}', '', text)
    # Remove remaining commands with arguments
    text = re.sub(r'\\[a-zA-Z]+\*?\{[^}]*\}', '', text)
    # Remove bare commands
    text = re.sub(r'\\[a-zA-Z]+\*?', '', text)
    # Remove leftover braces
    text = re.sub(r'[{}]', '', text)
    # Normalise whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ─── Index builder ────────────────────────────────────────────────────────────

def build_index(root: Path, version: str) -> dict:
    entries = []
    files_processed = []

    for tex_file in sorted(root.rglob("*.tex")):
        if tex_file.stem.lower() in ("ndstyle", "style"):
            continue

        code = tex_file.name[:5]
        label = FILE_LABELS.get(code, tex_file.name)

        raw = tex_file.read_text(encoding="utf-8", errors="replace")
        clean = strip_latex(raw)

        paragraphs = [
            p.strip()
            for p in re.split(r'\n\n+', clean)
            if len(p.strip()) >= MIN_PARAGRAPH_LENGTH
        ]

        for para in paragraphs:
            entries.append({"id": code, "label": label, "text": para})

        files_processed.append({
            "code":       code,
            "label":      label,
            "file":       str(tex_file.relative_to(root)),
            "paragraphs": len(paragraphs),
        })
        print(f"  {code}  {label:<42}  {len(paragraphs)} passages")

    meta = {
        "version":       version,
        "generated":     str(date.today()),
        "repo":          "NewDoggerland/Core-Documents",
        "total_entries": len(entries),
        "documents":     files_processed,
        "categories":    CATEGORIES,
    }

    return {"meta": meta, "entries": entries}


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build governance search index")
    parser.add_argument("--root",    default=None, help="Path to governance docs root")
    parser.add_argument("--version", default=None, help="Release version tag e.g. v0.5.2")
    parser.add_argument("--out",     default="search_index.json", help="Output path")
    args = parser.parse_args()

    script_dir = Path(__file__).parent

    # Auto-detect root
    if args.root:
        root = Path(args.root)
    else:
        candidates = sorted(script_dir.glob("New_Doggerland_Governance_Docs_*"))
        root = candidates[-1] if candidates else script_dir

    if not root.exists():
        print(f"ERROR: Root not found: {root}")
        return 1

    # Auto-detect version from folder name
    if args.version:
        version = args.version
    else:
        match = re.search(r'v[\d.]+', root.name)
        version = match.group(0) if match else "unknown"

    out_path = Path(args.out)

    print(f"\nNew Doggerland — Governance Search Index Builder")
    print(f"{'─' * 52}")
    print(f"Root:    {root}")
    print(f"Version: {version}")
    print(f"Output:  {out_path}")
    print(f"{'─' * 52}\n")

    index = build_index(root, version)

    out_path.write_text(
        json.dumps(index, separators=(',', ':'), ensure_ascii=False),
        encoding="utf-8"
    )

    size_kb = out_path.stat().st_size // 1024
    print(f"\n{'─' * 52}")
    print(f"✓  {len(index['entries'])} passages indexed")
    print(f"✓  {len(index['meta']['documents'])} documents processed")
    print(f"✓  Written to {out_path}  ({size_kb} kb)")
    print(f"\nNext steps:")
    print(f"  1. Copy {out_path.name} to repo root")
    print(f"  2. git add search_index.json && git commit -m 'chore: update search index {version}'")
    print(f"  3. git tag {version} && git push origin {version}")
    print(f"\n  The discovery page fetches from raw.githubusercontent.com at the latest tag.")
    print(f"  No release asset attachment needed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
