import piexif
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def check_file_exif(path):
    print(f"\nChecking: {os.path.basename(path)}")
    try:
        exif_dict = piexif.load(path)
        zero = exif_dict.get("0th", {})
        gps = exif_dict.get("GPS", {})
        
        make = zero.get(piexif.ImageIFD.Make, b"").decode("utf-8", errors="ignore")
        artist = zero.get(piexif.ImageIFD.Artist, b"").decode("utf-8", errors="ignore")
        copyright_val = zero.get(piexif.ImageIFD.Copyright, b"").decode("utf-8", errors="ignore")
        
        print(f"  Camera Make: {make}")
        print(f"  Artist:      {artist}")
        print(f"  Copyright:   {copyright_val}")
        
        if gps:
            lat = gps.get(piexif.GPSIFD.GPSLatitude)
            lat_ref = gps.get(piexif.GPSIFD.GPSLatitudeRef, b"").decode("utf-8", errors="ignore")
            lon = gps.get(piexif.GPSIFD.GPSLongitude)
            lon_ref = gps.get(piexif.GPSIFD.GPSLongitudeRef, b"").decode("utf-8", errors="ignore")
            print(f"  GPS Latitude:  {lat} {lat_ref}")
            print(f"  GPS Longitude: {lon} {lon_ref}")
        else:
            print("  GPS: None (Cleanly un-geotagged per 50% rule)")
    except Exception as e:
        print(f"  Error reading EXIF: {e}")

check_file_exif(r"D:\Projects\Rank_Rent_Flash_Engine\images\homepage\rockford-air-duct-pros-service-van-hero.webp")
check_file_exif(r"D:\Projects\Rank_Rent_Flash_Engine\images\homepage\residential-duct-cleaning-rockford-illinois.webp")
check_file_exif(r"D:\Projects\Rank_Rent_Flash_Engine\images\locations\loves-park\air-duct-cleaning-loves-park-illinois-hero.webp")
