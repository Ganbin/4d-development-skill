#!/usr/bin/env python3
"""
Validates that all docs/ paths referenced in SKILL.md and references/*.md
actually exist on disk.

Usage:
    python scripts/validate-paths.py
"""

import re
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
skill_dir = script_dir.parent
docs_dir = skill_dir / "docs"
refs_dir = skill_dir / "references"

errors = []
warnings = []
checked = 0

def check_paths_in_file(filepath: Path):
    global checked
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"Cannot read {filepath}: {e}")
        return

    # Pattern 1: backtick paths like `docs/API/CollectionClass.md`
    for m in re.finditer(r"`(docs/[^`]+\.md)`", content):
        path = m.group(1)
        # Skip template/pattern paths with {placeholders}
        if "{" in path:
            continue
        full = skill_dir / path
        checked += 1
        if not full.exists():
            errors.append(f"{filepath.name}: broken path `{path}`")

    # Pattern 2: backtick directory paths like `docs/API/`
    for m in re.finditer(r"`(docs/[\w\-]+/)`", content):
        path = m.group(1)
        full = skill_dir / path
        checked += 1
        if not full.exists():
            errors.append(f"{filepath.name}: broken directory `{path}`")

    # Pattern 3: markdown links to references like [file.md](references/file.md)
    for m in re.finditer(r"\]\((references/[\w\-]+\.md)\)", content):
        path = m.group(1)
        full = skill_dir / path
        checked += 1
        if not full.exists():
            errors.append(f"{filepath.name}: broken ref link `{path}`")

    # Pattern 4: docs paths in Go Deeper sections without backticks
    for m in re.finditer(r"(?:^|\s)(docs/[\w\-/]+\.md)", content):
        path = m.group(1)
        full = skill_dir / path
        checked += 1
        if not full.exists():
            warnings.append(f"{filepath.name}: possibly broken path `{path}`")


print("=" * 60)
print("4D Skill v21 — Path Validation")
print("=" * 60)
print()

# Validate SKILL.md
skill_md = skill_dir / "SKILL.md"
if skill_md.exists():
    print(f"Checking SKILL.md...")
    check_paths_in_file(skill_md)
else:
    errors.append("SKILL.md not found!")

# Validate all reference files
print(f"Checking references/*.md...")
for ref_file in sorted(refs_dir.glob("*.md")):
    check_paths_in_file(ref_file)

# Report
print()
print(f"Paths checked: {checked}")
print()

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  ✗ {e}")
    print()

if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  ? {w}")
    print()

if not errors and not warnings:
    print("ALL PATHS VALID")

print()

# Additional checks
print("=" * 60)
print("Consistency Checks")
print("=" * 60)
print()

# Check all curated reference files are mentioned in SKILL.md
skill_content = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
curated_files = [
    "language-syntax.md", "data-types.md", "orda-modern.md",
    "query-patterns.md", "error-handling.md", "classic-patterns.md",
    "forms-and-ui.md", "web-and-rest.md", "manual-insights.md"
]
index_files = [
    "api-index.md", "commands-index.md", "concepts-index.md",
    "orda-index.md", "rest-index.md", "events-index.md",
    "form-objects-index.md", "webserver-index.md",
    "legacy-commands-index.md", "all-categories-index.md"
]

print("Curated files referenced in SKILL.md:")
for f in curated_files:
    found = f in skill_content
    status = "ok" if found else "MISSING"
    print(f"  {'✓' if found else '✗'} {f}: {status}")

print()
print("Index files referenced in SKILL.md:")
for f in index_files:
    found = f in skill_content
    status = "ok" if found else "MISSING"
    print(f"  {'✓' if found else '✗'} {f}: {status}")

print()

# Check Go Deeper sections exist in curated files
print("Go Deeper sections in curated files:")
for f in curated_files:
    fp = refs_dir / f
    if fp.exists():
        content = fp.read_text(encoding="utf-8")
        has_deeper = "Go Deeper" in content or "go deeper" in content.lower()
        print(f"  {'✓' if has_deeper else '✗'} {f}: {'ok' if has_deeper else 'MISSING Go Deeper section'}")

print()

# Line count audit
print("=" * 60)
print("Line Count Audit")
print("=" * 60)
print()
print(f"{'File':<35} {'Lines':>6} {'Status':>10}")
print("-" * 55)

skill_lines = len(skill_content.splitlines())
status = "ok" if skill_lines <= 500 else "OVER 500!"
print(f"{'SKILL.md':<35} {skill_lines:>6} {status:>10}")

for f in curated_files:
    fp = refs_dir / f
    if fp.exists():
        lines = len(fp.read_text(encoding="utf-8").splitlines())
        status = "ok" if lines <= 400 else "OVER 400!"
        print(f"{f:<35} {lines:>6} {status:>10}")

print()

# Summary
total_errors = len(errors)
if total_errors == 0:
    print("VALIDATION PASSED")
    sys.exit(0)
else:
    print(f"VALIDATION FAILED: {total_errors} error(s)")
    sys.exit(1)
