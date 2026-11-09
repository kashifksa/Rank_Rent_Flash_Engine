#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seo_audit.py - Phase 1: primary keyword + density audit (WARN-only by default).

Reads thresholds from seo_standards.json, content from page_content_[slug].md,
meta from page_meta_[slug].json and images from image_plan_[slug].json.
Writes seo_report_[slug].json per page and prints a summary.

    python scripts/seo_audit.py                 # audit every page
    python scripts/seo_audit.py --page homepage # one page
    python scripts/seo_audit.py --strict        # exit code 1 when any check FAILs (default WARN never fails)
    python scripts/seo_audit.py --no-write      # print only, do not write seo_report_*.json
"""
import sys, re, json, argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
STD_PATH = ROOT / "seo_standards.json"


# ----------------------------------------------------------------- parsing
def load_json(p, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def split_front_matter(md):
    m = re.match(r"^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n?", md)
    fm_text, body = (m.group(1), md[m.end():]) if m else ("", md)
    fm = {}
    for line in fm_text.splitlines():
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")
    return fm, body


def split_sections(body):
    """-> [(section_id, text)] using <!-- SECTION: id ... --> markers."""
    pat = r"<!--\s*SECTION:\s*([A-Za-z0-9_-]+)[^>]*-->"
    parts = re.split(pat, body)
    if len(parts) == 1:
        return [("main", body)]
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def clean_text(md):
    """Visible words only: drop comments, markdown syntax, table pipes, urls, html."""
    t = re.sub(r"<!--[\s\S]*?-->", " ", md)
    t = re.sub(r"```[\s\S]*?```", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"^[\s>#*\-+|:]+", " ", t, flags=re.M)
    t = re.sub(r"[|*_`~#>]", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"\u2014|\u2013", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def raw_tokens(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


FILLER = {"in", "of", "for", "and", "the", "a", "an", "to", "near", "at", "by", "on", "with", "your", "our", "&"}


def ft(toks):
    """Drop filler words so 'Air Duct Cleaning in Rockford' still matches 'air duct cleaning rockford'."""
    return [t for t in toks if t not in FILLER]


def ntok(text):
    return ft(raw_tokens(text))


tokens = ntok  # every keyword comparison below is filler-tolerant; raw_tokens() is used only for word totals


def count_phrase(toks, phrase_toks):
    n = len(phrase_toks)
    if n == 0 or len(toks) < n:
        return 0, []
    hits, i = [], 0
    while i <= len(toks) - n:
        if toks[i:i + n] == phrase_toks:
            hits.append(i)
            i += n  # non-overlapping
        else:
            i += 1
    return len(hits), hits


def headings(body):
    out = []
    for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*#*\s*$", body, flags=re.M):
        out.append((len(m.group(1)), clean_text(m.group(2))))
    return out


def variant_phrase(kw_toks, extra_drop, city, state):
    """Core phrase = keyword minus trailing location tokens (city/state from the page's own front matter)."""
    drop = set(extra_drop)
    for part in (city, state):
        drop.update(tokens(part or ""))
    core = list(kw_toks)
    while core and core[-1] in drop:
        core.pop()
    return core if 0 < len(core) < len(kw_toks) else []


# ------------------------------------------------------------------- audit
def status(ok, severity):
    return "pass" if ok else severity


def audit_page(pid, std=None):
    std = std or load_json(STD_PATH)
    md_path = ROOT / f"page_content_{pid}.md"
    if not md_path.exists():
        return None
    fm, body = split_front_matter(md_path.read_text(encoding="utf-8", errors="ignore"))
    meta = load_json(ROOT / f"page_meta_{pid}.json")
    plan = load_json(ROOT / f"image_plan_{pid}.json")
    ptype = fm.get("page_type") or meta.get("page_type") or "service"

    cfg = dict(std["primary_keyword"])
    cfg.update(std.get("page_type_overrides", {}).get(ptype, {}))
    sev = std.get("severity", {}).get("default", "warn")

    kw = (fm.get("primary_keyword") or meta.get("target_keyword") or "").strip()
    if not kw:  # fall back to the content map (e.g. blog posts that only carry a keyword in topical_authority.json)
        for tp in load_json(ROOT / "topical_authority.json").get("pages", []):
            if tp.get("page_id") == pid:
                kw = (tp.get("target_keyword") or "").strip()
                break
    report = {"page_id": pid, "page_type": ptype, "primary_keyword": kw, "checks": [], "sections": []}
    if not kw:
        report["checks"].append({"id": "keyword_defined", "status": "fail", "label": "Primary keyword defined",
                                 "detail": "No primary_keyword in front matter or page_meta."})
        return report

    brief = load_json(ROOT / "master_brief.json")
    city = fm.get("city") or meta.get("city") or brief.get("city", "")
    state = fm.get("state") or meta.get("state") or brief.get("state", "")
    kt = tokens(kw)
    plain = clean_text(body)
    raw = raw_tokens(plain)
    toks = ft(raw)
    total = len(raw)  # density denominator = every visible word (same as keyword_checker.py)
    exact, _ = count_phrase(toks, kt)

    core = variant_phrase(kt, cfg.get("variant_drop_trailing_tokens", []), city, state) if cfg.get("count_variants") else []
    core_total = 0
    if core:
        core_total, _ = count_phrase(toks, core)
    variant_only = max(core_total - exact, 0)  # core hits that are not already part of an exact match

    # density = occurrences / total words * 100 (same definition as keyword_checker.py)
    exact_d = exact / total * 100 if total else 0
    comb_d = (exact + variant_only) / total * 100 if total else 0
    report["density"] = {
        "total_words": total, "exact_count": exact, "exact_pct": round(exact_d, 2),
        "variant_phrase": " ".join(core), "variant_only_count": variant_only, "combined_pct": round(comb_d, 2),
        "target": [cfg["density_min"], cfg["density_target_max"]],
    }
    lo, hi, wmax, fmax = cfg["density_min"], cfg["density_target_max"], cfg["density_warn_max"], cfg["density_fail_max"]
    need_more = max(0, int(-(-lo * total // 100)) - (exact + variant_only))
    allow = int(hi * total // 100)
    if comb_d < lo:
        st = cfg.get("density_min_severity", sev)
        det = (f"{comb_d:.2f}% is under {lo}%. Informational only: Google has no density target, so write naturally "
               f"and just make sure the topic is clear (about {need_more} more mention(s) would reach {lo}%).")
    elif comb_d <= hi:
        st, det = "pass", f"{comb_d:.2f}% is within the natural range ({lo}-{hi}%)."
    elif comb_d <= wmax:
        st, det = "pass", f"{comb_d:.2f}% is slightly above {hi}% but under the {wmax}% warning line."
    elif comb_d <= fmax:
        st, det = sev, f"{comb_d:.2f}% exceeds {wmax}% and may read as stuffing. Replace about {max(0, exact + variant_only - allow)} mention(s) with synonyms or pronouns."
    else:
        st, det = "fail", f"{comb_d:.2f}% exceeds {fmax}% (keyword stuffing). Replace about {max(0, exact + variant_only - allow)} mention(s)."
    report["checks"].append({"id": "density", "status": st, "label": "Primary keyword density (exact + core variant)",
                             "detail": det + f" Exact only: {exact_d:.2f}% ({exact}x) of {total} words."})

    # ---- placement checks
    heads = headings(body)
    h1s = [t for lvl, t in heads if lvl == 1] or ([fm["h1"]] if fm.get("h1") else []) or ([meta["h1"]] if meta.get("h1") else [])
    h1_ok = bool(h1s) and count_phrase(tokens(h1s[0]), kt)[0] > 0
    if h1_ok:
        pos = tokens(h1s[0]).index(kt[0]) if kt[0] in tokens(h1s[0]) else 0
        h1_det = f"Found in H1: \"{h1s[0][:70]}\"" + ("" if pos <= 3 else " (not at the start, ideal is the first words)")
    else:
        h1_det = "Primary keyword not found in the H1." + (f" H1: \"{h1s[0][:70]}\"" if h1s else " No H1 found.")
    add = lambda cid, label, ok, det: report["checks"].append({"id": cid, "status": status(ok, sev), "label": label, "detail": det})
    required = set(cfg.get("required_in", []))

    if "h1" in required:
        add("h1", "Keyword in H1", h1_ok, h1_det)

    if "first_words" in required:
        win = cfg.get("first_words_window", 100)
        first_toks = ft(raw[:win])
        first_ok = count_phrase(first_toks, kt)[0] > 0 or (bool(core) and count_phrase(first_toks, core)[0] > 0)
        add("first_words", f"Keyword in first {win} words", first_ok,
            "Found." if first_ok else f"Not in the first {win} words of the body.")

    if "h2_any" in required:
        h2s = [t for lvl, t in heads if lvl == 2]
        h2_hits = [t for t in h2s if count_phrase(tokens(t), kt)[0] or (core and count_phrase(tokens(t), core)[0])]
        every = bool(h2s) and len(h2_hits) == len(h2s) and len(h2s) > 2
        add("h2_any", "Keyword in at least one H2 (not all)", bool(h2_hits) and not every,
            ("Found in %d of %d H2s." % (len(h2_hits), len(h2s))) if h2_hits and not every
            else ("Every H2 repeats the keyword (stuffing)." if every else "No H2 contains the keyword."))

    mt, md_ = meta.get("meta_title", ""), meta.get("meta_description", "")
    if "meta_title" in required:
        ok = count_phrase(tokens(mt), kt)[0] > 0 or (bool(core) and count_phrase(tokens(mt), core)[0] > 0)
        add("meta_title", "Keyword in meta title", ok and len(mt) > 0, "Keyword present." if ok else "Keyword missing from meta title.")
        lo_, hi_ = cfg["meta_title_min_chars"], cfg["meta_title_max_chars"]
        add("meta_title_len", "Meta title length (display is pixel-based, ~50-60 chars)", lo_ <= len(mt) <= hi_,
            f"{len(mt)} chars (target {lo_}-{hi_}). Google may rewrite titles that are too long or stuffed.")
    if "meta_description" in required:
        ok = count_phrase(tokens(md_), kt)[0] > 0 or (bool(core) and count_phrase(tokens(md_), core)[0] > 0)
        add("meta_description", "Keyword in meta description", ok and len(md_) > 0, "Keyword present." if ok else "Keyword missing from meta description.")
        lo_, hi_ = cfg["meta_description_min_chars"], cfg["meta_description_max_chars"]
        add("meta_description_len", "Meta description length (snippet candidate)", lo_ <= len(md_) <= hi_,
            f"{len(md_)} chars (target {lo_}-{hi_}).")

    if "slug" in required:
        slug = meta.get("slug") or fm.get("slug") or pid
        if ptype in cfg.get("slug_exempt_page_types", []) or slug in ("/", ""):
            report["checks"].append({"id": "slug", "status": "pass", "label": "Keyword in URL slug", "detail": "Exempt (homepage)."})
        else:
            st_ = set(tokens(slug.replace("-", " ")))
            core_set = set(core or kt)
            overlap = len(core_set & st_) / max(len(core_set), 1)
            add("slug", "Keyword in URL slug", overlap >= 0.75, f"Slug \"{slug}\" covers {int(overlap * 100)}% of the core keyword words.")

    if "conclusion" in required:
        last_text = ""
        for sid, txt in reversed(split_sections(body)):
            last_text = clean_text(txt)
            if last_text:
                break
        ok = count_phrase(tokens(last_text), kt)[0] > 0 or (bool(core) and count_phrase(tokens(last_text), core)[0] > 0)
        add("conclusion", "Keyword in conclusion / final CTA", ok, "Found." if ok else "Not in the last section.")

    # ---- image alts (1-2 images, not all)
    imgs = [i for i in (plan.get("images") or plan.get("page_images") or []) if not re.search(r"logo|favicon", (i.get("slot", "") + i.get("filename", "")), re.I)]
    alt_hits = [i for i in imgs if (count_phrase(tokens(i.get("alt_text") or i.get("alt") or ""), kt)[0] or
                                    (core and count_phrase(tokens(i.get("alt_text") or i.get("alt") or ""), core)[0]))]
    if imgs:
        n = len(alt_hits)
        ok = cfg["image_alt_min"] <= n <= max(cfg["image_alt_max"], 0) or (n >= 1 and n < len(imgs))
        ok = n >= cfg["image_alt_min"] and n <= cfg["image_alt_max"]
        add("image_alt", "Keyword in 1-2 image alts (not all)", ok, f"{n} of {len(imgs)} content image alts contain the keyword.")

    # ---- per-section density heatmap
    sec_limit = cfg["section_density_max"]
    for sid, txt in split_sections(body):
        sraw = raw_tokens(clean_text(txt))
        stoks = ft(sraw)
        if not sraw:
            continue
        e, _ = count_phrase(stoks, kt)
        c = count_phrase(stoks, core)[0] if core else 0
        total_hits = max(e, c)
        d = total_hits / len(sraw) * 100
        report["sections"].append({"section": sid, "words": len(sraw), "hits": total_hits, "pct": round(d, 2),
                                   "flag": "over" if (d > sec_limit and len(sraw) >= 40) else ""})
    over = [s["section"] for s in report["sections"] if s["flag"]]
    report["checks"].append({"id": "section_density", "status": status(not over, sev), "label": f"No section above {sec_limit}% keyword density",
                             "detail": "All sections OK." if not over else "Over limit: " + ", ".join(over)})

    structure_checks(pid, ptype, body, meta, brief, std, sev, report)
    link_checks(pid, ptype, body, brief, std, sev, report, kw, city, state)
    eeat_checks(pid, ptype, body, plan, std, sev, report)

    scores = {"pass": 1.0, "info": 1.0, "warn": 0.5, "fail": 0.0}
    report["score"] = round(sum(scores[c["status"]] for c in report["checks"]) / len(report["checks"]) * 100)
    return report


PHONE_RE = re.compile(r"\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b")


def digits(s):
    return re.sub(r"\D", "", s or "")


def norm_sid(sid):
    return re.sub(r"^\d+[_-]", "", sid).replace("_", "-")


def structure_checks(pid, ptype, body, meta, brief, std, sev, report):
    """Phase 3: word budgets, answer-first, heading order, AI-parseable elements, FAQ, schema + NAP consistency."""
    S = std.get("structure", {})
    if not S:
        return
    add = lambda cid, label, st, detail: report["checks"].append({"id": cid, "status": st, "label": label, "detail": detail})
    ok_st = lambda ok: "pass" if ok else sev
    sections = split_sections(body)

    # ---- word budgets (from the *_STRUCTURE.md tables)
    bud = S.get("budgets", {}).get(ptype, {})
    # count only sections the live site renders (merged ones such as the trust bar are part of the hero, not separate sections)
    sch = load_json(ROOT / "sections_schema.json").get("page_types", {}).get(ptype, {})
    live_ids = {s["id"] for s in sch.get("sections", []) if s.get("live", True)}
    live_secs = [(sid, txt) for sid, txt in sections if sid in live_ids] or sections
    counts = {norm_sid(sid): len(raw_tokens(clean_text(txt))) for sid, txt in live_secs}
    total = sum(counts.values())
    if "total" in bud:
        lo, hi = bud["total"]
        add("word_total", f"Total words within structure target ({lo}-{hi})", ok_st(lo <= total <= hi), f"{total} words.")
    bad = []
    for key, (lo, hi) in ((k, v) for k, v in bud.items() if k != "total"):
        if key in counts:
            n = counts[key]
            if (lo is not None and n < lo) or (hi is not None and n > hi):
                bad.append(f"{key} {n} (allowed {lo if lo is not None else 0}-{hi if hi is not None else 'any'})")
    if bud:
        add("word_sections", "Every section within its word budget", ok_st(not bad), "All sections in range." if not bad else "; ".join(bad[:5]) + (f" (+{len(bad) - 5} more)" if len(bad) > 5 else ""))

    # ---- answer-first: first real paragraph under the H1
    af = S.get("answer_first", {})
    first_para = ""
    for sid, txt in sections:
        for block in re.split(r"\n\s*\n", re.sub(r"<!--[\s\S]*?-->", "", txt)):
            b = block.strip()
            if b and not b.startswith(("#", "|", "-", "*", ">", "!")) and len(raw_tokens(b)) >= 8:
                first_para = clean_text(b)
                break
        if first_para:
            break
    n_fp = len(raw_tokens(first_para))
    if af:
        add("answer_first", f"Answer-first opening paragraph ({af['min_words']}-{af['max_words']} words)", ok_st(af["min_words"] <= n_fp <= af["max_words"]),
            f"First paragraph is {n_fp} words. AI Overviews and snippets favour a direct answer near the top.")

    # ---- heading order
    hs = [lvl for lvl, _ in headings(body)]
    h1n, skips, prev = hs.count(1), 0, 0
    for lvl in hs:
        if prev and lvl > prev + 1:
            skips += 1
        prev = lvl
    add("headings", "One H1, no skipped heading levels", ok_st(h1n <= 1 and skips == 0),
        f"{h1n} H1, {skips} skipped level(s)." + (" Sections may hold the H1 elsewhere." if h1n == 0 else ""))

    # ---- AI-parseable elements
    has_list = bool(re.search(r"^\s*(?:[-*]\s+\S|\d+\.\s+\S)", body, re.M))
    has_table = bool(re.search(r"^\s*\|.+\|\s*$", body, re.M))
    add("parseable", "Has a list or table (easy for AI answers to cite)", ok_st(has_list or has_table), f"list: {has_list}, table: {has_table}.")

    # ---- FAQ
    F = S.get("faq", {})
    faq_qs = []
    if ptype in F.get("page_types", []):
        for sid, txt in sections:
            if "faq" in sid:
                parts = re.split(r"^###\s+(.+)$", txt, flags=re.M)
                for i in range(1, len(parts), 2):
                    faq_qs.append((clean_text(parts[i]), len(raw_tokens(clean_text(parts[i + 1])))))
        avg = sum(w for _, w in faq_qs) / len(faq_qs) if faq_qs else 0
        add("faq", f"FAQ has {F['min_questions']}+ questions with concise answers", ok_st(len(faq_qs) >= F["min_questions"] and avg <= F["max_avg_answer_words"]),
            f"{len(faq_qs)} questions, average answer {avg:.0f} words (max {F['max_avg_answer_words']}).")

    # ---- schema
    schema = meta.get("schema") or {}
    graph = schema.get("@graph") if isinstance(schema, dict) else (schema if isinstance(schema, list) else [])
    graph = graph or ([schema] if isinstance(schema, dict) and schema.get("@type") else [])
    types = set()
    for g in graph:
        t = g.get("@type")
        types.update(t if isinstance(t, list) else [t])
    exp = S.get("schema_expected", {}).get(ptype, [])
    missing = [" / ".join(opts) for opts in exp if not (set(opts) & types)]
    add("schema_types", "Structured data present for this page type", ok_st(bool(graph) and not missing),
        f"Found: {', '.join(sorted(t for t in types if t)) or 'none'}." + (f" Missing: {'; '.join(missing)}." if missing else ""))
    faq_node = next((g for g in graph if g.get("@type") == "FAQPage"), None)
    if faq_node is not None and ptype in F.get("page_types", []):
        sc = len(faq_node.get("mainEntity", []))
        add("schema_faq_match", "FAQ schema matches the visible FAQ", ok_st(sc == len(faq_qs)), f"Schema has {sc} questions, page shows {len(faq_qs)}. Schema must match what users see.")

    # ---- NAP consistency
    nap = brief.get("nap", {})
    bphone, bname, bsite = digits(nap.get("phone")), (nap.get("company_name") or "").strip(), (nap.get("website") or "").lower()
    host = lambda u: re.sub(r"^https?://(www\.)?", "", (u or "").lower()).split("/")[0]
    probs = []
    for g in graph:
        for node in [g] + ([g["provider"]] if isinstance(g.get("provider"), dict) else []):
            if node.get("telephone") and digits(node["telephone"]) not in (bphone, "1" + bphone):
                probs.append(f"schema phone {node['telephone']}")
            if node.get("@type") in ("HVACBusiness", "LocalBusiness", "Organization") and node.get("name") and bname and node["name"].strip() != bname:
                probs.append(f"schema name '{node['name']}'")
            if node.get("url") and bsite and host(node["url"]) != host(bsite):
                probs.append(f"schema url {node['url']}")
    page_phones = {digits(m.group(0)) for m in PHONE_RE.finditer(clean_text(body))}
    odd = [p for p in page_phones if p not in (bphone, "1" + bphone)]
    if odd:
        probs.append("page phone(s) " + ", ".join(sorted(odd)))
    street = re.split(r",", nap.get("address", ""))[0].strip()
    wrong_addr = bool(street) and bool(re.search(r"\b\d{3,5} [NSEW]\.? [A-Z][a-z]+ (?:Rd|Road|St|Street|Ave|Avenue|Blvd|Dr|Drive)\b", clean_text(body))) and street.lower() not in clean_text(body).lower()
    if wrong_addr:
        probs.append("a street address on the page differs from the brief")
    add("nap", "Name, address and phone match the brief (schema + page)", "pass" if not probs else "fail", "Consistent." if not probs else "Mismatch: " + "; ".join(probs[:4]))


LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")


def keyword_for(pid):
    md = ROOT / f"page_content_{pid}.md"
    if not md.exists():
        return "", "", ""
    fm, _ = split_front_matter(md.read_text(encoding="utf-8", errors="ignore"))
    meta = load_json(ROOT / f"page_meta_{pid}.json")
    brief = load_json(ROOT / "master_brief.json")
    kw = (fm.get("primary_keyword") or meta.get("target_keyword") or "").strip()
    if not kw:
        for tp in load_json(ROOT / "topical_authority.json").get("pages", []):
            if tp.get("page_id") == pid:
                kw = (tp.get("target_keyword") or "").strip()
    return kw, fm.get("city") or meta.get("city") or brief.get("city", ""), fm.get("state") or meta.get("state") or brief.get("state", "")


def split_kw(kw, city, state, extra):
    """keyword tokens -> (core tokens, location tokens). Location = this page's own city/state words."""
    loc = set(tokens(city or "")) | set(tokens(state or "")) | set(extra)
    t = tokens(kw)
    return {x for x in t if x not in loc}, {x for x in t if x in loc}


def resolve_link(href, live_files):
    h = href.split("#")[0].split("?")[0].strip()
    if not h or re.match(r"^(?:https?:|mailto:|tel:)", h):
        return None  # anchor-only or external
    h = h.strip("/")
    if h in ("", "index", "index.html"):
        return "homepage"
    h = re.sub(r"\.html?$", "", h)
    return h if h in live_files else "?" + h


def link_checks(pid, ptype, body, brief, std, sev, report, kw, city, state):
    """Phase 4: internal link integrity, anchor variety, cannibalization."""
    L = std.get("links", {})
    if not L:
        return
    add = lambda cid, label, st, detail: report["checks"].append({"id": cid, "status": st, "label": label, "detail": detail})
    ok_st = lambda ok: "pass" if ok else sev
    excluded = set(L.get("excluded_pages", []))
    live = {p for p in all_page_ids() if p not in excluded}
    planned = {tp.get("page_id") for tp in load_json(ROOT / "topical_authority.json").get("pages", []) if tp.get("page_id")} - live
    company = (brief.get("nap", {}).get("company_name") or "").strip().lower()

    sch = load_json(ROOT / "sections_schema.json").get("page_types", {}).get(ptype, {})
    live_ids = {s["id"] for s in sch.get("sections", []) if s.get("live", True)}
    secs = [(s, t) for s, t in split_sections(body) if s in live_ids] or split_sections(body)
    text = "\n\n".join(t for _, t in secs)
    links = []
    for m in LINK_RE.finditer(re.sub(r"<!--[\s\S]*?-->", "", text)):
        links.append((m.group(1).strip(), m.group(2).strip(), resolve_link(m.group(2).strip(), live)))
    internal = [(a, h, t) for a, h, t in links if t is not None]

    broken = [(a, h) for a, h, t in internal if t.startswith("?")]
    ghost = [(a, h) for a, h in broken if h.split("#")[0].strip("/").replace(".html", "") in planned]
    unknown = [x for x in broken if x not in ghost]
    if ghost:
        add("links_planned", "No links to planned-but-unbuilt pages", "fail", "Plain text only until live (log in pending_links.json): " + "; ".join(f"'{a}' -> {h}" for a, h in ghost[:4]))
    else:
        add("links_planned", "No links to planned-but-unbuilt pages", "pass", "None.")
    add("links_broken", "Every internal link points to a live page", "pass" if not unknown else "fail",
        "All resolve." if not unknown else "Broken: " + "; ".join(f"'{a}' -> {h}" for a, h in unknown[:4]))

    ctx = {t for a, h, t in internal if t and not t.startswith("?") and t != pid and t != "homepage" and a.strip().lower() != company}
    add("links_contextual", f"At least {L['min_contextual_links']} contextual links to other live pages", ok_st(len(ctx) >= L["min_contextual_links"]),
        f"{len(ctx)} linked page(s): {', '.join(sorted(ctx)) or 'none'}. Contextual links help users and spread relevance between related pages.")
    selfl = [a for a, h, t in internal if t == pid]
    add("links_self", "No links pointing to the same page", ok_st(not selfl), "None." if not selfl else f"Self-links: {', '.join(selfl[:3])}")

    anchors = [(a.lower(), t) for a, h, t in internal if a.strip().lower() != company]
    generic = sorted({a for a, _ in anchors if a in L.get("generic_anchors", [])})
    from collections import Counter
    same = [a for a, c in Counter(a for a, _ in anchors).items() if c > L["max_same_anchor"]]
    split_t = [a for a in {x for x, _ in anchors} if len({t for x, t in anchors if x == a}) > 1]
    probs = []
    if generic: probs.append("generic anchor(s): " + ", ".join(generic))
    if same: probs.append(f"anchor used more than {L['max_same_anchor']}x: " + ", ".join(same))
    if split_t: probs.append("same anchor for different pages: " + ", ".join(split_t))
    add("anchors", "Descriptive, varied anchor text", ok_st(not probs), "Good." if not probs else "; ".join(probs))

    # ---- cannibalization (this page's keyword vs every other live page)
    if kw:
        extra = std["primary_keyword"].get("variant_drop_trailing_tokens", [])
        core, loc = split_kw(kw, city, state, extra)
        clash = []
        for o in sorted(live):
            if o == pid:
                continue
            okw, ocity, ostate = keyword_for(o)
            if not okw:
                continue
            ocore, oloc = split_kw(okw, ocity, ostate, extra)
            if not core or not ocore:
                continue
            jac = len(core & ocore) / len(core | ocore)
            if jac >= L["cannibal_jaccard"] and (loc & oloc or (not loc and not oloc)):
                clash.append(f"{o} ({int(jac * 100)}% same topic)")
        add("cannibal", "Keyword does not compete with another page", ok_st(not clash), "Unique target." if not clash else "Same topic and place as: " + "; ".join(clash[:3]))
        if ptype == "blog":
            k = " " + kw.lower() + " "
            info = any(w in k for w in L.get("blog_informational", []))
            trans = [w for w in L.get("blog_transactional", []) if re.search(r"\b" + re.escape(w.strip()) + r"\b", k)]
            add("blog_intent", "Blog keyword is informational, not transactional", ok_st(info and not trans),
                ("Informational." if info else "No informational marker (how to, signs of, guide, what is, vs...).") + (f" Transactional words: {', '.join(trans)}." if trans else ""))
        if ptype == "location":
            hub = (brief.get("city") or "").lower()
            add("location_hub", "Location keyword targets the satellite city, not the hub (FIX 32)", "pass" if hub not in tokens(kw) else "fail",
                "Targets the satellite city." if hub not in tokens(kw) else f"Keyword contains hub city '{hub}'.")


EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2705\u2B50\u27A1\u2714\u274C]")  # NOT the plain text star U+2605 (CSS-style text stars are allowed)
QUOTE_RE = re.compile(r'^>\s*["\u201c](.+?)["\u201d]\s*$', re.M)
ATTR_RE = re.compile(r"^>\s*[-\u2013]\s+(.+?)\s*$", re.M)


def quote_texts(body):
    return [re.sub(r"\W+", " ", q.lower()).strip() for q in QUOTE_RE.findall(body)]


def image_facts(pid, filename):
    """Real file facts: (exists, size_kb, has_exif_gps). Same lookup rule as compile_builder_data.py (images/<page>/ else images/homepage/)."""
    d = ROOT / "images" / pid
    base = d if d.exists() else ROOT / "images" / "homepage"
    f = base / filename
    if not f.exists():
        return False, None, False
    gps = False
    try:
        from PIL import Image
        ex = Image.open(f).getexif()
        gps = bool(ex.get_ifd(0x8825))  # GPS IFD
    except Exception:
        gps = False
    return True, round(f.stat().st_size / 1024, 1), gps


def eeat_checks(pid, ptype, body, plan, std, sev, report):
    """Phase 5: first-hand experience, credentials, filler/superlatives, repetition, hard content rules, image QA, review authenticity."""
    E = std.get("eeat", {})
    if not E:
        return
    add = lambda cid, label, st, detail: report["checks"].append({"id": cid, "status": st, "label": label, "detail": detail})
    ok_st = lambda ok: "pass" if ok else sev
    plain = clean_text(body)
    rt = raw_tokens(plain)
    n = max(len(rt), 1)
    low = " " + plain.lower() + " "

    if ptype not in ("contact",):
        fp = set(E["first_person_words"])
        fp_n = sum(1 for t in rt if t in fp)
        units = "|".join(re.escape(u) for u in E["specific_units"])
        nums = r"(?:\d[\d,.]*|" + "|".join(E["number_words"]) + r")(?:[ -](?:" + "|".join(E["number_words"]) + r"))*"
        spec = re.findall(r"\b" + nums + r"[ -]?(?:" + units + r")\b|\bsince (?:19|20)\d\d\b|\b(?:19|20)\d\d\b", low)
        fp_r, sp_r = fp_n / n * 1000, len(spec) / n * 1000
        add("experience", "First-hand voice and concrete specifics (numbers, measurements, years)",
            ok_st(fp_r >= E["first_person_per_1000_min"] and sp_r >= E["specifics_per_1000_min"]),
            f"{fp_r:.1f} first-person words and {sp_r:.1f} concrete specifics per 1000 words (min {E['first_person_per_1000_min']} and {E['specifics_per_1000_min']}).")

    if ptype in E.get("credential_page_types", []):
        found = sorted({c for c in E["credential_terms"] if re.search(r"\b" + re.escape(c) + r"\b", low)})
        add("credentials", "Credentials or trust proof stated (certified, licensed, insured, BBB...)", ok_st(len(found) >= 1), f"Found: {', '.join(found) or 'none'}.")

    filler = [p for p in E["filler_phrases"] if p in low]
    add("filler", "No generic filler phrases", ok_st(len(filler) <= E["filler_max"]), "None." if not filler else "Found: " + ", ".join(filler[:5]))
    sup = []
    for pat in E["superlative_patterns"]:
        m = re.search(pat, plain, re.I)
        if m:
            sup.append(m.group(0).strip())
    add("superlatives", "No unsubstantiated superlatives or guarantees", ok_st(not sup), "None." if not sup else "Found: " + ", ".join(sup[:5]) + ". Back claims with proof or remove.")

    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", plain) if len(s.split()) >= 6]
    norm = [re.sub(r"\W+", " ", s.lower()).strip() for s in sents]
    from collections import Counter
    dup = [s for s, c in Counter(norm).items() if c > 1]
    k = E["repeat_opening_words"]
    openers = Counter(" ".join(s.split()[:k]) for s in norm)
    rep_open = [o for o, c in openers.items() if c >= E["repeat_opening_max"]]
    add("repetition", "No repeated sentences or templated openings", ok_st(not dup and not rep_open),
        "Varied." if not dup and not rep_open else ("Duplicate sentence(s): %d. " % len(dup) if dup else "") + (("Repeated opening: " + "; ".join(f"'{o}' x{openers[o]}" for o in rep_open[:3])) if rep_open else ""))

    hits = {}
    for label, pat in E["rule_patterns"].items():
        c = len(re.findall(pat, body_no_front(body), re.M | re.I))
        if c:
            hits[label] = c
    ec = len(EMOJI_RE.findall(body))
    if ec:
        hits["emoji"] = ec
    add("rules", "Hard content rules (no em dash, separators, emoji, placeholders, pricing)", "pass" if not hits else "fail",
        "Clean." if not hits else "Found: " + ", ".join(f"{k} x{v}" for k, v in hits.items()))

    I = E["images"]
    imgs = [i for i in (plan.get("images") or plan.get("page_images") or []) if not re.search(r"logo|favicon", i.get("slot", "") + i.get("filename", ""), re.I)]
    if imgs:
        probs = []
        alts = [(i.get("alt_text") or i.get("alt") or "").strip() for i in imgs]
        for i, a in zip(imgs, alts):
            nm = i.get("filename", "")
            exists, kb, gps = image_facts(pid, nm)
            if len(a) < I["alt_min_chars"] or a.lower() in I["generic_alts"]:
                probs.append(f"weak alt on {nm}")
            if re.search(r"\d", nm):
                probs.append(f"digits in filename {nm}")
            if not exists:
                probs.append(f"file missing: {nm}")
            else:
                if kb and kb > I["max_kb"]:
                    probs.append(f"{nm} is {kb} KB (max {I['max_kb']})")
                if i.get("geotag") and not gps:
                    probs.append(f"{nm} should be geotagged but has no GPS in the file")
        dupa = [a for a, c in Counter(alts).items() if a and c > 1]
        if dupa:
            probs.append("duplicate alt text")
        has_big = any(" KB " in p for p in probs)
        add("images", "Image QA: alt text, filenames, size, geotag", "pass" if not probs else ("fail" if has_big else sev), "All images OK." if not probs else "; ".join(probs[:4]) + (f" (+{len(probs) - 4} more)" if len(probs) > 4 else ""))

    qs = QUOTE_RE.findall(body)
    if qs:
        R = E["reviews"]
        attrs = ATTR_RE.findall(body)
        good = [a for a in attrs if len([p for p in a.split(",") if p.strip()]) >= 2]
        mine = set(quote_texts(body))
        shared = set()
        for o in all_page_ids():
            if o == pid:
                continue
            ob = split_front_matter((ROOT / f"page_content_{o}.md").read_text(encoding="utf-8", errors="ignore"))[1]
            shared |= mine & set(quote_texts(ob))
        probs = []
        if len(qs) < R["min_per_page_if_present"]:
            probs.append(f"only {len(qs)} review(s)")
        if R["attribution_required"] and len(good) < len(qs):
            probs.append(f"{len(qs) - len(good)} review(s) missing name + place")
        if shared:
            probs.append(f"{len(shared)} review(s) reused on other pages")
        add("reviews", "Reviews are attributed (name + place) and not reused across pages", ok_st(not probs),
            f"{len(qs)} reviews. " + ("OK. Replace sample text with real customer reviews before launch." if not probs else "; ".join(probs)))


def body_no_front(body):
    return body


def all_page_ids():
    ids = sorted(p.name[len("page_content_"):-3] for p in ROOT.glob("page_content_*.md"))
    return ids


ICON = {"pass": "PASS", "info": "INFO", "warn": "WARN", "fail": "FAIL"}


def print_report(r):
    print("\n" + "=" * 78)
    print(f"{r['page_id']}  ({r['page_type']})   keyword: \"{r['primary_keyword']}\"")
    if "density" in r:
        d = r["density"]
        print(f"  words {d['total_words']} | exact {d['exact_count']}x = {d['exact_pct']}% | "
              f"+variant \"{d['variant_phrase']}\" {d['variant_only_count']}x | combined {d['combined_pct']}% (target {d['target'][0]}-{d['target'][1]}%)")
    for c in r["checks"]:
        print(f"  [{ICON[c['status']]}] {c['label']}: {c['detail']}")
    hot = [s for s in r.get("sections", []) if s["pct"] > 0]
    if hot:
        print("  heatmap: " + ", ".join(f"{s['section']}={s['pct']}%" for s in hot))
    if "score" in r:
        print(f"  SEO keyword score: {r['score']}/100")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()

    std = load_json(STD_PATH)
    ids = [a.page] if a.page else all_page_ids()
    fails = warns = 0
    for pid in ids:
        r = audit_page(pid, std)
        if not r:
            print(f"skip {pid}: no page_content_{pid}.md")
            continue
        print_report(r)
        fails += sum(c["status"] == "fail" for c in r["checks"])
        warns += sum(c["status"] == "warn" for c in r["checks"])
        if not a.no_write:
            (ROOT / f"seo_report_{pid}.json").write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n" + "=" * 78)
    print(f"SUMMARY: {len(ids)} page(s), {warns} warning(s), {fails} fail(s). Mode: WARN-only" + (" (--strict: fails exit 1)" if a.strict else ""))
    return 1 if (a.strict and fails) else 0


if __name__ == "__main__":
    sys.exit(main())
