# LOCATION PAGE STRUCTURE
# Rank & Rent Pipeline — Page Type: Location / City Page
# Read by: PromptSeven.md (mandatory, before writing any location page)
# Research source: Confirmed 2026 local SEO + SAB (Service Area Business) best practices

---

## WHAT THIS FILE DEFINES
- Mandatory section order for all location/city pages
- H1 and H2 formulas
- Uniqueness requirements (what must be hyper-local vs. shared)
- Word count targets per section and total
- GEO / AI Overview optimization rules (2026)
- Schema markup requirements (SAB model)
- Internal linking rules specific to location pages

> PromptSeven.md writing rules (tone, parity, no em-dash, etc.) ALWAYS apply.
> This file defines WHAT sections and in WHAT order — not HOW to write them.

---

## 2026 GEO WRITING RULES (apply to every section)

1. **Self-contained blocks:** Each paragraph must answer its implied sub-question independently.
2. **Short paragraphs:** 2–3 sentences max.
3. **Bold key phrases:** Bold the most important local term per paragraph.
4. **Answer-first under every H2:** First sentence directly answers the section's implied question.
5. **Entity consistency:** NAP on this page must match Google Business Profile verbatim — no fake virtual office addresses for the location city.

---

## PAGE VARIABLES (from master_brief.json + topical_authority.json)
- `{PRIMARY_SERVICE}` — the hub service this location page belongs to
- `{LOCATION_CITY}` — the target city for this page (e.g., "Round Rock")
- `{HUB_CITY}` — the primary city of operations (e.g., "Austin")
- `{STATE}` — e.g., "TX"
- `{PHONE}` — from NAP block
- `{LOCAL_NEIGHBORHOODS}` — neighborhoods/zip codes within `{LOCATION_CITY}`
- `{LOCAL_LANDMARKS}` — real, verifiable local landmarks or districts in `{LOCATION_CITY}`
- `{LOCAL_CLIMATE_NOTE}` — local climate or geographic factor relevant to the service
- `{LOCAL_PERMIT_NOTE}` — any permit/regulatory nuance specific to `{LOCATION_CITY}` (research or leave blank)

---

## UNIQUENESS REQUIREMENT (2026 Research-Confirmed)

**Standard: 40% unique local data / 60% core service details.**

> This replaces the older "50–60% unique" benchmark. 2026 research confirms Google evaluates uniqueness by the presence of **genuine local proof** — not raw word percentage. A page with real local photos, neighborhood-specific reviews, and city-specific permit notes passes even at 40% unique.

| Content type | Requirement |
|---|---|
| Section 2 (localized-intro) | 100% UNIQUE — local landmarks, climate, community context. Never copy from hub or other location pages |
| Section 4 (local-proof) | 100% UNIQUE — city-specific reviews + project mentions from `{LOCATION_CITY}` ONLY |
| Section 5 (local-faq) | 100% UNIQUE — city-specific questions covering permits, response times, local conditions |
| Section 3 (services-overview) | Shared structure OK — localized framing and city name required |
| Section 6 (service-area-detail) | Unique neighborhood/zip list per city |
| Section 7 (bottom-cta) | Shared structure OK — city name injected |

**Realistic Radius Rule (2026):** Only build location pages for cities within a realistic operational radius (30–60 min drive) where you have actual customers or review velocity. Do NOT build pages for cities you do not actively service.

---

## MANDATORY SECTION ORDER — 7 SECTIONS

### SECTION 1 — gradient-hero
**Kadence block:** `kt-hero` with gradient background
**H1 formula:** `{PRIMARY_SERVICE} in {LOCATION_CITY}, {STATE}`
**Snippet Zone (2026):** 40–60 word direct answer block immediately beneath H1:
- What service is available, for whom, in which specific city
- Standalone paragraph — self-contained for RAG / AI Overview extraction
**Subheadline:** ≤50 words — reference `{LOCATION_CITY}` specifically, NOT the hub city
**Hero word budget:** ≤120 words total (HARD LIMIT)
**CTA:** Click-to-call + "Get a Free Estimate" anchor to bottom-cta
**No pricing**

---

### SECTION 2 — localized-intro (MUST BE 100% UNIQUE)
**Kadence block:** `kt-row` standard text block
**H2 formula:** `{PRIMARY_SERVICE} Services for {LOCATION_CITY} Residents`
**Answer-first rule:** First sentence states what makes this city's situation distinct.
**Structure:**
- 2–3 paragraphs, each 40–60 words, short paragraph format (2–3 sentences)
- Paragraph 1: Local hook — reference a **real, verifiable landmark or district** of `{LOCATION_CITY}` (e.g., "Whether your home is near the Dell Diamond or one of Round Rock's newer master-planned communities..."). Bold the landmark name.
- Paragraph 2: Connect `{LOCAL_CLIMATE_NOTE}` or `{LOCAL_PERMIT_NOTE}` to why the service matters specifically here.
- Paragraph 3: Brief brand introduction as a local provider — mention years serving the `{LOCATION_CITY}` area.
**Total word count:** 120–180 words
**HARD RULE:** Zero copy-paste from hub service page or any other location page. Google's doorway-page filter catches template spinning.

---

### SECTION 3 — services-overview
**Kadence block:** `kt-columns` (2 or 3 columns)
**H2 formula:** `Our {PRIMARY_SERVICE} Services in {LOCATION_CITY}`
**Answer-first rule:** First sentence states what services are available in this city.
**Structure:**
- 2–4 core sub-services framed from the local customer's perspective
- Each card: H3 sub-service name + 30–50 word description mentioning `{LOCATION_CITY}`
- **Bold** the key term in each card description
- Section parity: all cards within ±2% word count
- Internal link to hub service page: "See our full {PRIMARY_SERVICE} services" (must be live in phase1_registry.json)
**Total word count:** 120–200 words

---

### SECTION 4 — local-proof (MUST BE 100% UNIQUE)
**Kadence block:** `kt-testimonials` or `kt-columns`
**H2 formula:** `What {LOCATION_CITY} Customers Are Saying`
**Structure (2026 — GEO optimized):**
- 2–3 review excerpts — must reference `{LOCATION_CITY}` or a specific neighborhood within it
- Reviews with location-rich language rank higher in AI citation (e.g., "...fixed our roof right here in the Brushy Creek area")
- Each review: reviewer first name + neighborhood + 30–50 word quote
- 1 short paragraph (20–30 words): local projects completed stat + local area mention
- CSS text stars ONLY — never 3D rendered star images (FIX 18)
- **Optional but strongly preferred:** 1 geotagged project photo with alt text: "[Service] completed in [Neighborhood], {LOCATION_CITY}, {STATE}"
**HARD RULE:** Do NOT use generic reviews that could apply to any city

---

### SECTION 5 — local-faq (MUST BE 100% UNIQUE)
**Kadence block:** `kt-accordion`
**H2 formula:** `{PRIMARY_SERVICE} FAQs for {LOCATION_CITY} Homeowners`
**Answer-first rule:** Each answer opens with a direct 1-sentence reply.
**Structure:**
- 3–5 questions UNIQUE to `{LOCATION_CITY}` — framed as natural language voice-search queries
- Required question types:
  - **Permit/regulation:** "Does {LOCATION_CITY} require a permit for {PRIMARY_SERVICE}?" + `{LOCAL_PERMIT_NOTE}` answer
  - **Response time:** "How quickly can you reach [Neighborhood] in {LOCATION_CITY}?"
  - **Local condition:** "How does `{LOCAL_CLIMATE_NOTE}` affect {PRIMARY_SERVICE} in {LOCATION_CITY}?"
- Each answer: 40–70 words, short-paragraph format
**Schema:** FAQPage schema REQUIRED on these Q&A pairs
**HARD RULE:** Do NOT reuse questions from the hub service page FAQ or other location page FAQs

---

### SECTION 6 — service-area-detail
**Kadence block:** `kt-row` with text + optional map column
**H2 formula:** `Areas We Serve in and Around {LOCATION_CITY}`
**Structure:**
- Opening: "Our team covers {LOCATION_CITY} and these surrounding neighborhoods:"
- Bulleted list of neighborhoods and zip codes from `{LOCAL_NEIGHBORHOODS}`
- 1 sentence mentioning adjacent towns (plain text only if not live in phase1_registry.json)
- Google Maps iframe centered on `{LOCATION_CITY}` — NEVER AI-generated map image
**Total word count:** 60–100 words (excluding map)

---

### SECTION 7 — bottom-cta
**Kadence block:** `kt-row` with dark/brand background
**H2 formula:** `Serving {LOCATION_CITY} — Call for a Free Estimate Today`
**Structure:**
- 1–2 sentences (20–30 words): availability statement mentioning `{LOCATION_CITY}`
- Click-to-call button: `Call {PHONE}`
- Trust micro-copy: "Licensed • Insured • Serving {LOCATION_CITY} and Surrounding Areas"
**Word count:** ≤60 words

---

## WORD COUNT TARGETS

| Section | Min | Target | Max |
|---|---|---|---|
| hero (incl. snippet zone) | — | 100–120 | 120 (HARD) |
| localized-intro | 120 | 150–180 | 200 |
| services-overview | 120 | 150–200 | 220 |
| local-proof | 100 | 130–170 | 200 |
| local-faq | 150 | 200–280 | 350 |
| service-area-detail | 60 | 70–90 | 100 |
| bottom-cta | — | 40–60 | 60 |
| **TOTAL** | **700** | **1,000–1,400** | **1,600** |

---

## H2 FORMULA REFERENCE

| Section | H2 Template |
|---|---|
| localized-intro | `{PRIMARY_SERVICE} Services for {LOCATION_CITY} Residents` |
| services-overview | `Our {PRIMARY_SERVICE} Services in {LOCATION_CITY}` |
| local-proof | `What {LOCATION_CITY} Customers Are Saying` |
| local-faq | `{PRIMARY_SERVICE} FAQs for {LOCATION_CITY} Homeowners` |
| service-area-detail | `Areas We Serve in and Around {LOCATION_CITY}` |
| bottom-cta | `Serving {LOCATION_CITY} — Call for a Free Estimate Today` |

---

## SCHEMA MARKUP REQUIREMENTS (SAB — Service Area Business)

Do NOT use a fake LocalBusiness schema with the location city as the address — this violates GBP guidelines and triggers algorithmic penalties.

1. **Service** schema — describes the service in the location city
   - `serviceType`, `areaServed` → `City` or `AdministrativeArea` set to `{LOCATION_CITY}`
   - `provider` → references the main LocalBusiness entity on the hub/homepage
2. **AreaServed** — lists all neighborhoods and zip codes from Section 6
   - Use `GeoCircle`, `City`, or `AdministrativeArea` — not a fake physical address
3. **FAQPage** — wraps Section 5 Q&A pairs only

---

## INTERNAL LINKING RULES

| Link type | Target | Anchor text |
|---|---|---|
| Back to hub service page | Live service page in phase1_registry.json | Service name (e.g., "roof replacement services") |
| To sibling location pages | Live location pages in phase1_registry.json | City name (e.g., "Cedar Park") |
| To homepage | `/` | "our team" or company name |
| Deferred | Not live → log pending_links.json | NO hyperlink — plain text |

Minimum 2 internal links per location page. Hub service page link is mandatory.
Do NOT cross-link every city page to every other city page in a footer grid — this signals a manipulative network.

---

## QA CHECKLIST BEFORE PUBLISH

- [ ] H1 contains `{PRIMARY_SERVICE}` + `{LOCATION_CITY}` + `{STATE}`
- [ ] 40–60 word snippet zone present immediately after H1
- [ ] Hero word count ≤ 120 (including snippet zone)
- [ ] All 7 sections present in correct order
- [ ] Answer-first rule applied under every H2
- [ ] Sections 2, 4, 5 are 100% unique to this city — not copied from any other page
- [ ] Section 4 has location-rich review language (neighborhood/city named in quotes)
- [ ] Section 5 has 3–5 city-specific FAQ questions in natural language format
- [ ] FAQPage schema applied to Section 5 Q&A pairs
- [ ] SAB schema used — `areaServed` with City/GeoCircle (NOT fake LocalBusiness with location city address)
- [ ] Map in Section 6 is Google Maps iframe (not AI image)
- [ ] CSS stars used in Section 4 (not rendered star images)
- [ ] Location page is within realistic operational radius (30–60 min drive from hub)
- [ ] No em-dashes in content body
- [ ] No pricing anywhere
- [ ] All internal links verified against phase1_registry.json
- [ ] Deferred links logged in pending_links.json
- [ ] pre_publish_filter.py run with zero errors
