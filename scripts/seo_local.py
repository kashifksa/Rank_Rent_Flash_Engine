#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seo_local.py - Phase 2: location-page uniqueness + local-proof audit (doorway-page / scaled-content guard). WARN-only.

For every page_type == location page it checks:
  1. Similarity vs every other page (5-word shingle containment). High overlap = template swap = doorway risk.
  2. FIX 39: >=2 local landmarks and >=1 numbered highway / named thoroughfare for the satellite city.
  3. FIX 36: hub city must not appear in H2/H3 or the intro paragraph (brand name is ignored).
  4. Local proof: city-specific review, city in an image alt, neighbourhood names, city mentions per 1000 words.
  5. FIX 36 service-card parity: H3 cards in the services section must map to canonical Phase 1 services.

    python scripts/seo_local.py                # all location pages
    python scripts/seo_local.py --page air-duct-cleaning-loves-park-il
    python scripts/seo_local.py --strict       # exit 1 on any FAIL
"""
import sys, re, json, argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_audit as sa  # reuse parsing helpers

STD = {
    "shingle_size": 5, "similarity_warn": 0.30, "similarity_fail": 0.50,
    "min_landmarks": 2, "min_roads": 1, "min_city_mentions_per_1000": 4, "unique_body_min_words": 700,
}
STD.update(sa.load_json(ROOT / "seo_standards.json").get("location", {}))  # seo_standards.json is the single source of truth

ROAD_RE = re.compile(r"\b(?:Route|Rt\.?|IL|US|I|State Route|SR|Highway|Hwy|County Road|CR)[ -]?\d{1,3}[A-Z]?\b|"
                     r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)? (?:Road|Rd|Avenue|Ave|Boulevard|Blvd|Parkway|Pkwy|Highway|Drive|Street)\b")
LANDMARK_RE = re.compile(r"\b(?:[A-Z][A-Za-z.'&]+ ){0,3}(?:High School|Middle School|Elementary|Town Hall|Village Hall|City Hall|Library|Park District|"
                         r"Forest Preserve|Fairgrounds|Mall|Shopping Center|Plaza|Hospital|Museum|Golf Course|Community Center|"
                         r"Recreation Center|Sports Complex|Speedway|Ice Arena|Airport|Courthouse|Fire Station|Police Department)\b|"
                         r"\b[A-Z][a-z]+ (?:Park|Preserve|Lake|River|Creek|Heights|Village|Estates|Hills|Grove|Crossing)\b")


def shingles(text, n):
    t = sa.raw_tokens(text)
    return {" ".join(t[i:i + n]) for i in range(max(0, len(t) - n + 1))}


def brief_info():
    b = sa.load_json(ROOT / "master_brief.json")
    nap = b.get("nap", {})
    return b.get("city", ""), b.get("state", ""), nap.get("company_name", "")


def canonical_services():
    ta = sa.load_json(ROOT / "topical_authority.json")
    out = []
    for p in ta.get("pages", []):
        if p.get("page_type") == "service" and p.get("phase", 1) == 1:
            out.append(p.get("parent_service") or p.get("h1_title") or p.get("page_id", "").replace("-", " "))
    # The primary service lives on the homepage (FIX 32), so its card is also canonical (it routes to #contact, not an inner page).
    hp = ROOT / "page_content_homepage.md"
    if hp.exists():
        _, hbody = sa.split_front_matter(hp.read_text(encoding="utf-8", errors="ignore"))
        grid = next((t for s, t in sa.split_sections(hbody) if "services-grid" in s), "")
        first = [t for l, t in sa.headings(grid) if l == 3]
        if first:
            out.append(first[0])
    return out


def audit_location(pid, texts, hub, state, company):
    md = (ROOT / f"page_content_{pid}.md").read_text(encoding="utf-8", errors="ignore")
    fm, body = sa.split_front_matter(md)
    city = fm.get("city", "")
    plan = sa.load_json(ROOT / f"image_plan_{pid}.json")
    meta = sa.load_json(ROOT / f"page_meta_{pid}.json")
    rep = {"page_id": pid, "city": city, "hub_city": hub, "checks": [], "similarity": []}
    add = lambda cid, label, status, detail: rep["checks"].append({"id": cid, "label": label, "status": status, "detail": detail})

    plain = sa.clean_text(body)
    raw = sa.raw_tokens(plain)
    n = STD["shingle_size"]
    mine = shingles(plain, n)

    # 1. similarity vs every other page
    worst = 0.0
    for other, otext in texts.items():
        if other == pid:
            continue
        theirs = shingles(otext, n)
        shared = len(mine & theirs) / max(len(mine), 1)
        rep["similarity"].append({"page": other, "shared_pct": round(shared * 100, 1)})
        worst = max(worst, shared)
    rep["similarity"].sort(key=lambda x: -x["shared_pct"])
    top = rep["similarity"][0] if rep["similarity"] else {"page": "-", "shared_pct": 0}
    if worst >= STD["similarity_fail"]:
        st = "fail"
    elif worst >= STD["similarity_warn"]:
        st = "warn"
    else:
        st = "pass"
    add("similarity", "Unique vs other pages (doorway guard)", st,
        f"Highest overlap {top['shared_pct']}% with {top['page']} (warn {int(STD['similarity_warn'] * 100)}%, fail {int(STD['similarity_fail'] * 100)}%).")
    add("unique_words", f"Body has at least {STD['unique_body_min_words']} words", "pass" if len(raw) >= STD["unique_body_min_words"] else "warn", f"{len(raw)} words.")

    # 2. FIX 39 landmarks + roads (satellite city only; hub-only names excluded)
    scrub = re.sub(re.escape(company), " ", plain, flags=re.I) if company else plain
    roads = sorted({m.group(0).strip() for m in ROAD_RE.finditer(scrub)})
    lms = sorted({m.group(0).strip() for m in LANDMARK_RE.finditer(scrub)} - {city})
    lms = [x for x in lms if x.lower() not in {"loves park", hub.lower()} and not x.lower().startswith(("our ", "the "))]
    add("landmarks", f"At least {STD['min_landmarks']} local landmarks (FIX 39)", "pass" if len(lms) >= STD["min_landmarks"] else "warn",
        f"{len(lms)} found: {', '.join(lms[:6]) or 'none'}. (Heuristic: confirm they are real places in {city}.)")
    add("roads", f"At least {STD['min_roads']} numbered highway / thoroughfare (FIX 39)", "pass" if len(roads) >= STD["min_roads"] else "warn",
        f"{len(roads)} found: {', '.join(roads[:6]) or 'none'}.")

    # 3. FIX 36 hub-city leak in H2/H3 and the intro
    heads = [(l, t) for l, t in sa.headings(body) if l in (2, 3)]
    leaks = [t for l, t in heads if hub and re.search(r"\b" + re.escape(hub) + r"\b", re.sub(re.escape(company), "", t, flags=re.I), re.I)]
    sections = sa.split_sections(body)
    intro = next((sa.clean_text(t) for s, t in sections if "intro" in s), "")
    intro_leak = bool(hub) and bool(re.search(r"\b" + re.escape(hub) + r"\b", re.sub(re.escape(company), "", intro, flags=re.I), re.I))
    add("hub_leak", f"No hub city ({hub}) in H2/H3 or intro (FIX 36)", "pass" if not leaks and not intro_leak else "fail",
        "Clean." if not leaks and not intro_leak else f"Hub city found in: {leaks[:3] or 'intro paragraph'}.")

    # 4. local proof
    cmentions = len(re.findall(re.escape(city), plain, re.I)) if city else 0
    per1k = cmentions / max(len(raw), 1) * 1000
    add("city_mentions", "City is named naturally and often enough", "pass" if per1k >= STD["min_city_mentions_per_1000"] else "warn",
        f"{cmentions} mentions ({per1k:.1f} per 1000 words, min {STD['min_city_mentions_per_1000']}).")
    proof = next((sa.clean_text(t) for s, t in sections if "proof" in s or "review" in s), "")
    add("local_review", "City-specific review present", "pass" if city and re.search(re.escape(city), proof, re.I) else "warn",
        "Found." if city and re.search(re.escape(city), proof, re.I) else f"No review text in the proof section mentions {city}.")
    imgs = [i for i in (plan.get("images") or []) if not re.search(r"logo|favicon", i.get("slot", "") + i.get("filename", ""), re.I)]
    city_imgs = [i for i in imgs if city and re.search(re.escape(city), i.get("alt_text", "") or i.get("alt", ""), re.I)]
    add("local_photo", "Real local photo with city in alt text", "pass" if city_imgs else "warn",
        f"{len(city_imgs)} of {len(imgs)} images mention {city}. Use genuine, geotagged job photos, not stock.")
    nbr = re.findall(r"\b(?:Colonial Village|Meadow|Heights|Estates|Subdivision|neighbou?rhood)\b", plain)
    add("neighborhoods", "Neighbourhood-level detail", "pass" if len(set(nbr)) >= 1 else "warn", f"{len(nbr)} neighbourhood references.")
    add("meta_city", "City in meta title and description",
        "pass" if city and re.search(re.escape(city), meta.get("meta_title", ""), re.I) and re.search(re.escape(city), meta.get("meta_description", ""), re.I) else "warn",
        f"title: \"{meta.get('meta_title', '')[:60]}\"")

    # 5. service card parity
    svc_sec = next((t for s, t in sections if "service" in s), "")
    cards = [t for l, t in sa.headings(svc_sec) if l == 3]
    canon = [set(sa.raw_tokens(c)) - sa.FILLER for c in canonical_services()]
    bad = []
    for c in cards:
        ct = set(sa.raw_tokens(c)) - sa.FILLER
        if not any(len(ct & k) / max(len(ct), 1) >= 0.67 for k in canon):
            bad.append(c)
    add("service_cards", "Service cards match canonical Phase 1 services (FIX 36)", "pass" if not bad else "warn",
        "All cards map to a Phase 1 service." if not bad else "Not canonical: " + "; ".join(bad))

    sc = {"pass": 1.0, "warn": 0.5, "fail": 0.0}
    rep["score"] = round(sum(sc[c["status"]] for c in rep["checks"]) / len(rep["checks"]) * 100)
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    hub, state, company = brief_info()

    ids = sa.all_page_ids()
    texts, locs = {}, []
    for pid in ids:
        fm, body = sa.split_front_matter((ROOT / f"page_content_{pid}.md").read_text(encoding="utf-8", errors="ignore"))
        texts[pid] = sa.clean_text(body)
        if (fm.get("page_type") or "") == "location":
            locs.append(pid)
    if a.page:
        locs = [a.page]
    if not locs:
        print("No location pages found.")
        return 0
    fails = warns = 0
    for pid in locs:
        r = audit_location(pid, texts, hub, state, company)
        print("\n" + "=" * 78)
        print(f"{pid}   city: {r['city']}   (hub: {hub})   score {r['score']}/100")
        for c in r["checks"]:
            print(f"  [{c['status'].upper()}] {c['label']}: {c['detail']}")
            fails += c["status"] == "fail"
            warns += c["status"] == "warn"
        print("  closest pages: " + ", ".join(f"{s['page']} {s['shared_pct']}%" for s in r["similarity"][:3]))
        if not a.no_write:
            (ROOT / f"seo_local_report_{pid}.json").write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n" + "=" * 78)
    print(f"SUMMARY: {len(locs)} location page(s), {warns} warning(s), {fails} fail(s). Mode: WARN-only" + (" (--strict: fails exit 1)" if a.strict else ""))
    return 1 if (a.strict and fails) else 0


if __name__ == "__main__":
    sys.exit(main())

