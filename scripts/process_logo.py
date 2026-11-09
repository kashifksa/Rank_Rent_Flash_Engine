#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process_logo.py - turns the logo you drop in raw_research/ into web-ready brand assets for ANY site.

    python scripts/process_logo.py                      # finds raw_research/logo.* automatically
    python scripts/process_logo.py path/to/logo.png     # or point at a file

Reads (all optional except the logo):
    raw_research/logo.(webp|png|jpg|svg-less)        the main logo (transparent PNG/WebP is best; a logo on a plain white background also works)
    raw_research/logo-light.*                        your own white-text version for dark footers (otherwise one is derived)
    raw_research/favicon.*                           your own icon-only mark (otherwise the icon is cropped from the logo when it can be isolated)

Writes to images/homepage/ (slug comes from master_brief.json company name):
    <slug>-logo.webp, <slug>-logo-light.webp, <slug>-favicon.webp (+ .png) and favicon.ico in the project root
All WebP files are transparent and under 100 KB (hard rule). The builder auto-detects them by the `logo` / `favicon` file names.
"""
import sys, re, json, argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
BASE = HERE.parent if (HERE.parent / "raw_research").exists() or HERE.name == "scripts" else HERE
RAW = BASE / "raw_research"
MAX_KB = 100
EXTS = (".webp", ".png", ".jpg", ".jpeg")


def slug_for_project():
    name = ""
    try:
        b = json.loads((BASE / "master_brief.json").read_text(encoding="utf-8"))
        name = (b.get("nap", {}).get("company_name") or b.get("project_name") or "").strip()
    except Exception:
        pass
    if not name and RAW.exists():  # the brief does not exist yet at this stage: read the company name you gave in nap.txt
        for f in sorted(RAW.iterdir()):
            if f.is_file() and f.stem.lower() in ("nap", "business_info", "business-info", "company_info", "company-info") and f.suffix.lower() == ".txt":
                m = re.search(r"^\s*(?:company name|company|business name|name)\s*:\s*(.+)$", f.read_text(encoding="utf-8", errors="ignore"), re.I | re.M)
                if m:
                    name = m.group(1).strip()
                break
    s = re.sub(r"[^a-z]+", "-", name.lower()).strip("-")  # letters only: image filenames may not contain digits
    return s or "site"


def find(stem_test):
    if not RAW.exists():
        return None
    for p in sorted(RAW.iterdir()):
        if p.is_file() and p.suffix.lower() in EXTS and stem_test(p.stem.lower()):
            return p
    return None


def save_webp(img, path):
    for q in (95, 90, 85, 75, 65, 50):
        img.save(path, "WEBP", quality=q, method=6)
        if path.stat().st_size <= MAX_KB * 1024:
            return round(path.stat().st_size / 1024, 1)
    # still too big: scale down in steps
    w, h = img.size
    while path.stat().st_size > MAX_KB * 1024 and w > 64:
        w, h = int(w * 0.85), int(h * 0.85)
        img = img.resize((w, h))
        img.save(path, "WEBP", quality=80, method=6)
    return round(path.stat().st_size / 1024, 1)


def to_rgba(im):
    """Return a transparent RGBA. Already-transparent images are kept; plain light backgrounds are removed with edge unblending."""
    import numpy as np
    from PIL import Image
    im = im.convert("RGBA")
    a = np.array(im)
    if (a[:, :, 3] < 250).mean() > 0.02:  # real transparency already
        return im, "kept existing transparency"
    border = np.concatenate([a[0, :, :3], a[-1, :, :3], a[:, 0, :3], a[:, -1, :3]]).astype(np.float32)
    bg = np.median(border, axis=0)
    if bg.min() < 215 or (border.max(axis=0) - border.min(axis=0)).max() > 14:
        return im, "background is not a plain light color: kept as-is (supply a transparent PNG/WebP for best results)"
    arr = a[:, :, :3].astype(np.float32)
    diff = np.maximum.reduce([bg[c] - arr[:, :, c] for c in range(3)])
    diff = np.maximum(diff, 0.0)
    sat = arr.max(axis=2) - arr.min(axis=2)
    full = np.where(sat > 60, 250.0, np.maximum(bg.mean() - 40.0, 100.0))  # colored ink drops further than dark neutral ink
    alpha = np.clip((diff - 4.0) / (full - 4.0), 0.0, 1.0)
    alpha = np.where(diff <= 4.0, 0.0, alpha)
    fg = np.zeros_like(arr)
    for c in range(3):
        fg[:, :, c] = np.clip((arr[:, :, c] - (1.0 - alpha) * bg[c]) / np.maximum(alpha, 0.01), 0.0, 255.0)
    out = np.zeros(a.shape, dtype=np.uint8)
    out[:, :, :3] = np.uint8(np.round(fg))
    out[:, :, 3] = np.uint8(np.round(alpha * 255.0))
    return Image.fromarray(out, "RGBA"), "removed plain background (edge unblending, no white halo)"


def crop_bbox(rgba, pad=6):
    import numpy as np
    a = np.array(rgba)[:, :, 3]
    ys, xs = np.where(a > 8)
    if len(xs) == 0:
        return rgba
    return rgba.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(rgba.width, xs.max() + pad + 1), min(rgba.height, ys.max() + pad + 1)))


def light_variant(rgba):
    """White-out neutral dark ink (text/outline) for dark footers; coloured ink is kept."""
    import numpy as np
    from PIL import Image
    a = np.array(rgba).copy()
    rgb = a[:, :, :3].astype(np.float32)
    lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    dark = (a[:, :, 3] > 8) & (lum < 120) & (sat < 60)
    a[dark, 0] = a[dark, 1] = a[dark, 2] = 255
    return Image.fromarray(a, "RGBA")


def isolate_icon(rgba):
    """Left-most ink block separated from the rest by a clear gap (typical icon + wordmark logo). None if it can't be isolated."""
    import numpy as np
    a = np.array(rgba)[:, :, 3] > 8
    cols = a.any(axis=0)
    w = len(cols)
    segs, start = [], None
    min_gap = max(8, int(w * 0.02))
    gap = 0
    for x in range(w):
        if cols[x]:
            if start is None:
                start = x
            last = x
            gap = 0
        elif start is not None:
            gap += 1
            if gap >= min_gap:
                segs.append((start, last))
                start = None
    if start is not None:
        segs.append((start, last))
    if len(segs) < 2:
        return None
    x0, x1 = segs[0]
    ys = np.where(a[:, x0:x1 + 1].any(axis=1))[0]
    box = rgba.crop((x0, int(ys.min()), x1 + 1, int(ys.max()) + 1))
    ratio = box.width / box.height
    if not (0.4 <= ratio <= 2.5) or box.width < w * 0.08:
        return None
    return crop_bbox(box, pad=2)


def make_favicon(icon_rgba):
    import numpy as np
    from PIL import Image, ImageFilter
    size = 512
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scale = (size * 0.84) / max(icon_rgba.size)
    nw, nh = int(round(icon_rgba.width * scale)), int(round(icon_rgba.height * scale))
    icon = icon_rgba.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(icon, ((size - nw) // 2, (size - nh) // 2), icon)
    arr = np.array(canvas)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    dark = (lum < 100) & (arr[:, :, 3] > 80)
    if dark.any():  # thin light contour so dark parts stay visible on dark browser tabs
        m = Image.fromarray(np.uint8(dark * 255), "L").filter(ImageFilter.MaxFilter(7))
        halo = np.zeros_like(arr)
        halo[:, :, :3] = 255
        halo[:, :, 3] = np.array(m)
        canvas = Image.alpha_composite(Image.fromarray(halo, "RGBA").filter(ImageFilter.GaussianBlur(1.5)), canvas)
    return canvas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logo", nargs="?")
    a = ap.parse_args()
    from PIL import Image

    src = Path(a.logo) if a.logo else find(lambda s: "logo" in s and "light" not in s and "favicon" not in s)
    if not src or not src.exists():
        print("ERROR: no logo found. Put your logo in raw_research/ named logo.webp / logo.png (see raw_research/README.md).")
        return 1
    slug = slug_for_project()
    out = BASE / "images" / "homepage"
    out.mkdir(parents=True, exist_ok=True)
    print(f"Logo source : {src}\nSite slug   : {slug}\nOutput      : {out}")

    rgba, note = to_rgba(Image.open(src))
    print("  - " + note)
    logo = crop_bbox(rgba)
    p = out / f"{slug}-logo.webp"
    kb = save_webp(logo, p)
    print(f"  OK {p.name}  {logo.width}x{logo.height}px  {kb} KB")

    own_light = find(lambda s: "logo" in s and "light" in s)
    if own_light:
        light, _ = to_rgba(Image.open(own_light))
        light = crop_bbox(light)
        how = f"your file {own_light.name}"
    else:
        light, how = light_variant(logo), "derived (dark ink turned white, coloured ink kept)"
    p = out / f"{slug}-logo-light.webp"
    kb = save_webp(light, p)
    print(f"  OK {p.name}  {light.width}x{light.height}px  {kb} KB  [{how}]")

    own_fav = find(lambda s: "favicon" in s or s in ("icon", "favicon-icon"))
    if own_fav:
        icon, _ = to_rgba(Image.open(own_fav))
        icon, how = crop_bbox(icon, pad=2), f"your file {own_fav.name}"
    else:
        icon = isolate_icon(logo)
        how = "icon cropped from the logo (text excluded)"
        if icon is None:
            icon = logo
            how = "WARNING: could not isolate an icon from the logo, using the whole logo. Provide raw_research/favicon.png (icon only) for a clean favicon."
    fav = make_favicon(icon)
    p = out / f"{slug}-favicon.webp"
    kb = save_webp(fav.resize((128, 128), Image.Resampling.LANCZOS), p)
    fav.resize((128, 128), Image.Resampling.LANCZOS).save(out / f"{slug}-favicon.png")
    fav.resize((64, 64), Image.Resampling.LANCZOS).save(BASE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print(f"  OK {p.name}  128x128px  {kb} KB  [{how}]")
    print("  OK favicon.ico (project root)\n\nNext: python scripts/compile_builder_data.py  (the builder auto-detects *logo* / *favicon* in images/).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
