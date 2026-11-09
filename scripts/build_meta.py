#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_meta.py - generates page_meta_[slug].json (schema + technical meta) from the written content and master_brief.json,
so schema can never drift from the page and every page type (blogs included) always ships meta + structured data.

  * FAQPage schema is rebuilt from the page's visible FAQ every run (cannot mismatch).
  * Business name / phone / address / url come from master_brief.json nap (one source of truth, cannot mismatch).
  * Service / Article / AboutPage / ContactPage / business nodes are created when missing; existing richer nodes are kept
    (only their NAP fields are re-synced).
  * Missing meta_description / meta_title are drafted and flagged in "_drafts" so a human reviews them.
  * Never touches the page content, never invents facts: everything comes from the page text or the brief.

    python scripts/build_meta.py                 # write page_meta for every page
    python scripts/build_meta.py <page-id>       # one page
    python scripts/build_meta.py --check         # report only, exit 1 if anything would change (CI / gate)
"""
import sys, re, json, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_audit as sa

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = sa.ROOT
BUSINESS_RE = re.compile(r"Business$|^LocalBusiness$|^Organization$")


def e164(phone):
    d = re.sub(r"\D", "", phone or "")
    return ("+1" + d) if len(d) == 10 else ("+" + d if d else "")


def parse_address(addr):
    """'200 N Main St, Springfield, IL 62701' -> PostalAddress (best effort, only fields we can read)."""
    parts = [p.strip() for p in (addr or "").split(",")]
    out = {"@type": "PostalAddress", "addressCountry": "US"}
    if parts and parts[0]:
        out["streetAddress"] = parts[0]
    if len(parts) >= 2:
        out["addressLocality"] = parts[1]
    if len(parts) >= 3:
        m = re.match(r"([A-Z]{2})\s*(\d{5})?", parts[2])
        if m:
            out["addressRegion"] = m.group(1)
            if m.group(2):
                out["postalCode"] = m.group(2)
    return out


def plain(md):
    return sa.clean_text(md)


def faq_pairs(body):
    pairs = []
    for sid, txt in sa.split_sections(body):
        if "faq" not in sid:
            continue
        parts = re.split(r"^###\s+(.+)$", txt, flags=re.M)
        for i in range(1, len(parts), 2):
            q, a = plain(parts[i]), plain(parts[i + 1])
            if q and a:
                pairs.append((q, a))
    return pairs


def first_h1(body):
    for lvl, t in sa.headings(body):
        if lvl == 1:
            return t
    return ""


def first_answer(body, limit=155):
    """Draft meta description: the opening answer paragraph, cut cleanly at a word boundary."""
    for sid, txt in sa.split_sections(body):
        for block in re.split(r"\n\s*\n", re.sub(r"<!--[\s\S]*?-->", "", txt)):
            b = block.strip()
            if b and not b.startswith(("#", "|", "-", "*", ">", "!")) and len(b.split()) >= 8:
                t = plain(b)
                if len(t) <= limit:
                    return t
                window = t[:limit]
                ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", window)]
                if ends and ends[-1] >= 70:
                    return window[:ends[-1]].strip()  # last complete sentence that fits
                return window.rsplit(" ", 1)[0].rstrip(",;:- ")  # no clean sentence end: word boundary, no fake punctuation
    return ""


def node_by_type(graph, t):
    for g in graph:
        ty = g.get("@type")
        if ty == t or (isinstance(ty, list) and t in ty):
            return g
    return None


def build(pid, brief, topical, std):
    md_path = ROOT / f"page_content_{pid}.md"
    fm, body = sa.split_front_matter(md_path.read_text(encoding="utf-8", errors="ignore"))
    meta_path = ROOT / f"page_meta_{pid}.json"
    old = sa.load_json(meta_path) if meta_path.exists() else {}
    meta = json.loads(json.dumps(old))  # deep copy
    nap = brief.get("nap", {})
    site = (nap.get("website") or "").rstrip("/")
    ptype = fm.get("page_type") or meta.get("page_type") or "service"
    slug = fm.get("slug") or meta.get("slug") or ("/" if pid == "homepage" else pid)
    drafts = set(meta.get("_drafts", []))

    kw = (fm.get("primary_keyword") or meta.get("target_keyword") or "").strip()
    if not kw:
        for tp in topical.get("pages", []):
            if tp.get("page_id") == pid:
                kw = (tp.get("target_keyword") or "").strip()
    h1 = first_h1(body) or meta.get("h1", "")
    company = nap.get("company_name", "")

    meta.setdefault("page_id", pid)
    meta["page_type"] = ptype
    meta["slug"] = slug
    if h1:
        meta["h1"] = h1
    if kw:
        meta["target_keyword"] = kw
    for k in ("meta_title", "meta_description"):  # the writer's front matter wins over anything generated
        if fm.get(k):
            meta[k] = fm[k]
            drafts.discard(k)
    if not meta.get("meta_title"):
        t = fm.get("title") or (f"{h1} | {company}" if h1 and company else h1)
        meta["meta_title"] = t
        drafts.add("meta_title")
    if not meta.get("meta_description"):
        meta["meta_description"] = first_answer(body)
        drafts.add("meta_description")
    meta["canonical"] = (site + "/" if slug in ("/", "") else f"{site}/{slug}/") if site else meta.get("canonical", "")
    secs = [(s, t) for s, t in sa.split_sections(body)]
    meta["word_count"] = sum(len(sa.raw_tokens(plain(t))) for _, t in secs)

    # ---------------- schema
    sch = meta.get("schema") or {}
    graph = sch.get("@graph") if isinstance(sch, dict) and "@graph" in sch else (sch if isinstance(sch, list) else ([sch] if isinstance(sch, dict) and sch.get("@type") else []))
    graph = [dict(g) for g in graph]
    fm_types = re.findall(r'^\s*-\s*"?([A-Za-z]+)"?\s*$', re.search(r"^schema_types:\s*\n((?:\s*-.*\n?)+)", md_path.read_text(encoding="utf-8", errors="ignore"), re.M).group(1), re.M) if re.search(r"^schema_types:", md_path.read_text(encoding="utf-8", errors="ignore"), re.M) else []
    biz_type = next((t for t in fm_types if BUSINESS_RE.search(t)), None)
    existing_biz = next((g for g in graph if any(BUSINESS_RE.search(str(t)) for t in ([g.get("@type")] if not isinstance(g.get("@type"), list) else g["@type"]))), None)
    biz_type = biz_type or (existing_biz or {}).get("@type") or "LocalBusiness"
    biz_id = f"{site}/#business" if site else "#business"

    biz_fields = {"name": company, "telephone": e164(nap.get("phone")), "url": site + "/" if site else "", "email": nap.get("email", ""), "address": parse_address(nap.get("address", ""))}
    page_city = fm.get("city") or brief.get("city", "")

    def sync_biz(node):
        for k, v in biz_fields.items():
            if v:
                node[k] = v
        node.setdefault("@id", biz_id)
        node.setdefault("areaServed", {"@type": "City", "name": brief.get("city", "")})
        return node

    if existing_biz is not None:
        sync_biz(existing_biz)
    elif ptype in ("homepage", "about", "contact"):
        graph.append(sync_biz({"@type": biz_type}))

    canon = meta["canonical"]
    wanted = {"service": ["Service"], "location": ["Service"], "blog": ["Article"], "about": ["AboutPage"], "contact": ["ContactPage"], "homepage": []}.get(ptype, [])
    for t in wanted:
        n = node_by_type(graph, t)
        if n is None:
            n = {"@type": t}
            graph.append(n)
        n.setdefault("@id", f"{canon}#{t.lower()}")
        if t == "Service":
            n.setdefault("name", h1)
            n.setdefault("serviceType", kw or h1)
            n.setdefault("description", meta["meta_description"])
            n["provider"] = {"@type": biz_type, "@id": biz_id, "name": company, "telephone": e164(nap.get("phone")), "url": site + "/" if site else ""}
            n.setdefault("areaServed", [{"@type": "City", "name": page_city}])
        elif t == "Article":
            n.setdefault("headline", h1)
            n.setdefault("description", meta["meta_description"])
            n["author"] = {"@type": "Organization", "name": company, "url": site + "/" if site else ""}
            n["publisher"] = {"@type": "Organization", "name": company, "url": site + "/" if site else ""}
            n["mainEntityOfPage"] = canon
        else:  # AboutPage / ContactPage
            n.setdefault("name", h1)
            n["url"] = canon

    pairs = faq_pairs(body)
    faq = node_by_type(graph, "FAQPage")
    if pairs:
        if faq is None:
            faq = {"@type": "FAQPage"}
            graph.append(faq)
        faq.setdefault("@id", f"{canon}#faq")
        faq["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
    elif faq is not None:
        graph.remove(faq)  # never ship FAQ schema for a FAQ that is not on the page

    for g in graph:  # keep provider NAP in sync on any node that has one
        pr = g.get("provider")
        if isinstance(pr, dict):
            pr["name"], pr["telephone"], pr["url"] = company or pr.get("name"), e164(nap.get("phone")) or pr.get("telephone"), (site + "/") if site else pr.get("url")
    meta["schema"] = {"@context": "https://schema.org", "@graph": graph}
    if drafts:
        meta["_drafts"] = sorted(drafts)
    elif "_drafts" in meta:
        del meta["_drafts"]
    return meta, old


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    brief = sa.load_json(ROOT / "master_brief.json")
    topical = sa.load_json(ROOT / "topical_authority.json")
    std = sa.load_json(ROOT / "seo_standards.json")
    if not brief.get("nap"):
        print("WARN: master_brief.json has no nap block; NAP fields will be skipped.")
    ids = [a.page] if a.page else [p for p in sa.all_page_ids() if p not in set(std.get("links", {}).get("excluded_pages", []))]
    changed = 0
    for pid in ids:
        try:
            meta, old = build(pid, brief, topical, std)
        except Exception as ex:  # one bad page must not hide the others
            print(f"ERROR {pid}: {ex}")
            changed += 1
            continue
        if json.dumps(meta, sort_keys=True) != json.dumps(old, sort_keys=True):
            changed += 1
            what = "created" if not old else "updated"
            print(f"{'WOULD ' if a.check else ''}{what} page_meta_{pid}.json" + (f"  (drafts to review: {', '.join(meta['_drafts'])})" if meta.get("_drafts") else ""))
            if not a.check:
                (ROOT / f"page_meta_{pid}.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            print(f"ok      page_meta_{pid}.json")
    print(f"\n{changed} file(s) {'would change' if a.check else 'written'}.")
    return 1 if (a.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
