with open(r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
hostinger_matches = [m.start() for m in re.finditer(r'hostinger', text, re.I)]
denton_matches = [m.start() for m in re.finditer(r'denton', text, re.I)]

print(f"Total 'hostinger' occurrences: {len(hostinger_matches)}")
for p in hostinger_matches[:6]:
    print(text[max(0, p-30):min(len(text), p+70)].strip())
    print("---")

print(f"Total 'denton' occurrences: {len(denton_matches)}")
for p in denton_matches[:6]:
    print(text[max(0, p-30):min(len(text), p+70)].strip())
    print("---")

