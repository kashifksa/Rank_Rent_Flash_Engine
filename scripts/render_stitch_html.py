import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\Kashif\.gemini\antigravity\brain\652a7bff-4272-4ea9-a998-2015a13c31ae"
frame_path = os.path.join(artifact_dir, "stitch_frame_2.html")
screenshot_full = os.path.join(artifact_dir, "stitch_rendered_full.png")

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    file_url = f"file:///{frame_path.replace('\\', '/')}"
    print(f"Loading {file_url}...")
    page.goto(file_url, wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    # Capture full page
    page.screenshot(path=screenshot_full, full_page=True)
    print("Full rendered screenshot saved to:", screenshot_full)
    
    # List all sections
    sects = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('section, footer, header')).map((s, idx) => {
            const h = s.querySelector('h1, h2');
            return {
                idx: idx + 1,
                tag: s.tagName,
                heading: h ? h.innerText.trim() : 'NO HEADING',
                id: s.id,
                className: s.className.slice(0, 40),
                textSample: s.innerText.trim().slice(0, 100).replace(/\\n/g, ' ')
            };
        });
    }""")
    print("\nSections found in rendered Stitch HTML:")
    for s in sects:
        print(f"  [{s['idx']}] <{s['tag']}> {s['heading']} (id='{s['id']}')")
        print(f"      sample: {s['textSample'][:80]}...")
        
    browser.close()

