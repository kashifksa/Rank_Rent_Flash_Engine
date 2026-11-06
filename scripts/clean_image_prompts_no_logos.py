import json
import glob
import re
import os

files = glob.glob(r'D:\Projects\Rank_Rent_Flash_Engine\image_plan_*.json')
print(f"Auditing {len(files)} image plan files...")

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    
    modified = False
    for img in data.get('images', []):
        prompt = img.get('prompt', '')
        original_prompt = prompt
        
        # Check if prompt mentions company lettering, logos, etc.
        if re.search(r'company lettering|lettering|logo|branding|decals', prompt, re.IGNORECASE):
            print(f"[{os.path.basename(f)}] Found logo/lettering reference in {img.get('slot')}:")
            print("  OLD:", prompt[:120])
            
            # Replace with unmarked van / plain workwear instructions
            prompt = re.sub(r'with professional company lettering', 'unmarked with clean solid white exterior and zero lettering or decals', prompt, flags=re.IGNORECASE)
            prompt = re.sub(r'company lettering', 'clean unmarked exterior with zero text', prompt, flags=re.IGNORECASE)
            prompt = re.sub(r'with logo', 'with no logos or patches', prompt, flags=re.IGNORECASE)
            
        # Ensure negative constraints are explicitly added to every prompt involving vans or uniforms
        if 'van' in prompt.lower() and 'unmarked' not in prompt.lower():
            prompt += " The service van must be a completely unmarked, clean solid white commercial cargo vehicle with zero text, zero decals, and zero company logos on any surface."
            
        if any(w in prompt.lower() for w in ['uniform', 'technician', 'tradesmen', 'worker', 'shirt']) and 'no logos' not in prompt.lower() and 'zero logos' not in prompt.lower():
            prompt += " Technicians wear plain, solid-colored professional trade workwear with strictly zero logos, zero text, zero badges, and zero embroidery on their clothing."
            
        if prompt != original_prompt:
            img['prompt'] = prompt
            modified = True
            print(f"  UPDATED {img.get('slot')} in {os.path.basename(f)}")

    if modified:
        with open(f, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, indent=2)
        print(f"Saved cleaned {os.path.basename(f)}")

print("\nAll image plans updated with strict no-logo / unmarked vehicle & clothing constraints!")
