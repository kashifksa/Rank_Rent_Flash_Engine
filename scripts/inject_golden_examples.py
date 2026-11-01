"""
inject_golden_examples.py
=========================
Reads each golden example file and injects the relevant section content
into the corresponding mini-prompt files in prompts/P7_*/

Usage:
    python scripts/inject_golden_examples.py

What it does:
    1. Parses each golden example file by <!-- SECTION: XX_name --> markers
    2. For each section block, finds the matching mini-prompt file
    3. Replaces the <!-- PASTE YOUR CLAUDE/PRO OUTPUT... --> placeholder
       with the actual golden example content
    4. Reports what was injected and what was skipped
"""

import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Map: (page_type, section_num_str) -> mini-prompt filename
PROMPT_DIRS = {
    'service':   'prompts/P7_service',
    'location':  'prompts/P7_location',
    'blog':      'prompts/P7_blog',
    'about':     'prompts/P7_about',
}

EXAMPLE_FILES = {
    'service':   'examples/service_page_example.md',
    'location':  'examples/location_page_example.md',
    'blog':      'examples/blog_post_example.md',
    'about':     'examples/about_page_example.md',
}

# Mini-prompt filename prefix per type
PROMPT_PREFIXES = {
    'service':  'P7s',
    'location': 'P7l',
    'blog':     'P7b',
    'about':    'P7a',
}

# The placeholder block to replace in each mini-prompt
PLACEHOLDER_START = '## GOLDEN EXAMPLE'
PLACEHOLDER_CONTENT = '<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->'


def parse_sections(content):
    """
    Split a stitched page content into sections by <!-- SECTION: XX_name --> markers.
    Returns dict: section_num (str) -> section_content (str)
    """
    # Strip YAML front matter
    content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)

    # Find all section markers and their positions
    pattern = re.compile(r'<!-- SECTION: (\d+)_(\w+) -->')
    matches = list(pattern.finditer(content))

    sections = {}
    for i, m in enumerate(matches):
        sec_num = m.group(1)   # e.g. "01"
        # Content starts after the marker line
        start = m.end()
        # Content ends at next marker (or EOF)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sec_content = content[start:end].strip()
        sections[sec_num] = sec_content

    return sections


def inject_into_prompt(prompt_path, section_content, section_num, page_type):
    """
    Inject section_content into the GOLDEN EXAMPLE block of a mini-prompt file.
    """
    with open(prompt_path, encoding='utf-8') as f:
        original = f.read()

    if PLACEHOLDER_CONTENT not in original:
        print(f'  SKIP (already filled or no placeholder): {os.path.basename(prompt_path)}')
        return False

    # Build replacement block
    golden_block = (
        '## GOLDEN EXAMPLE\n'
        '<!-- Golden example generated from: ' + page_type + '_page_example.md -->\n'
        '<!-- Section ' + section_num + ' — injected by inject_golden_examples.py -->\n\n'
        + section_content + '\n\n'
        '## OUTPUT RULES'
    )

    # Replace from ## GOLDEN EXAMPLE through ## OUTPUT RULES
    # Pattern: ## GOLDEN EXAMPLE ... ## OUTPUT RULES
    updated = re.sub(
        r'## GOLDEN EXAMPLE.*?## OUTPUT RULES',
        golden_block,
        original,
        flags=re.DOTALL
    )

    if updated == original:
        print(f'  SKIP (replacement did not match pattern): {os.path.basename(prompt_path)}')
        return False

    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(updated)

    print(f'  INJECTED: {os.path.basename(prompt_path)} (section {section_num})')
    return True


def process_type(page_type):
    example_path = os.path.join(BASE, EXAMPLE_FILES[page_type])
    prompt_dir = os.path.join(BASE, PROMPT_DIRS[page_type])
    prefix = PROMPT_PREFIXES[page_type]

    if not os.path.exists(example_path):
        print(f'  [SKIP] Example not found: {example_path}')
        return

    content = open(example_path, encoding='utf-8').read()
    sections = parse_sections(content)

    if not sections:
        print(f'  [WARN] No section markers found in {example_path}')
        return

    print(f'\n{page_type.upper()} PAGE ({len(sections)} sections found):')

    # Get all mini-prompt files in the directory
    prompt_files = sorted(os.listdir(prompt_dir)) if os.path.exists(prompt_dir) else []

    for sec_num, sec_content in sorted(sections.items()):
        # Find matching prompt file: P7s_01_*.md, P7l_01_*.md, etc.
        pattern = f'{prefix}_{sec_num}_'
        matches = [f for f in prompt_files if f.startswith(pattern) and f.endswith('.md')]

        if not matches:
            print(f'  [NO MATCH] No prompt file for section {sec_num} (looking for {pattern}*.md)')
            continue

        prompt_path = os.path.join(prompt_dir, matches[0])
        inject_into_prompt(prompt_path, sec_content, sec_num, page_type)


def main():
    print('=' * 60)
    print('  INJECT GOLDEN EXAMPLES INTO MINI-PROMPTS')
    print('=' * 60)

    for page_type in ['service', 'location', 'blog', 'about']:
        process_type(page_type)

    print('\nDone. Review injected files in prompts/P7_*/')


if __name__ == '__main__':
    main()
