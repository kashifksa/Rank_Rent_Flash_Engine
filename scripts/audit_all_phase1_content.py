import os
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"D:\Projects\Rank_Rent_Flash_Engine")
from scripts.pre_publish_filter import filter_markdown, check_no_pricing

pages = [
    ("homepage", "page_content_homepage.md", "page_meta_homepage.json", "image_plan_homepage.json", "homepage"),
    ("about", "page_content_about.md", "page_meta_about.json", "image_plan_about.json", "about"),
    ("contact", "page_content_contact.md", "page_meta_contact.json", "image_plan_contact.json", "contact"),
    ("air-duct-cleaning-loves-park-il", "page_content_air-duct-cleaning-loves-park-il.md", "page_meta_air-duct-cleaning-loves-park-il.json", "image_plan_air-duct-cleaning-loves-park-il.json", "air-duct-cleaning-loves-park-il"),
    ("commercial-hvac-duct-cleaning", "page_content_commercial-hvac-duct-cleaning.md", "page_meta_commercial-hvac-duct-cleaning.json", "image_plan_commercial-hvac-duct-cleaning.json", "commercial-hvac-duct-cleaning"),
    ("dryer-vent-cleaning-and-lint-removal", "page_content_dryer-vent-cleaning-and-lint-removal.md", "page_meta_dryer-vent-cleaning-and-lint-removal.json", "image_plan_dryer-vent-cleaning-and-lint-removal.json", "dryer-vent-cleaning-and-lint-removal")
]

base_dir = r"D:\Projects\Rank_Rent_Flash_Engine"

print("=============================================================")
print("          PHASE 1 MASTER CONTENT & META AUDIT                ")
print("=============================================================")

total_words = 0
all_valid = True

for pid, md_file, meta_file, plan_file, img_folder in pages:
    md_path = os.path.join(base_dir, md_file)
    meta_path = os.path.join(base_dir, meta_file)
    plan_path = os.path.join(base_dir, plan_file)
    folder_path = os.path.join(base_dir, "images", img_folder)
    
    if not os.path.exists(md_path):
        print(f"[{pid}] FAIL: {md_file} missing")
        all_valid = False
        continue
    
    raw = open(md_path, encoding="utf-8").read()
    filtered = filter_markdown(raw)
    wcount = len(filtered.split())
    total_words += wcount
    
    has_pricing = False
    try:
        check_no_pricing(filtered, label=md_file)
    except ValueError:
        has_pricing = True
        all_valid = False

    has_emdash = "\u2014" in filtered
    if has_emdash:
        all_valid = False

    meta_ok = False
    if os.path.exists(meta_path):
        try:
            mdata = json.load(open(meta_path, encoding="utf-8"))
            meta_ok = "@graph" in mdata.get("schema", {})
        except Exception:
            meta_ok = False
            all_valid = False
            
    completed_imgs = 0
    if os.path.exists(folder_path):
        completed_imgs = len([f for f in os.listdir(folder_path) if f.endswith(".webp")])

    print(f"✓ {pid:36} | Words: {wcount:4} | Pricing: {'FAIL' if has_pricing else 'PASS'} | EmDash: {'FAIL' if has_emdash else 'PASS'} | MetaSchema: {'PASS' if meta_ok else 'FAIL'} | WebP Images: {completed_imgs}")

print("=============================================================")
print(f"Total Words Across Phase 1 Content: {total_words:,}")
print(f"Overall Content Integrity: {'100% PERFECT' if all_valid else 'FAILURES DETECTED'}")
print("=============================================================")
