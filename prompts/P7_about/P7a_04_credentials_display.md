# P7 About — Section 04: Credentials Display (NEW 2026)
# Flash Engine — About Page | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
COMPANY_NAME     = [fill in]
CITY             = [fill in]
STATE            = [fill in]
PHONE            = [fill in]
ADDRESS          = [fill in — full address from NAP]
FOUNDED_YEAR     = [fill in]
PRIMARY_SERVICE  = [fill in]
SERVICE_AREA     = [fill in — list of cities served]
CREDENTIALS      = [fill in — licenses, certs from master_brief.json]
COMMUNITY_TIES   = [fill in — memberships, sponsorships]
SOCIAL_PROFILES  = [fill in — GBP URL, Facebook, BBB, Yelp]

## SECTION RULES — Credentials Display (Section 4 of 8)
Word budget: 60-120 words

H2: Licensed, Certified, and Accountable

Write explicit credential list from {CREDENTIALS}:
- **Licensed [Trade] in {STATE}** — License #[number from master_brief]
- **[Insurance type]** — General Liability + Workers' Comp
- **[Certification name]** — e.g. "GAF Certified Installer"
- **[Association]** — e.g. "BBB Accredited Business"
- **[Local association]** — e.g. "Member, {CITY} Chamber of Commerce"

Bold every license number and certification name.

Note: "[BADGE IMAGES: BBB, Chamber, manufacturer cert logos]"

SELF-CHECK:
- [ ] H2 = "Licensed, Certified, and Accountable"
- [ ] Real license numbers from {CREDENTIALS} used
- [ ] Every credential bolded
- [ ] Badge image note included
- [ ] 60-120 words

## GOLDEN EXAMPLE
<!-- PASTE YOUR CLAUDE/PRO OUTPUT FOR THIS SECTION HERE -->
<!-- Until filled: Flash will follow the rules above without an example -->

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
