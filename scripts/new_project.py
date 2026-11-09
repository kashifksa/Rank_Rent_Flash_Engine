#!/usr/bin/env python3
"""
new_project.py — Rank & Rent Flash Engine
Resets the engine or initializes a clean state for a new niche/city project.
"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

_here = Path(__file__).resolve().parent
ROOT = _here if (_here / 'AGENTS.md').exists() else _here.parent

def reset_project(archive=True):
    print("=" * 60)
    print("  RANK & RENT FLASH ENGINE — NEW PROJECT INITIALIZER")
    print("=" * 60)
    
    if archive:
        archive_dir = ROOT / "archive" / datetime.now().strftime("project_%Y%m%d_%H%M%S")
        archive_dir.mkdir(parents=True, exist_ok=True)
        print(f"Archiving existing run data to: {archive_dir}")
        
        # Files to archive
        to_archive = [
            "master_brief.json", "topical_authority.json", "master_site_blueprint.json",
            "data.txt", "data_brief.txt", "research_data.txt"
        ]
        for fname in to_archive:
            fpath = ROOT / fname
            if fpath.exists():
                shutil.copy2(fpath, archive_dir / fname)
        
        # Archive raw_research
        raw_dir = ROOT / "raw_research"
        if raw_dir.exists():
            arc_raw = archive_dir / "raw_research"
            arc_raw.mkdir(exist_ok=True)
            for rf in raw_dir.iterdir():
                if rf.name != "README.md" and rf.is_file():
                    shutil.copy2(rf, arc_raw / rf.name)
    
    # Clean raw_research
    raw_dir = ROOT / "raw_research"
    if raw_dir.exists():
        for rf in raw_dir.iterdir():
            if rf.name != "README.md" and rf.is_file():
                rf.unlink()
        print("  ✓ Cleaned raw_research/ (ready for new CSV/TXT files)")
    
    # Remove project files
    for fname in ["data.txt", "data_brief.txt", "research_data.txt", "ahrefs_keywords.csv",
                  "competitor_intelligence.json", "market_intelligence.json"]:
        p = ROOT / fname
        if p.exists():
            p.unlink()
    
    # Remove image plans and page contents
    for p in ROOT.glob("image_plan_*.json"):
        p.unlink()
    for p in ROOT.glob("page_content_*.md"):
        p.unlink()
    for p in (ROOT / "prompts").glob("*argon*.txt"):
        p.unlink()
    for p in (ROOT / "prompts").glob("*clean*.txt"):
        p.unlink()
        
    # Reset work_in_progress
    wip = ROOT / "work_in_progress"
    if wip.exists():
        for sub in wip.iterdir():
            if sub.is_dir():
                shutil.rmtree(sub)
        (wip / ".gitkeep").write_text("# Keep work_in_progress\n", encoding="utf-8")
        print("  ✓ Cleaned work_in_progress/")

    # Reset schemas
    with open(ROOT / "master_brief.json", "w", encoding="utf-8") as f:
        json.dump({"project_name": "", "niche": "", "city": "", "state": "", "monetization_model": "rank_and_rent"}, f, indent=2)
    with open(ROOT / "topical_authority.json", "w", encoding="utf-8") as f:
        json.dump({"blog_categories": [], "pages": []}, f, indent=2)
    with open(ROOT / "master_site_blueprint.json", "w", encoding="utf-8") as f:
        json.dump({"site_name": "", "domain": "", "blog_categories": [], "pages": [], "site_architecture": {}}, f, indent=2)
    with open(ROOT / "pipeline_state.json", "w", encoding="utf-8") as f:
        json.dump({"project": "Rank & Rent Flash Engine", "current_page": None, "completed_pages": []}, f, indent=2)
    
    print("  ✓ Reset pipeline schemas and state")
    print("=" * 60)
    print("SUCCESS: Engine reset and ready for your new niche research!")
    print("Drop your new files into raw_research/ and run: python scripts/build_data.py")
    print("=" * 60)

if __name__ == "__main__":
    reset_project()
