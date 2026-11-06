path = r"D:\Projects\Rank_Rent_Flash_Engine\denton_site_dump.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

import re

# Find the hero row and its closing tag or up to next major section
hero_start = html.find('id="hero"')
if hero_start != -1:
    # Go back to the tag start
    tag_start = html.rfind('<div', 0, hero_start)
    # Find next section or next row layout
    sub = html[tag_start:tag_start+8000]
    out_file = r"D:\Projects\Rank_Rent_Flash_Engine\denton_hero_extracted.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(sub)
    print(f"Extracted hero section to {out_file} ({len(sub)} chars)")
