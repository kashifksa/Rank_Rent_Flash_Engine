import json, os, re, sys

files = [
    'image_plan_residential-air-duct-cleaning.json',
    'image_plan_homepage.json',
    'image_plan_air-duct-cleaning-loves-park-il.json',
    'image_plan_about.json',
    'image_plan_contact.json',
]

total_images = 0
errors = []

for fname in files:
    if not os.path.exists(fname):
        print(f'MISSING: {fname}')
        continue
    d = json.load(open(fname, encoding='utf-8'))
    images = d.get('images', [])
    count = len(images)
    total_images += count
    print(f'{fname}: {count} images')
    for img in images:
        fn = img.get('filename', '')
        alt = img.get('alt_text', '')
        # Check no digits in filename
        if re.search(r'\d', fn):
            errors.append(f'DIGIT IN FILENAME: {fname} -> {fn}')
        # Check alt text has location
        if 'rockford' not in alt.lower() and 'loves park' not in alt.lower() and 'winnebago' not in alt.lower() and 'illinois' not in alt.lower() and 'il' not in alt.lower():
            errors.append(f'NO LOCATION IN ALT: {fname} -> {alt[:60]}')
        # Check no map images
        if 'map' in fn.lower():
            errors.append(f'MAP IN FILENAME: {fname} -> {fn}')

print()
print(f'Total images: {total_images} / 15 quota limit')
if total_images > 15:
    errors.append(f'OVER QUOTA: {total_images} images (limit 15)')

if errors:
    print('ERRORS:')
    for e in errors:
        print(' ', e)
    sys.exit(1)
else:
    print('ALL CHECKS PASSED')

