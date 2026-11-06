import json
from pathlib import Path

plan_path = Path(r"D:\Projects\Rank_Rent_Flash_Engine\image_plan_homepage.json")
with open(plan_path, "r", encoding="utf-8") as f:
    plan = json.load(f)

for img in plan.get("images", []):
    if img["filename"] == "rockford-air-duct-pros-service-van-hero.webp":
        img["status"] = "geotagged"
        img["filesize_kb"] = 93.8
        img["gps"] = "42.2713945, -89.093966"
        break

with open(plan_path, "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2)

print("Updated hero image status to geotagged!")

