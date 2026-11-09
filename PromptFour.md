# 📊 Rank & Rent — Research Processor & Master Blueprint Generator (2026 Edition)
## Universal Template — Transforms All Research Into master_brief.json

---

## HOW TO USE THIS PROMPT

> **Pipeline Position:** This is Step 4 of 7. This is the most important step in the entire pipeline.
> Run AFTER both Prompt 2 and Prompt 3 are complete and saved.
> **This prompt merges THREE sources into one master document.**

### What you are doing in this step
You have now collected intelligence from three separate sources:
1. **Prompt 2 output** — The AI's analysis of the market, customer psychology, local geography, weather, and demographics.
2. **Prompt 3 output** — The AI's competitor intelligence report including entity extraction, scoring, and gap analysis.
3. **data.txt** — Your scraped research file containing 18 sections of real customer language, real prices from Reddit/Quora, real AnswerThePublic keyword variations, PAA questions, topical relevance data, and the full YouTube competitor transcript.

PromptFour reads all three and synthesizes them into one `master_brief.json` — the single source of truth for every page the site will ever publish.

> ✅ **PIPELINE MODE — No variable entry needed.**
> All variables (niche, city, state, primary keyword, monetization, competition level)
> are already loaded from the Prompt 1 session context. Do NOT re-enter them.
>
> **The ONLY thing you must provide are the 3 data inputs below:**

```
=== INPUT 1: PROMPT 2 OUTPUT — MARKET INTELLIGENCE ===
[Paste your complete saved Prompt 2 output here]

=== INPUT 2: PROMPT 3 OUTPUT — COMPETITOR INTELLIGENCE + ENTITY MAP ===
[Paste your complete saved Prompt 3 output here, including the
 === ENTITY OUTPUT FOR PROMPTFOUR === and
 === PROMPTTHREE FORWARD BLOCK === JSON sections]

=== INPUT 3: YOUR FULL DATA.TXT FILE ===
[Paste the entire contents of your data.txt file here.
 It contains 18 sections covering:
  - Section 1:  Project Info
  - Section 2:  Target Keywords (Semrush)
  - Section 3:  People Also Ask (413 questions)
  - Section 4:  Content Ideas (Topic Research)
  - Section 5:  Customer Pain Points (scraped)
  - Section 6:  Forum Questions (Reddit/Quora)
  - Section 7:  Pricing Data (scraped)
  - Section 8:  Competitor Names
  - Section 9:  Services in this Niche
  - Section 10: Local Context
  - Section 11: Trust Signals (scraped)
  - Section 12: Objections (scraped)
  - Section 13: Google SERP Snippets
  - Section 14: YouTube Competitor Transcript (notes)
  - Section 15: Uncategorized Forum Data (scraped)
  - Section 16: AnswerThePublic Keyword Variations (2890 rows)
  - Section 17: Topical Relevance + Schema JSON-LD
  - Section 18: Full YouTube Competitor Transcript
]
```



---

## SYSTEM CONTEXT

You are the central processing engine of a Rank & Rent content pipeline for 2026.

You have received:
- Market intelligence from PromptTwo
- Competitor analysis + entity map from PromptThree
- Raw research from data.txt compiled from 20+ sources

Your job is to **synthesize everything** into one structured `master_brief.json` — the single source of truth that will drive PromptFive (Topical Authority Map), PromptSix (Page Structure Generator), and all future content creation.

This is a **Rank & Rent website** which means every decision must serve:

> **PRICING RULE — HARD CONSTRAINT**
> This is a Rank & Rent site. Calls are forwarded to a service provider
> who sets their own prices. Do NOT include any pricing, cost estimates,
> service charges, or price ranges anywhere in master_brief.json or any
> downstream content — unless the user explicitly overrides this rule.
>
> NEVER generate content using: "starting from $X", "costs $X",
> "pricing starts at", "affordable", "cheap", "lowest price", "best price".
>
> If data.txt contains pricing data (Section 7), use it ONLY to understand
> the market — never to publish prices on the site.
1. Traditional Google organic rankings
2. AI search citations (AI Overviews, AI Mode, ChatGPT, Gemini, Claude, Perplexity, Copilot)
3. Inbound lead generation (calls, forms, chats)
4. Monthly rentable value to a local service business

Apply this filter to every decision:
> **"Does this page, entity, keyword, or content decision help us rank, earn AI citations, and convert visitors into leads?"**

Think like a combined team of:
- Senior Local SEO Expert
- Semantic & Entity SEO Specialist
- AI Search Strategist
- Information Architect
- Google Search Quality Engineer
- UX Designer & CRO Consultant
- Content Strategist
- Rank & Rent Operator

---

## OUTPUT INSTRUCTIONS

- Produce one complete `master_brief.json` file
- **EVERY planned page MUST have its own full object inside the `pages[]` array. Do NOT list pages only in the `publishing_roadmap`. If a page is planned, it MUST be in `pages[]`.**
- Include the complete entity map consolidated from ALL sources (PromptThree + data.txt)
- Include the complete tone block — this will be used by every content writing prompt
- Flag Information Gain opportunities — insights no competitor covers
- After the JSON, produce a **plain-language summary** of the top 10 strategic decisions made

---

## 🚨 MANDATORY PAGES CHECKLIST — HARD CONSTRAINT

Before you finish, you MUST verify that ALL of the following page types have a full object in `pages[]`.
If ANY page type below is missing a full object, you are NOT done — keep writing until every one is covered.

### Core Pages (Phase 1) — ALL REQUIRED
- [ ] Homepage
- [ ] About Page
- [ ] Contact Page
- [ ] Privacy Policy Page

### Service Pages (Phase 1–2) — ONE PAGE PER SERVICE
- [ ] Primary Sprinkler Repair page
- [ ] Sprinkler Head Repair & Replacement page
- [ ] Sprinkler Valve Repair page
- [ ] Underground Leak Detection & Pipe Repair page
- [ ] Emergency Sprinkler Repair page (24/7 focus)
- [ ] Smart Controller Installation page
- [ ] Winterization / System Shutdown page
- [ ] Backflow Testing & Prevention page

### Location Pages (Phase 2–3) — ONE PAGE PER LOCATION
- [ ] Primary City page (this city)
- [ ] Surrounding city pages (one per city found in research, minimum 4)
- [ ] Neighborhood pages (one per major neighborhood found in research, minimum 2)

### Supporting Content (Phase 2–4)
- [ ] FAQ Hub page
- [ ] Pricing / Cost Guide page (structure: explain how pricing works, NOT specific dollar amounts)
- [ ] At least one problem identification page (e.g., "Why Is My Water Bill So High?")
- [ ] At least one informational guide tied to local geography/climate

### Blog / Informational Content (Phase 2–5)
- [ ] At least 2 blog post page objects

### Trust Pages (Phase 1)
- [ ] Reviews / Testimonials page

**TOTAL MINIMUM: 20 page objects in `pages[]`**

---

## 🚨 MANDATORY SECTIONS RULES — HARD CONSTRAINT

Each page object's `sections[]` array MUST contain a MINIMUM of 5 section entries.
Each section entry must include ALL fields: `section_name`, `h2`, `purpose`, `content_notes`, `cta`.
Do NOT leave sections[] with only 1 entry. If you only write 1 section for a page, you have not finished that page.

---

## 🚨 MANDATORY KEYWORD MAP RULES — HARD CONSTRAINT

The `keyword_map` must include:
- `question_keywords`: minimum 15 unique entries drawn from PAA questions in data.txt
- `voice_and_conversational`: minimum 10 entries
- `emergency_intent`: minimum 5 entries
- `informational_intent`: minimum 8 entries
- `ai_search_queries`: minimum 5 entries

---

## 🚨 MANDATORY INFORMATION GAIN RULES — HARD CONSTRAINT

The `information_gain_opportunities` array must contain a minimum of **8 entries**.
Each entry must be a topic that NO competitor currently covers based on the PromptThree research.

---

## 🛑 SELF-VERIFICATION BLOCK — REQUIRED BEFORE FINISHING

After completing the JSON and plain-language summary, you MUST print the following self-verification checklist with your actual counts filled in. If any item shows FAIL, go back and fix it before finishing.

```
=== PROMPT FOUR SELF-VERIFICATION ===
[ ] Total pages in pages[] array:         [YOUR COUNT] / minimum 20 → PASS / FAIL
[ ] Pages with 5+ sections:               [YOUR COUNT] / [TOTAL PAGES] → PASS / FAIL
[ ] question_keywords count:              [YOUR COUNT] / minimum 15 → PASS / FAIL
[ ] voice_and_conversational count:       [YOUR COUNT] / minimum 10 → PASS / FAIL
[ ] emergency_intent count:               [YOUR COUNT] / minimum 5  → PASS / FAIL
[ ] information_gain_opportunities count: [YOUR COUNT] / minimum 8  → PASS / FAIL
[ ] About page in pages[]:                YES / NO → PASS / FAIL
[ ] Contact page in pages[]:              YES / NO → PASS / FAIL
[ ] Emergency service page in pages[]:    YES / NO → PASS / FAIL
[ ] At least 4 city pages in pages[]:     YES / NO → PASS / FAIL
[ ] Pricing guide page in pages[]:        YES / NO → PASS / FAIL
[ ] Blog post pages in pages[]:           YES / NO → PASS / FAIL
=== END VERIFICATION ===
```

---

## PROCESSING INSTRUCTIONS

Before generating the JSON, perform these internal analysis steps:

**Step 1 — Consolidate Entities**
Merge the entity output from PromptThree with any additional entities found in data.txt. Deduplicate. Rank by importance.

**Step 2 — Consolidate Keywords**
Merge Semrush keywords, PAA questions, related searches, Reddit/Quora questions, and competitor keywords. Organize by intent and priority. You MUST include at least 15 question_keywords pulled directly from the PAA section of data.txt.

**Step 3 — Identify All Pages Needed**
Based on all research, determine every page the site needs. Group by type: service pages, location pages, supporting content, blog, etc. Reference the MANDATORY PAGES CHECKLIST above and build each page into `pages[]`.

**Step 4 — Map Customer Pain Points to Content**
Every significant pain point, question, or frustration found in reviews, Reddit, and Quora must map to a specific page or section.

**Step 5 — Define Tone**
Based on the niche, customer psychology findings, and competitor analysis, define the exact tone, voice, and writing style for the entire site.

**Step 6 — Assign Schema**
Every page gets its required schema types assigned before content is written.

**Step 7 — Set Internal Linking Rules**
Define which pages link to which before content is written, so writers can include correct internal links.

**Step 8 — Build ALL Page Objects**
For EVERY page on the checklist, create a complete page object in `pages[]` with all required fields. Do NOT summarize pages in the roadmap instead of building them. Every page that will be published must have its own full object.

**Step 9 — Expand All sections[] Arrays**
For each page object, write a minimum of 5 entries in `sections[]`. Each entry must have: section_name, h2, purpose, content_notes, cta. This is the blueprint that PromptSix will use to write the actual content — if a section is missing here, it will never get written.

**Step 10 — Run Self-Verification**
Complete the SELF-VERIFICATION BLOCK above before outputting anything else.

---

## MASTER_BRIEF.JSON STRUCTURE

Generate the complete JSON in the following structure:

```json
{
  "master_brief": {

    "meta": {
      "generated_by": "PromptFour - Rank & Rent Pipeline",
      "version": "2026.1",
      "niche": "",
      "city": "",
      "state": "",
      "primary_keyword": "",
      "monetization_model": "",
      "competition_level": "",
      "market_opportunity_score": "",
      "pipeline_stage": "PromptFour → PromptFive (Topical Authority)"
    },

    "tone": {
      "voice": "",
      "personality": "",
      "reading_level": "",
      "person": "",
      "style": "",
      "emotional_tone": "",
      "local_authenticity": true,
      "avoid": [],
      "use_frequently": [],
      "cta_tone": "",
      "emergency_tone": "",
      "informational_tone": "",
      "trust_building_phrases": [],
      "forbidden_phrases": [],
      "example_headline_style": "",
      "example_body_style": ""
    },

    "market_intelligence": {
      "market_size": "",
      "demand_level": "",
      "seasonal_peaks": [],
      "customer_demographics": "",
      "residential_vs_commercial": "",
      "avg_job_value": "",
      "key_buying_triggers": [],
      "key_customer_fears": [],
      "key_trust_factors": [],
      "customer_pain_points": [],
      "customer_questions_top10": []
    },

    "competitor_intelligence": {
      "top_competitor": "",
      "weakest_competitor": "",
      "most_beatable_angle": "",
      "winning_position_statement": "",
      "critical_content_gaps": [],
      "critical_seo_gaps": [],
      "critical_eeat_gaps": [],
      "critical_ai_search_gaps": [],
      "critical_schema_gaps": [],
      "critical_local_seo_gaps": [],
      "critical_ux_gaps": []
    },

    "entity_map": {
      "primary": [],
      "secondary": [],
      "problems": [],
      "solutions": [],
      "processes": [],
      "materials_tools": [],
      "brands": [],
      "industry_terminology": [],
      "local": [],
      "persons_roles": [],
      "organizations": [],
      "semantic_keywords": [],
      "nlp_keywords": [],
      "missing_entities": [],
      "schema_entities_to_implement": [],
      "information_gain_entities": []
    },

    "keyword_map": {
      "primary": [],
      "secondary": [],
      "long_tail": [],
      "question_keywords": [],
      "emergency_intent": [],
      "commercial_intent": [],
      "transactional_intent": [],
      "informational_intent": [],
      "comparison_intent": [],
      "voice_and_conversational": [],
      "ai_search_queries": [],
      "local_intent": [],
      "untapped_opportunities": []
    },

    "eeat_requirements": {
      "experience_signals": [],
      "expertise_signals": [],
      "authority_signals": [],
      "trust_signals": [],
      "required_certifications": [],
      "required_associations": [],
      "required_guarantees": [],
      "required_policies": [],
      "photo_requirements": [],
      "review_strategy": ""
    },

    "schema_defaults": {
      "site_wide": [],
      "homepage": [],
      "service_pages": [],
      "location_pages": [],
      "blog_posts": [],
      "faq_pages": [],
      "about_page": [],
      "contact_page": []
    },

    "internal_linking_rules": {
      "homepage_links_to": [],
      "service_hub_links_to": [],
      "location_hub_links_to": [],
      "blog_links_to": [],
      "anchor_text_rules": {
        "exact_match": "",
        "partial_match": "",
        "natural_language": "",
        "avoid": ""
      },
      "max_click_depth": 3,
      "orphan_prevention_rule": "Every page must have minimum 2 internal links pointing to it"
    },

    "ai_search_strategy": {
      "content_formats_for_citations": [],
      "schema_for_ai": [],
      "faq_structure_rule": "",
      "definition_box_rule": "",
      "speakable_content_rule": "",
      "entity_coverage_checklist": [],
      "platforms": {
        "google_ai_overviews": "",
        "google_ai_mode": "",
        "chatgpt": "",
        "gemini": "",
        "claude": "",
        "perplexity": "",
        "copilot": ""
      }
    },

    "conversion_strategy": {
      "primary_cta": "",
      "secondary_cta": "",
      "emergency_cta": "",
      "phone_placement": "",
      "form_fields": [],
      "trust_elements_near_cta": [],
      "psychological_triggers": [],
      "mobile_ux_rules": [],
      "sticky_cta_rule": ""
    },

    "pages": [
      {
        "page_id": "homepage",
        "url": "/",
        "page_title": "",
        "meta_description": "",
        "h1": "",
        "target_keyword": "",
        "secondary_keywords": [],
        "intent": "commercial",
        "priority": "critical",
        "word_count_target": 1500,
        "publish_phase": 1,
        "publish_order": 1,
        "sections": [
          {
            "section_name": "Hero",
            "h2": "",
            "purpose": "Primary conversion entry point",
            "content_notes": "",
            "cta": ""
          }
        ],
        "entities_to_include": [],
        "schema_types": [],
        "internal_links_to": [],
        "internal_links_from": [],
        "eeat_elements": [],
        "ai_citation_elements": [],
        "tone_notes": "",
        "information_gain_angle": "",
        "local_elements": []
      }
    ],

    "publishing_roadmap": {
      "phase_1_foundation": {
        "timeframe": "Week 1-2",
        "goal": "Crawlable, indexable site with core money pages",
        "pages": []
      },
      "phase_2_authority": {
        "timeframe": "Weeks 3-6",
        "goal": "Secondary services, supporting locations, first blog content",
        "pages": []
      },
      "phase_3_expansion": {
        "timeframe": "Months 2-3",
        "goal": "Neighborhood pages, problem pages, cost pages",
        "pages": []
      },
      "phase_4_dominance": {
        "timeframe": "Months 3-6",
        "goal": "Comparison pages, nearby cities, case studies, glossary",
        "pages": []
      },
      "phase_5_future": {
        "timeframe": "Ongoing",
        "goal": "Seasonal content, PR, new areas, AI optimization updates",
        "pages": []
      }
    },

    "information_gain_opportunities": [
      {
        "topic": "",
        "source": "",
        "why_unique": "",
        "content_type": "",
        "target_page": "",
        "priority": ""
      }
    ],

    "topical_authority_summary": {
      "total_pages_planned": 0,
      "total_service_pages": 0,
      "total_location_pages": 0,
      "total_blog_posts": 0,
      "total_supporting_pages": 0,
      "pillar_pages": [],
      "topic_clusters": []
    }

  }
}
```

---

## PAGES ARRAY — PAGE TYPES TO INCLUDE

Populate the `pages[]` array with one object per page. Include all of the following page types based on the research:

**Core Pages (Phase 1)**
- Homepage
- Primary service page(s)
- About page
- Contact page
- Primary city/location page

**Service Pages (Phase 1-2)**
- One page per primary and secondary service
- Emergency service page
- Cost/pricing page per service

**Location Pages (Phase 2-3)**
- Primary city page
- Neighborhood pages (one per significant neighborhood)
- Zip code pages (if research supports)
- Nearby city pages

**Supporting Content (Phase 2-4)**
- FAQ hub page
- Problem identification pages
- Comparison pages (X vs Y)
- Maintenance/prevention guides
- How-to guides
- Glossary page

**Blog Content (Phase 2-5)**
- Informational blog posts by category
- Seasonal content
- Local news/PR content

**Trust Pages (Phase 1)**
- Privacy Policy
- Terms of Service
- Reviews/Testimonials page

---

## TONE BLOCK INSTRUCTIONS

The `tone` object is critical. Every future content writing prompt (PromptSix, PromptSeven) will inherit this tone block.

Define tone based on:
- Niche psychology (e.g., emergency services = urgent + reassuring; HVAC = reliable + technical)
- Customer demographics from market research
- Local culture of the target city
- Competitor tone gaps (if all competitors are dry and corporate, be warm and human)
- E-E-A-T requirements (expertise must come through in writing style)

**Tone must specify:**
- Voice (e.g., "knowledgeable neighbor, not a salesperson")
- Personality (e.g., "calm, reassuring, confident, local")
- Reading level (target 7th-8th grade for most local service niches)
- Person (second person "you/your" for direct customer connection)
- Emotional tone (e.g., "reassuring during emergencies, educational in guides")
- Forbidden phrases (e.g., "cheap", "best in the world", "click here")
- Trust-building phrases specific to this niche
- CTA tone (e.g., "action-oriented but pressure-free")

---

## FINAL OUTPUT AFTER JSON

After producing the complete `master_brief.json`, provide:

**Plain Language Summary:**
1. Total pages planned and why
2. Top 3 entity gaps we will own
3. Top 3 information gain opportunities
4. Tone summary in 2 sentences
5. Top 5 AI search citation strategies
6. Publishing order rationale
7. Biggest competitive advantage identified
8. Top schema priorities
9. Biggest local SEO opportunity
10. One-paragraph mission statement for this site

**Next Step Instruction:**
> "This master_brief.json is ready for PromptFive — Topical Authority Map Generator. Paste the `topical_authority_summary` and `pages[]` array into PromptFive to generate the complete content cluster map."

---

*Universal Template — Fill in niche, city, primary keyword, monetization model, and paste all required inputs. All processing instructions and JSON structure apply to any local service niche.*
