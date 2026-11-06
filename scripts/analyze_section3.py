with open(r'D:\Projects\Rank_Rent_Flash_Engine\denton_section3_extracted.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# find all headings
headings = re.findall(r'<h[234][^>]*>.*?</h[234]>', html, re.DOTALL)
print(f"Total headings found: {len(headings)}")
for h in headings:
    # clean tag
    clean = re.sub(r'<[^>]+>', '', h).strip()
    tag = h[:3]
    print(f"  {tag}: {clean}")

# find card classes, structure
print("\nKey classes:")
classes = set(re.findall(r'class="([^"]+)"', html))
svc_classes = [c for c in classes if any(k in c for k in ['svc', 'card', 'col', 'grid', 'btn'])]
print("Service classes:", svc_classes[:15])

# find images inside section 3
images = re.findall(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', html)
if not images:
    # check background images in style
    bg_images = re.findall(r'background(?:-image)?:\s*url\([\'"]?([^\'")]+)[\'"]?\)', html)
    print("Background images:", bg_images)
else:
    print("Images found:", images)

