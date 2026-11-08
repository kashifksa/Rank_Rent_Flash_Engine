import os
from PIL import Image

artifact_dir = r"C:\Users\Kashif\.gemini\antigravity\brain\652a7bff-4272-4ea9-a998-2015a13c31ae"
img_path = os.path.join(artifact_dir, "stitch_rendered_full.png")

im = Image.open(img_path)
width, height = im.size
print(f"Full image dimensions: {width} x {height}")

# Split into 3 parts: top (0 to 3000), mid (2800 to 6000), bottom (5800 to end)
p1 = im.crop((0, 0, width, min(height, 2800)))
p1.save(os.path.join(artifact_dir, "stitch_part1_hero_services.png"))

if height > 2800:
    p2 = im.crop((0, 2600, width, min(height, 5600)))
    p2.save(os.path.join(artifact_dir, "stitch_part2_process_comp.png"))

if height > 5600:
    p3 = im.crop((0, 5400, width, height))
    p3.save(os.path.join(artifact_dir, "stitch_part3_faq_footer.png"))

print("Cropped parts saved successfully.")

