with open(r'D:\Projects\Rank_Rent_Flash_Engine\scripts\builder_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import json
prefix = "window.BUILDER_PAGES_DATA = "
start = text.find(prefix)
if start != -1:
    raw_json = text[start + len(prefix):text.rfind(';')]
    data = json.loads(raw_json)
    hp_intro = data['homepage']['sections']['intro | BLOCK: CS-01-INTRO']
    print("Raw intro markdown:")
    print(hp_intro)

