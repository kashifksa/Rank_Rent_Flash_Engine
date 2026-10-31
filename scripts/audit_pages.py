"""
audit_pages.py
==============
Post-publish content audit. Scans live page HTML dumps for artifacts
that should never appear on a published page.

HOW TO USE:
1. After publishing a page, copy the live page HTML source and save it
   as audit_[page_id].txt in your project folder.
2. Run: python audit_pages.py
   It auto-discovers all audit_*.txt files in the current directory.

Alternatively, pass specific files:
   python audit_pages.py audit_homepage.txt audit_service_page.txt
"""

import re
import os
import sys


# Patterns that should NEVER appear on a live published page
BAD_PATTERNS = [
    (r'-->',                'Arrow/comment artifact "-->"'),
    (r'---',                'Separator line "---"'),
    (r'coming in Phase \d', 'Pending link placeholder'),
    (r'\(Phase \d\)',       'Phase marker'),
    (r'\(link to',          'Internal link note'),
    (r'👉',                 'Emoji CTA note'),
    (r'Internal Links',     'Internal metadata section'),
    (r'Entities to Include','Internal metadata section'),
    (r'Page Metadata',      'Internal metadata section'),
    (r'Target Keyword',     'Metadata field'),
    (r'Secondary Keywords', 'Metadata field'),
    (r'Meta Description',   'Metadata field'),
    (r'Schema:',            'Metadata field'),
    (r'Word Count',         'Metadata field'),
    (r'WP Type',            'Metadata field'),
    (r'page_id:',           'YAML front matter leaked'),
    (r'page_type:',         'YAML front matter leaked'),
    (r'wp_slug:',           'YAML front matter leaked'),
    (r'stitch_layout:',     'YAML front matter leaked'),
    (r'SECTION:',           'Annotation comment leaked'),
    (r'component:',         'Annotation comment leaked'),
    (r'image-desc:',        'Annotation comment leaked'),
    (r'image-filename:',    'Annotation comment leaked'),
    (r'cta-text:',          'Annotation comment leaked'),
    (r'design_brief:',      'YAML front matter leaked'),
    (r'\bURL:\b',           'Metadata URL field'),
    (r'\bH1:\b',            'Metadata field'),
    (r'\bH2:\b',            'Metadata field'),
]


def audit_file(filepath: str) -> list:
    """Scan a single HTML file for bad patterns. Returns list of (label, context) tuples."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Strip HTML tags to get plain text for analysis
    plain = re.sub(r'<[^>]+>', ' ', content)
    plain = re.sub(r'<!--.*?-->', ' ', plain, flags=re.DOTALL)

    issues = []
    for pattern, label in BAD_PATTERNS:
        matches = re.findall(r'.{0,40}' + pattern + r'.{0,40}', plain)
        for m in matches:
            issues.append((label, m.strip()))

    return issues


def main():
    # Use files passed as arguments, or auto-discover audit_*.txt in current dir
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = sorted([f for f in os.listdir('.') if f.startswith('audit_') and f.endswith('.txt')])

    if not files:
        print("No audit files found. Save live page HTML as audit_[page_id].txt and re-run.")
        return

    print("=" * 70)
    print(f"CONTENT AUDIT — {len(files)} PAGE(S)")
    print("=" * 70)

    total_issues = 0

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"\n[MISSING] {filepath}")
            continue

        issues = audit_file(filepath)
        total_issues += len(issues)

        print(f"\n{'=' * 70}")
        print(f"PAGE: {filepath}")
        print(f"{'=' * 70}")

        if not issues:
            print("  ✅ No issues found.")
        else:
            for label, context in issues:
                print(f"  ❌ [{label}]")
                print(f"     Context: ...{context}...")
                print()

    print(f"\n{'=' * 70}")
    print(f"AUDIT COMPLETE — {total_issues} issue(s) found across {len(files)} page(s)")
    print("=" * 70)


if __name__ == '__main__':
    main()
