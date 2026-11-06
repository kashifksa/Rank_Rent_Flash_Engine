with open(r'D:\Projects\Rank_Rent_Flash_Engine\builder_v4_dumped_dom.html', encoding='utf-8') as f:
    text = f.read()

start = text.find('id="page-render-target"')
start_tag_close = text.find('>', start) + 1
end = text.find('id="code-drawer"')
end_tag = text.rfind('</div>', start, end)
# Also previous div closing viewport-frame
end_tag = text.rfind('</div>', start, end_tag)

content = text[start_tag_close:end_tag].strip()
print(f"Extracted content length: {len(content)} characters")

styles = open(r'D:\Projects\Rank_Rent_Flash_Engine\target_site_styles.css', encoding='utf-8').read()

out_html = r"D:\Projects\Rank_Rent_Flash_Engine\build\homepage_industrial_hostinger.html"
full_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Air Duct Cleaning Rockford, IL | Same-Day Service | Rockford Air Duct Pros</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
{styles}
  </style>
</head>
<body>
{content}
<script>
  document.querySelectorAll('.faq-question').forEach(q => {{
    q.addEventListener('click', () => q.parentElement.classList.toggle('active'));
  }});
</script>
</body>
</html>"""

with open(out_html, "w", encoding="utf-8") as f:
    f.write(full_doc)

print(f"Updated {out_html} ({len(full_doc)} bytes)")
