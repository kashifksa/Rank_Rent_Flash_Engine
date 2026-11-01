# P7 Blog — Section 07: FAQ
# Flash Engine — Blog Post | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
POST_TITLE       = [fill in — exact title from topical_authority.json, do not rewrite]
POST_KEYWORD     = [fill in — primary informational keyword]
CITY             = [fill in]
STATE            = [fill in]
PRIMARY_SERVICE  = [fill in — parent service this post supports]
PHONE            = [fill in]
RELATED_SERVICE_PAGE = [fill in — slug of live service page from phase1_registry.json]
AUTHOR_NAME      = [fill in — from master_brief.json]
AUTHOR_TITLE     = [fill in — e.g. "Master Roofer, 15 years serving Austin"]

## SECTION RULES — FAQ (Section 7 of 8)
Word budget: 150-350 words

H2: Frequently Asked Questions About [Topic of {POST_KEYWORD}] in {CITY}

Write 3-5 questions in natural language format (voice search + AI Overview).

Required question types — include at least one of each:
- LONG-TAIL: variation of {POST_KEYWORD}
- LOCAL REGULATORY: "Do I need a permit for [action] in {CITY}?" (high AI value)
- PROCESS/TIMELINE: framed without pricing
- VOICE SEARCH: "Can I..." or "Should I..." or "Is it safe to..."

Per answer:
- Open with direct 1-sentence reply (answer-first)
- Then elaborate: 40-80 words total
- No pricing — "Contact us for a free estimate" for cost questions

IMPORTANT: Do NOT repeat questions already in {RELATED_SERVICE_PAGE} FAQ.
Check the service page FAQ before writing.

SELF-CHECK:
- [ ] H2 mentions topic and {CITY}
- [ ] 3-5 questions, all natural language format
- [ ] Local regulatory question included
- [ ] Each answer opens with direct reply
- [ ] No pricing
- [ ] No duplicate questions from service page FAQ
- [ ] 150-350 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: blog_page_example.md -->
<!-- Section 07 — injected by inject_golden_examples.py -->

## Frequently Asked Questions About Air Duct Cleaning Scams in Rockford

### How can I verify that a duct cleaning company is actually NADCA certified?

You can verify NADCA membership directly at nadca.com using the company's name or ZIP code. **NADCA maintains a public member directory** that is updated in real time. Any company claiming certification that does not appear in that directory is misrepresenting their credentials. You can also call NADCA directly at 1-855-NADCA-NOW to verify a membership number.

### Is it safe to let a duct cleaning company into my home if they cannot show certification?

No. Allowing an uncertified company access to your duct system carries real risk beyond the financial. **Unqualified technicians can physically damage flexible ducts**, disconnect branch runs, or use equipment that blows debris into your living space rather than extracting it. Insist on NADCA certification and proof of liability insurance before any technician enters.

### What should I do if I already paid a duct cleaning company and suspect it was a scam?

If you paid by credit card, file a chargeback dispute with your card issuer immediately and document your reason. If you paid by cash or check, file a complaint with the **Illinois Attorney General's Consumer Protection Hotline at 1-800-386-5438**. Also report the company to the Better Business Bureau so other Rockford homeowners see the complaint record.

### Can a duct cleaning company test for mold on the spot during a cleaning appointment?

No. **Legitimate mold identification requires laboratory analysis** of a physical sample sent to an accredited environmental testing lab. Visual identification during a duct cleaning is not a valid mold diagnosis. Any company that claims to have found mold and offers to treat it immediately without a lab report is using a well-documented upsell tactic.

### How do I know if the duct cleaning I already had done was actually completed properly?

If you did not receive before-and-after camera documentation, you have no verifiable proof that source removal was performed. **The only reliable way to verify a past cleaning** is to schedule a new camera inspection, which a legitimate company will perform. If interior duct surfaces still show heavy particulate adhesion to walls, the previous cleaning did not meet NADCA source removal standards.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
