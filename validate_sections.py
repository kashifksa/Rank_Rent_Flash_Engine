#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_sections.py - checks every page_content_*.md against sections_schema.json.

Usage:  python validate_sections.py            (all pages)
        python validate_sections.py --page <slug>

ERROR   = marker id not in schema / required section missing / wrong order
WARNING = alias used (will be auto-renamed by the compiler) / section the live site skips
Exit code 1 if any ERROR.
"""
import re, sys, json, glob, argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
if not (ROOT / "sections_schema.json").exists() and (ROOT.parent / "sections_schema.json").exists():
    ROOT = ROOT.parent

SCHEMA = json.loads((ROOT / "sections_schema.json").read_text(encoding="utf-8"))["page_types"]
MARK = re.compile(r"<!--\s*SECTION:\s*([A-Za-z0-9_-]+)")
PTYPE = re.compile(r"^page_type:\s*(\w+)", re.M)


def load_topical_types():
    tp = ROOT / "topical_authority.json"
    out = {}
    if tp.exists():
        try:
            for p in json.loads(tp.read_text(encoding="utf-8")).get("pages", []):
                if p.get("page_id") and p.get("page_type"):
                    out[p["page_id"]] = p["page_type"]
        except Exception:
            pass
    return out


TOPICAL = load_topical_types()


def page_type_of(slug, text):
    t = TOPICAL.get(slug)
    if t in SCHEMA:
        return t
    m = PTYPE.search(text)
    if m and m.group(1) in SCHEMA:
        return m.group(1)
    if slug == "homepage":
        return "homepage"
    if slug in ("about", "contact"):
        return slug
    return "service"


def validate(md_path: Path):
    slug = md_path.stem.replace("page_content_", "")
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    ptype = page_type_of(slug, text)
    spec = SCHEMA[ptype]
    ids = [s["id"] for s in spec["sections"]]
    live = {s["id"] for s in spec["sections"] if s.get("live", True)}
    aliases = spec.get("aliases", {})
    found = MARK.findall(text)
    errors, warns = [], []

    if not found:
        errors.append("no <!-- SECTION: id --> markers found")
        return ptype, errors, warns

    canon_found = []
    for f in found:
        if f in ids:
            canon_found.append(f)
        elif f in aliases:
            warns.append(f"alias '{f}' should be '{aliases[f]}'")
            canon_found.append(aliases[f])
        elif spec.get("flexible"):
            canon_found.append(f)
        else:
            errors.append(f"unknown section id '{f}' (not in schema for '{ptype}')")

    for sid in ids:
        if sid in live and sid not in canon_found:
            if spec.get("flexible") and sid not in spec.get("required", []):
                continue
            errors.append(f"missing section '{sid}'")
    for f in canon_found:
        s = next((x for x in spec["sections"] if x["id"] == f), None)
        if s and not s.get("live", True):
            warns.append(f"section '{f}' is not rendered live (merged into {s.get('merged_into', 'hero')})")

    if not spec.get("flexible"):
        order = [i for i in ids if i in canon_found]
        got = [i for i in canon_found if i in ids]
        if order != got:
            errors.append("sections are out of the schema order")
    return ptype, errors, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    args = ap.parse_args()
    files = sorted(Path(ROOT).glob("page_content_*.md"))
    if args.page:
        files = [f for f in files if f.stem == f"page_content_{args.page}"]
    bad = 0
    for f in files:
        ptype, errors, warns = validate(f)
        status = "OK " if not errors else "ERR"
        print(f"[{status}] {f.stem.replace('page_content_', ''):<48} ({ptype})")
        for e in errors:
            print(f"        ERROR   {e}")
        for w in warns:
            print(f"        warning {w}")
        bad += 1 if errors else 0
    print(f"\n{len(files) - bad}/{len(files)} pages match sections_schema.json")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
