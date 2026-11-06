import os
import json
import re

base_dir = r"D:\Projects\Rank_Rent_Flash_Engine"

pages_config = [
    {
        "id": "homepage",
        "title": "Homepage (Primary Service)",
        "slug": "/",
        "type": "homepage",
        "md": "page_content_homepage.md",
        "meta": "page_meta_homepage.json",
        "plan": "image_plan_homepage.json",
        "img_dir": "images/homepage"
    },
    {
        "id": "about",
        "title": "About Us",
        "slug": "about",
        "type": "about",
        "md": "page_content_about.md",
        "meta": "page_meta_about.json",
        "plan": "image_plan_about.json",
        "img_dir": "images/about"
    },
    {
        "id": "contact",
        "title": "Contact Us",
        "slug": "contact",
        "type": "contact",
        "md": "page_content_contact.md",
        "meta": "page_meta_contact.json",
        "plan": "image_plan_contact.json",
        "img_dir": "images/contact"
    },
    {
        "id": "air-duct-cleaning-loves-park-il",
        "title": "Loves Park Location Page",
        "slug": "air-duct-cleaning-loves-park-il",
        "type": "location",
        "md": "page_content_air-duct-cleaning-loves-park-il.md",
        "meta": "page_meta_air-duct-cleaning-loves-park-il.json",
        "plan": "image_plan_air-duct-cleaning-loves-park-il.json",
        "img_dir": "images/air-duct-cleaning-loves-park-il"
    },
    {
        "id": "commercial-hvac-duct-cleaning",
        "title": "Commercial HVAC Duct Cleaning",
        "slug": "commercial-hvac-duct-cleaning",
        "type": "service",
        "md": "page_content_commercial-hvac-duct-cleaning.md",
        "meta": "page_meta_commercial-hvac-duct-cleaning.json",
        "plan": "image_plan_commercial-hvac-duct-cleaning.json",
        "img_dir": "images/commercial-hvac-duct-cleaning"
    },
    {
        "id": "dryer-vent-cleaning-and-lint-removal",
        "title": "Dryer Vent Cleaning & Lint Removal",
        "slug": "dryer-vent-cleaning-and-lint-removal",
        "type": "service",
        "md": "page_content_dryer-vent-cleaning-and-lint-removal.md",
        "meta": "page_meta_dryer-vent-cleaning-and-lint-removal.json",
        "plan": "image_plan_dryer-vent-cleaning-and-lint-removal.json",
        "img_dir": "images/dryer-vent-cleaning-and-lint-removal"
    },
    {
        "id": "how-to-spot-air-duct-cleaning-scams",
        "title": "Blog: How to Spot Duct Cleaning Scams",
        "slug": "how-to-spot-air-duct-cleaning-scams",
        "type": "blog",
        "md": "page_content_how-to-spot-air-duct-cleaning-scams.md",
        "meta": "",
        "plan": "",
        "img_dir": "images/homepage"
    }
]

compiled = {}

for p in pages_config:
    md_path = os.path.join(base_dir, p["md"])
    meta_path = os.path.join(base_dir, p["meta"])
    plan_path = os.path.join(base_dir, p["plan"])
    
    # Read MD
    md_text = open(md_path, encoding="utf-8").read() if os.path.exists(md_path) else ""
    
    # Parse YAML
    yaml_match = re.search(r"^---([\s\S]*?)---", md_text)
    yaml_str = yaml_match.group(1) if yaml_match else ""
    body_str = md_text[yaml_match.end():].strip() if yaml_match else md_text
    
    # Parse sections
    raw_sections = re.split(r"<!-- SECTION: ([^>]+) -->", body_str)
    sections_dict = {}
    if len(raw_sections) > 1:
        for i in range(1, len(raw_sections), 2):
            sec_name = raw_sections[i].strip()
            sec_content = raw_sections[i+1].strip() if i+1 < len(raw_sections) else ""
            sections_dict[sec_name] = sec_content
    else:
        sections_dict["main"] = body_str
        
    # Read Meta
    meta_data = json.load(open(meta_path, encoding="utf-8")) if p.get("meta") and os.path.exists(meta_path) else {}
    
    # Read Image Plan
    plan_data = json.load(open(plan_path, encoding="utf-8")) if p.get("plan") and os.path.exists(plan_path) else {}
    images_list = plan_data.get("images", [])
    
    compiled[p["id"]] = {
        "id": p["id"],
        "title": p["title"],
        "slug": p["slug"],
        "type": p["type"],
        "sections": sections_dict,
        "meta": meta_data,
        "images": images_list,
        "img_dir": p["img_dir"]
    }

out_js = "window.BUILDER_PAGES_DATA = " + json.dumps(compiled, indent=2) + ";"
out_path = os.path.join(base_dir, "scripts", "builder_data.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out_js)

print(f"Successfully compiled all 6 pages to {out_path} ({len(out_js)} bytes)")

