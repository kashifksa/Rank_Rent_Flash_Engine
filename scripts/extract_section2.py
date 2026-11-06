import re

path = r"D:\Projects\Rank_Rent_Flash_Engine\denton_site_dump.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Find the section starting at id="about" or right after the hero
start_idx = html.find('id="about"')
if start_idx == -1:
    start_idx = html.find('How a Broken Sprinkler Can Damage')

tag_start = html.rfind('<div', 0, start_idx) if start_idx != -1 else 0

# Grab the next 6000 characters
sub = html[tag_start:tag_start+7000]

with open(r"D:\Projects\Rank_Rent_Flash_Engine\denton_section2_extracted.html", "w", encoding="utf-8") as f:
    f.write(sub)

print(f"Extracted Section 2 ({len(sub)} chars)")

