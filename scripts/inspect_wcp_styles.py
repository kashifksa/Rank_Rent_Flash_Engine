with open(r'D:\Projects\Rank_Rent_Flash_Engine\denton_site_dump.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
wcp_styles = re.findall(r'(\.wcp-[^{]+{[^}]+})', text)
print(f"Total wcp styles found: {len(wcp_styles)}")
for s in wcp_styles:
    print(s[:250])
    print("---")

# Also print the HTML of the first wcp-card from denton_section4_extracted.html
with open(r'D:\Projects\Rank_Rent_Flash_Engine\denton_section4_extracted.html', 'r', encoding='utf-8') as f:
    s4 = f.read()

card_start = s4.find('wcp-card')
if card_start != -1:
    print("\nFirst wcp-card HTML snippet:")
    print(s4[card_start-30:card_start+1500].encode('ascii', 'replace').decode('ascii'))

