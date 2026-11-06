with open(r'D:\Projects\Rank_Rent_Flash_Engine\page_content_homepage.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('BLOCK: CS-03')
end_idx = text.find('BLOCK: CS-04', idx)
print(text[idx:end_idx].encode('ascii', 'replace').decode('ascii'))

