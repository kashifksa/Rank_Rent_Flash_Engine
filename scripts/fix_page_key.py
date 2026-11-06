import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = "const whyData = parseWhyUsFromContent(rawSec, pageKey);"
replacement = "const whyData = parseWhyUsFromContent(rawSec, currentActivePage);"

if target in code:
    code = code.replace(target, replacement)
    print("Fixed pageKey -> currentActivePage successfully!")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(code)
else:
    print("Target not found!")

