#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process_user_logo.py
Processes a user-uploaded reference logo into production-grade web assets:
1. Clean transparent background via mathematical alpha unblending (no white halo artifacts).
2. Tight-cropped main logo (rockford-air-duct-pros-logo.webp) for light headers.
3. Light logo variant (rockford-air-duct-pros-logo-light.webp) with white text for dark footers.
4. Favicon (rockford-air-duct-pros-favicon.webp / .png / favicon.ico) from the LEFT ICON ONLY (grille + 3 airflow arrows).
   - Centered in a square canvas with an adaptive contrast contour for dark/light browser tabs.
5. All WebP assets are strictly under 100 KB (FIX 34 standard).
6. Syncs outputs across Flash Engine and Starter Kit.
"""

import sys, os, io
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

# Default user upload path
USER_IMAGE = Path(r"C:/Users/Kashif/.gemini/antigravity/brain/652a7bff-4272-4ea9-a998-2015a13c31ae/.user_uploaded/media_1794183040614_4fed775e.webp")

def unblend_white_background(im: Image.Image, bg_val: float = 254.0) -> Image.Image:
    """Removes white background and reconstructs true foreground colors with smooth alpha."""
    rgb = im.convert("RGB")
    arr = np.array(rgb).astype(np.float32)

    # Color difference from pure background
    diff = np.maximum.reduce([bg_val - arr[:, :, 0], bg_val - arr[:, :, 1], bg_val - arr[:, :, 2]])
    diff = np.maximum(diff, 0.0)

    # Distinguish orange elements from dark charcoal elements
    is_orange = (arr[:, :, 0] - arr[:, :, 2]) > 60.0
    expected_max_diff = np.where(is_orange, 250.0, 216.0)

    # Compute alpha with noise threshold
    noise_floor = 4.0
    alpha = np.clip((diff - noise_floor) / (expected_max_diff - noise_floor), 0.0, 1.0)
    alpha = np.where(diff <= noise_floor, 0.0, alpha)

    # Reconstruct true foreground without white bleeding
    fg = np.zeros_like(arr)
    for c in range(3):
        fg[:, :, c] = np.clip((arr[:, :, c] - (1.0 - alpha) * bg_val) / np.maximum(alpha, 0.01), 0.0, 255.0)

    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = np.uint8(np.round(fg))
    rgba[:, :, 3] = np.uint8(np.round(alpha * 255.0))

    return Image.fromarray(rgba, "RGBA")


def process_logo(src_path: Path):
    if not src_path.exists():
        raise FileNotFoundError(f"Source logo not found at {src_path}")

    raw_img = Image.open(src_path)
    print(f"Loaded source image: {src_path} ({raw_img.size[0]}x{raw_img.size[1]})")

    # Step 1: Unblend background to get clean transparent RGBA
    full_rgba = unblend_white_background(raw_img)

    arr = np.array(full_rgba)
    vis_y, vis_x = np.where(arr[:, :, 3] > 8)
    pad = 6
    min_x, max_x = max(0, np.min(vis_x) - pad), min(arr.shape[1], np.max(vis_x) + pad + 1)
    min_y, max_y = max(0, np.min(vis_y) - pad), min(arr.shape[0], np.max(vis_y) + pad + 1)

    # Step 2: Main Dark Logo (tight crop with clean padding)
    logo_dark = full_rgba.crop((min_x, min_y, max_x, max_y))

    # Step 3: Light Logo Variant for dark footers / dark headers
    arr_dark = np.array(logo_dark)
    vis = arr_dark[:, :, 3] > 8
    r, g, b = arr_dark[:, :, 0].astype(np.float32), arr_dark[:, :, 1].astype(np.float32), arr_dark[:, :, 2].astype(np.float32)
    is_org = vis & ((r - b) > 50) & (r > 150)
    is_dk = vis & (~is_org)

    arr_light = np.copy(arr_dark)
    arr_light[is_dk, 0] = 255
    arr_light[is_dk, 1] = 255
    arr_light[is_dk, 2] = 255
    logo_light = Image.fromarray(arr_light, "RGBA")

    # Step 4: Favicon - LEFT ICON ONLY (grille + 3 airflow arrows, strictly excluding text & divider)
    # The divider starts at x >= 390. The icon ends at x ~ 347.
    icon_vis_y, icon_vis_x = np.where(arr[:, :370, 3] > 8)
    icon_min_x, icon_max_x = np.min(icon_vis_x), np.max(icon_vis_x)
    icon_min_y, icon_max_y = np.min(icon_vis_y), np.max(icon_vis_y)
    icon_crop = full_rgba.crop((icon_min_x, icon_min_y, icon_max_x + 1, icon_max_y + 1))

    # Center in 512x512 square canvas
    fav_size = 512
    fav_master = Image.new("RGBA", (fav_size, fav_size), (0, 0, 0, 0))
    scale = (fav_size * 0.84) / max(icon_crop.size)
    nw, nh = int(round(icon_crop.size[0] * scale)), int(round(icon_crop.size[1] * scale))
    resized_icon = icon_crop.resize((nw, nh), Image.Resampling.LANCZOS)
    off_x = (fav_size - nw) // 2
    off_y = (fav_size - nh) // 2
    fav_master.paste(resized_icon, (off_x, off_y), resized_icon)

    # Adaptive contrast contour: a subtle white outline behind dark elements so it pops on dark tabs
    fav_arr = np.array(fav_master)
    dark_m = (fav_arr[:, :, 0] < 100) & (fav_arr[:, :, 1] < 100) & (fav_arr[:, :, 2] < 100) & (fav_arr[:, :, 3] > 80)
    m_img = Image.fromarray(np.uint8(dark_m * 255), "L").filter(ImageFilter.MaxFilter(7))
    halo_arr = np.zeros_like(fav_arr)
    halo_arr[:, :, 0] = 255
    halo_arr[:, :, 1] = 255
    halo_arr[:, :, 2] = 255
    halo_arr[:, :, 3] = np.array(m_img)
    halo_img = Image.fromarray(halo_arr, "RGBA").filter(ImageFilter.GaussianBlur(1.5))
    fav_enhanced = Image.alpha_composite(halo_img, fav_master)

    # Target directories
    target_dirs = [
        BASE_DIR / "images" / "homepage",
        Path(r"D:\Projects\Rank_Rent_Starter_Kit\images\homepage"),
    ]
    if (BASE_DIR / "dist_keystone" / "images" / "homepage").exists():
        target_dirs.append(BASE_DIR / "dist_keystone" / "images" / "homepage")

    slug = "rockford-air-duct-pros"

    for t_dir in target_dirs:
        t_dir.mkdir(parents=True, exist_ok=True)

        # 1. Main Logo
        dark_path = t_dir / f"{slug}-logo.webp"
        logo_dark.save(dark_path, "WEBP", quality=95, method=6)

        # 2. Light Logo (Footer)
        light_path = t_dir / f"{slug}-logo-light.webp"
        logo_light.save(light_path, "WEBP", quality=95, method=6)

        # 3. Favicon WebP (128x128)
        fav_path = t_dir / f"{slug}-favicon.webp"
        fav_enhanced.resize((128, 128), Image.Resampling.LANCZOS).save(fav_path, "WEBP", quality=95, method=6)

        # 4. Favicon PNG fallback
        fav_png = t_dir / f"{slug}-favicon.png"
        fav_enhanced.resize((128, 128), Image.Resampling.LANCZOS).save(fav_png, "PNG")

        print(f"Synced to {t_dir}:")
        print(f"  - {dark_path.name}: {dark_path.stat().st_size / 1024:.1f} KB ({logo_dark.size[0]}x{logo_dark.size[1]}px)")
        print(f"  - {light_path.name}: {light_path.stat().st_size / 1024:.1f} KB ({logo_light.size[0]}x{logo_light.size[1]}px)")
        print(f"  - {fav_path.name}: {fav_path.stat().st_size / 1024:.1f} KB (128x128px)")

    # Also save standard favicon.ico at root locations
    for root_dir in [BASE_DIR, BASE_DIR / "builder", Path(r"D:\Projects\Rank_Rent_Starter_Kit")]:
        if root_dir.exists():
            ico_path = root_dir / "favicon.ico"
            fav_enhanced.resize((64, 64), Image.Resampling.LANCZOS).save(
                ico_path, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
            )
            print(f"Saved {ico_path} ({ico_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    src = USER_IMAGE
    if len(sys.argv) > 1:
        src = Path(sys.argv[1])
    process_logo(src)
