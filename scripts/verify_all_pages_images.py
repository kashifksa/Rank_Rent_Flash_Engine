import json
import os

base_dir = r"D:\Projects\Rank_Rent_Flash_Engine"
plans = [
    "image_plan_homepage.json",
    "image_plan_about.json",
    "image_plan_contact.json",
    "image_plan_air-duct-cleaning-loves-park-il.json",
    "image_plan_commercial-hvac-duct-cleaning.json",
    "image_plan_dryer-vent-cleaning-and-lint-removal.json"
]

total_images = 0
all_valid = True

print("================================================================================")
print(f"{'PAGE':<35} | {'SLOT':<25} | {'SIZE (KB)':<10} | {'GPS STATUS':<15}")
print("================================================================================")

for p in plans:
    ppath = os.path.join(base_dir, p)
    if not os.path.exists(ppath):
        continue
    data = json.load(open(ppath, encoding="utf-8"))
    page_id = data.get("page_id", p)
    for img in data.get("images", []):
        total_images += 1
        fn = img.get("filename", "")
        slot = img.get("slot", "")
        status = img.get("status", "")
        # Find file
        full_path = None
        for root, dirs, files in os.walk(os.path.join(base_dir, "images")):
            if fn in files:
                full_path = os.path.join(root, fn)
                break
        
        if full_path and os.path.exists(full_path):
            size_kb = os.path.getsize(full_path) / 1024
            valid_size = size_kb < 100.0
            if not valid_size:
                all_valid = False
            flag = "PASS" if valid_size else "FAIL (>100KB)"
            print(f"{page_id:<35} | {slot:<25} | {size_kb:>6.1f} KB  | {status:<15} [{flag}]")
        else:
            all_valid = False
            print(f"{page_id:<35} | {slot:<25} | {'MISSING':>9} | {status:<15} [FAIL]")

print("================================================================================")
print(f"Total Images: {total_images} | All Exist & < 100KB: {all_valid}")
