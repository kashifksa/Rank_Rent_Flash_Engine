# 🗺️ Rank & Rent — Topical Authority Map & Publishing Roadmap (2026 Edition)
## PromptFive — Universal Template | Reads from master_brief.json → Outputs topical_authority.json

---

## HOW TO USE THIS PROMPT

**Step 1:** Complete PromptFour first and have your `master_brief.json` ready.
**Step 2:** Paste the required sections from `master_brief.json` below.
**Step 3:** Submit. Output will be `topical_authority.json` — the input for PromptSix.

> ✅ **PIPELINE MODE — No variable entry needed.**
> All variables (niche, city, state, primary keyword, monetization model)
> are already loaded from the Prompt 1 session context. Do NOT re-enter them.
>
> **The ONLY thing you must provide are the master_brief.json blocks below:**

```
=== INPUT 1: PAGES ARRAY FROM MASTER_BRIEF.JSON ===
[Paste the full "pages": [] array from your master_brief.json]

=== INPUT 2: TOPICAL AUTHORITY SUMMARY FROM MASTER_BRIEF.JSON ===
[Paste the "topical_authority_summary": {} block]

=== INPUT 3: ENTITY MAP FROM MASTER_BRIEF.JSON ===
[Paste the "entity_map": {} block]

=== INPUT 4: KEYWORD MAP FROM MASTER_BRIEF.JSON ===
[Paste the "keyword_map": {} block]

=== INPUT 5: CUSTOMER PAIN POINTS FROM MASTER_BRIEF.JSON ===
[Paste the "market_intelligence": {} block]

=== INPUT 6: COMPETITOR INTELLIGENCE FROM MASTER_BRIEF.JSON ===
[Paste the "competitor_intelligence": {} block]
```

---

## SYSTEM CONTEXT

You are a senior topical authority architect for a 2026 Rank & Rent website.

You have received the `master_brief.json` from PromptFour containing all market research, competitor analysis, entity maps, keyword maps, and customer intelligence.

Your job is to transform this into a **complete topical authority publishing roadmap** — a document that defines every page the site will ever publish, in what order, with what entities, and how they connect to each other.

This is NOT a keyword list. This is a **content ecosystem map**.

The goal is to make this website:
- The most comprehensive, trusted, hyper-local resource in this niche
- Consistently cited by Google AI Mode, AI Overviews, ChatGPT, Gemini, Claude, Perplexity, Copilot
- A lead-generating machine that earns rankings through genuine topical authority

Think like a combined expert team of:
- Senior Local SEO Expert
- Semantic SEO Specialist
- Entity SEO Expert
- AI Search Strategist (AEO, GEO, LLMO, ASO)
- Information Architect
- Google Search Quality Engineer
- UX Designer & CRO Consultant
- Content Strategist
- Rank & Rent Operator

Apply this filter to every page decision:
> **"Does this page fill a genuine topical gap, serve a real customer need, and strengthen our authority with Google and AI search?"**

---

## ⚠️ HARD RULES — Read Before Any Processing Step

These rules are derived from live project failures. Violating them produces a structurally weak blueprint that requires a full Prompt 6 re-run to fix.

---

### RULE A — Niche Service Pages Must Be Derived From `data.txt` Keyword Volume (FIX 20)

**The problem:** Defaulting to generic audience-label service pages (Residential / Commercial) ignores high-intent niche keywords already in `data.txt` and produces a commercially weak blueprint.

**The rule:**

> **Before finalising the service pages list, run this derivation process against `data.txt`:**

1. Pull every keyword cluster from `data.txt` under:
   - `[TOPICAL CLUSTERS & CONTENT PILLARS]`
   - `[PEOPLE ALSO ASK]`
   - Customer research sections (what customers throw away, project types, specific service requests)

2. Score each cluster against **three criteria**:

   | Criteria | Threshold |
   |---|---|
   | Estimated search volume | 100+ Vol minimum for a standalone page |
   | Commercial / transactional intent | Someone ready to book — not just learn |
   | Niche specificity | A distinct service type — not just an audience label |

3. Any cluster passing all 3 criteria → gets its **own dedicated Phase 1 service page** in the blueprint. Do not bury it as a section on an existing page.

4. Each niche service page must have a **unique primary keyword** — run a cannibalization check.

**The key rule:**

> **Service pages are NOT audience labels (Residential / Commercial).**
> **They are niche-specific intent pages derived directly from real keyword volume in `data.txt`.**
>
> Audience labels are valid as secondary hub pages that link OUT to niche pages. **Niche service pages must outnumber generic audience hub pages in every project.**

---

### RULE B — Location Pages Must Come Exclusively From `data.txt` Volume Data (FIX 22)

**The problem:** Adding cities based on geographic proximity alone (e.g., "Hiawatha is close to Cedar Rapids") produces location pages with zero search volume — wasted Phase capacity and diluted topical authority.

**The rules:**

| Rule | Requirement |
|---|---|
| Source | City must be listed in `data.txt` under `[Expansion Cities Identified]` |
| Min volume | Primary niche keyword for that city must be ≥ 20 Vol |
| Distance | Must be within 15 miles of primary business address |
| No assumptions | **Never add a location page based on geographic knowledge alone** |

**Do not add any location page that is not explicitly listed in the `[Expansion Cities Identified]` section of `data.txt` with confirmed search volume.** If a city is geographically close but has 0 volume in `data.txt` — remove it from the blueprint entirely.

---

### RULE C — ALL Location Pages Go in the FINAL Phase Only (FIX 23)

**The problem:** Publishing location pages too early dilutes topical authority for the primary keyword before it has established any ranking momentum. Google must associate the site with the primary city first.

**The rule:**

> **ALL pages of these types must be placed in the FINAL phase — no exceptions:**
> - `location_hub`
> - `location_page`
> - `zip_code_page`
> - `neighborhood_page`

The correct phase sequence:

| Phase | Content |
|---|---|
| **Phase 1 (MANDATORY ALL SERVICES — FIX 37)** | Homepage, **ALL inner service pages**, About, Contact, trust pages, 1 Golden location page, 1 Golden blog |
| Phase 2 | Expansion Satellite location pages (surrounding cities in service radius) |
| Phase 3 | Topical Authority blog cluster (informational guides, FAQs, comparisons) |
| Phase 4 | Deep topical guides, calculators, seasonal guides |

### RULE C2 — ALL Inner Service Pages Must Be in Phase 1 (FIX 37)
- **ALL Inner Service Pages MUST be assigned `phase: 1`.**
- NEVER defer core or specialized inner service pages to Phase 2 or later.
- Every inner service page derived from `master_brief.json` services and sub-services must be scheduled for Phase 1 release.
- This guarantees the site has 100% complete topical service coverage and populates the `Services ▼` navigation dropdown completely upon launch.

Within Phase 5, order location pages by **descending primary keyword volume — highest volume city first**.

Not Phase 1. Not Phase 2. Not "early location page for a big suburb." The last phase only.

---

### RULE D — Blog Post Keywords Must Be Semantically Unique (FIX 31)

Blog posts cannibalize each other when two posts answer the same searcher question
from the same angle. This is as damaging as blog-vs-service cannibalization.

**Before finalising the `topical_authority.json` blog post list:**

1. List every planned blog post keyword in a single column
2. For each pair, ask: *"Does this pair answer the same searcher question?"*
3. If YES — they are cannibalizing. Reframe one using a different intent:

   | Intent Angle   | Example keyword |
   |---|---|
   | Diagnosis      | "signs your sprinkler head needs repair" |
   | DIY fix        | "how to replace a sprinkler head yourself" |
   | Cost research  | "sprinkler head repair cost guide" |
   | Prevention     | "how to protect sprinkler heads from damage" |
   | Comparison     | "pop-up vs rotary sprinkler heads" |

4. Blog posts must ONLY target **informational intent** keywords:
   `how to`, `what is`, `signs of`, `guide to`, `when to`, `why does`, `vs`
   NEVER target transactional keywords — those belong to service pages.

5. After generating `topical_authority.json`, include a **Blog Keyword Uniqueness Table**
   in the output listing every blog post keyword and its intent angle.
   Flag any pair with >50% keyword token overlap as a cannibalization risk.

6. Run `check_blog_cannibalization.py` after saving `topical_authority.json`
   to get a programmatic PASS/FAIL before proceeding to Prompt 6.

---

## OUTPUT INSTRUCTIONS

- Produce a complete `topical_authority.json` file
- Every page gets its own object in the `pages[]` array
- Use the **priority scoring system** below for every page
- Flag cannibalization risks before finalizing
- After the JSON, produce the **Topical Authority Validation Checklist**
- End with the **PromptSix Forward Block** — a ready-to-paste input for the Page Structure Generator

---

## PRIORITY SCORING SYSTEM

Score every page on these 5 factors (1–10 each). Max score = 50.

| Factor | What It Measures |
|---|---|
| **Search Volume** | How many people search for this page's keyword |
| **Commercial Value** | How directly does this page drive leads or calls |
| **Topical Necessity** | How critical is this page to topical authority |
| **AI Citation Potential** | How likely is this page to be cited by AI search |
| **Competitive Gap** | How weak is competitor coverage of this topic |

**Priority Tiers based on total score:**
- 🔴 **Critical (40–50):** Publish first — foundational authority pages
- 🟠 **High (30–39):** Publish in Phase 2 — important supporting pages
- 🟡 **Medium (20–29):** Publish in Phase 3 — depth and expansion pages
- 🟢 **Future (below 20):** Publish after initial launch — long-tail and seasonal

---

## PROCESSING STEPS

Before generating output, complete these internal steps:

**Step 1 — Audit the Pages Array**
Review every page from `master_brief.json`. Verify no duplicates, no keyword cannibalization, no intent overlap. Flag any conflicts.

**Step 2 — Score Every Page**
Apply the 5-factor priority scoring system to every page.

**Step 3 — Assign Publishing Phase**
Based on scores and topical dependencies, assign each page to Phase 1, 2, 3, or Future.

**Step 4 — Map Dependencies**
Identify which pages must exist before others can link to them. Build the dependency chain.

**Step 5 — Assign Entities Per Page**
From the entity map, assign which entities must appear on each page.

**Step 6 — Assign Schema Per Page**
From schema_defaults in master_brief.json, assign required schema types to each page.

**Step 7 — Design Internal Link Flow**
Map parent → child relationships and cross-silo links for every page.

**Step 8 — Verify Topical Completeness**
Check all 9 validation criteria (listed in Step 9 below) before finalizing.

**Step 9 — Identify Cannibalization Risks**
Flag any two pages targeting overlapping intent + keyword combinations. Recommend resolution.

---

## TOPICAL_AUTHORITY.JSON STRUCTURE

```json
{
  "topical_authority": {

    "meta": {
      "generated_by": "PromptFive - Rank & Rent Pipeline",
      "reads_from": "master_brief.json",
      "feeds_into": "PromptSix - Page Structure Generator",
      "niche": "",
      "city": "",
      "state": "",
      "primary_keyword": "",
      "total_pages": 0,
      "phase_1_count": 0,
      "phase_2_count": 0,
      "phase_3_count": 0,
      "future_count": 0,
      "topical_authority_score": "",
      "cannibalization_risks_found": 0,
      "cannibalization_risks_resolved": 0
    },

    "blog_categories": [
      {
        "name": "Category Name",
        "slug": "category-slug",
        "description": "One sentence describing what posts in this category cover.",
        "supporting_service": "page_id of the service page this silo supports"
      }
    ],

    "topic_clusters": [
      {
        "cluster_id": "",
        "cluster_name": "",
        "pillar_page_url": "",
        "pillar_page_title": "",
        "supporting_pages": [],
        "total_pages_in_cluster": 0,
        "primary_entity": "",
        "cluster_intent": "",
        "internal_link_hub": "",
        "ai_citation_angle": ""
      }
    ],

    "publishing_phases": {
      "phase_1": {
        "name": "Foundation & Authority Core",
        "goal": "Establish crawlable site with core money pages, E-E-A-T signals, and primary topical authority",
        "publishing_priority": "Publish these pages before any traffic strategy or link building",
        "pages": []
      },
      "phase_2": {
        "name": "Authority Expansion",
        "goal": "Secondary services, supporting locations, commercial content, FAQ hub",
        "pages": []
      },
      "phase_3": {
        "name": "Topical Depth & Long-Tail Dominance",
        "goal": "Informational content, comparisons, guides, neighborhood pages, cost pages",
        "pages": []
      },
      "future_expansion": {
        "name": "Future Expansion",
        "goal": "Seasonal content, new service areas, PR content, AI citation optimization",
        "pages": []
      }
    },

    "pages": [
      {
        "page_id": "",
        "publish_order": 1,
        "phase": 1,
        "page_type": "",
        "page_title": "",
        "url": "",
        "meta_description": "",
        "h1": "",
        "target_keyword": "",
        "secondary_keywords": [],
        "intent": "",
        "priority_scores": {
          "search_volume": 0,
          "commercial_value": 0,
          "topical_necessity": 0,
          "ai_citation_potential": 0,
          "competitive_gap": 0,
          "total": 0,
          "tier": ""
        },
        "word_count_target": 0,
        "content_sections": [],
        "entities": {
          "primary": "",
          "secondary": [],
          "local": [],
          "semantic": [],
          "nlp": []
        },
        "schema_types": [],
        "internal_linking": {
          "parent_page": "",
          "child_pages": [],
          "hub_page": "",
          "cross_links_to": [],
          "recommended_anchor_texts": []
        },
        "eeat_requirements": {
          "experience": [],
          "expertise": [],
          "authority": [],
          "trust": []
        },
        "ai_search": {
          "citation_formats": [],
          "faq_block_required": true,
          "definition_box_required": false,
          "table_required": false,
          "speakable_required": false,
          "platforms_targeted": []
        },
        "conversion": {
          "cta_type": "",
          "cta_placement": [],
          "lead_capture": ""
        },
        "cannibalization_check": {
          "risk": false,
          "conflicts_with": "",
          "resolution": ""
        },
        "publish_reason": "",
        "category": "(blog pages only - category name from blog_categories)",
        "category_slug": "(blog pages only - URL-safe slug from blog_categories)",
        "information_gain_angle": "",
        "local_elements": [],
        "dependency": {
          "must_publish_after": [],
          "enables_publishing_of": []
        }
      }
    ],

    "internal_linking_map": {
      "homepage_links_to": [],
      "service_hub_links_to": [],
      "location_hub_links_to": [],
      "blog_hub_links_to": [],
      "blog_category_hubs": [],
      "authority_flow_diagram": "Homepage → Service Hub → Service Pages → Location Pages → Neighborhood Pages",
      "cross_silo_links": [],
      "anchor_text_rules": {
        "homepage_to_service": "exact match primary keyword",
        "service_to_location": "local keyword variant",
        "blog_to_service": "partial match or natural language",
        "blog_to_category_hub": "category name as anchor text",
        "location_to_location": "geographic anchor"
      }
    },

    "entity_coverage_map": {
      "total_entities_mapped": 0,
      "entities_covered_across_site": [],
      "entities_per_cluster": [],
      "missing_entity_opportunities": [],
      "local_entity_coverage": []
    },

    "eeat_coverage_map": {
      "experience_pages": [],
      "expertise_pages": [],
      "authority_pages": [],
      "trust_pages": [],
      "photo_required_on": [],
      "video_required_on": [],
      "certification_required_on": [],
      "review_integration_on": [],
      "case_study_pages": []
    },

    "ai_search_coverage_map": {
      "google_ai_overviews_optimized": [],
      "google_ai_mode_optimized": [],
      "chatgpt_optimized": [],
      "gemini_optimized": [],
      "claude_optimized": [],
      "perplexity_optimized": [],
      "copilot_optimized": [],
      "faq_schema_pages": [],
      "howto_schema_pages": [],
      "speakable_schema_pages": [],
      "definition_rich_pages": [],
      "data_table_pages": []
    },

    "content_balance": {
      "homepage": 1,
      "primary_service_pages": 0,
      "secondary_service_pages": 0,
      "emergency_pages": 0,
      "cost_pages": 0,
      "comparison_pages": 0,
      "faq_pages": 0,
      "city_location_pages": 0,
      "neighborhood_pages": 0,
      "zip_code_pages": 0,
      "nearby_city_pages": 0,
      "resource_guides": 0,
      "maintenance_guides": 0,
      "blog_posts": 0,
      "case_studies": 0,
      "glossary_pages": 0,
      "trust_pages": 0
    },

    "topical_authority_validation": {
      "all_customer_questions_answered": false,
      "all_major_services_covered": false,
      "all_local_areas_represented": false,
      "all_journey_stages_covered": false,
      "all_major_entities_covered": false,
      "all_semantic_relationships_covered": false,
      "no_obvious_content_gaps": false,
      "no_cannibalization_risks": false,
      "eeat_fully_addressed": false,
      "ai_search_fully_addressed": false,
      "validation_notes": []
    },

    "future_expansion_opportunities": [
      {
        "topic": "",
        "reason": "",
        "estimated_value": "",
        "suggested_publish_timing": ""
      }
    ]

  }
}
```

---

## STEP-BY-STEP ANALYSIS INSTRUCTIONS

### STEP 1 — PAGE PRIORITY SCORING

For every page from `master_brief.json`, apply the 5-factor scoring system. Produce:

| Page Title | URL | Vol | Commercial | Topical | AI | Gap | Total | Tier | Phase |
|---|---|---|---|---|---|---|---|---|---|

---

### STEP 2 — TOPIC CLUSTER MAP

Organize all pages into clusters. Every cluster must have:
- One pillar page (hub)
- Minimum 3 supporting pages (spokes)
- Clear internal link flow from pillar → supporting → pillar

Produce a cluster diagram:

```
[Pillar Page: Primary Service]
├── [Supporting: Service Variant 1]
├── [Supporting: Service Variant 2]
├── [Supporting: Cost Guide]
├── [Supporting: Emergency Page]
├── [FAQ: Service FAQs]
└── [Location: Primary City]
    ├── [Neighborhood 1]
    └── [Neighborhood 2]
```

---

### STEP 3 — PUBLISHING ORDER

Number every page sequentially (1, 2, 3...) in exact publishing order.

**Publishing logic rules:**
1. Homepage always publishes first
2. Primary money pages (top service + primary city) publish within first 5
3. About + Contact publish within first 7 (E-E-A-T requirement)
4. No location page publishes before its parent service page
5. No blog post publishes before its pillar page
6. No comparison page publishes before both compared pages exist
7. Internal links must only point to already-published pages

---

### STEP 4 — INTERNAL LINKING MAP

For every page produce:

| Page | Parent | Children | Hub | Cross-Links | Anchor Texts |
|---|---|---|---|---|---|

**Authority flow rule:**
- Homepage = maximum authority
- Authority flows DOWN the hierarchy
- Cross-silo links (service → location) must use relevant anchor text
- Every page must receive at least 2 internal links before publishing

---

### STEP 5 — ENTITY COVERAGE MAP

For every page, assign entities from the `entity_map` in master_brief.json:

| Page | Primary Entity | Secondary Entities | Local Entities | Semantic | NLP |
|---|---|---|---|---|---|

Flag any page with fewer than 3 assigned entities — it needs content expansion.

---

### STEP 6 — EEAT ASSIGNMENT

For every page, specify which E-E-A-T elements must be present:

| Page | Experience | Expertise | Authority | Trust | Photos | Video | Certs | Reviews |
|---|---|---|---|---|---|---|---|---|

---

### STEP 7 — AI SEARCH COVERAGE

For every page, specify:

| Page | Citation Format | FAQ Block | Definition Box | Table | Speakable | Platforms |
|---|---|---|---|---|---|---|

**Citation formats to assign:**
- `how-to-list` — numbered process steps
- `faq-qa` — question and answer blocks
- `definition` — clear term definitions
- `data-table` — comparison or cost tables
- `local-fact-block` — locally specific data
- `stat-block` — statistics with source

---

### STEP 8 — CANNIBALIZATION CHECK

Before finalizing, compare every pair of pages targeting similar keywords.

Flag any cannibalization risk:

| Page A | Page B | Conflict | Resolution |
|---|---|---|---|

**Resolutions:**
- Merge pages if intent is identical
- Differentiate if intent is slightly different (informational vs transactional)
- Add canonical tag if content overlap is unavoidable

---

### STEP 9 — TOPICAL AUTHORITY VALIDATION CHECKLIST

Before producing final output, verify all 10 criteria:

- [ ] Every important customer question from PAA, Reddit, Quora has a dedicated page or section
- [ ] Every major service variant has its own page
- [ ] Every significant local area (neighborhoods, zip codes, nearby cities) is represented
- [ ] Every stage of the customer journey (Awareness → Referral) has supporting content
- [ ] Every major entity from the entity map appears on at least one page
- [ ] All semantic keyword relationships are covered across the site
- [ ] No two pages have identical or nearly identical search intent
- [ ] Every page has a minimum of 2 inbound internal links assigned
- [ ] E-E-A-T signals are distributed across all critical pages
- [ ] AI search citation formats are assigned to every page

---

## FINAL OUTPUT AFTER JSON

### Topical Authority Validation Report
Complete the 10-point checklist with notes on any gaps found and how they were resolved.

### Content Balance Report
Confirm the site has the correct mix of page types (no over-indexing on one type).

### Cannibalization Report
List all risks found and how each was resolved.

### Top 10 Publishing Priorities
The 10 most important pages to publish first and why.

---

## PROMPTSIX FORWARD BLOCK

At the very end, produce this block ready to paste into PromptSix:

```
=== PROMPTFIVE FORWARD BLOCK — PASTE INTO PROMPTSIX ===
{
  "promptfive_forward": {
    "total_pages": 0,
    "publishing_phases": {
      "phase_1_pages": [],
      "phase_2_pages": [],
      "phase_3_pages": [],
      "future_pages": []
    },
    "next_page_to_brief": {
      "page_id": "",
      "page_title": "",
      "url": "",
      "target_keyword": "",
      "intent": "",
      "word_count_target": 0,
      "sections": [],
      "entities": {},
      "schema_types": [],
      "internal_links": {},
      "eeat_requirements": {},
      "ai_search": {},
      "tone_notes": ""
    },
    "internal_linking_rules": {},
    "entity_map_reference": "See master_brief.json entity_map",
    "tone_reference": "See master_brief.json tone block"
  }
}
=== END PROMPTFIVE FORWARD BLOCK ===
```

**Instruction to user:**
> Copy the `next_page_to_brief` object and paste it into PromptSix to generate the full page structure brief. Repeat for every page in publishing order.

---

*Universal Template — Paste master_brief.json inputs at the top. All steps and JSON structure apply to any local service niche.*
