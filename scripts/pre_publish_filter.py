"""
pre_publish_filter.py
=====================
Runs BEFORE any markdown content is converted to Gutenberg blocks and pushed to WordPress.
Strips all internal/editorial content that should never appear on a live page.

Usage (import):
    from pre_publish_filter import filter_markdown, filter_html, safe_publish
    clean_md = filter_markdown(raw_md)
    clean_html = filter_html(raw_html)

Usage (as publish gate — PREFERRED):
    from pre_publish_filter import safe_publish
    safe_publish(call_mcp_fn, post_id, raw_content, post_type='page')

WARNING: Never call wp_update_page or wp_update_post directly.
Always route through safe_publish() so the filter is guaranteed to run.
"""

import re


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1 — Filter the raw markdown BEFORE conversion
# ─────────────────────────────────────────────────────────────────────────────

# Any line or paragraph containing these strings is an internal note.
# It must never appear in published content.
PENDING_MARKERS = [
    'coming in Phase',
    'coming in phase',
    '(Phase 2)',
    '(Phase 3)',
    '(Phase 4)',
    'Phase 2)',
    'Phase 3)',
    '(link to ',
    '→ *(link',
    '(coming soon)',
    '(TBD)',
    '(TODO)',
    '[PENDING]',
]

# Old-format section headers that are internal metadata, not publishable content.
INTERNAL_SECTION_HEADERS = [
    '## Internal Links',
    '## Entities to Include',
    '## Page Metadata',
    '## Meta ',
    '## Schema',
    '## Secondary Keywords',
    '## WP Type',
    '## Target Keyword',
    '## Word Count',
    '## SECTION ',
    '### Current ',
]


def filter_markdown(content: str) -> str:
    """
    Strips internal editorial content from a raw markdown string.
    Returns a clean markdown string safe for conversion and publishing.
    """
    # Step 1: Remove YAML front matter (between the first two --- markers)
    content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)

    # Step 2: Remove section annotation comment blocks entirely
    # These look like: <!-- ==...== \n SECTION: hero \n ... \n ==...== -->
    content = re.sub(r'<!--\s*=+.*?=+\s*-->', '', content, flags=re.DOTALL)

    # Step 3: Process line by line
    lines = content.split('\n')
    result = []
    skip_section = False

    for line in lines:
        stripped = line.strip()

        # Skip empty separator-only lines (---, ***, ===)
        if re.match(r'^[-=\*]{2,}$', stripped):
            continue

        # Skip lines that are pure "-->" (comment artifact)
        if stripped == '-->' or re.match(r'^-->\s*$', stripped):
            continue

        # Skip emoji-prefixed internal notes (👉, ➡, →)
        if stripped.startswith('👉') or stripped.startswith('➡') or re.match(r'^→\s', stripped):
            continue

        # Skip lines that are bullet points of internal link notes
        if re.match(r'^[-*]\s*(Link to|link to|Internal|internal)\s', stripped):
            continue

        # Detect start of an internal-only section (old format)
        is_internal_header = any(stripped.startswith(h) for h in INTERNAL_SECTION_HEADERS)
        if is_internal_header:
            skip_section = True
            continue

        # Reset skip when we hit a new real heading
        if skip_section:
            if re.match(r'^#{1,3} ', stripped) and not is_internal_header:
                skip_section = False
            else:
                continue

        # Skip any line containing a pending link marker
        if any(marker in line for marker in PENDING_MARKERS):
            continue

        result.append(line)

    return '\n'.join(result)


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2 — Filter the rendered HTML AFTER conversion
# ─────────────────────────────────────────────────────────────────────────────

def filter_html(html: str) -> str:
    """
    Final cleanup pass on Gutenberg block HTML.
    Catches any artifacts that slipped through the markdown filter.
    Handles both plain <p> tags and <p> tags with inner HTML (strong, em, etc.)
    """
    # Remove artifact paragraphs: <p>--></p>, <p>---</p>, <p>—</p>
    html = re.sub(r'<!-- wp:paragraph -->\n<p>\s*(-->|---|–|—|–)\s*</p>\n<!-- /wp:paragraph -->', '', html)

    # Remove any paragraph block that contains pending markers
    # Pass 1: plain <p> with no inner tags
    for marker in PENDING_MARKERS:
        pattern = r'<!-- wp:paragraph -->\n<p>[^<]*' + re.escape(marker) + r'[^<]*</p>\n<!-- /wp:paragraph -->'
        html = re.sub(pattern, '', html)

    # Pass 2: <p> blocks with inner HTML tags (e.g. <strong>, <em>, <a>)
    def check_p_block(m):
        inner_text = re.sub(r'<[^>]+>', '', m.group(1))  # strip HTML tags
        if any(marker in inner_text for marker in PENDING_MARKERS):
            return ''  # remove the whole block
        return m.group(0)  # keep it

    html = re.sub(
        r'<!-- wp:paragraph -->\n(<p>.*?</p>)\n<!-- /wp:paragraph -->',
        check_p_block,
        html,
        flags=re.DOTALL
    )

    # Remove empty heading blocks
    html = re.sub(r'<!-- wp:heading[^>]*-->\n<h\d[^>]*>\s*</h\d>\n<!-- /wp:heading -->', '', html)

    # Remove consecutive blank lines left by removals
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html.strip()


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3 — Pricing guard (FIX 1 open item)
# ─────────────────────────────────────────────────────────────────────────────

# Regex patterns that signal pricing content -- all must be absent before publish.
_PRICING_PATTERNS = [
    re.compile(r'\$\s*\d'),
    re.compile(r'\d+\s*dollars', re.IGNORECASE),
    re.compile(r'per\s+(yard|ton|load|haul|dump)', re.IGNORECASE),
    re.compile(r'starting\s+at\s+\$', re.IGNORECASE),
    re.compile(r'as\s+low\s+as\s+\$', re.IGNORECASE),
    re.compile(r'only\s+\$', re.IGNORECASE),
    re.compile(r'from\s+\$\s*\d', re.IGNORECASE),
]


def check_no_pricing(content: str, label: str = 'content') -> None:
    """
    FIX 1 (open item): Raise ValueError if any pricing pattern is found.
    This is a Rank & Rent site -- pricing must never appear on any page.
    Call this before safe_publish() to block dollar amounts from going live.

    Args:
        content: The raw markdown or HTML string to scan.
        label:   Descriptor used in the error message.

    Raises:
        ValueError with the first offending match and its context.
    """
    for pattern in _PRICING_PATTERNS:
        match = pattern.search(content)
        if match:
            start = max(0, match.start() - 60)
            end = min(len(content), match.end() + 60)
            snippet = content[start:end].replace('\n', ' ')
            raise ValueError(
                'PRICING DETECTED in {} -- publish blocked.\n'
                'Pattern : {}\n'
                'Context : ...{}...'.format(label, pattern.pattern, snippet)
            )


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4 — Safe publish gate
# ─────────────────────────────────────────────────────────────────────────────

def safe_publish(call_mcp_fn, post_id: int, raw_content: str, post_type: str = 'page') -> dict:
    """
    The correct way to push content to WordPress.
    Runs check_no_pricing() on both sides of filter_html().
    Raises ValueError and blocks the publish if pricing is found.

    Args:
        call_mcp_fn: Your call_mcp function that sends requests to the WP API
        post_id:     WordPress post/page ID
        raw_content: The raw HTML content string to publish
        post_type:   'page' or 'post'

    Returns:
        The API response dict

    Raises:
        ValueError if any pricing content is detected (publish is blocked).

    Example:
        from pre_publish_filter import safe_publish
        result = safe_publish(call_mcp, 42, my_html_content, post_type='page')
    """
    # Gate 1: Pricing check -- blocks publish if any $ amount or pricing phrase found
    check_no_pricing(raw_content, label='HTML (pre-filter)')

    # Gate 2: Strip internal annotations and artifacts
    clean_content = filter_html(raw_content)

    # Gate 3: Re-check after filtering (ensures filter did not introduce pricing)
    check_no_pricing(clean_content, label='HTML (post-filter)')

    method = 'wp_update_page' if post_type == 'page' else 'wp_update_post'
    id_key = 'page_id' if post_type == 'page' else 'post_id'
    return call_mcp_fn(method, {id_key: post_id, 'content': clean_content})
