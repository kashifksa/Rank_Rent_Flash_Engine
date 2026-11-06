with open(r'D:\Projects\Rank_Rent_Flash_Engine\denton_site_dump.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('wcp-heading')
print("wcp-heading found at:", pos)
if pos != -1:
    row_start = text.rfind('<div class="kb-row-layout-wrap', 0, pos)
    print("Row start:", row_start)
    next_h2 = text.find('<h2', pos + 20)
    print("Next H2 at:", next_h2)
    next_row = text.find('<div class="kb-row-layout-wrap', next_h2 - 200) if next_h2 != -1 else pos + 5000
    print("Next row at:", next_row)

    section4_html = text[row_start:next_row]
    print(f"Section 4 length: {len(section4_html)}")
    with open(r'D:\Projects\Rank_Rent_Flash_Engine\denton_section4_extracted.html', 'w', encoding='utf-8') as out:
        out.write(section4_html)
    print("Saved denton_section4_extracted.html")

