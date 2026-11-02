# raw_research/ — Manual Drop Folder

Place exported research files here before running `scripts/build_data.py`.
`build_data.py` reads whatever it finds — missing files are skipped gracefully.

> **Full Step-by-Step Instructions:**
> See `MANUAL_RESEARCH_COLLECTION_GUIDE.md` in the project root for exact URLs, export steps, and free tool alternatives for each file below.

## Expected Files (all optional — drop what you have)

> **Golden Rule of Query Intent:**
> - **Questions / Informational files (`semrush_questions.csv`, `paa_export.csv`, `answerthepublic.csv`):** Search **broad niche only** (e.g. `air duct cleaning`, NOT `air duct cleaning rockford`). Homeowners ask questions broadly; the AI localizes the answers.
> - **Keywords / Transactional files (`semrush_keywords.csv`, `ahrefs_keywords.csv`, `serp_snippets.csv`):** Search **local** (e.g. `air duct cleaning rockford il`).

| File Keyword Pattern | Example Filename You Drop In | Source Tool | What It Captures |
|---|---|---|---|
| `*alsoasked*` or `*paa*` | `alsoasked-air-duct-cleaning-rockford...csv` | AlsoAsked.com / Google PAA | Real customer PAA questions |
| `*table*`, `*semrush*`, `*magic*` | `table_air+duct+cleaning_1416rows...csv` | SEMrush Keyword Magic | High-volume questions & KD |
| `*answerthepublic*` or `*atp*` | `answerthepublic.txt` (or `.csv`) | AnswerThePublic.com | Informational content ideas |
| `*serp*`, `*snippet*`, `*sbmm*` | `serp_snippets.txt` (or `.csv`) | SBMM / Google Search | Competitor domains & titles |
| `*topical*` or `*relevance*` | `topicalrelevance.txt` | TopicalRelevance.com | Semantic entities & Schema |
| `*youtube*` or `*transcript*` | `youtube_transcript.txt` | YouTube URLs or Transcript | Tradesperson terminology |
| `*ahrefs*` | `ahrefs_keywords.csv` (root or raw/) | Ahrefs Explorer | Primary & local target keywords |
| `*compiled*` or `*forum*` | `compiled_research.txt` | Reddit / Quora / Scraper | Real customer complaints & scams |

## Flexible File Naming (Adaptive Ingestion)
`build_data.py` uses intelligent pattern matching! You do NOT need to rename your files to rigid names. As long as the filename contains words like `alsoasked`/`paa`, `table`/`semrush`, `answerthepublic`, `serp`/`sbmm`, `topical`, or `youtube`, it will automatically be parsed in either `.csv` or `.txt` format.
- CSV files: first column = keyword or question, header row optional
- TXT files: paste raw text, any format — build_data.py reads full content

## What Gets Auto-Generated
- `research_data.txt` — from `scripts/research_scraper.py` (Playwright scraper)
- `data.txt` — from `scripts/build_data.py` (merges all sources above)
- `data_brief.txt` — from `scripts/data_extractor.py` (compresses data.txt for P4)

