import re

filepath = r"D:\Projects\Rank_Rent_Flash_Engine\page_content_air-duct-cleaning-loves-park-il.md"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

body = re.sub(r"^---[\s\S]*?---", "", text).strip()
words = body.lower().split()
total_words = len(words)

primary_kw = "air duct cleaning loves park il"
kw_count = len(re.findall(re.escape(primary_kw), body, re.IGNORECASE))
density = (kw_count * len(primary_kw.split()) / total_words) * 100

print(f"Total words in body: {total_words}")
print(f"Primary keyword occurrences: {kw_count}")
print(f"Primary keyword density: {density:.2f}%")

# Check section word counts
sections = re.split(r"<!-- SECTION: [^>]+ -->", text)
section_names = ["header_yaml"] + re.findall(r"<!-- SECTION: ([^>]+) -->", text)
print("\nSection breakdown:")
for name, sec in zip(section_names[1:], sections[1:]):
    sec_clean = re.sub(r"^#[^\n]*\n", "", sec.strip())
    sec_clean = re.sub(r"^##[^\n]*\n", "", sec_clean)
    count = len(sec_clean.split())
    print(f"- {name}: {count} words")

