# raw_research/ — Manual Drop Folder

Everything the pipeline cannot invent goes here **before** you run `build_data.py`. The AI prompts (1, 2, 3) supply market, local and competitor
knowledge from their own training. This folder supplies the real facts and the real research data that the AI cannot know.

> **Full Step-by-Step Instructions:** see `MANUAL_RESEARCH_COLLECTION_GUIDE.md` in the project root for exact URLs, export steps and free tool alternatives.

## REQUIRED for every site: NAP and logo

A site cannot be built without these two. `build_data.py` reads them, `pre_brief_check.py` blocks Prompt 4 if the NAP is missing, and the logo is needed before the site build.

### 1. NAP file (Name, Address, Phone): `nap.txt`
Copy `nap.example.txt` to `nap.txt` (or provide `nap.json`) and fill it in. One `Key: value` per line.

| Key | Required | Notes |
|---|---|---|
| `Company Name` | yes | Exactly as on the Google Business Profile |
| `Phone` | yes | The number customers will call (your tracking / forwarding number if you use one). Format `(555) 555-0100` |
| `Address` | yes | `Street, City, ST 12345`. This is what goes into schema, so it must be a real, consistent address |
| `Email`, `Website` | yes | `https://` full domain |
| `Founded` | recommended | Year |
| `License Number`, `Insurance`, `Hours`, `Service Area`, profile links, `External Phones` | optional | Anything listed here is passed to the brief and the writer may state it. The writer is not allowed to invent license numbers, hours or credentials |

Why it matters: the phone, name and address are copied into the schema and every page. The pipeline gate **fails** any page that shows a different phone number.
A third-party number cited in your content (for example a state consumer hotline) must be listed under `External Phones`.

### 2. Logo: `logo.webp` (or `logo.png`)
Drop these in this folder. Only the first one is required:

| File | Required | Notes |
|---|---|---|
| `logo.webp` / `logo.png` / `logo.jpg` | yes | Best: transparent background, at least 800 px wide. A logo on a plain white background also works (the tool removes the white) |
| `logo-light.*` | optional | Your own white-text version for dark footers. If missing, one is derived (dark ink turned white) |
| `favicon.*` | optional | Icon-only mark, no text, square is best. If missing, the icon is cropped from the logo when it sits apart from the text |

Then run:
```
python scripts/process_logo.py
```
It writes `images/homepage/<company-slug>-logo.webp`, `-logo-light.webp`, `-favicon.webp/.png` (all transparent, each under 100 KB, no digits in file names)
and `favicon.ico`, then the builder finds them by name. If it prints a warning that the icon could not be isolated, provide `favicon.png` yourself.
Do not put a logo on service vans or uniforms in AI images: that is a separate white-label rule.

## Research files (all optional, drop what you have)

`build_data.py` reads whatever it finds. Missing files are skipped gracefully.

> **Golden Rule of Query Intent:**
> - **Questions / informational files (`semrush_questions.csv`, `paa_export.csv`, `answerthepublic.csv`):** search the **broad niche only** (e.g. `air duct cleaning`, NOT `air duct cleaning rockford`). People ask questions broadly; the AI localizes the answers.
> - **Keyword / transactional files (`semrush_keywords.csv`, `ahrefs_keywords.csv`, `serp_snippets.csv`):** search **local** (e.g. `air duct cleaning rockford il`).

| File Keyword Pattern | Example Filename You Drop In | Source Tool | What It Captures |
|---|---|---|---|
| `nap` (exact name) | `nap.txt` or `nap.json` | You / client | **REQUIRED.** Name, address, phone and business facts |
| `logo*`, `favicon*` | `logo.webp`, `logo-light.png`, `favicon.png` | You / client | **REQUIRED (logo).** Brand assets |
| `*alsoasked*` or `*paa*` | `alsoasked-air-duct-cleaning-rockford...csv` | AlsoAsked.com / Google PAA | Real customer PAA questions |
| `*table*`, `*semrush*`, `*magic*` | `table_air+duct+cleaning_1416rows...csv` | SEMrush Keyword Magic | High-volume questions & KD |
| `*answerthepublic*` or `*atp*` | `answerthepublic.txt` (or `.csv`) | AnswerThePublic.com | Informational content ideas |
| `*serp*`, `*snippet*`, `*sbmm*` | `serp_snippets.txt` (or `.csv`) | SBMM / Google Search | Competitor domains & titles |
| `*topical*` or `*relevance*` | `topicalrelevance.txt` | TopicalRelevance.com | Semantic entities & schema |
| `*youtube*` or `*transcript*` | `youtube_transcript.txt` | YouTube URLs or transcript | Tradesperson terminology |
| `*ahrefs*` | `ahrefs_keywords.csv` (root or here) | Ahrefs Explorer | Primary & local target keywords |
| `*compiled*` or `*forum*` | `compiled_research.txt` | Reddit / Quora / scraper | Real customer complaints & scams |

## Flexible File Naming (Adaptive Ingestion)
`build_data.py` uses pattern matching, so you do not need rigid names. As long as the file name contains words like `alsoasked`/`paa`, `table`/`semrush`, `answerthepublic`, `serp`/`sbmm`, `topical` or `youtube`, it is parsed as `.csv` or `.txt`.
The two required files are the exception: the NAP file must be named exactly `nap` (or `business_info`) and the logo file name must contain `logo`.
- CSV files: first column = keyword or question, header row optional
- TXT files: paste raw text, any format

## What Gets Auto-Generated
- `research_data.txt`: from `scripts/research_scraper.py` (Playwright scraper)
- `data.txt`: from `build_data.py` (merges all sources above, with your NAP at the top)
- `data_brief.txt`: from `scripts/data_extractor.py` (compresses data.txt for Prompt 4)
- `images/homepage/<slug>-logo*.webp`, `-favicon.*`, `favicon.ico`: from `scripts/process_logo.py`

## Order of operations for a new site
1. `python new_project.py` (clears the previous site; keeps this README and the `*.example.*` templates)
2. Fill in `nap.txt`, add `logo.*`, drop your research exports
3. `python build_data.py`, then `python pre_brief_check.py` (use the `scripts/` copy if that is where yours lives) (fails if NAP is missing or still a placeholder)
4. `python scripts/process_logo.py`
5. Prompts 4 to 8, running `python scripts/pipeline_gate.py` after each page
