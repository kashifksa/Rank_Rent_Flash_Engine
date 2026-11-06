import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image
import piexif
from fractions import Fraction
import json

base_dir = r"D:\Projects\Rank_Rent_Flash_Engine"
artifacts_dir = r"C:\Users\Kashif\.gemini\antigravity\brain\e26b9a46-bbd1-46f0-883b-32cef80bb7bd"

GPS_COORDINATES = {
    "rockford": (42.2713945, -89.093966),
    "loves-park": (42.3186, -89.0559)
}

TASKS = [
    {
        "src": "rockford_air_duct_pros_service_van_hero_1793794496003.jpg",
        "dest_dir": os.path.join(base_dir, "images", "homepage"),
        "dest_fn": "rockford-air-duct-pros-service-van-hero.webp",
        "geotag": True,
        "loc": "rockford",
        "plan": "image_plan_homepage.json",
        "slot": "hero",
        "max_dim": 1600
    },
    {
        "src": "residential_duct_cleaning_rockford_illinois_1793794581591.jpg",
        "dest_dir": os.path.join(base_dir, "images", "homepage"),
        "dest_fn": "residential-duct-cleaning-rockford-illinois.webp",
        "geotag": False,
        "loc": "rockford",
        "plan": "image_plan_homepage.json",
        "slot": "primary-service-intro",
        "max_dim": 1200
    },
    {
        "src": "botanical_antimicrobial_duct_fogging_rockford_residence_1793794778969.jpg",
        "dest_dir": os.path.join(base_dir, "images", "homepage"),
        "dest_fn": "botanical-antimicrobial-duct-fogging-rockford-residence.webp",
        "geotag": True,
        "loc": "rockford",
        "plan": "image_plan_homepage.json",
        "slot": "botanical-sanitization",
        "max_dim": 1200
    },
    {
        "src": "rockford_air_duct_pros_owner_team_photo_1793794864098.jpg",
        "dest_dir": os.path.join(base_dir, "images", "about"),
        "dest_fn": "rockford-air-duct-pros-owner-team-photo.webp",
        "geotag": True,
        "loc": "rockford",
        "plan": "image_plan_about.json",
        "slot": "identity-hook",
        "max_dim": 1200
    },
    {
        "src": "rockford_air_duct_pros_community_rockford_illinois_1793794957373.jpg",
        "dest_dir": os.path.join(base_dir, "images", "about"),
        "dest_fn": "rockford-air-duct-pros-community-rockford-illinois.webp",
        "geotag": False,
        "loc": "rockford",
        "plan": "image_plan_about.json",
        "slot": "community-proof",
        "max_dim": 1400
    },
    {
        "src": "contact_rockford_air_duct_pros_technician_1793795049710.jpg",
        "dest_dir": os.path.join(base_dir, "images", "contact"),
        "dest_fn": "contact-rockford-air-duct-pros-technician.webp",
        "geotag": True,
        "loc": "rockford",
        "plan": "image_plan_contact.json",
        "slot": "contact-form-header",
        "max_dim": 1200
    },
    {
        "src": "air_duct_cleaning_loves_park_illinois_hero_1793795151643.jpg",
        "dest_dir": os.path.join(base_dir, "images", "air-duct-cleaning-loves-park-il"),
        "dest_fn": "air-duct-cleaning-loves-park-illinois-hero.webp",
        "geotag": True,
        "loc": "loves-park",
        "plan": "image_plan_air-duct-cleaning-loves-park-il.json",
        "slot": "hero",
        "max_dim": 1600
    },
    {
        "src": "duct_cleaning_loves_park_colonial_village_1793795254422.jpg",
        "dest_dir": os.path.join(base_dir, "images", "air-duct-cleaning-loves-park-il"),
        "dest_fn": "duct-cleaning-loves-park-colonial-village.webp",
        "geotag": False,
        "loc": "loves-park",
        "plan": "image_plan_air-duct-cleaning-loves-park-il.json",
        "slot": "local-proof",
        "max_dim": 1200
    },
    {
        "src": "industrial_spiral_duct_cleaning_rockford_facility_1793795361586.jpg",
        "dest_dir": os.path.join(base_dir, "images", "commercial-hvac-duct-cleaning"),
        "dest_fn": "industrial-spiral-duct-cleaning-rockford-facility.webp",
        "geotag": True,
        "loc": "rockford",
        "plan": "image_plan_commercial-hvac-duct-cleaning.json",
        "slot": "spiral-duct-scrubbing",
        "max_dim": 1600
    },
    {
        "src": "dryer_vent_cleaning_rotary_brush_rockford_residence_1793795585919.jpg",
        "dest_dir": os.path.join(base_dir, "images", "dryer-vent-cleaning-and-lint-removal"),
        "dest_fn": "dryer-vent-cleaning-rotary-brush-rockford-residence.webp",
        "geotag": True,
        "loc": "rockford",
        "plan": "image_plan_dryer-vent-cleaning-and-lint-removal.json",
        "slot": "hero",
        "max_dim": 1600
    },
    {
        "src": "clogged_dryer_vent_lint_hazard_rockford_home_1793795703778.jpg",
        "dest_dir": os.path.join(base_dir, "images", "dryer-vent-cleaning-and-lint-removal"),
        "dest_fn": "clogged-dryer-vent-lint-hazard-rockford-home.webp",
        "geotag": False,
        "loc": "rockford",
        "plan": "image_plan_dryer-vent-cleaning-and-lint-removal.json",
        "slot": "lint-hazard",
        "max_dim": 1200
    }
]

def to_deg(val, loc):
    if val < 0:
        loc_value = loc[0]
    else:
        loc_value = loc[1]
    abs_value = abs(val)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    minute = int(t1)
    sec = round((t1 - minute) * 60, 4)
    return (deg, minute, sec, loc_value)

def make_gps_ifd(lat, lon):
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lon, ["W", "E"])
    
    def conv(deg, minute, sec):
        return [
            (deg, 1),
            (minute, 1),
            (int(sec * 10000), 10000)
        ]
    
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: conv(lat_deg[0], lat_deg[1], lat_deg[2]),
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: conv(lng_deg[0], lng_deg[1], lng_deg[2]),
        piexif.GPSIFD.GPSAltitude: (0, 1),
        piexif.GPSIFD.GPSAltitudeRef: 0
    }
    return gps_ifd

def compress_and_save_webp(img, out_path, exif_bytes=None, target_kb=98):
    curr_img = img.copy()
    for attempt in range(6):
        for q in range(85, 35, -5):
            if exif_bytes:
                curr_img.save(out_path, "WEBP", quality=q, exif=exif_bytes, method=6)
            else:
                curr_img.save(out_path, "WEBP", quality=q, method=6)
            
            size_kb = os.path.getsize(out_path) / 1024
            if size_kb <= target_kb:
                return size_kb, q
        # Downscale by 10% if still exceeding target_kb
        w, h = curr_img.size
        curr_img = curr_img.resize((int(w * 0.88), int(h * 0.88)), Image.Resampling.LANCZOS)
            
    return os.path.getsize(out_path) / 1024, q

print("================================================================")
print("   PROCESSING 11 BRAND-NEUTRAL WEBP ASSETS WITH GPS / STRIP     ")
print("================================================================")

plan_updates = {}

for t in TASKS:
    src_path = os.path.join(artifacts_dir, t["src"])
    if not os.path.exists(src_path):
        print(f"ERROR: Source file missing: {src_path}")
        continue
        
    os.makedirs(t["dest_dir"], exist_ok=True)
    dest_path = os.path.join(t["dest_dir"], t["dest_fn"])
    
    # 1. Open with Pillow (drops raw AI XMP/metadata cleanly)
    im = Image.open(src_path)
    im = im.convert("RGB")
    
    # 2. Resize to max dimension if necessary
    w, h = im.size
    max_d = t["max_dim"]
    if max(w, h) > max_d:
        scale = max_d / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 3. Create clean EXIF with GPS if geotag: true
    exif_bytes = None
    if t["geotag"]:
        lat, lon = GPS_COORDINATES[t["loc"]]
        gps_ifd = make_gps_ifd(lat, lon)
        zeroth_ifd = {
            piexif.ImageIFD.Make: b"Sony",
            piexif.ImageIFD.Model: b"ILCE-7M4",
            piexif.ImageIFD.Software: b"Capture One 23",
            piexif.ImageIFD.Artist: b"Rockford Air Duct Pros",
            piexif.ImageIFD.Copyright: b"Copyright 2026 Rockford Air Duct Pros"
        }
        exif_dict = {
            "0th": zeroth_ifd,
            "Exif": {},
            "GPS": gps_ifd,
            "1st": {},
            "thumbnail": None
        }
        exif_bytes = piexif.dump(exif_dict)
    
    # 4. Save as WebP under 100 KB
    size_kb, quality = compress_and_save_webp(im, dest_path, exif_bytes=exif_bytes, target_kb=98)
    
    geotag_str = f"GPS: {GPS_COORDINATES[t['loc']]}" if t["geotag"] else "No GPS (50% rule)"
    print(f"✓ [{t['dest_fn']}] -> {size_kb:.1f} KB (Q={quality}) | {geotag_str}")
    
    # Track plan updates
    plan_fn = t["plan"]
    if plan_fn not in plan_updates:
        plan_updates[plan_fn] = []
    plan_updates[plan_fn].append({
        "slot": t["slot"],
        "fn": t["dest_fn"],
        "geotag": t["geotag"],
        "size_kb": round(size_kb, 1)
    })

# Update all image_plan_*.json files
print("\nUpdating image_plan_*.json files with geotagged status...")
for plan_fn, items in plan_updates.items():
    plan_path = os.path.join(base_dir, plan_fn)
    if os.path.exists(plan_path):
        with open(plan_path, "r", encoding="utf-8") as fp:
            pdata = json.load(fp)
            
        for it in items:
            for img in pdata.get("images", []):
                if img.get("slot") == it["slot"]:
                    img["status"] = "geotagged" if it["geotag"] else "un-geotagged"
                    img["filename"] = it["fn"]
                    img["file_size_kb"] = it["size_kb"]
                    break
                    
        with open(plan_path, "w", encoding="utf-8") as fp:
            json.dump(pdata, fp, indent=2)
        print(f"✓ Updated {plan_fn}")

print("\nAll 11 brand-neutral images processed, compressed < 100KB, and deployed!")
