import urllib.request
import ssl
import subprocess
import os

url = "https://sprinklerrepairdentontx.com/"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
        html = response.read().decode('utf-8', errors='ignore')
        out_path = r"D:\Projects\Rank_Rent_Flash_Engine\denton_site_dump.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Successfully fetched {url}: {len(html)} bytes saved to {out_path}")
except Exception as e:
    print(f"urllib error: {e}")

# Take screenshots with Chrome
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
desktop_out = r"C:\Users\Kashif\.gemini\antigravity\brain\652a7bff-4272-4ea9-a998-2015a13c31ae\denton_desktop.png"
mobile_out = r"C:\Users\Kashif\.gemini\antigravity\brain\652a7bff-4272-4ea9-a998-2015a13c31ae\denton_mobile.png"

print("Capturing desktop screenshot...")
subprocess.run([
    chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=1440,1200", f"--screenshot={desktop_out}", url
], capture_output=True)

print("Capturing mobile screenshot...")
subprocess.run([
    chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
    "--window-size=390,844", f"--screenshot={mobile_out}", url
], capture_output=True)

if os.path.exists(desktop_out):
    print(f"Desktop screenshot captured: {os.path.getsize(desktop_out)} bytes")
if os.path.exists(mobile_out):
    print(f"Mobile screenshot captured: {os.path.getsize(mobile_out)} bytes")
