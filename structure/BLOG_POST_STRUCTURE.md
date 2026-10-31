# BLOG POST STRUCTURE
# Rank & Rent Pipeline — Page Type: Blog Post (Informational)
# Read by: PromptSeven.md (mandatory, before writing any blog post)
# Research source: Confirmed 2026 local SEO + GEO (Generative Engine Optimization) best practices

---

## WHAT THIS FILE DEFINES
- Mandatory section order for all blog posts
- H1, H2, H3 formulas (question-based headings for AI Overview targeting)
- Informational intent rules (what IS and IS NOT allowed)
- Word count targets per section and total
- GEO / AI Overview optimization rules (2026)
- Schema markup requirements
- Internal linking rules specific to blog posts
- Pre-write cannibalization check requirement

> PromptSeven.md writing rules (tone, parity, no em-dash, etc.) ALWAYS apply.
> This file defines WHAT sections and in WHAT order — not HOW to write them.

---

## 2026 GEO WRITING RULES (apply to every section)

1. **Answer-first model:** Every H2 section opens with a 1–2 sentence direct answer. Elaboration follows. AI engines pull from first-sentence answers.
2. **Question-based headings:** Frame ALL H2 and H3 tags as questions local customers actually ask — this targets AI Overviews, "People Also Ask" boxes, and voice search.
3. **Short paragraphs:** 2–3 sentences max. RAG engines parse chunk by chunk.
4. **Bold key phrases:** Bold the most important term or data point in each paragraph.
5. **Local entity embedding:** Weave in local landmarks, municipal codes, utility providers, or neighborhood names naturally. This prevents AI from treating the post as generic national advice.
6. **At least one structured data element per post:** A table, numbered list, or bullet list — AI Overviews heavily favor parseable structured formats.

---

## INTENT GATE — MUST PASS BEFORE WRITING

Blog posts on this site target **informational intent ONLY**.

**Allowed keyword intents:**
- `how to [do something]`
- `signs of [problem]`
- `what is [term]`
- `when to [call/replace/fix]`
- `why does [thing] happen`
- `guide to [topic]`
- `[A] vs [B]` (comparison, educational — not "which company to hire")

**NEVER use transactional intent keywords:**
- "best [service] company in [city]"
- "[service] cost / pricing / quote"
- "hire [service] [city]"
- "[service] near me"

**Cannibalization check REQUIRED before writing:**
```
python check_blog_cannibalization.py --new-keyword "[proposed keyword]"
```
Do NOT write the post if this script returns FAIL. Update the keyword in topical_authority.json and re-run.

---

## PAGE VARIABLES (from master_brief.json + topical_authority.json)
- `{POST_KEYWORD}` — the primary informational keyword for this post
- `{POST_TITLE}` — the H1 / SEO title (set by topical_authority.json — do not rewrite it)
- `{CITY}` — primary service city (for local context sections)
- `{STATE}` — e.g., "TX"
- `{PRIMARY_SERVICE}` — the parent service this post supports
- `{PHONE}` — from NAP block (for CTA section only)
- `{RELATED_SERVICE_PAGE}` — slug of the live service page to link to (from phase1_registry.json)
- `{AUTHOR_NAME}` — owner/operator name from master_brief.json (for author attribution)
- `{AUTHOR_TITLE}` — trade credential / role (e.g., "Master Roofer, 15 years serving Austin")

---

## MANDATORY SECTION ORDER — 8 SECTIONS

### SECTION 1 — post-header (H1 + immediate answer block)
**Kadence block:** Standard post title + `kt-row` intro block
**H1:** Use `{POST_TITLE}` exactly as set in topical_authority.json — do NOT rewrite it
**Immediate Answer Block (Featured Snippet / AI Overview target — 2026 REQUIRED):**
- 40–60 words immediately beneath the H1
- Directly answer the core question stated in `{POST_KEYWORD}` — one standalone paragraph
- Do NOT open with "In this article..." or "We will cover..." — get straight to the answer
- Short sentences, mobile-first format
**Author Attribution Line (NEW — 2026 E-E-A-T):**
- Immediately after the immediate answer block
- Format: "By {AUTHOR_NAME} | {AUTHOR_TITLE}"
- Link author name to About page (if live in phase1_registry.json)
**Total word count for this section:** 80–120 words

---

### SECTION 2 — cause-or-context
**Kadence block:** Standard text block
**H2 formula (question-based):** `What Causes [Core Problem Related to {POST_KEYWORD}]?`
**Answer-first rule:** First sentence directly answers the H2 question.
**Structure:**
- 2–3 short paragraphs (2–3 sentences each)
- Cause list: 3–5 bullets with **bolded** cause labels
- At least one H3 for a local/seasonal factor:
  - H3 formula: `How [Local Condition] in {CITY} Makes [Issue] Worse`
- Include at least one local entity (city code, regional weather pattern, local infrastructure)
**Total word count:** 150–250 words

---

### SECTION 3 — diy-vs-pro
**Kadence block:** Standard text block or two-column layout
**H2 formula (question-based):** `When Should {CITY} Homeowners Call a Professional vs. DIY?`
**Answer-first rule:** First sentence states the general rule of thumb.
**Structure:**
- H3: `Safe checks you can do yourself` — 3–5 bullets, **bolded** action per bullet
- H3: `Red flags that require a licensed expert in {CITY}` — 3–5 bullets
- Demonstrates E-E-A-T: trade expertise without becoming a sales pitch
- Keeps informational intent — no direct pitching of services here
**Total word count:** 150–220 words

---

### SECTION 4 — structured-data-element (NEW — 2026 required)
**Kadence block:** Table block or structured list block
**H2 formula (question-based):** `[Quick Reference: Topic Summary Table or Key Facts]`
**Purpose:** AI Overviews heavily favor structured data — tables, comparison lists, step-by-step numbered lists. Every blog post MUST have at least one.
**Options (choose whichever fits the post topic):**
- **Comparison table:** Type of issue | Severity | Recommended action | Timeframe
- **Step-by-step numbered list:** Professional process steps (3–5 steps)
- **Quick-reference bullet list:** Key facts about the topic, localized where possible
**Do NOT add pricing columns** — redirect with "Contact us for a free estimate"
**Total word count:** 60–120 words (table labels + brief context sentence)

---

### SECTION 5 — how-it-works (bridge section)
**Kadence block:** Standard text block or numbered list
**H2 formula (question-based):** `How Does Professional [Service/Process] Work?`
**Answer-first rule:** First sentence states what the professional process involves.
**Structure:**
- Step-by-step outline of the professional approach (3–5 steps)
- Bridges informational content to commercial service naturally — educational framing, not sales
- **Internal link placement:** Add 1 contextual link to `{RELATED_SERVICE_PAGE}` within this section
  - Example: "Our [service name] team starts with a thorough inspection..." linked to the service page
- Bold step titles or key terms
**Total word count:** 150–200 words

---

### SECTION 6 — local-considerations
**Kadence block:** Standard text block
**H2 formula (question-based):** `What Should {CITY} Homeowners Know About [Topic]?`
**Answer-first rule:** First sentence states the most important local consideration.
**Structure:**
- 2–3 paragraphs embedding local relevance naturally
- Reference local building codes, regional climate, municipal rules, or local geography
- Mention at least one: local utility company, city code reference, specific neighborhood, or local landmark
- Example framing: "**{CITY}'s [local condition]** means [specific implication for homeowners]"
- City name: 1–2 natural mentions per paragraph max — no stuffing
**Total word count:** 120–180 words

---

### SECTION 7 — faq
**Kadence block:** `kt-accordion`
**H2 formula:** `Frequently Asked Questions About [Topic of {POST_KEYWORD}] in {CITY}`
**Answer-first rule:** Each answer opens with a direct 1-sentence reply.
**Structure:**
- 3–5 questions in natural language format (voice search + AI Overview targeting)
- Question types:
  - Long-tail variation of the main keyword
  - Local regulatory/permit question (high AI Overview value in 2026)
  - How long / how much — answer without pricing ("varies, contact us for a free estimate")
  - Voice search format: "Can I...?" or "Should I...?" or "Is it safe to...?"
- Each answer: 40–80 words
**Schema:** FAQPage schema REQUIRED on all Q&A pairs
**Do NOT ask questions that overlap with the FAQ on `{RELATED_SERVICE_PAGE}`** — check before writing

---

### SECTION 8 — conclusion-cta
**Kadence block:** `kt-row` with subtle background or standard text
**H2 formula:** `Get Expert {PRIMARY_SERVICE} Help in {CITY}`
**Answer-first rule:** First sentence summarizes the post's key takeaway.
**Structure:**
- 1–2 sentence wrap-up (25–40 words): key takeaway + transition to action
- Low-friction local CTA: "If you're dealing with [issue] in the greater {CITY} area..." + action statement
- Click-to-call link: `{PHONE}` formatted as clickable phone link
- 2 related blog post or service page links (must be live in phase1_registry.json)
**Total word count:** 60–100 words

---

## WORD COUNT TARGETS

| Section | Min | Target | Max |
|---|---|---|---|
| post-header (incl. answer block) | 80 | 90–120 | 130 |
| cause-or-context | 150 | 180–220 | 250 |
| diy-vs-pro | 150 | 170–200 | 220 |
| structured-data-element | 60 | 80–110 | 120 |
| how-it-works | 150 | 160–190 | 200 |
| local-considerations | 120 | 140–170 | 180 |
| faq | 150 | 200–300 | 400 |
| conclusion-cta | 60 | 70–90 | 100 |
| **TOTAL** | **1,000** | **1,300–1,600** | **1,800** |

---

## H2 FORMULA REFERENCE

| Section | H2 Template (question-based) |
|---|---|
| cause-or-context | `What Causes [Core Problem]?` |
| diy-vs-pro | `When Should {CITY} Homeowners Call a Professional vs. DIY?` |
| structured-data-element | `[Quick Reference: Topic Summary Table or Key Facts]` |
| how-it-works | `How Does Professional [Service/Process] Work?` |
| local-considerations | `What Should {CITY} Homeowners Know About [Topic]?` |
| faq | `Frequently Asked Questions About [Topic] in {CITY}` |
| conclusion-cta | `Get Expert {PRIMARY_SERVICE} Help in {CITY}` |

---

## SCHEMA MARKUP REQUIREMENTS

1. **BlogPosting** (or `Article`) schema — wraps the full post
   - `headline` = H1 title
   - `author` → `Person`: `{AUTHOR_NAME}`, `jobTitle`: `{AUTHOR_TITLE}`
   - `datePublished`, `dateModified`
   - `publisher` → LocalBusiness entity reference
2. **FAQPage** — wraps Section 7 Q&A pairs

---

## INTERNAL LINKING RULES

| Link type | Target | Anchor text |
|---|---|---|
| To service page | Live service page in phase1_registry.json | Descriptive (e.g., "roof replacement services") |
| To related blog posts | Live blog posts in phase1_registry.json | Post topic (e.g., "signs of roof damage") |
| To About page (for author link) | Live About page in phase1_registry.json | Author name |
| To homepage | `/` | Company name or "our team" |
| Deferred | Not live → log pending_links.json | NO hyperlink — plain text |

**Minimum 3 internal links per blog post:**
- 1 mandatory link to `{RELATED_SERVICE_PAGE}`
- At least 2 additional links to live pages (service or blog)

---

## CANNIBALIZATION PREVENTION RULES

1. Run `check_blog_cannibalization.py --new-keyword "[keyword]"` — if FAIL, update keyword and re-run before writing
2. Each post must answer a **distinct question** — not the same angle as any existing post
3. No two blog posts may share >50% of meaningful keyword tokens (Jaccard similarity)
4. Blog post keywords must NOT overlap with any service or location page keyword
5. Section 7 FAQ must NOT duplicate Q&As from `{RELATED_SERVICE_PAGE}` FAQ

---

## QA CHECKLIST BEFORE PUBLISH

- [ ] `check_blog_cannibalization.py` run — returned PASS
- [ ] H1 matches `{POST_TITLE}` exactly as in topical_authority.json
- [ ] 40–60 word immediate answer block present beneath H1
- [ ] Author attribution line present (By {AUTHOR_NAME} | {AUTHOR_TITLE})
- [ ] Keyword intent is informational — no transactional language
- [ ] All 8 sections present in correct order
- [ ] All H2/H3 headings written as natural language questions
- [ ] At least 1 structured data element (table or structured list) in Section 4
- [ ] Local entities embedded (landmark, code, climate factor, neighborhood)
- [ ] Section 7 FAQ has FAQPage schema
- [ ] BlogPosting schema applied with Person author
- [ ] Minimum 3 internal links, all verified in phase1_registry.json
- [ ] No FAQ questions that duplicate service page FAQ
- [ ] No pricing mentioned anywhere
- [ ] No em-dashes in content body
- [ ] pre_publish_filter.py run with zero errors
