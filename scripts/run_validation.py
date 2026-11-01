import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from pre_publish_filter import filter_markdown, check_no_pricing

filename = sys.argv[1] if len(sys.argv) > 1 else 'page_content_residential-air-duct-cleaning.md'
content = open(filename, encoding='utf-8').read()

print('Running pre_publish_filter validation on:', filename)
print('Word count (raw):', len(content.split()))

# Check for pricing
try:
    check_no_pricing(content, label=filename)
    print('PRICING CHECK: PASS - no pricing detected')
except ValueError as e:
    print('PRICING CHECK: FAIL')
    print(str(e))
    sys.exit(1)

# Check for em-dashes
if '\u2014' in content:
    print('EM-DASH CHECK: FAIL - em-dash detected')
    sys.exit(1)
else:
    print('EM-DASH CHECK: PASS')

# Check for separator lines (lines that are only ---)
import re
lines = content.split('\n')
sep_lines = [i+1 for i, l in enumerate(lines) if re.match(r'^-{3,}$', l.strip())]
if sep_lines:
    print('SEPARATOR CHECK: FAIL - separator lines found at lines:', sep_lines)
    sys.exit(1)
else:
    print('SEPARATOR CHECK: PASS')

# Run filter
cleaned = filter_markdown(content)
print('FILTER: Complete -', len(cleaned.split()), 'words after filter')
print()
print('ALL CHECKS PASSED - content is safe to stitch and save as golden example')

