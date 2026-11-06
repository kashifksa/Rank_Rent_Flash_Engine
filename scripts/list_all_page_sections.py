with open(r'D:\Projects\Rank_Rent_Flash_Engine\scripts\builder_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import json
prefix = "window.BUILDER_PAGES_DATA = "
start = text.find(prefix)
if start != -1:
    raw_json = text[start + len(prefix):text.rfind(';')]
    data = json.loads(raw_json)
    for page_key, pdata in data.items():
        print(f"Page: {page_key} ({pdata.get('type')})")
        print("  Sections:", list(pdata.get('sections', {}).keys()))
