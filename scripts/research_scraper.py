"""
=============================================================
  MULTI-PLATFORM RESEARCH SCRAPER — VERSION 2 (V2)
  Rank & Rent Pipeline — Optimized Research Tool
=============================================================

Platforms: Reddit | Quora | Google Reviews
V1 backup: quora_scraper_v1.py (untouched)

What's new in V2 vs V1:
  ✓ Platform-specific modifiers (Reddit, Quora, Google Reviews)
  ✓ No fallback queries — primary query format works correctly
  ✓ Self-contained query generation — no query_list.txt needed
  ✓ Resource blocking (images, fonts, media, ads) — faster loads
  ✓ Configurable delay profiles: fast (2–4s) or safe (5–10s)
  ✓ Explicit waits instead of fixed sleeps where possible
  ✓ Real-time incremental saving + auto-resume after Ctrl+C
  ✓ Reddit + Google Reviews scrapers added alongside Quora

First time setup (run once):
  pip install playwright
  python -m playwright install chromium

Usage:
  python research_scraper.py --niche "Sprinkler Repair" --city "Denton" --state "TX"
  python research_scraper.py --niche "Sprinkler Repair" --city "Denton" --state "TX" --platform Reddit
  python research_scraper.py --niche "Sprinkler Repair" --city "Denton" --state "TX" --profile safe
  python research_scraper.py --niche "Sprinkler Repair" --city "Denton" --state "TX" --headless
=============================================================
"""

import sys
import os
import time
import random
import argparse
import textwrap
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

# ── Force UTF-8 output on Windows ──────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: playwright not installed.")
    print("Run: pip install playwright && python -m playwright install chromium")
    sys.exit(1)

# =============================================================
#  CONFIGURATION — All tunable values in one place
# =============================================================

# Browser profile — saves cookies and login sessions between runs
BROWSER_PROFILE = str(Path(__file__).parent / "browser_profile")

# Seconds to wait for the user to solve a CAPTCHA manually
CAPTCHA_WAIT_TIMEOUT = 120

# Max characters saved per answer block (keeps output file manageable)
MAX_ANSWER_LENGTH = 2000

# ── Delay Profiles ────────────────────────────────────────────────────────
# Adjust these to balance speed vs. bot-detection risk.
# Values are (min_seconds, max_seconds) — a random value is chosen each time.
DELAY_PROFILES = {
    # FAST: ~3–5s between requests. Safer than 2–4s. Still 2× faster than V1.
    "fast": {
        "between_queries": (3.0, 5.0),   # Between each new Google search
        "between_pages":   (2.0, 4.0),   # Between opening individual result pages
        "after_load":      (1.0, 2.0),   # Short settle time after page navigation
    },
    # SAFE: ~5–10s (same as V1). More conservative, lower risk of blocking.
    "safe": {
        "between_queries": (5.0, 10.0),
        "between_pages":   (3.0, 6.0),
        "after_load":      (1.5, 3.0),
    },
}

# ── Resource Blocking ─────────────────────────────────────────────────────
# These are never needed for text scraping. Blocking them speeds up page loads.
BLOCKED_RESOURCE_TYPES = {"image", "font", "media"}

BLOCKED_DOMAINS = [
    "google-analytics.com",
    "googletagmanager.com",
    "doubleclick.net",
    "googlesyndication.com",
    "facebook.net",
    "hotjar.com",
    "clarity.ms",
    "segment.io",
    "mixpanel.com",
]

# =============================================================
#  PLATFORM-SPECIFIC MODIFIERS
#  These are the exact modifiers requested for V2.
#  Each modifier becomes one Google search query.
#  No fallback queries — the primary format works correctly.
# =============================================================

PLATFORMS = {
    "Reddit": {
        "site_op":   "site:reddit.com",
        "modifiers": [
            "problem",
            "issue",
            "broken",
            "recommend",
            "reviews",
            "scam",
            "avoid",
        ],
        "intent_map": {
            "problem":   "Pain Point",
            "issue":     "Pain Point",
            "broken":    "Pain Point",
            "recommend": "Decision",
            "reviews":   "Trust",
            "scam":      "Risk",
            "avoid":     "Risk",
        },
    },

    "Quora": {
        "site_op":   "site:quora.com",
        "modifiers": [
            "how much",
            "cost",
            "best",
            "recommend",
            "vs",
            "worth it",
        ],
        "intent_map": {
            "how much":  "Pricing",
            "cost":      "Pricing",
            "best":      "Commercial",
            "recommend": "Decision",
            "vs":        "Comparison",
            "worth it":  "Decision",
        },
    },

    "Google Reviews": {
        "site_op":   "",   # No site restriction — finds Yelp, BBB, Angi, etc.
        "modifiers": [
            "reviews",
            "1 star",
            "2 star",
            "complaints",
        ],
        "intent_map": {
            "reviews":    "Social Proof",
            "1 star":     "Complaints",
            "2 star":     "Complaints",
            "complaints": "Complaints",
        },
    },
}

# ── Valid result domains to accept per platform ──────────────────────────
PLATFORM_DOMAINS = {
    "Reddit":         ["reddit.com"],
    "Quora":          ["quora.com"],
    "Google Reviews": [
        "yelp.com", "bbb.org", "angi.com", "homeadvisor.com",
        "thumbtack.com", "houzz.com", "trustpilot.com", "sitejabber.com",
    ],
}

# =============================================================
#  QUERY GENERATION
#  Builds all Google search queries from the modifier lists above.
#  - Niche is NOT quoted (keeps results broad and findable — V1 improvement)
#  - Modifier IS quoted for precision
#  - No fallback queries generated
# =============================================================

def generate_queries(niche, city, state, platforms_to_run):
    """
    Generate 4 location variants per modifier per platform.

    Location levels (same as V1 query_generator.py):
      Level 1 — Niche only   : site:reddit.com sprinkler repair "problem"
      Level 2 — State abbrev : site:reddit.com sprinkler repair tx "problem"
      Level 3 — State full   : site:reddit.com sprinkler repair texas "problem"
      Level 4 — City         : site:reddit.com sprinkler repair denton "problem"

    4 variants × 17 modifiers = 68 queries total across all platforms.
    Niche is NOT quoted — keeps results broad and findable (V1 improvement kept).
    Modifier IS quoted — for precision.
    No fallback queries — one clean primary query per variant.
    """
    niche_l  = niche.lower()
    city_l   = city.lower()
    state_l  = state.lower()                      # e.g. "tx"
    state_full = _state_full_name(state.upper())  # e.g. "texas"
    queries  = []

    for platform_name in platforms_to_run:
        cfg        = PLATFORMS[platform_name]
        site_op    = cfg["site_op"]
        intent_map = cfg["intent_map"]
        prefix     = f"{site_op} " if site_op else ""

        for modifier in cfg["modifiers"]:
            intent = intent_map.get(modifier, "General")
            q = f'"{modifier}"'   # quoted modifier shorthand

            # ── 4 location variants per modifier ──────────────────────
            location_variants = [
                # Level 1: Niche only — most results, works for any city size
                (f"{prefix}{niche_l} {q}",                       "niche only"),
                # Level 2: State abbreviation — e.g. tx
                (f"{prefix}{niche_l} {state_l} {q}",             f"state: {state.upper()}"),
                # Level 3: State full name — e.g. texas
                (f"{prefix}{niche_l} {state_full} {q}",          f"state: {state_full}"),
                # Level 4: City — most specific, fewest results for small cities
                (f"{prefix}{niche_l} {city_l} {q}",              f"city: {city}"),
            ]

            for google_query, location_label in location_variants:
                queries.append({
                    "google_query":   google_query,
                    "platform":       platform_name,
                    "modifier":       modifier,
                    "intent":         intent,
                    "location_level": location_label,
                })

    return queries


# State abbreviation → full name lookup (add more as needed)
_STATE_NAMES = {
    "AL": "alabama", "AK": "alaska", "AZ": "arizona", "AR": "arkansas",
    "CA": "california", "CO": "colorado", "CT": "connecticut", "DE": "delaware",
    "FL": "florida", "GA": "georgia", "HI": "hawaii", "ID": "idaho",
    "IL": "illinois", "IN": "indiana", "IA": "iowa", "KS": "kansas",
    "KY": "kentucky", "LA": "louisiana", "ME": "maine", "MD": "maryland",
    "MA": "massachusetts", "MI": "michigan", "MN": "minnesota", "MS": "mississippi",
    "MO": "missouri", "MT": "montana", "NE": "nebraska", "NV": "nevada",
    "NH": "new hampshire", "NJ": "new jersey", "NM": "new mexico", "NY": "new york",
    "NC": "north carolina", "ND": "north dakota", "OH": "ohio", "OK": "oklahoma",
    "OR": "oregon", "PA": "pennsylvania", "RI": "rhode island", "SC": "south carolina",
    "SD": "south dakota", "TN": "tennessee", "TX": "texas", "UT": "utah",
    "VT": "vermont", "VA": "virginia", "WA": "washington", "WV": "west virginia",
    "WI": "wisconsin", "WY": "wyoming",
}

def _state_full_name(state_abbrev):
    """Convert state abbreviation to lowercase full name. Falls back to abbrev."""
    return _STATE_NAMES.get(state_abbrev.upper(), state_abbrev.lower())

# =============================================================
#  RESOURCE BLOCKER
#  Intercepts every browser request and aborts unnecessary ones.
#  Saves bandwidth and reduces page load time by 30–50%.
# =============================================================

# Domains that must NEVER be blocked — reCAPTCHA and Google auth depend on them.
BLOCKING_WHITELIST = [
    "google.com",
    "gstatic.com",
    "googleapis.com",
    "recaptcha.net",
]

def handle_route(route, request):
    """Block images, fonts, media, and analytics. Allow everything else.
    Whitelists Google/gstatic so reCAPTCHA widgets always render correctly.
    """
    req_url = request.url.lower()

    # Always allow Google and reCAPTCHA domains — never block them
    if any(domain in req_url for domain in BLOCKING_WHITELIST):
        route.continue_()
        return

    # Block by resource type (images, fonts, media)
    if request.resource_type in BLOCKED_RESOURCE_TYPES:
        route.abort()
        return

    # Block analytics/ad domains
    if any(domain in req_url for domain in BLOCKED_DOMAINS):
        route.abort()
        return

    route.continue_()

# =============================================================
#  CAPTCHA DETECTION & WAIT
# =============================================================

def is_captcha_present(page):
    """Google redirects to /sorry when blocking. That is the only reliable signal."""
    try:
        return "google.com/sorry" in page.url
    except Exception:
        return False


def wait_for_captcha_solve(page):
    """
    Handle Google's /sorry block page.
    Two possible states:
      A) Hard IP block — no CAPTCHA widget, just a message. Auto-waits 90s then retries.
      B) Solvable CAPTCHA — checkbox appears. Waits for user to solve it.
    """
    print()
    print("  " + "=" * 56)
    print("  GOOGLE BLOCK DETECTED")
    print("  Reloading page to check if a CAPTCHA checkbox appears...")
    print("  " + "=" * 56)

    # Reload once — if it's a solvable CAPTCHA, the checkbox will now render
    # (Google/gstatic assets are whitelisted so reCAPTCHA loads correctly)
    try:
        page.reload(wait_until="domcontentloaded", timeout=15000)
        time.sleep(3)
    except Exception:
        pass

    # Check if a reCAPTCHA checkbox is now visible
    has_captcha_widget = False
    try:
        has_captcha_widget = page.locator(
            "iframe[src*='recaptcha'], iframe[title*='reCAPTCHA'], #captcha-form"
        ).count() > 0
    except Exception:
        pass

    if has_captcha_widget:
        # Solvable CAPTCHA — wait for user to check the box
        print()
        print("  CAPTCHA checkbox visible — please solve it in the browser!")
        print("  Script continues automatically once solved.")
    else:
        # Hard IP block — no widget, just a message. Must wait it out.
        print()
        print("  !! HARD IP BLOCK — Google is not showing a CAPTCHA.")
        print("  !! This means requests were too fast. Waiting 90 seconds...")
        print("  !! TIP: Restart with --profile safe for slower, safer delays.")
        time.sleep(90)
        print("  Retrying after 90s pause...")
        return False   # Skip this query and move on

    start = time.time()
    while time.time() - start < CAPTCHA_WAIT_TIMEOUT:
        time.sleep(3)
        if not is_captcha_present(page):
            print("  CAPTCHA solved. Continuing...")
            time.sleep(1)
            return True

    print("  TIMEOUT — CAPTCHA not solved. Skipping query.")
    return False

# =============================================================
#  GOOGLE SEARCH — Returns platform-specific result URLs
# =============================================================

def google_search(page, query, platform_name, max_results, delays):
    """
    Search Google for a query and return valid URLs for the target platform.
    Single query only — no fallback (V1 fallback logic removed).
    """
    # OPT: removed &num=10 — requesting 10 results is a known bot signal to Google
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&hl=en"
    valid_domains = PLATFORM_DOMAINS[platform_name]

    try:
        # domcontentloaded is faster than waiting for full "load"
        page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
        time.sleep(random.uniform(*delays["after_load"]))

        if is_captcha_present(page):
            if not wait_for_captcha_solve(page):
                return []

        all_links  = page.locator("a").all()
        found_urls = []
        seen       = set()

        for link in all_links:
            try:
                href = link.get_attribute("href") or ""

                # Resolve Google's /url?q= redirect format
                if href.startswith("/url?") or "google.com/url" in href:
                    parsed = urlparse(href)
                    qs     = parse_qs(parsed.query)
                    href   = unquote(qs.get("q", [""])[0])

                if not href.startswith("https://"):
                    continue

                # STRICT domain check: URL must START WITH the correct domain.
                # Using 'in href' is too loose — Google's own sign-in / redirect
                # URLs often contain the target domain in a query parameter:
                # e.g. accounts.google.com/SignOutOptions?continue=quora.com/...
                # That would pass a loose 'in' check but lead to the wrong site.
                href_lower = href.lower()
                valid_prefixes = (
                    f"https://{d}" for d in valid_domains
                )
                if not any(href_lower.startswith(f"https://{d}") or
                           href_lower.startswith(f"https://www.{d}")
                           for d in valid_domains):
                    continue

                # Platform-specific path exclusions
                if platform_name == "Quora":
                    if any(x in href for x in ["/profile/", "/topic/", "/search?"]):
                        continue
                elif platform_name == "Reddit":
                    # Skip subreddit index pages, need individual threads
                    stripped = href.rstrip("/")
                    if stripped.count("/") <= 4:   # too short to be a thread
                        continue

                base = href.split("?")[0].rstrip("/")
                if len(base) > 25 and base not in seen:
                    seen.add(base)
                    found_urls.append(base)

                if len(found_urls) >= max_results:
                    break

            except Exception:
                continue

        print(f"    Found {len(found_urls)} {platform_name} URL(s)")
        for u in found_urls:
            print(f"      {u[:90]}")

        return found_urls

    except PlaywrightTimeout:
        print("    Timeout on Google search.")
        return []
    except Exception as e:
        print(f"    Google search error: {e}")
        return []

# =============================================================
#  SCRAPE: QUORA
# =============================================================

def scrape_quora_page(page, url, max_answers, delays):
    """Extract question + top answers from a Quora page."""
    result = {"url": url, "platform": "Quora", "question": "", "answers": [], "error": None}

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=25000)
        time.sleep(random.uniform(*delays["after_load"]))

        if is_captcha_present(page):
            if not wait_for_captcha_solve(page):
                result["error"] = "CAPTCHA not solved"
                return result

        # Extract question title
        question = ""
        for sel in ["h1", "[data-test='question-title']", ".q-text h1", "span.q-text"]:
            try:
                el = page.query_selector(sel)
                if el:
                    question = el.inner_text().strip()
                    if question:
                        break
            except Exception:
                continue
        result["question"] = question

        # Scroll to trigger lazy-loaded answers
        page.evaluate("window.scrollBy(0, 900)")
        try:
            page.wait_for_selector(".q-text, [class*='answer_text']", timeout=3000)
        except Exception:
            pass
        time.sleep(0.5)
        page.evaluate("window.scrollBy(0, 900)")
        time.sleep(0.3)

        # Extract answer blocks
        answers_found = []
        for sel in [".q-text", "[class*='answer_text']", "[class*='spacing_log_answer']",
                    "[class*='ui_qtext_render']", "div[class*='Answer']"]:
            try:
                els = page.query_selector_all(sel)
                if els:
                    for el in els[:max_answers]:
                        t = el.inner_text().strip()
                        if len(t) > 80:
                            answers_found.append(t[:MAX_ANSWER_LENGTH])
                    if answers_found:
                        break
            except Exception:
                continue

        # Fallback: largest text blocks on the page
        if not answers_found:
            seen_t = set()
            for el in (page.query_selector_all("div, p") or [])[:80]:
                try:
                    t = el.inner_text().strip()
                    if 100 < len(t) < 3000 and t[:50] not in seen_t:
                        seen_t.add(t[:50])
                        answers_found.append(t[:MAX_ANSWER_LENGTH])
                    if len(answers_found) >= max_answers:
                        break
                except Exception:
                    continue

        result["answers"] = answers_found

    except PlaywrightTimeout:
        result["error"] = "Page load timeout"
    except Exception as e:
        result["error"] = str(e)

    return result

# =============================================================
#  SCRAPE: REDDIT
# =============================================================

def scrape_reddit_page(page, url, max_answers, delays):
    """Extract thread title, post body, and top comments from a Reddit thread."""
    result = {"url": url, "platform": "Reddit", "question": "", "answers": [], "error": None}

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=25000)
        time.sleep(random.uniform(*delays["after_load"]))

        # Extract thread title
        title = ""
        for sel in ["h1", "[data-testid='post-title']", "shreddit-title", ".Post h1"]:
            try:
                el = page.query_selector(sel)
                if el:
                    title = el.inner_text().strip()
                    if title:
                        break
            except Exception:
                continue
        result["question"] = title

        # Scroll to load comments
        page.evaluate("window.scrollBy(0, 600)")
        try:
            page.wait_for_selector(
                "[data-testid='comment'], shreddit-comment, .Comment",
                timeout=4000
            )
        except Exception:
            pass
        time.sleep(0.5)

        # Extract post body + comments
        text_blocks = []
        seen_t = set()
        for sel in [
            "[data-testid='post-rtjson-content']",
            ".RichTextJSON-root",
            "[data-testid='comment']",
            "shreddit-comment",
            ".Comment",
            "p",
        ]:
            try:
                for el in (page.query_selector_all(sel) or [])[:max_answers + 5]:
                    t = el.inner_text().strip()
                    if len(t) > 40 and t[:50] not in seen_t:
                        seen_t.add(t[:50])
                        text_blocks.append(t[:MAX_ANSWER_LENGTH])
                    if len(text_blocks) >= max_answers:
                        break
                if text_blocks:
                    break
            except Exception:
                continue

        result["answers"] = text_blocks[:max_answers]

    except PlaywrightTimeout:
        result["error"] = "Page load timeout"
    except Exception as e:
        result["error"] = str(e)

    return result

# =============================================================
#  SCRAPE: GOOGLE REVIEWS (Yelp, BBB, Angi, HomeAdvisor, etc.)
# =============================================================

def scrape_reviews_page(page, url, max_answers, delays):
    """Extract review text from third-party review sites."""
    result = {"url": url, "platform": "Google Reviews", "question": "", "answers": [], "error": None}

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=25000)
        time.sleep(random.uniform(*delays["after_load"]))

        try:
            result["question"] = page.title().strip()[:120]
        except Exception:
            pass

        page.evaluate("window.scrollBy(0, 700)")
        time.sleep(0.5)

        # Try platform-specific selectors first, then fall back to generic
        review_selectors = [
            "[class*='raw__']", "p[class*='comment']",       # Yelp
            ".review-body", "[class*='review-text']",          # BBB
            ".reviews-review-text", "[data-testid='review-text']",  # Angi
            "[class*='ReviewCard']",                           # Thumbtack
            "div[itemprop='reviewBody']",                      # Schema.org
            "p",                                               # Generic fallback
        ]

        reviews = []
        seen_t  = set()
        for sel in review_selectors:
            try:
                for el in (page.query_selector_all(sel) or [])[:max_answers * 3]:
                    t = el.inner_text().strip()
                    if len(t) > 50 and t[:50] not in seen_t:
                        seen_t.add(t[:50])
                        reviews.append(t[:MAX_ANSWER_LENGTH])
                    if len(reviews) >= max_answers:
                        break
                if reviews:
                    break
            except Exception:
                continue

        result["answers"] = reviews

    except PlaywrightTimeout:
        result["error"] = "Page load timeout"
    except Exception as e:
        result["error"] = str(e)

    return result

# =============================================================
#  DISPATCHER — Routes URL to correct platform scraper
# =============================================================

def scrape_page(page, url, platform_name, max_answers, delays):
    if platform_name == "Quora":
        return scrape_quora_page(page, url, max_answers, delays)
    elif platform_name == "Reddit":
        return scrape_reddit_page(page, url, max_answers, delays)
    elif platform_name == "Google Reviews":
        return scrape_reviews_page(page, url, max_answers, delays)
    return {"url": url, "platform": platform_name, "question": "", "answers": [], "error": "Unknown platform"}

# =============================================================
#  INCREMENTAL SAVE — Writes one query result to disk immediately
# =============================================================

def append_result(result, output_path, niche):
    """Append one result to disk right after scraping. Ctrl+C safe."""
    file_exists = os.path.exists(output_path)
    lines = []

    if not file_exists:
        lines += [
            "=" * 70,
            "  MULTI-PLATFORM RESEARCH DATA — V2",
            f"  Niche   : {niche}",
            f"  Created : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 70,
            "",
            "HOW TO USE: Review each answer below. Copy useful insights,",
            "pain points, and customer language into your data.txt file.",
            "",
        ]

    lines += [
        "",
        "=" * 70,
        f"  PLATFORM : {result['platform']}",
        f"  QUERY    : {result['google_query']}",
        f"  MODIFIER : {result['modifier']}",
        f"  INTENT   : {result['intent']}",
        f"  LOCATION : {result.get('location_level', '')}",
        "=" * 70,
    ]

    if not result.get("pages"):
        lines.append("  (No results found for this query)")
    else:
        for i, pd in enumerate(result["pages"], 1):
            lines += ["", f"  PAGE {i}: {pd['url']}"]
            if pd.get("error"):
                lines.append(f"  Error : {pd['error']}")
                continue
            if pd.get("question"):
                lines += [f"  TITLE : {pd['question']}", ""]
            if pd.get("answers"):
                lines.append(f"  CONTENT ({len(pd['answers'])} blocks):")
                lines.append("  " + "-" * 50)
                for j, ans in enumerate(pd["answers"], 1):
                    lines.append(f"\n  [{j}] {ans}")
            else:
                lines.append("  (No content extracted)")

    lines.append("")
    with open(output_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))

# =============================================================
#  RESUME SUPPORT — Reads completed queries from output file
# =============================================================

def load_completed(output_path):
    """Return the set of query strings already saved in the output file WITH valid data."""
    completed = set()
    if not os.path.exists(output_path):
        return completed
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = content.split("PLATFORM :")
        for block in blocks[1:]:
            if "(No results found for this query)" not in block and "(No content extracted)" not in block:
                for line in block.splitlines():
                    if "QUERY    :" in line:
                        completed.add(line.split("QUERY    :")[1].strip())
                        break
    except Exception:
        pass
    return completed

# =============================================================
#  MAIN
# =============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Platform Research Scraper V2 — Rank & Rent Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python research_scraper.py --niche "Sprinkler Repair" --city "Denton" --state "TX"
          python research_scraper.py --niche "Plumbing" --city "Dallas" --state "TX" --profile safe
          python research_scraper.py --niche "Sprinkler Repair" --city "Denton" --state "TX" --platform Reddit
          python research_scraper.py --niche "Sprinkler Repair" --city "Denton" --state "TX" --headless

        Platforms (comma separated): Reddit, Quora, Google Reviews
        """)
    )

    parser.add_argument("--niche",       required=True, help='e.g. "Sprinkler Repair"')
    parser.add_argument("--city",        default="",    help='e.g. "Denton"')
    parser.add_argument("--state",       default="",    help='e.g. "TX"')
    parser.add_argument("--platform",    default="Quora,Reddit,Google Reviews",
                        help="Comma-separated platforms (default: all three)")
    parser.add_argument("--out",         default="research_data.txt", help="Output file")
    parser.add_argument("--max-results", type=int, default=3,  help="Max pages per query (default: 3)")
    parser.add_argument("--max-answers", type=int, default=5,  help="Max answer blocks per page (default: 5)")
    parser.add_argument("--batch-size",  type=int, default=15, help="Queries before 10min pause (default: 15)")
    parser.add_argument("--profile",     default="fast", choices=["fast", "safe"],
                        help="Delay profile: fast (2–4s) or safe (5–10s). Default: fast")
    parser.add_argument("--headless",    action="store_true", help="Run browser invisibly")

    args = parser.parse_args()

    # Validate selected platforms
    selected_platforms = [p.strip() for p in args.platform.split(",")]
    for p in selected_platforms:
        if p not in PLATFORMS:
            print(f"ERROR: Unknown platform '{p}'. Choose from: {', '.join(PLATFORMS.keys())}")
            sys.exit(1)

    delays = DELAY_PROFILES[args.profile]

    print()
    print("=" * 65)
    print("  MULTI-PLATFORM RESEARCH SCRAPER — V2")
    print(f"  Niche       : {args.niche}")
    print(f"  City/State  : {args.city}, {args.state}")
    print(f"  Platforms   : {', '.join(selected_platforms)}")
    print(f"  Modifiers   : Reddit({len(PLATFORMS['Reddit']['modifiers'])}) "
          f"Quora({len(PLATFORMS['Quora']['modifiers'])}) "
          f"Reviews({len(PLATFORMS['Google Reviews']['modifiers'])})")
    print(f"  Max results : {args.max_results} per query | Max answers: {args.max_answers} per page")
    print(f"  Delay profile: {args.profile.upper()} "
          f"({delays['between_queries'][0]}–{delays['between_queries'][1]}s between queries)")
    print(f"  Browser     : {'Headless (no window)' if args.headless else 'Visible window'}")
    print(f"  Output      : {args.out}")
    print("=" * 65)

    # ── Generate queries ──
    print(f"\n[Step 1] Generating queries...")
    queries = generate_queries(args.niche, args.city, args.state, selected_platforms)
    print(f"  Generated {len(queries)} queries total")
    for p in selected_platforms:
        count = sum(1 for q in queries if q["platform"] == p)
        mods  = PLATFORMS[p]["modifiers"]
        print(f"    {p}: {count} queries | modifiers: {', '.join(mods)}")

    # ── Resume: skip completed queries ──
    completed = load_completed(args.out)
    if completed:
        print(f"\n  Resuming: {len(completed)} queries already in {args.out}")

    remaining = [q for q in queries if q["google_query"] not in completed]
    print(f"  Queries remaining: {len(remaining)} of {len(queries)}")

    if not remaining:
        print(f"\n  All queries already completed in {args.out}!")
        sys.exit(0)

    # Rough runtime estimate
    avg_q = sum(delays["between_queries"]) / 2
    avg_p = sum(delays["between_pages"]) / 2
    est_s = len(remaining) * (avg_q + args.max_results * avg_p)
    print(f"  Estimated time: {int(est_s // 60)}–{int(est_s // 60) + 3} minutes ({args.profile} profile)")

    # ── Launch browser ──
    print(f"\n[Step 2] Launching Chrome browser...")
    os.makedirs(BROWSER_PROFILE, exist_ok=True)
    total_blocks = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=BROWSER_PROFILE,
            headless=args.headless,
            channel="chrome",
            # slow_mo removed — V2 controls timing explicitly per action
            viewport={"width": 1280, "height": 800},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu",                    # Not needed for scraping
                "--disable-background-networking",   # Reduces background requests
            ],
        )

        # Reuse the first tab — avoids creating a second background tab
        page = browser.pages[0] if browser.pages else browser.new_page()

        # Route all requests through the resource blocker
        page.route("**/*", handle_route)

        page.set_extra_http_headers({
            "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        })

        print(f"  Browser ready. Resource blocking: ON | Profile: {args.profile.upper()}\n")

        queries_run_in_batch = 0

        for i, q in enumerate(queries, 1):
            if q["google_query"] in completed:
                print(f"[{i}/{len(queries)}] SKIP: {q['google_query'][:70]}")
                continue

            print(f"\n[{i}/{len(queries)}] [{q['platform']}] [{q['intent']}] [{q['location_level']}]")
            print(f"  Query    : {q['google_query']}")
            print(f"  Modifier : \"{q['modifier']}\"")

            try:
                # Google search → extract platform URLs
                urls = google_search(page, q["google_query"], q["platform"], args.max_results, delays)

                pages_data = []
                for j, url in enumerate(urls, 1):
                    print(f"  [{j}/{len(urls)}] Scraping: {url[:80]}...")
                    time.sleep(random.uniform(*delays["between_pages"]))

                    pd = scrape_page(page, url, q["platform"], args.max_answers, delays)
                    pages_data.append(pd)

                    if pd.get("error"):
                        print(f"    ✗ {pd['error']}")
                    else:
                        title  = pd.get("question", "")[:55]
                        blocks = len(pd.get("answers", []))
                        print(f"    ✓ Title  : {title}")
                        print(f"    ✓ Blocks : {blocks} extracted")
                        total_blocks += blocks

                # Append to disk immediately — Ctrl+C safe
                append_result({
                    "platform":       q["platform"],
                    "google_query":   q["google_query"],
                    "modifier":       q["modifier"],
                    "intent":         q["intent"],
                    "location_level": q["location_level"],
                    "pages":          pages_data,
                }, args.out, args.niche)

                completed.add(q["google_query"])

            except KeyboardInterrupt:
                print("\n  [Script interrupted by user. Progress saved!]")
                break
            except Exception as query_err:
                print(f"  ✗ Query failed with error: {query_err}")
                continue

            # Delay before next query
            if i < len(queries):
                queries_run_in_batch += 1
                if queries_run_in_batch >= args.batch_size:
                    print(f"\n  [BATCH LIMIT] Reached {args.batch_size} queries.")
                    print("  [SLEEPING] Pausing for 10 minutes (600s) to avoid Google CAPTCHA blocks...")
                    time.sleep(600)
                    queries_run_in_batch = 0
                    print("  [RESUMING] Starting next batch...\n")
                else:
                    delay = random.uniform(*delays["between_queries"])
                    print(f"  → Saved. Next query in {delay:.1f}s...")
                    time.sleep(delay)

        try:
            browser.close()
        except Exception:
            pass

    print()
    print("=" * 65)
    print("  DONE!")
    print(f"  {total_blocks} content blocks saved to: {args.out}")
    print("  Review the file, then copy sections into data.txt")
    print("=" * 65)
    print()


if __name__ == "__main__":
    main()
