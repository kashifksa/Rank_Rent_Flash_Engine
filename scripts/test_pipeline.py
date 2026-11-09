#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_pipeline.py - proves the pipeline works on a BRAND NEW niche/city with zero per-site edits.

Builds a throw-away project (gutter cleaning, Springfield IL: nothing to do with the real project), then checks:
  1. build_meta creates page_meta for every page type (blog included), FAQ schema == visible FAQ, NAP comes from the brief
  2. the gate passes on clean content and build_meta is idempotent
  3. the gate BLOCKS: em dash + price, link to an unbuilt page, wrong phone number, hub city in a location heading
  4. the shipped scripts contain no niche/city-specific strings

    python scripts/test_pipeline.py
"""
import sys, os, re, json, shutil, random, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC_ROOT = HERE.parent
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails = []


def check(name, ok, extra=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" -> " + str(extra)[:300]) if extra and not ok else ""))
    if not ok:
        fails.append(name)


VOCAB = ("ladder downspout shingle fascia debris leaf sealant bracket elbow overflow drainage foundation roofline sediment bucket scoop "
         "hose flush pitch slope fastener mesh screen gutter trough soffit eave granule moss algae sparrow acorn maple oak storm "
         "spring autumn crew truck safety harness inspect photograph report estimate schedule arrive tidy bag haul sweep rinse "
         "clear block clog seam rivet hanger spike ferrule corner miter outlet splash apron flashing valley dormer chimney").split()


def words(seed, n):
    r = random.Random(seed)
    return " ".join(r.choice(VOCAB) for _ in range(n))


def make_project(root):
    brief = {
        "project_name": "Springfield Gutter Pros", "niche": "Gutter Cleaning", "city": "Springfield", "state": "IL",
        "nap": {"company_name": "Springfield Gutter Pros", "address": "200 N Main St, Springfield, IL 62701", "phone": "(217) 555-0188",
                "email": "hello@springfieldgutterpros.com", "website": "https://springfieldgutterpros.com"},
        "credentials": ["Fully Licensed and Insured", "Angi Super Service Award"], "external_phones": [],
    }
    pages = [
        ("homepage", "homepage", "gutter cleaning springfield", "Springfield", "Gutter Cleaning in Springfield, IL"),
        ("gutter-guard-installation", "service", "gutter guard installation springfield il", "Springfield", "Gutter Guard Installation in Springfield, IL"),
        ("gutter-cleaning-chatham-il", "location", "gutter cleaning chatham il", "Chatham", "Gutter Cleaning in Chatham, IL"),
        ("how-to-clean-gutters-safely", "blog", "how to clean gutters safely", "Springfield", "How to Clean Gutters Safely From the Ground"),
        ("about", "about", "springfield gutter company", "Springfield", "About Springfield Gutter Pros"),
        ("contact", "contact", "contact springfield gutter pros", "Springfield", "Contact Springfield Gutter Pros"),
    ]
    topical = {"pages": [{"page_id": p[0], "page_type": p[1], "target_keyword": p[2], "phase": 1} for p in pages] +
               [{"page_id": "gutter-cleaning-rochester-il", "page_type": "location", "target_keyword": "gutter cleaning rochester il", "phase": 2}]}
    (root / "master_brief.json").write_text(json.dumps(brief, indent=2), encoding="utf-8")
    (root / "topical_authority.json").write_text(json.dumps(topical, indent=2), encoding="utf-8")
    schema = json.loads((SRC_ROOT / "sections_schema.json").read_text(encoding="utf-8"))["page_types"]
    for pid, ptype, kw, city, h1 in pages:
        fm = [f'title: "{h1}"', f'slug: "{"/" if pid == "homepage" else pid}"', f'page_type: "{ptype}"', 'niche: "Gutter Cleaning"',
              f'city: "{city}"', 'state: "IL"', f'primary_keyword: "{kw}"']
        if ptype != "blog":  # the blog deliberately has NO meta: the pipeline must draft it
            fm += [f'meta_title: "{h1} | Springfield Gutter Pros"'[:75].replace("Springfield Gutter Pros | Springfield Gutter Pros", "Springfield Gutter Pros"),
                   f'meta_description: "{words(pid + "md", 18)} {kw} {words(pid + "md2", 6)}."']
        out = ["---"] + fm + ["---", ""]
        for s in schema[ptype]["sections"]:
            if not s.get("live", True):
                continue
            sid = s["id"]
            out.append(f"<!-- SECTION: {sid} -->")
            if s.get("render") == "hero" or sid in ("01_header", "01_contact_hero", "01_identity_hook"):
                out += [f"# {h1}", "", f"We {words(pid + sid, 8)} and {words(pid + sid + 'b', 22)}.", ""]
            elif "faq" in sid:
                out += [f"## {words(pid + sid + 'h', 3).title()} questions", ""]
                for i in range(5):
                    out += [f"### {words(pid + sid + str(i), 5).capitalize()}?", f"Our crew {words(pid + sid + 'a' + str(i), 18)}.", ""]
            else:
                out += [f"## {words(pid + sid + 'h', 3).title()}", "", f"Our team {words(pid + sid, 40)}. We {words(pid + sid + 'z', 30)}.", ""]
        (root / f"page_content_{pid}.md").write_text("\n".join(out), encoding="utf-8")


def run(root, *args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(root))


def main():
    tmp = Path(tempfile.mkdtemp(prefix="pipeline_test_"))
    try:
        (tmp / "scripts").mkdir()
        for f in ("seo_audit.py", "seo_local.py", "seo_check.py", "build_meta.py", "pipeline_gate.py"):
            shutil.copyfile(HERE / f, tmp / "scripts" / f)
        std = json.loads((SRC_ROOT / "seo_standards.json").read_text(encoding="utf-8"))
        std["links"]["excluded_pages"] = []
        (tmp / "seo_standards.json").write_text(json.dumps(std), encoding="utf-8")
        shutil.copyfile(SRC_ROOT / "sections_schema.json", tmp / "sections_schema.json")
        shutil.copyfile(SRC_ROOT / "validate_sections.py", tmp / "validate_sections.py")
        make_project(tmp)

        g = run(tmp, "scripts/pipeline_gate.py")
        check("gate PASSES on a fresh niche with clean content", g.returncode == 0, g.stdout[-900:] + g.stderr[-300:])
        metas = {p.stem.replace("page_meta_", ""): json.loads(p.read_text(encoding="utf-8")) for p in tmp.glob("page_meta_*.json")}
        check("page_meta created for all 6 pages (blog included)", len(metas) == 6, sorted(metas))
        blog = metas.get("how-to-clean-gutters-safely", {})
        types = {x.get("@type") for x in blog.get("schema", {}).get("@graph", [])}
        check("blog gets Article + FAQPage schema and a drafted meta flagged for review", {"Article", "FAQPage"} <= types and blog.get("meta_description") and blog.get("_drafts"), (types, blog.get("_drafts")))
        bad_faq = []
        for pid, m in metas.items():
            fa = [x for x in m["schema"]["@graph"] if x.get("@type") == "FAQPage"]
            md = (tmp / f"page_content_{pid}.md").read_text(encoding="utf-8")
            n_page = len(re.findall(r"^### .+\?$", md, re.M))
            if fa and len(fa[0]["mainEntity"]) != n_page:
                bad_faq.append(pid)
        check("FAQ schema question count == visible FAQ on every page", not bad_faq, bad_faq)
        svc = metas["gutter-guard-installation"]["schema"]["@graph"]
        tel = [x.get("provider", {}).get("telephone") for x in svc if x.get("@type") == "Service"]
        check("NAP in schema comes from the brief (+E.164 phone)", tel == ["+12175550188"], tel)
        check("canonical built from website + slug", metas["gutter-cleaning-chatham-il"]["canonical"] == "https://springfieldgutterpros.com/gutter-cleaning-chatham-il/", metas["gutter-cleaning-chatham-il"]["canonical"])
        r = run(tmp, "scripts/build_meta.py", "--check")
        check("build_meta is idempotent (second run changes nothing)", r.returncode == 0, r.stdout[-300:])

        svc_md = tmp / "page_content_gutter-guard-installation.md"
        original = svc_md.read_text(encoding="utf-8")
        svc_md.write_text(original + "\nOnly $99 flat-rate \u2014 call now. See [Rochester gutter cleaning](gutter-cleaning-rochester-il.html).\n", encoding="utf-8")
        g = run(tmp, "scripts/pipeline_gate.py")
        out = g.stdout
        check("gate BLOCKS price + em dash", g.returncode == 1 and "Hard content rules" in out, out[-500:])
        check("gate BLOCKS a link to a planned-but-unbuilt page", "planned-but-unbuilt" in out, out[-500:])
        svc_md.write_text(original, encoding="utf-8")

        c = tmp / "page_content_contact.md"
        orig_c = c.read_text(encoding="utf-8")
        c.write_text(orig_c + "\nCall us at (217) 555-9999 today.\n", encoding="utf-8")
        g = run(tmp, "scripts/pipeline_gate.py")
        check("gate BLOCKS a phone number that is not the brief's", g.returncode == 1 and "Name, address and phone" in g.stdout, g.stdout[-400:])
        c.write_text(orig_c, encoding="utf-8")

        l = tmp / "page_content_gutter-cleaning-chatham-il.md"
        orig_l = l.read_text(encoding="utf-8")
        l.write_text(re.sub(r"(<!-- SECTION: 03_services_overview -->\n## )", r"\1Springfield Hub ", orig_l), encoding="utf-8")
        g = run(tmp, "scripts/pipeline_gate.py")
        check("gate BLOCKS the hub city in a location heading", g.returncode == 1 and "hub city" in g.stdout.lower(), g.stdout[-400:])
        l.write_text(orig_l, encoding="utf-8")
        g = run(tmp, "scripts/pipeline_gate.py")
        check("gate passes again after the problems are fixed", g.returncode == 0, g.stdout[-400:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    bad = re.compile(r"rockford|loves park|winnebago|nadca|perryville|colonial village|dumpster|denton|cedar rapids", re.I)
    leaks = []
    for f in ("seo_audit.py", "seo_local.py", "seo_check.py", "build_meta.py", "pipeline_gate.py"):
        for i, line in enumerate((HERE / f).read_text(encoding="utf-8").splitlines(), 1):
            if bad.search(line):
                leaks.append(f"{f}:{i}")
    check("shipped scripts contain no niche/city-specific strings", not leaks, leaks)
    print("\nRESULT: " + ("ALL PASSED" if not fails else f"{len(fails)} FAILED"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

