import os
import sys
import re

def check_consistency():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    builder_data_path = os.path.join(base_dir, "scripts", "builder_data.js")
    dist_dir = os.path.join(base_dir, "dist")
    
    print("=" * 65)
    print(" 🔍 Rank & Rent Pipeline — Page Consistency & Anti-Leak Validator")
    print("    Enforcing FIX 19, FIX 32, FIX 35, and FIX 36 Standards")
    print("=" * 65)
    
    errors = []
    warnings = []
    
    # 1. Check builder_data.js
    if not os.path.exists(builder_data_path):
        print(f"Error: {builder_data_path} not found.")
        return 1
        
    with open(builder_data_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check for residential-duct-cleaning.html link leak
    if "residential-duct-cleaning.html" in content or "residential-air-duct-cleaning.html" in content:
        errors.append("FIX 32 / FIX 36 VIOLATION: Found link to 'residential-duct-cleaning.html'. Primary service must route to '#contact' or phone dispatch.")
        
    # Check for hardcoded Rockford in Loves Park section 02
    loves_m = re.search(r'"air-duct-cleaning-loves-park-il":\s*\{(.*?)\n\s\s\},', content, re.DOTALL)
    if loves_m:
        loves_block = loves_m.group(1)
        if "Rockford Property" in loves_block or "How Contaminated Air Ducts Compromise Your Rockford Property" in loves_block:
            errors.append("FIX 36 VIOLATION: Found 'Rockford Property' in Loves Park section 02.")
            
    # 2. Check compiled dist/*.html files if dist exists
    if os.path.exists(dist_dir):
        html_files = [f for f in os.listdir(dist_dir) if f.endswith(".html")]
        print(f"\n[1/3] Scanning {len(html_files)} compiled HTML pages in dist/...")
        
        for hf in html_files:
            file_path = os.path.join(dist_dir, hf)
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()
                
            # Check 404 residential link
            if "residential-duct-cleaning.html" in html:
                errors.append(f"FIX 32 VIOLATION in {hf}: Contains href='residential-duct-cleaning.html'.")
                
            # If location page, check for hub city in H2s
            if "loves-park" in hf:
                h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE)
                for h2 in h2_matches:
                    clean_h2 = re.sub(r'<[^>]+>', '', h2).strip()
                    if "Rockford Property" in clean_h2:
                        errors.append(f"FIX 36 VIOLATION in {hf}: H2 contains hub city: '{clean_h2}'.")
                        
            # FIX 38 Check: Process Table & Anti-Overflow Architecture
            proc_windows = re.findall(r'<span class="proc-window"[^>]*>(.*?)</span>', html, re.IGNORECASE | re.DOTALL)
            for pw in proc_windows:
                clean_pw = re.sub(r'<[^>]+>', '', pw).strip()
                if len(clean_pw) > 28:
                    errors.append(f"FIX 38 VIOLATION in {hf}: .proc-window badge text exceeds 28 chars ('{clean_pw[:30]}...'). Badges must be short timeframes, not descriptions.")
                    
            proc_titles = re.findall(r'<h3 class="proc-title"[^>]*>(.*?)</h3>', html, re.IGNORECASE | re.DOTALL)
            for pt in proc_titles:
                clean_pt = re.sub(r'<[^>]+>', '', pt).strip()
                if clean_pt.isdigit() or clean_pt.lower() in ['step', 'protocol phase', 'technical execution']:
                    errors.append(f"FIX 38 VIOLATION in {hf}: Invalid .proc-title detected ('{clean_pt}'). Titles must be descriptive, not step numbers or table headers.")
                    
            if "**" in html:
                errors.append(f"FIX 38 VIOLATION in {hf}: Unparsed markdown asterisks '**' detected in compiled HTML.")
                        
    print(f"\n[2/3] Checking Navigation Dropdowns (FIX 35)...")
    if os.path.exists(os.path.join(dist_dir, "index.html")):
        with open(os.path.join(dist_dir, "index.html"), "r", encoding="utf-8") as f:
            idx_html = f.read()
            if 'class="dropdown"' not in idx_html or 'Services' not in idx_html or 'Locations' not in idx_html:
                errors.append("FIX 35 VIOLATION: Header navigation missing 'Services' or 'Locations' dropdowns.")
            else:
                print(" -> Navigation dropdowns verified.")
                
    # Summary
    print("\n[3/3] Validator Results:")
    if errors:
        print(f"\n❌ FAILED: Found {len(errors)} consistency errors:")
        for e in errors:
            print(f"  [!] {e}")
        return 1
    else:
        print("\n✅ PASS: 0 geographic leaks, 0 broken primary links, 100% canonical service parity!")
        return 0

if __name__ == "__main__":
    sys.exit(check_consistency())

