import re
import json

with open(r'D:\Projects\Rank_Rent_Flash_Engine\target_site_dump.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print(f"Target site HTML size: {len(html)} bytes")

# 1. Identify CMS, theme, builders
theme_m = re.findall(r'wp-content/themes/([^/\'"]+)', html)
plugins_m = re.findall(r'wp-content/plugins/([^/\'"]+)', html)
print("Themes detected:", list(set(theme_m)))
print("Plugins detected:", list(set(plugins_m)))

# 2. Fonts detected
fonts_m = re.findall(r'fonts\.googleapis\.com/css2?\?family=([^"\'&]+)', html)
print("Google Fonts:", list(set(fonts_m)))

# 3. Title & Headings
title_m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
print("Title:", title_m.group(1) if title_m else "N/A")

h1_m = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
print("H1 headings:", [re.sub(r'<[^>]+>', '', h).strip() for h in h1_m])

h2_m = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL | re.IGNORECASE)
print("H2 headings (first 8):", [re.sub(r'<[^>]+>', '', h).strip() for h in h2_m[:8]])

# 4. Color codes in inline styles or style tags
colors = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', html)
from collections import Counter
print("Top 10 Colors:", Counter(colors).most_common(10))

# 5. Check CSS classes
classes = re.findall(r'class=["\']([^"\']+)["\']', html)
all_classes = " ".join(classes).split()
print("Top 15 CSS class tokens:", Counter(all_classes).most_common(15))

