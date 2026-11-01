# P7 Location — Section 05: Local FAQ (MUST BE 100% UNIQUE)
# Flash Engine — Location Page | Atomic Mini-Prompt
# Model: Gemini Flash 3.8
# Write ONLY this section. Nothing else.

## VARIABLES — fill ALL before submitting
PRIMARY_SERVICE  = [fill in]
LOCATION_CITY    = [fill in — the TARGET city for this page]
HUB_CITY         = [fill in — your main operating city]
STATE            = [fill in]
PHONE            = [fill in]
LOCAL_LANDMARKS  = [fill in — real verifiable landmarks in LOCATION_CITY]
LOCAL_CLIMATE    = [fill in — climate/geographic factor relevant to service]
LOCAL_PERMIT     = [fill in — any permit note for LOCATION_CITY, or leave blank]
LOCAL_NEIGHBORHOODS = [fill in — neighborhoods/zips in LOCATION_CITY]

## SECTION RULES — Local FAQ (Section 5 of 7)
Word budget: 150-280 words
THIS SECTION MUST BE 100% UNIQUE — questions must be specific to {LOCATION_CITY}

H2: {PRIMARY_SERVICE} FAQs for {LOCATION_CITY} Homeowners

Write 3-5 questions UNIQUE to {LOCATION_CITY}. Format as natural language questions.

REQUIRED question types (must include all three):
1. PERMIT: "Does {LOCATION_CITY} require a permit for {PRIMARY_SERVICE}?"
   Answer: use {LOCAL_PERMIT} if set, otherwise give general guidance.
2. RESPONSE TIME: "How quickly can you reach [Neighborhood] in {LOCATION_CITY}?"
3. LOCAL CONDITION: "How does {LOCAL_CLIMATE} affect {PRIMARY_SERVICE} in {LOCATION_CITY}?"

Per answer: open with direct 1-sentence reply, then elaborate. 40-70 words each.

Do NOT reuse questions from:
- The hub service page FAQ
- Any other location page FAQ

SELF-CHECK:
- [ ] H2 = "{PRIMARY_SERVICE} FAQs for {LOCATION_CITY} Homeowners"
- [ ] 3-5 questions, all unique to {LOCATION_CITY}
- [ ] All 3 required question types present
- [ ] Each answer opens with direct reply
- [ ] 150-280 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: location_page_example.md -->
<!-- Section 05 — injected by inject_golden_examples.py -->

## Air Duct Cleaning FAQs for Loves Park Homeowners

### Does Loves Park require a permit for air duct cleaning?

No permit is required in Loves Park for residential air duct cleaning. **Air duct cleaning is a maintenance service**, not a mechanical installation, and it does not require municipal permit approval under Loves Park city ordinances or Winnebago County building codes. Permit requirements apply only to new mechanical system installation or substantial duct modifications, not to cleaning existing ductwork.

### How quickly can you reach homes in the Machesney Park Road and Colonial Village areas of Loves Park?

**Our Rockford-based team typically reaches Loves Park addresses within 30 to 45 minutes** of dispatch. The Machesney Park Road corridor and Colonial Village neighborhood are within our standard service radius. We schedule Loves Park appointments Monday through Saturday and can often accommodate same-week bookings for non-emergency residential cleaning.

### How does the Rock River valley humidity affect air ducts in Loves Park homes?

The **Rock River valley creates above-average seasonal humidity variations** that promote condensation inside basement plenum sections, particularly in Loves Park homes where HVAC systems were not rebalanced after window replacement or insulation upgrades. Moisture-laden air entering return ducts accelerates debris adhesion to duct walls and increases the risk of mold colonization in plenum boxes. Annual or biennial inspections are recommended for Loves Park homes with finished basements and original duct layouts.

### Do you service both the Loves Park and Machesney Park sides of the area?

Yes. **We serve both Loves Park and adjacent Machesney Park** as part of our standard service area. Both communities fall within our primary Winnebago County coverage zone. There is no additional travel charge for either municipality.

### What is the best time of year to schedule air duct cleaning in Loves Park?

**Late summer or early fall is the optimal window** for duct cleaning in Loves Park, before the heating season begins and forced-air systems switch to continuous furnace operation. Scheduling before October allows the cleaning to be completed before the heavy demand period and ensures your system is delivering clean air from the first cold day of the season.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
