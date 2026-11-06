import re
import os

dom_file = r"D:\Projects\Rank_Rent_Flash_Engine\builder_v4_dumped_dom.html"
if os.path.exists(dom_file):
    with open(dom_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Extract only the canvas-container inner HTML (ignore script templates)
    canvas_match = re.search(r'<div class="canvas-container"[^>]*>([\s\S]*?)<\/div>\s*<\/div>\s*<\/main>', text)
    if canvas_match:
        canvas_html = canvas_match.group(1)
    else:
        # Fallback to everything before the main script tag
        script_idx = text.find("<script>")
        canvas_html = text[:script_idx] if script_idx != -1 else text

    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', canvas_html)
    print(f"Total img tags in canvas: {len(imgs)}")
    for src in imgs:
        local_path = os.path.join(r"D:\Projects\Rank_Rent_Flash_Engine", src) if not src.startswith("http") else src
        exists = os.path.exists(local_path) if not src.startswith("http") else True
        size_kb = os.path.getsize(local_path) / 1024 if exists and not src.startswith("http") else 0
        print(f"  [{'EXISTS' if exists else 'MISSING'}] {src} ({size_kb:.1f} KB)")
else:
    print("DOM file does not exist.")
