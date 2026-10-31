"""
======================================================================
  KEYWORD DENSITY & HTML TAG COVERAGE CHECKER
  Rank & Rent Pipeline — Pre-Publish Quality Tool
======================================================================

HOW TO USE:
  1. Save your page HTML content to a .txt or .html file
  2. Run: python keyword_checker.py
  3. Enter your primary keyword when prompted
  4. Paste or provide the path to your HTML content
  5. Review the report before publishing

"""

import re
import sys
import os


def strip_html(html):
    """Remove all HTML tags and return plain text."""
    return re.sub(r'<[^>]+>', ' ', html)


def count_keyword(text, keyword):
    """Count keyword occurrences (case insensitive, whole phrase)."""
    pattern = re.escape(keyword.lower())
    return len(re.findall(pattern, text.lower()))


def check_tag(html, tag_pattern, keyword):
    """Check if keyword appears in any matched HTML tag content."""
    matches = re.findall(tag_pattern, html, re.IGNORECASE | re.DOTALL)
    found_in = []
    for match in matches:
        if keyword.lower() in match.lower():
            preview = match.strip()[:60].replace('\n', ' ')
            found_in.append(f'"{preview}..."')
    return found_in


def get_first_paragraph_text(html, keyword):
    """Check if keyword appears in the first <p> tag."""
    first_p = re.search(r'<p[^>]*>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)
    if first_p:
        text = strip_html(first_p.group(1))
        words = text.split()[:100]  # first 100 words
        snippet = ' '.join(words)
        return keyword.lower() in snippet.lower()
    return False


def get_last_paragraph_text(html, keyword):
    """Check if keyword appears in the last <p> tag."""
    all_p = re.findall(r'<p[^>]*>(.*?)</p>', html, re.IGNORECASE | re.DOTALL)
    if all_p:
        last = strip_html(all_p[-1])
        return keyword.lower() in last.lower()
    return False


def analyze(html, keyword):
    """Run full keyword density and tag coverage analysis."""

    plain_text = strip_html(html)
    words = plain_text.split()
    total_words = len(words)
    kw_occurrences = count_keyword(plain_text, keyword)

    density = (kw_occurrences / total_words * 100) if total_words > 0 else 0
    target_min = 0.5
    target_max = 0.8
    min_needed = max(0, round((target_min / 100) * total_words) - kw_occurrences)
    max_allowed = round((target_max / 100) * total_words)

    # ── Tag checks ──
    tags = {
        '<title>':          (r'<title[^>]*>(.*?)</title>', False),
        '<meta description>': (r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', False),
        '<h1>':             (r'<h1[^>]*>(.*?)</h1>', False),
        '<h2>':             (r'<h2[^>]*>(.*?)</h2>', True),  # True = one match is enough
        '<h3>':             (r'<h3[^>]*>(.*?)</h3>', True),
        '<strong> or <b>':  (r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', True),
        '<u> or <em>':      (r'<(?:u|em)[^>]*>(.*?)</(?:u|em)>', True),
        'img alt=""':       (r'alt=["\']([^"\']*)["\']', True),
        '<table> cell':     (r'<t[dh][^>]*>(.*?)</t[dh]>', True),
    }

    tag_results = {}
    for label, (pattern, any_match) in tags.items():
        found = check_tag(html, pattern, keyword)
        tag_results[label] = found

    first_p_ok = get_first_paragraph_text(html, keyword)
    last_p_ok = get_last_paragraph_text(html, keyword)

    # ── URL Slug check ──
    slug_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']*)["\']', html, re.IGNORECASE)
    slug_url = slug_match.group(1) if slug_match else None
    slug_ok = keyword.lower().replace(' ', '-') in slug_url.lower() if slug_url else None

    # ── Report ──
    print("\n" + "=" * 65)
    print(f"  KEYWORD CHECKER REPORT")
    print(f"  Keyword : \"{keyword}\"")
    print("=" * 65)

    print(f"\n📊 DENSITY ANALYSIS")
    print(f"  Total Words      : {total_words:,}")
    print(f"  Keyword Count    : {kw_occurrences}")
    print(f"  Current Density  : {density:.2f}%")
    print(f"  Target Range     : {target_min}% – {target_max}%")

    if density < target_min:
        print(f"\n  ⚠️  TOO LOW — Add keyword {min_needed} more time(s) to reach 0.5%")
    elif density > target_max:
        over = kw_occurrences - max_allowed
        print(f"\n  ⚠️  TOO HIGH — Remove or replace {over} occurrence(s) with synonyms")
    else:
        print(f"\n  ✅  DENSITY OK — Within target range")

    print(f"\n🏷️  HTML TAG COVERAGE")
    print(f"  {'Tag':<25} {'Status':<10} {'Preview'}")
    print(f"  {'-'*60}")

    mandatory = ['<title>', '<meta description>', '<h1>', '<h2>', '<strong> or <b>', 'img alt=""']
    optional  = ['<h3>', '<u> or <em>', '<table> cell']

    for label, found in tag_results.items():
        is_mandatory = label in mandatory
        flag = "REQUIRED" if is_mandatory else "optional"
        if found:
            status = "✅ Found"
            preview = found[0] if found else ""
        else:
            status = "❌ Missing" if is_mandatory else "➖ Not found"
            preview = ""
        print(f"  {label:<25} {status:<12} {preview[:40]}")

    # First/Last paragraph
    fp_status = "✅ Found" if first_p_ok else "❌ Missing"
    lp_status = "✅ Found" if last_p_ok else "❌ Missing"
    print(f"  {'First <p> (100 words)':<25} {fp_status}")
    print(f"  {'Last <p>':<25} {lp_status}")

    # Slug
    if slug_url is not None:
        sk_status = "✅ Found" if slug_ok else "❌ Missing"
        print(f"  {'URL Slug (canonical)':<25} {sk_status:<12} {slug_url[:40] if slug_url else ''}")
    else:
        print(f"  {'URL Slug (canonical)':<25} {'➖ No canonical tag found'}")

    # ── Summary ──
    missing_mandatory = [
        label for label in mandatory
        if not tag_results.get(label)
    ]
    if not first_p_ok:
        missing_mandatory.append("First <p> (first 100 words)")
    if not last_p_ok:
        missing_mandatory.append("Last <p>")

    print(f"\n📋 SUMMARY")
    if not missing_mandatory and target_min <= density <= target_max:
        print("  ✅ ALL CHECKS PASSED — Page is ready to publish.")
    else:
        print("  ❌ ISSUES FOUND — Fix before publishing:")
        if density < target_min:
            print(f"     • Add keyword {min_needed} more time(s) — current density {density:.2f}% is below 0.5%")
        elif density > target_max:
            print(f"     • Remove/replace {kw_occurrences - max_allowed} keyword occurrence(s) — density {density:.2f}% exceeds 0.8%")
        for tag in missing_mandatory:
            print(f"     • Keyword missing from: {tag}")

    print("\n" + "=" * 65 + "\n")


def main():
    print("\n======================================================")
    print("  KEYWORD DENSITY & TAG COVERAGE CHECKER")
    print("======================================================\n")

    keyword = input("Enter your PRIMARY KEYWORD: ").strip()
    if not keyword:
        print("No keyword entered. Exiting.")
        sys.exit(1)

    print("\nHow do you want to provide the HTML content?")
    print("  1. Paste HTML directly (press Enter twice when done)")
    print("  2. Provide a file path to an .html or .txt file")
    choice = input("\nEnter 1 or 2: ").strip()

    if choice == "1":
        print("\nPaste your HTML content below. Press Enter twice when done:\n")
        lines = []
        empty_count = 0
        while empty_count < 2:
            line = input()
            if line == "":
                empty_count += 1
            else:
                empty_count = 0
            lines.append(line)
        html = "\n".join(lines)
    elif choice == "2":
        path = input("Enter the full file path: ").strip().strip('"')
        if not os.path.exists(path):
            print(f"File not found: {path}")
            sys.exit(1)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    analyze(html, keyword)


if __name__ == "__main__":
    main()
