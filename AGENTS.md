# AGENTS.md — Rank & Rent Flash Engine
## Read this file first before doing anything else in this project.

---

## WHAT THIS REPO IS

This is the **Flash-optimized** version of the Rank & Rent SEO pipeline.

It is designed to run entirely on **Gemini Flash 3.8** — no Gemini Pro, no Claude required.

The quality gap is closed by:
1. **Atomic mini-prompts** — one prompt per page section (not one giant prompt per page)
2. **Golden examples** — embedded real output examples in every mini-prompt
3. **Self-check blocks** — Flash validates its own output against a checklist before finalizing
4. **Strict structure files** — section order, H2 formulas, word counts leave no room for drift

All project variables (niche, city, state, NAP, keywords) come from `data.txt` → `master_brief.json`.
Do NOT hardcode niche-specific data anywhere.

---

## REPO RELATIONSHIP

| Repo | Purpose | Model |
|---|---|---|
| `Rank_Rent_Starter_Kit` | Universal template kit — reference prompts | Gemini Pro + Claude Sonnet |
| `Rank_Rent_Flash_Engine` | Production automation — this repo | Gemini Flash 3.8 only |

This repo inherits all hard rules from `Rank_Rent_Starter_Kit/AGENTS.md`.
Flash Engine rules EXTEND those rules — they do not replace them.

---

## FOLDER STRUCTURE

```
Rank_Rent_Flash_Engine/
├── AGENTS.md                    ← This file — read first
├── PIPELINE_GUIDE.txt           ← Execution flow and commands
├── README.md                    ← Repo overview
│
├── prompts/
│   ├── P1_role.md               ← Set Flash role for session
│   ├── P2_market.md             ← Market intelligence (JSON output)
│   ├── P3_competitor.md         ← Competitor analysis (JSON output)
│   ├── P4_brief.md              ← → master_brief.json
│   ├── P5_topical.md            ← → topical_authority.json
│   ├── P6_blueprint.md          ← → master_site_blueprint.json (ONCE only)
│   ├── P8_images.md             ← → image_plan_[slug].json
│   │
│   ├── P7_service/              ← Atomic section prompts — service pages
│   │   ├── P7s_01_hero.md
│   │   ├── P7s_02_trust_bar.md
│   │   ├── P7s_03_services_grid.md
│   │   ├── P7s_04_why_us.md
│   │   ├── P7s_05_process.md
│   │   ├── P7s_06_local_proof.md
│   │   ├── P7s_07_service_area.md
│   │   ├── P7s_08_mid_cta.md
│   │   ├── P7s_09_faq.md
│   │   └── P7s_10_bottom_cta.md
│   │
│   ├── P7_location/             ← Atomic section prompts — location pages
│   │   ├── P7l_01_hero.md
│   │   ├── P7l_02_localized_intro.md
│   │   ├── P7l_03_services_overview.md
│   │   ├── P7l_04_local_proof.md
│   │   ├── P7l_05_local_faq.md
│   │   ├── P7l_06_service_area.md
│   │   └── P7l_07_bottom_cta.md
│   │
│   ├── P7_blog/                 ← Atomic section prompts — blog posts
│   │   ├── P7b_01_header.md
│   │   ├── P7b_02_cause_context.md
│   │   ├── P7b_03_diy_vs_pro.md
│   │   ├── P7b_04_structured_data.md
│   │   ├── P7b_05_how_it_works.md
│   │   ├── P7b_06_local_considerations.md
│   │   ├── P7b_07_faq.md
│   │   └── P7b_08_conclusion_cta.md
│   │
│   └── P7_about/                ← Atomic section prompts — about/contact
│       ├── P7a_01_identity_hook.md
│       ├── P7a_02_origin_story.md
│       ├── P7a_03_team_credentials.md
│       ├── P7a_04_credentials_display.md
│       ├── P7a_05_community_proof.md
│       ├── P7a_06_trust_signals.md
│       ├── P7a_07_service_area_nap.md
│       └── P7a_08_bottom_cta.md
│
├── examples/                    ← Golden outputs (generated with Claude/Pro)
│   ├── service_page_example.md  ← Perfect service page — Flash copies this pattern
│   ├── location_page_example.md
│   ├── blog_post_example.md
│   └── about_page_example.md
│
├── scripts/                     ← All pipeline scripts
│   ├── data_extractor.py        ← Compresses data.txt → data_brief.txt for Flash 3.8
│   ├── orchestrator.py          ← Master pipeline runner — sequences all steps
│   ├── pipeline_state.json      ← Tracks current step — enables resume
│   ├── pre_publish_filter.py
│   ├── audit_pages.py
│   ├── check_blog_cannibalization.py
│   ├── check_blueprint_sync.py
│   ├── clean_research.py
│   ├── pre_brief_check.py
│   ├── build_data.py
│   ├── keyword_checker.py
│   ├── image_geotagger.py
│   ├── research_scraper.py
│   ├── youtube_scraper.py
│   ├── phase1_registry.json
│   └── pending_links.json
│
└── structure/                   ← Page type structure files (from starter kit)
    ├── SERVICE_PAGE_STRUCTURE.md
    ├── LOCATION_PAGE_STRUCTURE.md
    ├── BLOG_POST_STRUCTURE.md
    └── ABOUT_PAGE_STRUCTURE.md
```

---

## MANDATORY READ ORDER — Before Starting Any Task

1. **This file** (`AGENTS.md`) — you are reading it now ✅
2. **`PIPELINE_GUIDE.txt`** — full execution flow with commands
3. **`master_brief.json`** (project folder) — niche, city, NAP, all variables
4. **`scripts/phase1_registry.json`** (project folder) — all live pages and slugs
5. **Structure file for the page type being written** (in `structure/`)

---

## PIPELINE EXECUTION ORDER

| Step | File | Output |
|---|---|---|
| 1 | `prompts/P1_role.md` | Flash role set for session |
| 2 | `prompts/P2_market.md` | Market intelligence (JSON) |
| 3 | `prompts/P3_competitor.md` | Competitor analysis (JSON) |
| — | `python scripts/pre_brief_check.py` | Validates data.txt |
| 4 | `prompts/P4_brief.md` | `master_brief.json` |
| 5 | `prompts/P5_topical.md` | `topical_authority.json` |
| 6 | `prompts/P6_blueprint.md` | `master_site_blueprint.json` (ONCE only) |
| 7 | `prompts/P7_[type]/P7[x]_NN_[section].md` | One section at a time → stitched by orchestrator |
| 8 | `prompts/P8_images.md` | `image_plan_[slug].json` |

---

## FLASH-SPECIFIC HARD RULES

### Atomic Prompt Execution
- **NEVER** run a full-page prompt at once — always run section mini-prompts in order
- Each mini-prompt = one section output only
- `orchestrator.py` stitches sections into the final `page_content_[slug].md`

### Golden Examples
- Every mini-prompt contains an embedded golden example
- Flash MUST follow the example pattern — not invent its own structure
- Golden examples are in the `examples/` folder and referenced inline in mini-prompts

### Self-Check Block
- Every mini-prompt ends with a SELF-CHECK block
- Flash must run the checklist before outputting the section
- If any check fails — rewrite the section internally, then output

### Model
- **ALL steps run on Gemini Flash 3.8** — no model switching
- If a step produces low-quality output: run the self-check prompt again, not a different model

### Everything else — inherits from Rank_Rent_Starter_Kit AGENTS.md
- NEVER call `wp_update_page` directly — always `safe_publish()`
- NEVER link to a page not in `phase1_registry.json`
- NEVER put pricing on any page
- NEVER run PromptSix (P6) more than once per project
- Content-Before-HTML rule (FIX 25) applies
- Blueprint Drift Prevention (FIX 19) applies
- Blog Cannibalization Prevention (FIX 31) applies

