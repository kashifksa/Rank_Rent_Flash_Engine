with open(r'D:\Projects\Rank_Rent_Flash_Engine\denton_section4_extracted.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# find all headings
headings = re.findall(r'<h[234][^>]*>.*?</h[234]>', html, re.DOTALL)
print(f"Total headings found: {len(headings)}")
for h in headings:
    clean = re.sub(r'<[^>]+>', '', h).strip()
    tag = h[:3]
    print(f"  {tag}: {clean}")

# find wcp classes
classes = set(re.findall(r'class="([^"]+)"', html))
wcp_classes = [c for c in classes if any(k in c for k in ['wcp', 'card', 'col', 'grid', 'benefit', 'pillar', 'trust'])]
print("\nWCP classes found:")
for c in sorted(wcp_classes):
    print(" ", c)

