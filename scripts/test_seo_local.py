#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_seo_local.py - sanity tests for the doorway guard. Run: python scripts/test_seo_local.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_local as sl

fails = []
def check(name, ok, extra=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" -> " + str(extra)) if extra and not ok else ""))
    if not ok: fails.append(name)

base = ("We clean air ducts in Loves Park with rotary brushes and negative air machines. Technicians inspect every trunk line "
        "with a camera before and after the work so you can see the result for yourself. Homes near Perryville Road often have older "
        "ductwork that collects construction dust and pet dander over many winters.")
swapped = base.replace("Loves Park", "Belvidere").replace("Perryville Road", "State Street")
different = ("Our crew arrives with a written scope, protects floors, and explains what was found. Dryer vents are separate "
             "from supply ducts and need their own brush and exhaust test at the roof termination before we leave.")

a, b, c = sl.shingles(base, 5), sl.shingles(swapped, 5), sl.shingles(different, 5)
overlap_swap = len(a & b) / len(a)
overlap_diff = len(a & c) / len(a)
check("city-swapped doorway copy scores as similar (>=30%)", overlap_swap >= 0.30, round(overlap_swap, 2))
check("genuinely different text scores low (<10%)", overlap_diff < 0.10, round(overlap_diff, 2))
check("road regex finds Route 251 and Perryville Road", len(sl.ROAD_RE.findall("Take Route 251 past Perryville Road.")) == 2)
check("landmark regex finds school and park", len({m.group(0) for m in sl.LANDMARK_RE.finditer("near Harlem High School and Rock River Park")}) >= 2)
print("\nRESULT: " + ("ALL PASSED" if not fails else f"{len(fails)} FAILED"))
sys.exit(1 if fails else 0)
