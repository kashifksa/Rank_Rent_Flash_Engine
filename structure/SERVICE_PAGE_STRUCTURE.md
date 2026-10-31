# SERVICE PAGE STRUCTURE
# Rank & Rent Pipeline — Page Type: Service Page
# Read by: PromptSeven.md (mandatory, before writing any service page)
# Research source: Confirmed 2026 local SEO + GEO (Generative Engine Optimization) best practices

---

## WHAT THIS FILE DEFINES
- Mandatory section order for all service pages
- H1 and H2 formulas (exact fill-in patterns)
- Word count targets per section and total
- GEO / AI Overview optimization rules (2026)
- Schema markup requirements
- Internal linking rules specific to service pages

> PromptSeven.md writing rules (tone, parity, no em-dash, etc.) ALWAYS apply.
> This file defines WHAT sections to write and in WHAT order — not HOW to write them.

---

## 2026 GEO WRITING RULES (apply to every section)

These rules apply to all service pages to optimize for Google AI Overviews, ChatGPT Search, and Perplexity (Retrieval-Augmented Generation / RAG engines):

1. **Self-contained blocks:** Each paragraph must stand alone and answer its implied sub-question without requiring surrounding context.
2. **Short paragraphs:** 2–3 sentences max. RAG engines parse text chunk by chunk.
3. **Bold key phrases:** Bold the most important phrase in each paragraph (e.g., `**licensed and insured in {STATE}**`). AI engines extract bolded terms first.
4. **Answer-first under every H2:** First sentence beneath every H2 directly answers the implied question. Elaboration follows.
5. **Entity consistency:** Business name, phone, address, and service area on this page must match Google Business Profile verbatim.

---

## PAGE VARIABLES (from master_brief.json)
- `{PRIMARY_SERVICE}` — e.g., "Roof Replacement"
- `{CITY}` — e.g., "Austin"
- `{STATE}` — e.g., "TX"
- `{COMPANY_NAME}` — from NAP block
- `{PHONE}` — from NAP block
- `{SUB_SERVICES}` — array of sub-services (from master_brief.json → services list)
- `{NEIGHBORHOODS}` — list of served neighborhoods/zip codes
- `{EXPANSION_CITIES}` — adjacent cities (for service area section)
- `{LOCAL_CHALLENGE}` — a regional/climate factor relevant to the service (e.g., "Austin's intense hail storms")

---

## MANDATORY SECTION ORDER — 10 SECTIONS

### SECTION 1 — gradient-hero
**Kadence block:** `kt-hero` with gradient background
**H1 formula:** `{PRIMARY_SERVICE} in {CITY}, {STATE}`
**Snippet Zone (NEW — 2026):** Immediately beneath the H1, write a 40–60 word direct answer block:
- What the service is, who it is for, and the geographic area covered
- Written as a standalone paragraph — no lead-in phrase like "We offer..."
- This block is the Featured Snippet / AI Overview capture target
**Subheadline:** ≤50 words — one sentence benefit statement referencing `{LOCAL_CHALLENGE}`
**Hero word budget:** ≤120 words total (H1 + snippet zone + subheadline + CTA text) — HARD LIMIT
**CTA:** Click-to-call button + secondary "Get a Free Quote" anchor to mid-cta section
**No pricing** on this section or anywhere on the page

---

### SECTION 2 — trust-bar
**Kadence block:** `kt-row` with icon columns
**Content:** 3–4 trust signals displayed horizontally:
- Star rating badge (e.g., "4.9★ Rated")
- Licensed & Insured badge
- Years in business (e.g., "Serving {CITY} Since [Year]")
- Guarantee (e.g., "100% Satisfaction Guarantee")
**Word count:** ≤40 words across all badges
**No H2** in this section — decorative trust bar only

---

### SECTION 3 — services-grid
**Kadence block:** `kt-columns` (3-column grid)
**H2 formula:** `Our {CITY} {PRIMARY_SERVICE} Solutions`
**Answer-first rule:** First sentence directly states what this grid covers.
**Structure:**
- One H3 per sub-service (from `{SUB_SERVICES}`)
- 40–60 words per sub-service card (SECTION PARITY ±2%)
- Brief description of what the sub-service covers + who it helps
- Bold the key term in each card description
- No pricing, no "starting at" language
**Minimum sub-services:** 3 | **Maximum:** 6

---

### SECTION 4 — why-choose-us
**Kadence block:** `kt-columns` with icon list
**H2 formula:** `Why {CITY} Homeowners Choose Us for {PRIMARY_SERVICE}`
**Answer-first rule:** First sentence states the core differentiator in 1–2 sentences.
**Structure:**
- 4–6 bullet points with icons
- Each bullet: **bold label** (3–5 words) + 1-sentence explanation (15–25 words)
- At least 2 bullets must reference LOCAL advantages: response time to `{CITY}`, local knowledge, `{LOCAL_CHALLENGE}` experience
- Mention `{CITY}` at least once in the body text
**Total word count:** 120–180 words

---

### SECTION 5 — process
**Kadence block:** `kt-columns` (3-column numbered steps) OR clean HTML table (preferred for AI extraction)
**H2 formula:** `How Our {PRIMARY_SERVICE} Process Works in {CITY}`
**Answer-first rule:** First sentence states how many steps and approximately how long.
**Structure:** Exactly 3 steps
- Step 1: Initial contact / assessment
- Step 2: On-site evaluation / proposal
- Step 3: Work completed / follow-up
- Each step: **bold title** (3–6 words) + 20–30 word description
**Table format option (2026 preferred):** Use a 3-column table: Step | What Happens | Timeframe — AI engines extract tables efficiently.
**Section parity:** All 3 step descriptions within ±2% word count
**Total word count:** 80–120 words

---

### SECTION 6 — local-proof (NEW — 2026)
**Kadence block:** `kt-testimonials` or `kt-columns`
**H2 formula:** `What {CITY} Customers Say About Our {PRIMARY_SERVICE}`
**Structure (required for GEO / AI Overview citation):**
- 2–3 review excerpts with geo-tagged context — must reference `{CITY}` or a specific neighborhood
- Each review: reviewer first name + neighborhood + 30–50 word quote
- 1 short paragraph (20–30 words): number of local projects completed + average rating stat
- CSS text stars — NEVER 3D rendered star images
**Note:** AI engines (ChatGPT Search, Gemini) factor in brand sentiment and review text. Location-rich review language ("Fixed our roof right here in Hyde Park") validates local authority.

---

### SECTION 7 — service-area
**Kadence block:** `kt-row` with text column + map column
**H2 formula:** `Proudly Serving {CITY} and Surrounding Areas`
**Answer-first rule:** First sentence states the service radius.
**Structure:**
- Opening: "Our {PRIMARY_SERVICE} team covers `{CITY}` and the following neighborhoods:"
- Bulleted list of neighborhoods and zip codes (from `{NEIGHBORHOODS}`)
- 1–2 sentences mentioning `{EXPANSION_CITIES}` — plain text only if not live in phase1_registry.json
- Map: Real Google Maps iframe — NEVER AI-generated map image (FIX 16)
**Total word count:** 80–150 words (excluding map)

---

### SECTION 8 — mid-cta
**Kadence block:** `kt-row` with contrasting background color
**H2 formula:** `Get Your Free {PRIMARY_SERVICE} Estimate in {CITY}`
**Structure:**
- 1–2 sentence urgency statement referencing `{LOCAL_CHALLENGE}` (20–30 words)
- Click-to-call button: `Call {PHONE}`
- Secondary: Short contact form (Name, Phone, Message — 3 fields only)
**No pricing** — never mention dollar amounts or ranges

---

### SECTION 9 — faq
**Kadence block:** `kt-accordion`
**H2 formula:** `Frequently Asked Questions About {PRIMARY_SERVICE} in {CITY}`
**Answer-first under each H3:** Each answer opens with a direct 1-sentence reply, then elaborates.
**Structure:**
- Minimum 5 questions | Target 8–12 questions
- Format H3 questions as natural language queries (voice search + AI Overview targeting)
- Each answer: 40–80 words
- Mix of question types:
  - **Process questions:** "How long does {PRIMARY_SERVICE} take in {CITY}?"
  - **Local questions:** "Do you serve [Neighborhood]?"
  - **Regulatory/permit questions:** "Do I need a permit for {PRIMARY_SERVICE} in {STATE}?" (2026: high AI Overview value)
  - **Trust questions:** "Are you licensed in {STATE}?"
  - **Problem questions:** "What happens if I delay {PRIMARY_SERVICE}?"
- NO pricing questions — redirect with "Contact us for a free estimate"
**Schema:** FAQPage schema REQUIRED — wrap each Q&A pair

---

### SECTION 10 — bottom-cta
**Kadence block:** `kt-row` with dark/brand background
**H2 formula:** `Ready for Professional {PRIMARY_SERVICE} in {CITY}?`
**Structure:**
- 1 sentence recap of core value (15–25 words)
- Click-to-call button (same `{PHONE}`)
- Trust micro-copy: "Licensed • Insured • {CITY}'s Trusted {PRIMARY_SERVICE} Team"
**Word count:** ≤60 words total

---

## WORD COUNT TARGETS

| Section | Min | Target | Max |
|---|---|---|---|
| hero (incl. snippet zone) | — | 100–120 | 120 (HARD) |
| trust-bar | — | 30–40 | 40 |
| services-grid | 180 | 250–350 | 420 |
| why-choose-us | 120 | 150–180 | 200 |
| process | 80 | 90–110 | 120 |
| local-proof | 100 | 130–170 | 200 |
| service-area | 80 | 100–130 | 150 |
| mid-cta | 20 | 30–50 | 60 |
| faq | 200 | 400–650 | 800 |
| bottom-cta | — | 40–60 | 60 |
| **TOTAL** | **1,100** | **1,600–2,200** | **2,500** |

---

## H2 FORMULA REFERENCE

| Section | H2 Template |
|---|---|
| services-grid | `Our {CITY} {PRIMARY_SERVICE} Solutions` |
| why-choose-us | `Why {CITY} Homeowners Choose Us for {PRIMARY_SERVICE}` |
| process | `How Our {PRIMARY_SERVICE} Process Works in {CITY}` |
| local-proof | `What {CITY} Customers Say About Our {PRIMARY_SERVICE}` |
| service-area | `Proudly Serving {CITY} and Surrounding Areas` |
| mid-cta | `Get Your Free {PRIMARY_SERVICE} Estimate in {CITY}` |
| faq | `Frequently Asked Questions About {PRIMARY_SERVICE} in {CITY}` |
| bottom-cta | `Ready for Professional {PRIMARY_SERVICE} in {CITY}?` |

---

## SCHEMA MARKUP REQUIREMENTS

Apply all four schema types to each service page:

1. **LocalBusiness** (or `HomeAndConstructionBusiness`) — wraps the full page entity
   - `name`, `telephone`, `address`, `areaServed`, `url`
2. **Service** — describes the specific service offered
   - `serviceType`, `provider`, `areaServed`
3. **FAQPage** — wraps Section 9 Q&A pairs
   - One `Question` + `Answer` per accordion item
4. **AreaServed** — lists all neighborhoods and zip codes from Section 7

---

## INTERNAL LINKING RULES

| Link type | Target | Anchor text |
|---|---|---|
| To location pages | Live location pages in phase1_registry.json | City name (e.g., "Austin") |
| To related services | Live service pages in phase1_registry.json | Service name (e.g., "roof inspection") |
| To homepage | `/` | Company name or "our team" |
| Deferred (not live) | Log in pending_links.json | NO hyperlink — plain text only |

Minimum 3 internal links per service page. Check phase1_registry.json before creating any link.

---

## QA CHECKLIST BEFORE PUBLISH

- [ ] H1 contains `{PRIMARY_SERVICE}` + `{CITY}` + `{STATE}`
- [ ] 40–60 word snippet zone present immediately after H1
- [ ] Hero word count ≤ 120 (including snippet zone)
- [ ] All 10 sections present in correct order
- [ ] Answer-first rule applied under every H2
- [ ] Key phrases bolded in services-grid and why-choose-us sections
- [ ] Section parity verified (services-grid cards, process steps within ±2%)
- [ ] local-proof section has geo-tagged review excerpts (city/neighborhood named)
- [ ] No pricing anywhere on page
- [ ] No em-dashes (`—`) in content body
- [ ] No separator lines (`---`) in content body
- [ ] FAQ has ≥ 5 questions with FAQPage schema, H3s written as natural language queries
- [ ] Map in service-area is Google Maps iframe (not AI image)
- [ ] All internal links verified against phase1_registry.json
- [ ] Deferred links logged in pending_links.json
- [ ] pre_publish_filter.py run with zero errors
