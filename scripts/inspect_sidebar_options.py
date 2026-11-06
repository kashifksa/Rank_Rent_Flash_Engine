with open(r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Services Grid Variant' in line:
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f"{j+1}: {lines[j].encode('ascii', 'replace').decode('ascii')}", end="")
        print("\n" + "="*40 + "\n")

