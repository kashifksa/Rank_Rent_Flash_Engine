with open(r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'why-us' in line.lower() or 'why_us' in line.lower() or 'why_choose' in line.lower():
        print(f"Line {i+1}: {line.strip()[:100]}")

