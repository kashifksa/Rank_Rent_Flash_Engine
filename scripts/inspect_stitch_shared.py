import os
from playwright.sync_api import sync_playwright

url = "https://stitch.withgoogle.com/projects/2602542779932590678"
artifact_dir = r"C:\Users\Kashif\.gemini\antigravity\brain\652a7bff-4272-4ea9-a998-2015a13c31ae"
screenshot_path = os.path.join(artifact_dir, "stitch_shared_view.png")
full_screenshot_path = os.path.join(artifact_dir, "stitch_shared_full.png")

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]
exec_path = None
for cp in chrome_paths:
    if os.path.exists(cp):
        exec_path = cp
        break

with sync_playwright() as p:
    launch_kwargs = {"headless": True}
    if exec_path:
        launch_kwargs["executable_path"] = exec_path
    else:
        launch_kwargs["channel"] = "msedge"
        
    browser = p.chromium.launch(**launch_kwargs)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    print(f"Navigating to {url}...")
    try:
        resp = page.goto(url, wait_until="networkidle", timeout=25000)
        print("Status:", resp.status if resp else "None")
    except Exception as e:
        print("Goto timeout or error:", e)
        
    page.wait_for_timeout(4000)
    print("Page Title:", page.title())
    print("Page URL:", page.url)
    
    page.screenshot(path=screenshot_path)
    try:
        page.screenshot(path=full_screenshot_path, full_page=True)
    except:
        pass
        
    # Get headings and text summary
    text_content = page.evaluate("""() => {
        const hs = Array.from(document.querySelectorAll('h1, h2, h3, h4, [class*="title"], [class*="heading"]'));
        const headings = hs.map(h => `${h.tagName}: ${h.innerText.trim()}`);
        return {
            title: document.title,
            headings: headings.slice(0, 30),
            bodyLength: document.body.innerText.length,
            bodySample: document.body.innerText.slice(0, 500)
        };
    }""")
    print("Text Content:")
    print(text_content)
    
    browser.close()

