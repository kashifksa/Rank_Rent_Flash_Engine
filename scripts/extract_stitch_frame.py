import os
from playwright.sync_api import sync_playwright

url = "https://stitch.withgoogle.com/projects/2602542779932590678"
artifact_dir = r"C:\Users\Kashif\.gemini\antigravity\brain\652a7bff-4272-4ea9-a998-2015a13c31ae"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    
    print(f"Loading {url}...")
    page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Find iframe
    for idx, f in enumerate(page.frames):
        print(f"Frame {idx}: URL={f.url}, Name={f.name}")
        try:
            content = f.content()
            print(f"  Content length: {len(content)}")
            if len(content) > 500:
                # Save frame html
                fname = os.path.join(artifact_dir, f"stitch_frame_{idx}.html")
                with open(fname, "w", encoding="utf-8") as out:
                    out.write(content)
                print(f"  Saved to {fname}")
                
                # Check headings in this frame
                hs = f.evaluate("""() => {
                    return Array.from(document.querySelectorAll('h1, h2, h3, h4, section')).map(el => ({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        text: el.innerText ? el.innerText.trim().slice(0, 80) : ''
                    }));
                }""")
                print(f"  Headings/Sections count: {len(hs)}")
                for h in hs[:25]:
                    print(f"    <{h['tag']}> class='{h['className'][:20]}' id='{h['id']}': {h['text']}")
        except Exception as e:
            print("  Error reading frame:", e)
            
    browser.close()

