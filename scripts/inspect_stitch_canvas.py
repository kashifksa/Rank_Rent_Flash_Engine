import os
from playwright.sync_api import sync_playwright

url = "https://stitch.withgoogle.com/projects/2602542779932590678"
artifact_dir = r"C:\Users\Kashif\.gemini\antigravity\brain\652a7bff-4272-4ea9-a998-2015a13c31ae"
screenshot_path = os.path.join(artifact_dir, "stitch_prototype_open.png")

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 1000})
    
    print(f"Loading {url}...")
    page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Try clicking "Prototype" or double clicking the canvas area
    # In the screenshot, there is text "Double click to open"
    try:
        proto = page.locator("text=Double click to open")
        if proto.count() > 0:
            print("Found 'Double click to open', dblclicking...")
            proto.first.dblclick()
            page.wait_for_timeout(3000)
    except Exception as e:
        print("Error dblclicking:", e)
        
    # Check if there is an iframe or fullscreen modal
    iframes = page.frames
    print(f"Frames detected: {len(iframes)}")
    for f in iframes:
        print(f"  Frame URL: {f.url}")
        
    page.screenshot(path=screenshot_path)
    print("Screenshot saved to:", screenshot_path)
    
    # Also let's inspect the export button if available
    try:
        export_btn = page.locator("button:has-text('Export')")
        if export_btn.count() > 0:
            print("Export button found, clicking...")
            export_btn.first.click()
            page.wait_for_timeout(1000)
            page.screenshot(path=os.path.join(artifact_dir, "stitch_export_dialog.png"))
    except Exception as e:
        print("Export click error:", e)
        
    browser.close()

