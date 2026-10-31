# ABOUT PAGE STRUCTURE
# Rank & Rent Pipeline — Page Type: About Page (and Contact variant)
# Read by: PromptSeven.md (mandatory, before writing About or Contact page)
# Research source: Confirmed 2026 local SEO / E-E-A-T / Entity Authority best practices

---

## WHAT THIS FILE DEFINES
- Mandatory section order for the About page
- Contact page variant (simplified version)
- H1 and H2 formulas
- E-E-A-T signal requirements (Experience, Expertise, Authoritativeness, Trustworthiness)
- Entity triangulation rules (2026 — cross-platform NAP + social consistency)
- Word count targets per section and total
- Schema markup requirements
- Internal linking rules specific to About/Contact pages

> PromptSeven.md writing rules (tone, parity, no em-dash, etc.) ALWAYS apply.
> This file defines WHAT sections and in WHAT order — not HOW to write them.

---

## 2026 ENTITY AUTHORITY RULES (apply to every section)

In 2026, Google's AI systems validate local businesses through **entity triangulation** — cross-referencing website content against Google Business Profile, social profiles, directories, and review platforms:

1. **NAP lock:** Business name, address, and phone on this page must match Google Business Profile verbatim. Any mismatch damages local pack rankings.
2. **sameAs signals:** Link to (or reference) verified social profiles and directories — Google uses `sameAs` schema to connect your entity across platforms.
3. **Real media only:** Unique, geo-tagged original photos (real team, real vehicles, real work) signal a genuine local entity to both algorithms and human visitors. Stock photos signal a fake/faceless business.
4. **License numbers visible:** Displaying actual license numbers (`Licensed {TRADE} in {STATE} — License #XXXXX`) satisfies both algorithmic trust checks and human skepticism.
5. **Short paragraphs:** 2–3 sentences max. Bold the most important credential or fact per paragraph.

---

## PAGE VARIABLES (from master_brief.json)
- `{COMPANY_NAME}` — from NAP block
- `{CITY}` — primary city of operations
- `{STATE}` — e.g., "TX"
- `{PHONE}` — from NAP block
- `{ADDRESS}` — full street address from NAP block
- `{FOUNDED_YEAR}` — year business was founded
- `{PRIMARY_SERVICE}` — main service category
- `{SERVICE_AREA}` — full list of cities/regions served
- `{CREDENTIALS}` — licenses, certifications, accreditations (from master_brief.json)
- `{COMMUNITY_TIES}` — local memberships, sponsorships, chamber memberships
- `{SOCIAL_PROFILES}` — Facebook, Instagram, Google Business Profile URL, BBB, Yelp

---

## E-E-A-T SIGNAL MAP

| Section | E-E-A-T Signal | 2026 Focus |
|---|---|---|
| identity-hook | Experience | Geographic + temporal establishment, real photo |
| origin-story | Experience | Human history, real-world milestones, local milestones |
| team-credentials | Expertise | Named people + real licenses + linked author bios |
| credentials-display | Expertise + Trustworthiness | Dedicated visible license/cert block (NEW 2026) |
| community-proof | Authoritativeness | Local org logos, event photos, press mentions |
| trust-signals | Trustworthiness | Live reviews, real stats, before/after local work |
| service-area-nap | Trustworthiness | NAP consistency, entity triangulation links |
| bottom-cta | Conversion | Action step after trust is established |

---

## MANDATORY SECTION ORDER — 8 SECTIONS (About Page)

### SECTION 1 — identity-hook
**Kadence block:** `kt-hero` or `kt-row` with team/owner photo
**H1 formula:** `About {COMPANY_NAME} — {PRIMARY_SERVICE} Experts in {CITY}, {STATE}`
**Structure:**
- 2–3 sentence value proposition: who, what, where, how long
  - Example: "**Proudly serving {CITY} homeowners** with expert {PRIMARY_SERVICE} since {FOUNDED_YEAR}."
- Authentic photo: real owner, team, or work vehicle — NEVER stock photos (entity signal)
- Quick trust bar beneath photo: years in business | licensed/insured status | CTA "Call Us Today"
- No pricing, no unsubstantiated "we're the best" claims
**E-E-A-T:** Establishes Experience + geographic relevance instantly
**Total word count:** 60–100 words (excluding H1 and trust bar labels)

---

### SECTION 2 — origin-story
**Kadence block:** Standard text block or timeline layout (if 3+ year history)
**H2 formula:** `Our Story: How {COMPANY_NAME} Came to Serve {CITY}`
**Answer-first rule:** First sentence states how long the business has been operating and why it was founded.
**Structure:**
- Narrative: why the business was founded, local market gap identified
- Mention specific local context: city, neighborhood, early client milestones
- If 3+ years of history: use a timeline format — milestone | year (AI engines extract this cleanly)
- Tone: personal, community-first, honest — not corporate
- 2–3 paragraphs, each 50–70 words, **bold** key milestone facts
**E-E-A-T:** Feeds Experience — proves human history and active local participation
**Total word count:** 150–220 words

---

### SECTION 3 — team-credentials
**Kadence block:** `kt-columns` (team card layout) or standard text block
**H2 formula:** `Meet the {COMPANY_NAME} Team`
**Structure:**
- Owner/operator bio: real name, role, years of experience, personal connection to `{CITY}`
- Key staff bios if applicable (same card format)
- Per bio: **Name + Role** + 30–50 word description
- Link author names to dedicated author bio pages if blog posts exist (2026 GEO — AI engines validate authorship entities)
- Real headshots STRONGLY required — no stock imagery
**E-E-A-T:** Direct Expertise signal — Google links real people + verified credentials to business entity
**Schema:** `Person` schema: `name`, `jobTitle`, `worksFor` → LocalBusiness, link to author page if available
**Total word count:** 150–250 words

---

### SECTION 4 — credentials-display (NEW — 2026)
**Kadence block:** `kt-columns` with badge/icon layout or clean list
**H2 formula:** `Licensed, Certified, and Accountable`
**Purpose (2026):** Dedicated credentials section separate from team bios — makes license numbers and accreditations scannable by both users and AI engines.
**Structure:**
- Explicit list from `{CREDENTIALS}`:
  - **Format:** "Licensed {TRADE} in {STATE} — License #XXXXX"
  - Insurance details (general liability, workers' comp)
  - Industry certifications (e.g., NARI Member, GAF Certified, BBB Accredited)
  - State board or municipal license numbers
- Include badge images for recognized accreditations (BBB, Chamber of Commerce, manufacturer certs)
- Bold every license number and certification name
**E-E-A-T:** Expertise + Trustworthiness — transparency here lowers customer friction AND satisfies algorithmic trust checks
**Total word count:** 60–120 words

---

### SECTION 5 — community-proof
**Kadence block:** `kt-columns` with logo/icon badges or text list
**H2 formula:** `Rooted in the {CITY} Community`
**Answer-first rule:** First sentence states the business's core community commitment.
**Structure:**
- 1 paragraph introducing community ties (30–50 words)
- Badge/logo display of `{COMMUNITY_TIES}`:
  - Chamber of Commerce membership
  - Local trade associations
  - Youth sports sponsorships or local charity involvement
  - Civic group participation, local press mentions
- Use actual logos of recognized local organizations where possible
- Mention any press/media mentions by name ("Featured in [Local Publication]")
- Tone: genuine investment — not a marketing checklist
**E-E-A-T:** Authoritativeness — validates physical existence as a local entity (signals to Google this is NOT a lead-gen spam site)
**Total word count:** 80–150 words

---

### SECTION 6 — trust-signals
**Kadence block:** `kt-row` with stats bar + `kt-testimonials` for reviews
**H2 formula:** `Why {CITY} Homeowners Trust {COMPANY_NAME}`
**Answer-first rule:** First sentence states the most credible trust metric.
**Structure:**
- Stats bar (3–4 concrete numbers):
  - "500+ Local Projects Completed" | "4.9★ Average Rating" | "Serving {CITY} Since {FOUNDED_YEAR}"
  - **Bold** each stat number
- 2–3 real customer review excerpts — must name `{CITY}` or a specific neighborhood
- Each review: First name + Neighborhood + 30–50 word quote
- CSS text stars ONLY — NEVER 3D rendered star images (FIX 18)
- Optional: before/after project teaser with geo-tagged photo (alt text: "[Service] in [Neighborhood], {CITY}")
**E-E-A-T:** Trustworthiness — specific, real-world validation vs. generic claims
**Total word count:** 120–180 words

---

### SECTION 7 — service-area-nap
**Kadence block:** `kt-row` two columns: NAP info + Google Maps iframe
**H2 formula:** `Serving {CITY} and Surrounding Communities`
**Structure:**
- Left column (NAP block — must match Google Business Profile verbatim):
  - Business name: `{COMPANY_NAME}`
  - Address: `{ADDRESS}`
  - Phone: `{PHONE}` (click-to-call formatted)
  - Hours of operation
  - Service area list: `{SERVICE_AREA}` (hyperlink only if live in phase1_registry.json)
- Right column: Google Maps iframe centered on `{ADDRESS}` — NEVER AI-generated map
- **Entity triangulation links (2026):** Below the NAP block, add text links to `{SOCIAL_PROFILES}`:
  - "Find us on [Google Business Profile] | [Facebook] | [BBB]"
  - These validate the entity across platforms — Google checks `sameAs` cross-references
**E-E-A-T:** Trustworthiness — NAP consistency + entity triangulation = stronger local entity signal
**Total word count:** 80–120 words (text only, excluding map and link labels)

---

### SECTION 8 — bottom-cta
**Kadence block:** `kt-row` with brand/dark background
**H2 formula:** `Ready to Work with {CITY}'s Trusted {PRIMARY_SERVICE} Team?`
**Structure:**
- 1–2 sentences: trust recap + action statement (25–40 words)
- Click-to-call button: `Call {PHONE}`
- Secondary: contact form link or embedded 3-field form (Name, Phone, Message)
- Trust micro-copy: "Licensed • Insured • Proudly Serving {CITY} Since {FOUNDED_YEAR}"
**Total word count:** ≤60 words

---

## WORD COUNT TARGETS (About Page)

| Section | Min | Target | Max |
|---|---|---|---|
| identity-hook | 60 | 80–100 | 110 |
| origin-story | 150 | 170–210 | 230 |
| team-credentials | 150 | 180–230 | 260 |
| credentials-display | 60 | 80–110 | 130 |
| community-proof | 80 | 100–140 | 160 |
| trust-signals | 120 | 140–170 | 190 |
| service-area-nap | 80 | 90–110 | 130 |
| bottom-cta | — | 40–60 | 60 |
| **TOTAL** | **800** | **1,000–1,200** | **1,400** |

---

## CONTACT PAGE VARIANT

The Contact page is a simplified version of the About page. Use sections 7 and 8 only, plus an expanded contact form.

**Contact Page section order:**
1. **contact-hero:** H1 = `Contact {COMPANY_NAME} in {CITY}, {STATE}` | 30–50 word intro
2. **contact-form:** Full contact form (Name, Phone, Email, Message, Service dropdown)
3. **nap-block:** Identical to About Page Section 7 — NAP + Google Maps iframe + entity triangulation links
4. **trust-bar:** Same 3–4 trust badges as service page Section 2

**Contact page word count target:** 150–300 words total (form labels excluded)
**Schema:** `LocalBusiness` + `ContactPage`

---

## H2 FORMULA REFERENCE (About Page)

| Section | H2 Template |
|---|---|
| origin-story | `Our Story: How {COMPANY_NAME} Came to Serve {CITY}` |
| team-credentials | `Meet the {COMPANY_NAME} Team` |
| credentials-display | `Licensed, Certified, and Accountable` |
| community-proof | `Rooted in the {CITY} Community` |
| trust-signals | `Why {CITY} Homeowners Trust {COMPANY_NAME}` |
| service-area-nap | `Serving {CITY} and Surrounding Communities` |
| bottom-cta | `Ready to Work with {CITY}'s Trusted {PRIMARY_SERVICE} Team?` |

---

## SCHEMA MARKUP REQUIREMENTS (2026)

1. **LocalBusiness** (specific subtype preferred — e.g., `Plumber`, `RoofingContractor`) — primary schema
   - `name`, `telephone`, `address`, `url`, `foundingDate`
   - `areaServed` — all cities in `{SERVICE_AREA}`
   - `sameAs` array → all URLs from `{SOCIAL_PROFILES}` (Google Business Profile, Facebook, BBB, Yelp)
2. **Person** — for owner/operator in Section 3
   - `name`, `jobTitle`, `worksFor` → LocalBusiness entity
   - `url` → author bio page (if exists)
3. **Organization** (if applicable)
   - `sameAs` → same social profiles as LocalBusiness for cross-entity linking

---

## INTERNAL LINKING RULES

| Link type | Target | Anchor text |
|---|---|---|
| To homepage | `/` | Company name |
| To core service page | Live service page in phase1_registry.json | Service name |
| To contact page | Live contact page in phase1_registry.json | "Contact us" |
| To blog (from author name) | Live About page in phase1_registry.json | Author name |
| To location pages | Live location pages (if applicable) | City names |
| Deferred | Not live → log pending_links.json | NO hyperlink |

Minimum 2 internal links on About page. Core service page link is mandatory.

---

## REAL MEDIA RULES (2026 — E-E-A-T requirement)

- **Owner/team photos:** Real people only — no stock smiling-person imagery. Google's computer vision detects common stock images and penalizes them on About pages.
- **Storefront/vehicle:** Use actual business photos with geo-tagged EXIF data (run `image_geotagger.py`)
- **Community event photos:** Real event photos — not staged stock
- **Before/after project photos:** Geo-tagged, locally captioned alt text required
- **Map:** Google Maps iframe only — never AI-generated map image

---

## QA CHECKLIST BEFORE PUBLISH

- [ ] H1 contains `{COMPANY_NAME}` + `{CITY}` + `{STATE}`
- [ ] All 8 sections present in correct order
- [ ] No stock photos in Section 1 or Section 3 — real team/owner photos used
- [ ] Section 4 includes real license numbers and certification names from master_brief.json
- [ ] Section 4 credential section is present (separate from team bios)
- [ ] CSS stars used in Section 6 (not rendered star images)
- [ ] NAP in Section 7 matches Google Business Profile verbatim
- [ ] Entity triangulation links present in Section 7 (social profiles listed)
- [ ] Map in Section 7 is Google Maps iframe (not AI image)
- [ ] Person schema applied for owner/operator
- [ ] LocalBusiness schema applied with `sameAs` social profile array
- [ ] No pricing anywhere
- [ ] No em-dashes in content body
- [ ] All internal links verified against phase1_registry.json
- [ ] Deferred links logged in pending_links.json
- [ ] pre_publish_filter.py run with zero errors
