# P7 Service — Section 09: FAQ
# Flash Engine — Service Page | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
PRIMARY_SERVICE = [fill in]
CITY            = [fill in]
STATE           = [fill in]
COMPANY_NAME    = [fill in]
PHONE           = [fill in]
LOCAL_CHALLENGE = [fill in — e.g. "Austin's intense hail storms"]

## SECTION RULES — FAQ (Section 9 of 10)
Word budget: 400-650 words total (all Q&A combined)

H2: Frequently Asked Questions About {PRIMARY_SERVICE} in {CITY}

Write 8-12 FAQ items. Each H3 must be a natural language question
(voice search + AI Overview targeting format).

Required question types — must include at least one of each:
- PROCESS: "How long does {PRIMARY_SERVICE} take in {CITY}?"
- LOCAL: "Do you serve [specific neighborhood] in {CITY}?"
- PERMIT/REGULATORY: "Do I need a permit for {PRIMARY_SERVICE} in {STATE}?"
  (HIGH AI Overview value in 2026 — always include this)
- TRUST: "Are you licensed and insured in {STATE}?"
- PROBLEM: "What happens if I delay {PRIMARY_SERVICE}?"

Per answer:
- Open with a direct 1-sentence answer (answer-first rule)
- Then elaborate: 40-80 words total per answer
- No pricing — redirect with "Contact us for a free estimate"

SELF-CHECK before outputting:
- [ ] H2 matches: "Frequently Asked Questions About {PRIMARY_SERVICE} in {CITY}"
- [ ] 8-12 questions written
- [ ] All H3s are natural language questions (not keyword-stuffed)
- [ ] Every answer opens with a direct 1-sentence reply
- [ ] Permit/regulatory question is included
- [ ] No pricing in any answer
- [ ] Total 400-650 words

## GOLDEN EXAMPLE
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->
<!-- Priority: fill this before Nov 2 while Claude access is available -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
