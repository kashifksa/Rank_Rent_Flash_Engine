"""
=============================================================
  IMAGE GEOTAGGER & EXIF STRIPPER (Rank & Rent Pipeline)
=============================================================

What it does:
1. Reads image_plan_[page].json
2. Finds the corresponding images in the target folder
3. Converts them to WebP (with transparent background support for logo/favicon)
4. Strips all existing EXIF data (removes AI metadata)
5. Injects GPS coordinates (auto-looked up via city/state) for images marked geotag: true
6. Injects Copyright and Author metadata (Company Name)
7. Renames them exactly to the SEO filenames required.

Requirements:
  pip install Pillow piexif geopy

Usage:
  python image_geotagger.py --plan image_plan_homepage.json --folder ./images
"""

import os
import sys
import json
import glob
import argparse
from PIL import Image
import piexif
from geopy.geocoders import Nominatim
from fractions import Fraction

# ── Ensure UTF-8 output on Windows ─────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def get_gps_coordinates(city, state):
    """Auto-lookup GPS coordinates for the city/state using OpenStreetMap."""
    print(f"  Looking up GPS coordinates for {city}, {state}...")
    try:
        geolocator = Nominatim(user_agent="rank_and_rent_geotagger")
        location = geolocator.geocode(f"{city}, {state}, USA")
        if location:
            print(f"  \u2713 Found: {location.latitude}, {location.longitude}")
            return location.latitude, location.longitude
        else:
            print(f"  \u2717 Could not find GPS for {city}, {state}. Defaulting to 0,0.")
            return 0.0, 0.0
    except Exception as e:
        print(f"  \u2717 Geocoding error: {e}. Defaulting to 0,0.")
        return 0.0, 0.0


MAX_SIZE_KB = 100

import re as _re

def validate_image_filename(filename):
    """
    FIX 30 (bonus): No numeric digits allowed in production image filenames.
    Raises ValueError if the filename (excluding extension) contains any digit.
    Call this at image_plan generation time (Prompt 8) before accepting a filename.
    """
    name_only = os.path.splitext(filename)[0]
    if _re.search(r"[0-9]", name_only):
        raise ValueError(
            "Image filename '{}' contains a numeric digit. "
            "Production filenames must use descriptive hyphenated words only "
            "(e.g., 'concrete-dumpster-cedar-rapids-iowa.webp').".format(filename)
        )

def save_webp_under_limit(img, output_path, exif_bytes, is_transparent, max_kb=MAX_SIZE_KB):
    """
    FIX 30: Save image as WebP strictly under max_kb.

    Strategy:
      1. Try quality reduction first: [85, 75, 65, 55] -- floor at 55 to prevent
         visible artifacting on photorealistic AI-generated images.
      2. If quality reduction alone is insufficient, iteratively scale dimensions
         down by 20% increments using high-quality Lanczos resampling and repeat
         the quality loop at each reduced size.
      3. The first (quality, scale) combination that produces <= max_kb wins.
      4. If all combinations are exhausted (extremely rare), saves the smallest
         version found -- never the original oversized file.

    EXIF bytes are injected inside every encode attempt so the size check always
    reflects the exact bytes that will be uploaded to WordPress.

    Returns (final_quality, final_size_kb).
    """
    import io

    qualities = [85, 75, 65, 55]           # Quality floor: 55 (prevents bad artifacting)
    scale_factors = [1.0, 0.8, 0.64, 0.51, 0.40]  # 100% -> 80% -> 64% -> 51% -> 40%
    orig_w, orig_h = img.width, img.height

    best_buf = None
    best_size = float("inf")
    best_q = qualities[-1]

    for scale in scale_factors:
        w = int(orig_w * scale)
        h = int(orig_h * scale)

        # Apply high-quality Lanczos resize for any scale below 100%
        if scale < 1.0:
            resized = img.resize((w, h), Image.Resampling.LANCZOS)
        else:
            resized = img.copy()

        for q in qualities:
            buf = io.BytesIO()
            save_kwargs = {"format": "webp", "quality": q}
            if not is_transparent:
                save_kwargs["exif"] = exif_bytes   # EXIF included in every size check
            resized.save(buf, **save_kwargs)
            size_kb = buf.tell() / 1024

            # Track the smallest version produced across all combinations
            if size_kb < best_size:
                best_size = size_kb
                best_buf = buf.getvalue()
                best_q = q

            # First combination that passes the limit wins -- write and return
            if size_kb <= max_kb:
                with open(output_path, "wb") as f:
                    f.write(buf.getvalue())
                return q, round(size_kb, 1)

    # Safety fallback: all loops exhausted -- save the smallest version found
    # (never saves the original oversized file)
    with open(output_path, "wb") as f:
        f.write(best_buf)
    return best_q, round(best_size, 1)

def to_deg(value, loc):
    """Convert decimal coordinates into degrees, minutes and seconds tuple for EXIF."""
    if value < 0:
        loc_value = loc[0]
    elif value > 0:
        loc_value = loc[1]
    else:
        loc_value = ""
    abs_value = abs(value)
    deg = int(abs_value)
    t1 = (abs_value - deg) * 60
    min = int(t1)
    sec = round((t1 - min) * 60, 5)
    return (deg, 1), (min, 1), (int(sec * 100000), 100000), loc_value

def change_to_rational(number):
    """Convert a number to a rational tuple for EXIF."""
    f = Fraction(str(number))
    return (f.numerator, f.denominator)

def create_gps_exif(lat, lng):
    """Generate the GPS IFD dictionary for piexif."""
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3].encode(),
        piexif.GPSIFD.GPSLatitude: (lat_deg[0], lat_deg[1], lat_deg[2]),
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3].encode(),
        piexif.GPSIFD.GPSLongitude: (lng_deg[0], lng_deg[1], lng_deg[2]),
    }
    return gps_ifd

def process_image(target_filename, image_data, folder_path, company_name, lat, lon):
    """Process a single image: convert to WebP, strip EXIF, add custom EXIF if needed."""
    base_name = os.path.splitext(target_filename)[0]
    
    # 1. Find the file in the folder (Antigravity appends timestamps, e.g., name_12345.jpg)
    # We look for any file starting with the base_name.
    search_pattern = os.path.join(folder_path, f"{base_name}*.*")
    matching_files = glob.glob(search_pattern)
    
    if not matching_files:
        print(f"  ✗ Could not find any image starting with '{base_name}' in {folder_path}")
        return False
        
    # Pick the most recently modified file if there are multiple
    source_file = max(matching_files, key=os.path.getmtime)
    print(f"  Processing {os.path.basename(source_file)} -> {target_filename}...")
    
    output_path = os.path.join(folder_path, target_filename)
    
    try:
        with Image.open(source_file) as img:
            # 2. Convert to WebP format
            # If transparent_bg is true, ensure we keep the alpha channel
            is_transparent = image_data.get("transparent_bg", False)
            if is_transparent and img.mode != "RGBA":
                img = img.convert("RGBA")
            elif not is_transparent and img.mode in ("RGBA", "P"):
                # Convert to RGB to remove alpha if not needed
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                img = bg
                
            # 3. Create fresh EXIF data
            zeroth_ifd = {
                piexif.ImageIFD.Artist: company_name.encode('utf-8'),
                piexif.ImageIFD.Copyright: f"© {company_name}".encode('utf-8'),
            }
            exif_dict = {"0th": zeroth_ifd, "Exif": {}, "1st": {}, "thumbnail": None, "GPS": {}}
            
            # 4. Inject GPS if geotag: true
            if image_data.get("geotag", False):
                exif_dict["GPS"] = create_gps_exif(lat, lon)
                print("    ✓ Geotag injected")
                
            exif_bytes = piexif.dump(exif_dict)
            
            # Save as WebP under 100KB
            quality, size_kb = save_webp_under_limit(
                img, output_path, exif_bytes, is_transparent
            )
            print(f"    ✓ Saved as WebP | Quality: {quality} | Size: {size_kb} KB")
            if size_kb > MAX_SIZE_KB:
                print(f"    ⚠  WARNING: Could not compress below {MAX_SIZE_KB}KB "
                      f"(final size: {size_kb}KB). Consider resizing source image.")
            else:
                print(f"    ✓ Under {MAX_SIZE_KB}KB limit")
            
        # Clean up the original file if it has a different name/extension
        if os.path.abspath(source_file) != os.path.abspath(output_path):
            os.remove(source_file)
            
        return True
    except Exception as e:
        print(f"  ✗ Error processing {source_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Image Geotagger & EXIF Stripper")
    parser.add_argument("--plan", required=True, help="Path to image_plan_[page].json")
    parser.add_argument("--folder", default=".", help="Folder containing the images")
    args = parser.parse_args()
    
    if not os.path.exists(args.plan):
        print(f"ERROR: Plan file '{args.plan}' not found.")
        sys.exit(1)
        
    with open(args.plan, "r", encoding="utf-8") as f:
        plan = json.load(f).get("image_plan", {})
        
    meta = plan.get("meta", {})
    company_name = meta.get("company_name", "Local Service Company")
    city = meta.get("primary_city", "")
    state = meta.get("state", "")
    
    print("=" * 60)
    print("  IMAGE GEOTAGGER & EXIF STRIPPER")
    print(f"  Company : {company_name}")
    print(f"  Location: {city}, {state}")
    print(f"  Folder  : {args.folder}")
    print("=" * 60)
    
    lat, lon = get_gps_coordinates(city, state)
    
    # Collect all images to process
    images_to_process = []
    
    if "logo" in plan and plan["logo"].get("filename"):
        images_to_process.append((plan["logo"]["filename"], plan["logo"]))
        
    if "favicon" in plan and plan["favicon"].get("filename"):
        images_to_process.append((plan["favicon"]["filename"], plan["favicon"]))
        
    for img in plan.get("page_images", []):
        if img.get("filename"):
            images_to_process.append((img["filename"], img))
            
    import random
    success_count = 0
    for filename, data in images_to_process:
        # Add a random offset (approx +/- 2-3 miles) so images aren't stacked on one exact coordinate
        img_lat = lat + random.uniform(-0.04, 0.04) if lat != 0.0 else lat
        img_lon = lon + random.uniform(-0.04, 0.04) if lon != 0.0 else lon
        
        if process_image(filename, data, args.folder, company_name, img_lat, img_lon):
            success_count += 1
            
    print("=" * 60)
    print(f"  DONE! Successfully processed {success_count} of {len(images_to_process)} images.")
    print("=" * 60)

if __name__ == "__main__":
    main()
