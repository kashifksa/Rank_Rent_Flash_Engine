import os

base = r'D:\Projects\Rank_Rent_Flash_Engine'
img_dir = os.path.join(base, 'images')

for root, dirs, files in os.walk(img_dir):
    for f in files:
        if f.endswith('.webp') or f.endswith('.jpg'):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base)
            size = os.path.getsize(full) / 1024
            print(f"{rel.replace(chr(92), '/')} ({size:.1f} KB)")

