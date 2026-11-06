import os
import json
import re
from PIL import Image
import piexif

folder = r"D:\Projects\Rank_Rent_Flash_Engine\images\contact"
plan_path = r"D:\Projects\Rank_Rent_Flash_Engine\image_plan_contact.json"
with open(plan_path, "r", encoding="utf-8") as f:
    plan = json.load(f)

print("--- CONTACT PAGE IMAGE AUDIT ---")
all_passed = True
for idx, item in enumerate(plan["images"], 1):
    fn = item["filename"]
    fp = os.path.join(folder, fn)
    if not os.path.exists(fp):
        print(f"FAIL: {fn} missing")
        all_passed = False
        continue
    
    stem = os.path.splitext(fn)[0]
    has_digits = bool(re.search(r"\d", stem))
    size_kb = os.path.getsize(fp) / 1024
    size_ok = size_kb <= 100.0
    
    with Image.open(fp) as img:
        dims = f"{img.width}x{img.height}"
        exif_raw = img.info.get("exif")
        has_gps = False
        artist = ""
        if exif_raw:
            try:
                exif_dict = piexif.load(exif_raw)
                has_gps = bool(exif_dict.get("GPS"))
                artist = exif_dict.get("0th", {}).get(piexif.ImageIFD.Artist, b"").decode("utf-8", errors="ignore")
            except Exception:
                pass

    status_str = "PASS" if (size_ok and not has_digits and has_gps) else "FAIL"
    if status_str == "FAIL":
        all_passed = False
    print(f"[{status_str}] Image {idx}: {fn} | Dims: {dims} | Size: {size_kb:.1f} KB | Digits: {has_digits} | GPS: {has_gps} | Artist: {artist}")

print("--- OVERALL RESULT ---")
print("ALL CHECKS PASSED: ", all_passed)

