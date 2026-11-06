import os
import sys
import shutil
from playwright.sync_api import sync_playwright

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
builder_url = f"file:///{base_dir.replace('\\', '/')}/studio_builder.html"
dist_dir = os.path.join(base_dir, "dist")
os.makedirs(dist_dir, exist_ok=True)

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]
exec_path = None
for cp in chrome_paths:
    if os.path.exists(cp):
        exec_path = cp
        break

print(f"Building production distribution from {builder_url}...")

with sync_playwright() as p:
    launch_kwargs = {"headless": True}
    if exec_path:
        launch_kwargs["executable_path"] = exec_path
    else:
        launch_kwargs["channel"] = "msedge"
        
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(builder_url)
    page.wait_for_timeout(1000)

    pages = page.evaluate("Object.keys(window.BUILDER_PAGES_DATA)")
    print(f"Exporting {len(pages)} production pages to {dist_dir}...")

    for pid in pages:
        doc_html = page.evaluate(f"generateProductionDocument('{pid}')")
        filename = "index.html" if pid in ["homepage", "home"] else f"{pid}.html"
        out_path = os.path.join(dist_dir, filename)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(doc_html)
        
        print(f"  -> {filename} ({len(doc_html) // 1024} KB)")

    browser.close()

# Sync images to dist/images
src_images = os.path.join(base_dir, "images")
dst_images = os.path.join(dist_dir, "images")
if os.path.exists(dst_images):
    shutil.rmtree(dst_images)
shutil.copytree(src_images, dst_images)
print("Distribution export complete: dist/ updated successfully.")

