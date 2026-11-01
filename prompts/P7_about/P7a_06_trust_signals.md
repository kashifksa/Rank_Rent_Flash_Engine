# P7 About — Section 06: Trust Signals
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

## SECTION RULES — Trust Signals (Section 6 of 8)
Word budget: 120-180 words

H2: Why {CITY} Homeowners Trust {COMPANY_NAME}

Answer-first: First sentence states the most credible trust metric.

Write:
1. Stats bar — 3-4 concrete numbers (bold each stat number):
   - "**[Number]+** Local Projects Completed"
   - "**[X.X]★** Average Rating"
   - "**Serving {CITY} Since {FOUNDED_YEAR}**"
   - "[Response time or other stat]"

2. 2-3 customer review excerpts:
   > "[30-50 word quote naming {CITY} or a neighborhood]"
   > — [First name], [Neighborhood], {CITY}
   CSS text stars: ★★★★★ — never rendered images

3. Optional note: "[BEFORE/AFTER PHOTO with geo-tagged alt text]"

SELF-CHECK:
- [ ] H2 = "Why {CITY} Homeowners Trust {COMPANY_NAME}"
- [ ] Answer-first opening with most credible metric
- [ ] 3-4 stats, all bolded numbers
- [ ] 2-3 reviews, each names {CITY} or neighborhood
- [ ] CSS text stars used
- [ ] 120-180 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: about_page_example.md -->
<!-- Section 06 — injected by inject_golden_examples.py -->

## What Our Customers Say and What the Numbers Show

**4.9-star average rating** across 120+ verified Google reviews from Rockford-area homeowners.

> "I called three companies before choosing Rockford Air Duct Pros. They were the only ones who offered camera documentation before and after and did not pressure me with add-ons. **Everything was exactly as described.** Highly recommend."
> -- James H., Highland Park, Rockford
> *****

> "Our 1974 ranch had never had the ducts cleaned. I was nervous after reading horror stories about scam operations online. These guys showed me the camera footage before they started, explained every step, and were done in under three hours. **No surprises, no upsells.**"
> -- Patricia M., Rolling Green, Rockford
> *****

Our team has completed residential and commercial air duct cleaning projects throughout Rockford, Loves Park, Machesney Park, and surrounding Winnebago County communities since 2014. Before-and-after camera documentation is provided on every job.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
