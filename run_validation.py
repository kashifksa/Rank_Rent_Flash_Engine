import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))
from scripts.pre_publish_filter import filter_markdown, check_no_pricing

filename = sys.argv[1] if len(sys.argv) > 1 else 'page_content_residential-air-duct-cleaning.md'
raw = open(filename, encoding='utf-8').read()

sys.stdout.reconfigure(encoding='utf-8')

print('Running pre_publish_filter validation on:', filename)
print('Word count (raw):', len(raw.split()))

# Step 1: Run filter first (strips YAML front matter, section comments, etc.)
filtered = filter_markdown(raw)
print('Word count (filtered):', len(filtered.split()))

# Step 2: Pricing check on filtered content
try:
    check_no_pricing(filtered, label=filename)
    print('PRICING CHECK: PASS - no pricing detected')
except ValueError as e:
    print('PRICING CHECK: FAIL -', str(e)[:200])
    sys.exit(1)

# Step 3: Em-dash check on filtered content
if '\u2014' in filtered:
    lines = filtered.split('\n')
    bad = [i+1 for i, l in enumerate(lines) if '\u2014' in l]
    print('EM-DASH CHECK: FAIL - em-dash on lines:', bad)
    sys.exit(1)
else:
    print('EM-DASH CHECK: PASS')

# Step 4: Separator line check on filtered content (should have none after filter)
lines = filtered.split('\n')
sep_lines = [i+1 for i, l in enumerate(lines) if re.match(r'^-{3,}$', l.strip())]
if sep_lines:
    print('SEPARATOR CHECK: FAIL - separator lines at:', sep_lines)
    sys.exit(1)
else:
    print('SEPARATOR CHECK: PASS')

print()
print('ALL CHECKS PASSED - content is safe to save as golden example')
