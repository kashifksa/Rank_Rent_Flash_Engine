import os
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

base_dir = r"D:\Projects\Rank_Rent_Flash_Engine"
build_dir = os.path.join(base_dir, "build")
os.makedirs(build_dir, exist_ok=True)

data_js_path = os.path.join(base_dir, "scripts", "builder_data.js")
raw_js = open(data_js_path, encoding="utf-8").read()
json_str = raw_js.replace("window.BUILDER_PAGES_DATA = ", "").rstrip(";")
pages_data = json.loads(json_str)

def parse_md(md):
    html = md
    html = re.sub(r"^### (.*$)", r'<h3 style="font-size: 1.25rem; font-weight: 700; margin: 16px 0 8px; color: #121315;">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r"^## (.*$)", r'<h2 style="font-size: 1.75rem; font-weight: 800; margin: 24px 0 12px; color: #121315;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r"^# (.*$)", r'<h1 style="font-size: 2.25rem; font-weight: 800; margin-bottom: 16px; color: #121315; line-height: 1.2;">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.*?)\*\*", r'<strong style="color: #121315;">\1</strong>', html)
    html = re.sub(r"\*(.*?)\*", r'<em>\1</em>', html)
    html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" style="color: #fd761a; text-decoration: underline; font-weight: 600;">\1</a>', html)
    html = re.sub(r"\n\n", r'</p><p style="margin-bottom: 14px; font-size: 1rem; line-height: 1.6; color: #374151;">', html)
    html = re.sub(r"^> (.*$)", r'<blockquote style="border-left: 4px solid #fd761a; padding-left: 16px; margin: 16px 0; font-style: italic; color: #4b5563;">\1</blockquote>', html, flags=re.MULTILINE)
    
    # Handle tables
    if '|' in html:
        lines = html.split('\n')
        in_table = False
        table_html = '<div style="overflow-x: auto; margin: 20px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 14px;">'
        new_lines = []
        for line in lines:
            if line.strip().startswith('|') and line.strip().endswith('|'):
                if not in_table: in_table = True
                if '---' in line: continue
                cells = line.split('|')[1:-1]
                table_html += '<tr style="border-bottom: 1px solid #e5e7eb;">'
                for c in cells:
                    table_html += f'<td style="padding: 10px 14px; text-align: left;">{c.strip()}</td>'
                table_html += '</tr>'
            else:
                if in_table:
                    table_html += '</table></div>'
                    new_lines.append(table_html)
                    in_table = False
                new_lines.append(line)
        if in_table: table_html += '</table></div>'
        html = '\n'.join(new_lines)
        
    return f'<p style="margin-bottom: 14px; font-size: 1rem; line-height: 1.6; color: #374151;">{html}</p>'

print("Generating static HTML files into build/...")

for pid, pdata in pages_data.items():
    meta = pdata.get("meta", {})
    title = meta.get("meta_title", pdata.get("title", ""))
    desc = meta.get("meta_description", "")
    schema_json = json.dumps(meta.get("schema", {}), indent=2)
    
    body_sections = []
    for skey, scontent in pdata.get("sections", {}).items():
        parsed = parse_md(scontent)
        bg = "#ffffff"
        if "hero" in skey:
            bg = "linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)"
        elif "trust" in skey or "cta" in skey:
            bg = "#f1f5f9"
            
        sec_block = f"""
        <section id="sec-{skey}" style="background: {bg}; padding: 48px 32px; border-bottom: 1px solid #f1f5f9;">
          <div style="max-width: 1100px; margin: 0 auto;">
            {parsed}
          </div>
        </section>
        """
        body_sections.append(sec_block)
        
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; color: #1a1c1d; background: #ffffff; line-height: 1.6; }}
    h1, h2, h3 {{ font-family: 'Montserrat', sans-serif; color: #121315; }}
    a {{ color: #fd761a; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .btn-primary {{ background: #fd761a; color: #ffffff !important; padding: 10px 20px; border-radius: 4px; font-weight: 700; display: inline-block; text-decoration: none !important; }}
    .btn-primary:hover {{ background: #e06210; }}
  </style>
  <script type="application/ld+json">
{schema_json}
  </script>
</head>
<body>
  <nav style="display: flex; align-items: center; justify-content: space-between; padding: 18px 32px; border-bottom: 1px solid #e5e7eb; background: #ffffff;">
    <div style="font-weight: 800; font-size: 18px; color: #121315;">Rockford Air Duct Pros</div>
    <div style="display: flex; align-items: center; gap: 20px; font-size: 13px; font-weight: 600;">
      <a href="/" style="color: #374151;">Home</a>
      <a href="/about/" style="color: #374151;">About</a>
      <a href="/contact/" style="color: #374151;">Contact</a>
      <a href="tel:8155550142" class="btn-primary">(815) 555-0142</a>
    </div>
  </nav>

  {"".join(body_sections)}

  <footer style="background: #121315; color: #94a3b8; padding: 40px 32px; text-align: center; font-size: 13px;">
    <p style="margin-bottom: 8px; color: #ffffff; font-weight: 700;">Rockford Air Duct Pros</p>
    <p style="margin-bottom: 12px;">1111 S Alpine Rd, Rockford, IL 61108 | Phone: (815) 555-0142</p>
    <p>© 2026 Rockford Air Duct Pros. Licensed, Insured & NADCA Certified. All rights reserved.</p>
  </footer>
</body>
</html>
"""
    out_file = os.path.join(build_dir, f"{pid}.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"✓ Generated build/{pid}.html ({(len(page_html)/1024):.1f} KB)")

print("All Phase 1 production HTML files generated successfully!")
