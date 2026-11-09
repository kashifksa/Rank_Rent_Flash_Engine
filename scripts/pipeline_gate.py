#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pipeline_gate.py - the ONE step that must pass before a site is built or published. Works for any niche/city: it only reads
the project's own files (page_content_*.md, master_brief.json, topical_authority.json, seo_standards.json).

    python scripts/pipeline_gate.py                 # every page
    python scripts/pipeline_gate.py <page-id>       # one page (e.g. right after writing it)
    python scripts/pipeline_gate.py --no-meta       # skip the page_meta regeneration step
    python scripts/pipeline_gate.py --strict-warn   # warnings also block (default: only FAIL blocks)

Steps (stops at the first hard error):
  1. build_meta.py      -> schema + technical meta generated from the content and master_brief.json (cannot drift)
  2. validate_sections  -> every page uses the live section ids from sections_schema.json
  3. seo_check          -> keyword, structure, links, cannibalization, E-E-A-T, hard rules, image QA, location uniqueness
Exit code 0 = safe to build. 1 = fix the FAIL rows listed at the end.
"""
import sys, argparse, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seo_audit as sa
import seo_check

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = sa.ROOT


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?")
    ap.add_argument("--no-meta", action="store_true")
    ap.add_argument("--strict-warn", action="store_true")
    a = ap.parse_args()

    std = sa.load_json(ROOT / "seo_standards.json")
    excluded = set(std.get("links", {}).get("excluded_pages", []))
    ids = [a.page] if a.page else [p for p in sa.all_page_ids() if p not in excluded]
    if not ids:
        print("GATE: no page_content_*.md files found.")
        return 1

    print("=" * 72 + "\n  PIPELINE GATE\n" + "=" * 72)
    if not a.no_meta:
        meta_script = HERE / "build_meta.py"
        if meta_script.exists():
            r = run([sys.executable, str(meta_script)] + ([a.page] if a.page else []))
            lines = [l for l in r.stdout.splitlines() if l.strip() and not l.startswith("ok ")]
            print("1. page_meta (schema + meta generated from content + brief)")
            for l in lines:
                print("   " + l)
            if r.returncode != 0 and "ERROR" in r.stdout:
                print("GATE: build_meta.py reported errors.")
                return 1
        else:
            print("1. build_meta.py not found, skipped")
    vs = ROOT / "validate_sections.py"
    if vs.exists():
        r = run([sys.executable, str(vs)])
        print("2. validate_sections: " + (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"))
        if r.returncode != 0:
            print(r.stdout[-1500:])
            print("GATE FAILED: section ids do not match sections_schema.json.")
            return 1

    print("3. seo_check")
    reports = seo_check.audit_all(ids)
    fails, warns = [], 0
    for r in reports:
        f = [c for c in r["checks"] if c["status"] == "fail"]
        w = [c for c in r["checks"] if c["status"] == "warn"]
        warns += len(w)
        print(f"   {r['page_id']:46} score {r.get('score', 0):>3}   warn {len(w):>2}   fail {len(f):>2}")
        fails += [(r["page_id"], c) for c in f]
    drafts = []
    for pid in ids:
        mp = ROOT / f"page_meta_{pid}.json"
        if mp.exists():
            d = sa.load_json(mp).get("_drafts")
            if d:
                drafts.append((pid, d))
    if drafts:
        print("\n   Drafted by the pipeline, have a human review: " + "; ".join(f"{p}: {', '.join(d)}" for p, d in drafts))

    print("\n" + "=" * 72)
    if fails:
        print(f"GATE FAILED: {len(fails)} blocking issue(s)")
        for pid, c in fails:
            print(f"  [{pid}] {c['label']}: {c['detail']}")
        return 1
    if a.strict_warn and warns:
        print(f"GATE FAILED (--strict-warn): {warns} warning(s)")
        return 1
    print(f"GATE PASSED: {len(reports)} page(s), {warns} warning(s), 0 blocking issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
