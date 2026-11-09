#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seo_check.py - ONE command for every SEO check (keyword/density + location uniqueness when the page is a location).

    python scripts/seo_check.py                          # every page
    python scripts/seo_check.py commercial-hvac-duct-cleaning   # just the page you name
    python scripts/seo_check.py --strict                 # exit 1 on any FAIL (default is warn-only)

The builder's SEO button runs the same checks live on whichever page you have open.
"""
import sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_audit as sa
import seo_local as sl

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SC = {"pass": 1.0, "info": 1.0, "warn": 0.5, "fail": 0.0}


def audit_all(ids):
    """Full report (incl. location checks) for each page id. Returns [report]. Pages with no content file are skipped."""
    hub, state, company = sl.brief_info()
    texts = {}
    for pid in sa.all_page_ids():
        fm, body = sa.split_front_matter((sa.ROOT / f"page_content_{pid}.md").read_text(encoding="utf-8", errors="ignore"))
        texts[pid] = sa.clean_text(body)
    out = []
    for pid in ids:
        r = sa.audit_page(pid)
        if not r:
            continue
        if r["page_type"] == "location":
            loc = sl.audit_location(pid, texts, hub, state, company)
            r["checks"] += loc["checks"]
            r["similarity"] = loc["similarity"]
            r["score"] = round(sum(SC[c["status"]] for c in r["checks"]) / len(r["checks"]) * 100)
        out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    ids = [a.page] if a.page else sa.all_page_ids()
    warns = fails = 0
    for r in audit_all(ids):
        sa.print_report(r)
        warns += sum(c["status"] == "warn" for c in r["checks"])
        fails += sum(c["status"] == "fail" for c in r["checks"])
    print("\n" + "=" * 78)
    print(f"SUMMARY: {len(ids)} page(s), {warns} warning(s), {fails} fail(s). Mode: WARN-only" + (" (--strict: fails exit 1)" if a.strict else ""))
    return 1 if (a.strict and fails) else 0


if __name__ == "__main__":
    sys.exit(main())
