import re
from collections import Counter
from bs4 import BeautifulSoup

path = r"D:\Projects\Rank_Rent_Flash_Engine\denton_site_dump.html"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

print("="*60)
print(f"ANALYSIS OF https://sprinklerrepairdentontx.com/ (Size: {len(html)} bytes)")
print("="*60)

# 1. CMS & Theme
themes = list(set(re.findall(r'wp-content/themes/([^/\'"]+)', html)))
plugins = list(set(re.findall(r'wp-content/plugins/([^/\'"]+)', html)))
print("Theme:", themes)
print("Key Plugins detected:", [p for p in plugins if any(k in p for k in ['elementor', 'kadence', 'divi', 'generate', 'form', 'builder', 'block'])])

# 2. Fonts
fonts = list(set(re.findall(r'fonts\.googleapis\.com/css2?\?family=([^"\'&]+)', html)))
print("Google Fonts:", fonts)

# 3. Headings
soup = BeautifulSoup(html, 'html.parser')
title = soup.title.string if soup.title else "N/A"
print("Title:", title.strip())

h1s = [h.get_text().strip() for h in soup.find_all('h1')]
print("H1 Headings:", h1s)

h2s = [h.get_text().strip() for h in soup.find_all('h2')]
print("H2 Headings (First 10):", h2s[:10])

# 4. Phone numbers & CTAs
phones = list(set(re.findall(r'tel:([0-9\-\+\(\)\s]+)', html)))
print("Phone Links:", phones)

# 5. Hero Section Inspection
print("\n--- HERO SECTION DETAILS ---")
# Search for hero container or first section
hero_candidates = soup.find_all(['header', 'section', 'div'], class_=lambda c: c and any(k in str(c).lower() for k in ['hero', 'banner', 'masthead', 'top-section', 'elementor-top-section']))
print(f"Hero candidates found: {len(hero_candidates)}")

for i, h in enumerate(hero_candidates[:3]):
    classes = h.get('class', [])
    text_snippet = h.get_text()[:250].replace('\n', ' ')
    print(f"Candidate {i+1} classes: {classes[:4]} | Text: {text_snippet}")

# 6. Colors in CSS
colors = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', html)
print("\nTop 10 Colors:", Counter(colors).most_common(10))

# 7. Images in Hero
images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
print("Hero/First 5 Images:", images[:5])
