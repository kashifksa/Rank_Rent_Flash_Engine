import re
from collections import Counter

path = r"D:\Projects\Rank_Rent_Flash_Engine\denton_site_dump.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# 1. Themes & Plugins
themes = list(set(re.findall(r'wp-content/themes/([^/\'"]+)', html)))
plugins = list(set(re.findall(r'wp-content/plugins/([^/\'"]+)', html)))
print("Theme:", themes)
print("Plugins:", plugins[:10])

# 2. Typography & Fonts
fonts = list(set(re.findall(r'fonts\.googleapis\.com/css2?\?family=([^"\'&]+)', html)))
print("Fonts:", fonts)

# 3. Headings
h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
print("\nH1:", [re.sub(r'<[^>]+>', '', h).strip() for h in h1s])

h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL | re.IGNORECASE)
print("\nH2 (first 8):", [re.sub(r'<[^>]+>', '', h).strip() for h in h2s[:8]])

# 4. Color codes
colors = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', html)
print("\nColors:", Counter(colors).most_common(12))

# 5. Extract Hero CSS / Inline Styles
hero_matches = re.findall(r'(<(?:section|div)[^>]*class=["\'][^"\']*(?:hero|banner|wp-block-cover)[^"\']*["\'][^>]*>)', html, re.IGNORECASE)
print("\nHero tags:", hero_matches[:3])

# 6. Extract Hero inner HTML
hero_block = re.search(r'(<section[^>]*class=["\'][^"\']*(?:hero|banner)[^"\']*["\'][\s\S]*?</section>)', html, re.IGNORECASE)
if not hero_block:
    hero_block = re.search(r'(<div[^>]*class=["\'][^"\']*(?:wp-block-cover|hero|elementor-top-section)[^"\'][\s\S]*?</div>\s*</div>)', html, re.IGNORECASE)

if hero_block:
    print("\nHero block snippet (500 chars):")
    print(hero_block.group(1)[:500])
else:
    print("Could not isolate single hero block regex, searching for H1 parent...")
    h1_idx = html.find('<h1')
    if h1_idx != -1:
        start = max(0, h1_idx - 600)
        end = min(len(html), h1_idx + 1200)
        print("\nH1 context:\n", html[start:end])
