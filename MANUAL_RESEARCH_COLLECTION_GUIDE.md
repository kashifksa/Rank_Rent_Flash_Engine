# MANUAL RESEARCH COLLECTION GUIDE
## Pre-Project Research Gathering Checklist for Rank & Rent Sites

> **Read this before starting any new Rank & Rent project.**
> Collect these files *before* executing the pipeline prompts. Having clean, high-intent research in place ensures `master_brief.json`, `topical_authority.json`, and all page content are hyper-relevant and rank quickly.

---

## 1. Folder Setup

All research files must be placed in:
```
<project_root>/raw_research/
```

Once dropped, running `python scripts/build_data.py` merges all sources into `data.txt` across all 18 sections.

---

> [!IMPORTANT]
> ### THE GOLDEN RULE OF QUERY INTENT (Broad vs. Local)
> * **For Questions (`semrush_questions.csv`, `paa_export.csv`, `answerthepublic.csv`):**
>   * **Search BROAD NICHE ONLY** (e.g. `air duct cleaning`, NOT `air duct cleaning rockford il`).
>   * *Why?* Homeowners never type city names into informational questions (nobody searches *"how often should i clean my air ducts in rockford il"* — adding the city name yields zero results). The pipeline takes these universal questions for your H2s, FAQs, and blog posts, and the AI automatically localizes the **answers** with your target city's weather, home types, and local context.
> * **For Keywords & SERP (`semrush_keywords.csv`, `ahrefs_keywords.csv`, `serp_snippets.csv`):**
>   * **Search LOCAL** (e.g. `air duct cleaning rockford il`).
>   * *Why?* People looking to hire search with local intent. We need local search volume and local competitor rankings for our service and location pages.

---

## 2. Quick Master Inventory

| Filename Pattern (Fuzzy) | Example Name You Can Drop | Source Tool | Key Purpose |
|---|---|---|---|
| `*alsoasked*` or `*paa*` | `alsoasked-air-duct-cleaning...csv` | [AlsoAsked.com](https://alsoasked.com) | Google People Also Ask tree (H2 questions, FAQ section) |
| `*table*`, `*semrush*`, `*magic*` | `table_air+duct_1416rows...csv` | SEMrush / Ahrefs | Search volume-backed questions & KD metrics |
| `*answerthepublic*` or `*atp*` | `answerthepublic.txt` (or `.csv`) | [AnswerThePublic.com](https://answerthepublic.com) | Informational long-tail questions, comparisons, prepositions |
| `*serp*`, `*snippet*`, `*sbmm*` | `serp_snippets.txt` (or `.csv`) | Google / SBMM | Top 5-10 competitor domains, titles & snippets |
| `*topical*` or `*relevance*` | `topicalrelevance.txt` | [TopicalRelevance.com](https://topicalrelevance.com) | Frequency & relevance semantic entities, Schema markup |
| `*youtube*` or `*transcript*` | `youtube_transcript.txt` | YouTube URLs or Transcript | Real technician spoken language, equipment terms, scam talk |
| `*ahrefs*` | `ahrefs_keywords.csv` | Ahrefs Explorer | Niche + city keyword variations, volume, KD |
| `*compiled*` or `*forum*` | `compiled_research.txt` | Reddit / Quora / Scraper | Real customer complaints, fears, pricing pushback |

---

## 3. Step-by-Step Collection Guide

### File 1: `topicalrelevance.txt`
* **Website:** https://topicalrelevance.com
* **Cost:** Free
* **Why it matters:** Google uses semantic entity relationships to evaluate topical authority. This tool tells you the exact words, frequency targets, and Schema entities Google expects on the topic.

#### How to collect:
1. Open [TopicalRelevance.com](https://topicalrelevance.com).
2. Enter your primary niche (e.g., `air duct cleaning`, `sprinkler repair`, `epoxy flooring`).
3. Select Country: **United States** (or your target country).
4. Click **Generate / Submit**.
5. Once the report loads, copy the entire output containing:
   - **Frequency Entities** (words to use frequently)
   - **Relevance Entities** (high-confidence semantic entities)
   - **Schema Markup** (`<script type="application/ld+json">`)
6. Open Notepad or VS Code, paste the content, and save as:
   ```
   raw_research/topicalrelevance.txt
   ```

---

### File 2: `answerthepublic.csv`
* **Website:** https://answerthepublic.com
* **Cost:** Free tier allows 1-3 free searches per day
* **Why it matters:** Generates 100-300 customer search queries organized by *How*, *What*, *Why*, *Where*, *Can*, *Vs*, and prepositions. Feeds Phase 5 blog posts and service page FAQs.

#### How to collect:
1. Go to [AnswerThePublic.com](https://answerthepublic.com).
2. Enter your primary niche (e.g., `air duct cleaning`).
3. Select Country: **United States** and Language: **English**.
4. Click **Search**.
5. In the top right corner of the results page, click **Download CSV**.
6. Move the downloaded file into `raw_research/` and rename it to:
   ```
   raw_research/answerthepublic.csv
   ```

---

### File 3: `paa_export.csv`
* **Website:** https://alsoasked.com (or Google PAA via free Chrome extensions)
* **Cost:** Free tier allows 3 searches per month
* **Why it matters:** Google's "People Also Ask" box reflects real-time searcher intent. Using these exact questions as H2/H3 subheadings directly triggers Google Featured Snippets and PAA placements.

#### How to collect:
1. Go to [AlsoAsked.com](https://alsoasked.com).
2. Enter your **broad niche** query: `[niche]` (e.g. `air duct cleaning`).
   > ⚠️ **Do NOT add the city name.** Search `air duct cleaning`, not `air duct cleaning rockford`. AlsoAsked will map out the complete real-time Google PAA question tree.
3. Select Region: **United States** and Language: **English**.
4. Click **Search**.
5. Click the **Export CSV** button (top right).
6. Move the file into `raw_research/` and rename it to:
   ```
   raw_research/paa_export.csv
   ```
*(Alternative: If using SEMrush or Ahrefs, export the "Questions" tab filtered by "people also ask".)*

---

### File 4: `semrush_questions.csv`
* **Website:** SEMrush (Keyword Magic Tool) or Ahrefs / Ubersuggest
* **Cost:** Free or Paid
* **Why it matters:** Provides search-volume filtered questions for blog posts and service page sections.

#### How to collect:
1. Open SEMrush / Ahrefs Keyword Explorer.
2. Enter your **broad niche** keyword: `[niche]` (e.g., `air duct cleaning`).
   > ⚠️ **Do NOT include the city name.** Searching `air duct cleaning rockford il` in the Questions tab will return 0 results because people ask questions broadly. Search `air duct cleaning` to get thousands of high-volume questions.
3. Click the **Questions** tab/filter.
4. Export the list to CSV (first 100-200 rows is plenty).
5. Save or rename the CSV to:
   ```
   raw_research/semrush_questions.csv
   ```
> *Format Note: The first column of the CSV should contain the question text.*

---

### File 5: `semrush_keywords.csv` (or `ahrefs_keywords.csv`)
* **Website:** SEMrush / Ahrefs / Google Keyword Planner
* **Cost:** Free or Paid
* **Why it matters:** Maps primary, secondary, and LSI keywords with monthly search volume and KD. Ingested into Section 2 of `data.txt`.

#### How to collect:
1. Search `[niche] [city]` and related variations (e.g., `dryer vent cleaning [city]`, `hvac duct cleaning [city]`).
2. Export the keyword list as CSV.
3. Save as:
   ```
   raw_research/semrush_keywords.csv
   ```
*(If you already have `ahrefs_keywords.csv`, leave it in the project root folder; `build_data.py` reads both.)*

---

### File 6: `youtube_transcript.txt`
* **Source:** Automated via `scripts/youtube_scraper.py` (No API key needed)
* **Cost:** 100% Free
* **Why it matters:** Transcripts capture the authentic spoken terminology of tradespeople: exact equipment names (*negative air vacuum*, *rotary brush*, *HEPA filtration*), step-by-step procedures, and warnings about common industry scams.

#### How to run:
1. Find 1-2 top competitor or explainer videos on YouTube:
   - Search 1: `[niche] process step by step` or `how [niche] is done`
   - Search 2: `[niche] scams exposed` or `how to avoid [niche] scams`
2. Paste their URLs into `youtube_urls.txt` (one per line).
3. Run our scraper:
   ```powershell
   python scripts/youtube_scraper.py
   ```
   *The script automatically extracts the cleaned transcripts and writes them directly to `raw_research/youtube_transcript.txt`.*

*(Optional Fallback: If a specific video has auto-captions turned off by the creator, you can grab the transcript using NoteGPT.io and paste it into `raw_research/youtube_transcript.txt`.)*

---

### File 7: `serp_snippets.csv`
* **Website:** Google Search (Incognito window)
* **Cost:** Free
* **Why it matters:** Analyzes what Google is *currently* ranking in the top 5-10 positions for `[niche] [city]`. Ingests competitor meta descriptions, value propositions, and calls to action.

#### How to collect:
1. Open an Incognito browser window.
2. Search: `[niche] [city] [state]` (e.g., `air duct cleaning rockford il`).
3. Create a CSV file with columns: `Title,Snippet,URL`.
4. Copy the Title, Meta Snippet, and URL of the top 5 to 10 local organic results (skip national directories like Yelp/Angi if local sites exist).
5. Save as:
   ```
   raw_research/serp_snippets.csv
   ```

---

### File 8: `compiled_research.txt` (Customer Voice / Forum Notes)
* **Website:** Reddit, Quora, or Scraper output
* **Cost:** Free
* **Why it matters:** Gives your content authentic local voice, real customer pain points, and objection responses that AI prompts cannot invent out of thin air.

#### How to collect:
If the automated Playwright scraper (`research_scraper.py`) encounters CAPTCHA or blocks, collect manual forum nuggets:
1. Search Google with:
   - `site:reddit.com "[niche]" "scam" OR "cost" OR "problem"`
   - `site:reddit.com "[niche]" "worth it" OR "diy"`
   - `site:quora.com "[niche]" "how often" OR "complaint"`
2. Copy 5-10 raw paragraphs of customer rants, questions, and honest experiences.
3. Save as:
   ```
   raw_research/compiled_research.txt
   ```

---

## 4. Pre-Project Verification Checklist

Before running Prompt 1 or Prompt 4, verify your `raw_research/` folder:

- [ ] `raw_research/topicalrelevance.txt` is present and contains Frequency/Relevance entities
- [ ] `raw_research/answerthepublic.csv` is present
- [ ] `raw_research/paa_export.csv` is present
- [ ] `raw_research/youtube_transcript.txt` is present and contains real transcript text
- [ ] `raw_research/semrush_questions.csv` or `semrush_keywords.csv` is present
- [ ] (Optional) `raw_research/serp_snippets.csv` is present

---

## 5. Ingestion Command

Once the files are placed in `raw_research/`, run:

```powershell
python scripts/build_data.py
```

### What happens:
1. `build_data.py` scans `raw_research/` for every file above.
2. It categorizes pain points, trust signals, objections, and forum questions.
3. It merges all keywords, PAA questions, topical entities, and YouTube transcripts.
4. It outputs `data.txt` with all 18 structured sections.
5. Missing files are skipped gracefully without breaking the build.

Then run the validation check:
```powershell
python scripts/pre_brief_check.py
```
If validation passes, proceed directly to the pipeline prompts!

