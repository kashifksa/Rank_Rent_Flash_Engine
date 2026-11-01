# P7 Location — Section 02: Localized Intro (MUST BE 100% UNIQUE)
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

## SECTION RULES — Localized Intro (Section 2 of 7)
Word budget: 120-180 words
THIS SECTION MUST BE 100% UNIQUE — never copy from hub page or other location pages

H2: {PRIMARY_SERVICE} Services for {LOCATION_CITY} Residents

Answer-first: First sentence states what makes {LOCATION_CITY}'s situation distinct.

Write 2-3 paragraphs (2-3 sentences each, short format):

Paragraph 1: Local hook — reference a REAL, VERIFIABLE landmark or district
  of {LOCATION_CITY} from {LOCAL_LANDMARKS}.
  Example: "Whether your home is near [landmark] or one of {LOCATION_CITY}'s
  newer communities..."
  Bold the landmark name.

Paragraph 2: Connect {LOCAL_CLIMATE} to why the service matters here.
  If {LOCAL_PERMIT} is set — mention the local permit context.

Paragraph 3: Brief brand intro as a local provider for {LOCATION_CITY}.

SELF-CHECK:
- [ ] H2 = "{PRIMARY_SERVICE} Services for {LOCATION_CITY} Residents"
- [ ] Real landmark from {LOCAL_LANDMARKS} referenced + bolded
- [ ] {LOCAL_CLIMATE} mentioned
- [ ] Zero copy-paste from any other page
- [ ] 120-180 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: location_page_example.md -->
<!-- Section 02 — injected by inject_golden_examples.py -->

## Air Duct Cleaning Services for Loves Park Residents

**Loves Park's residential neighborhoods** stretch along the north bank of the Rock River from the Harlem High School corridor west toward the Perryville Road commercial strip, and most of the housing stock in that corridor was built between 1955 and 1982. That era of construction used galvanized sheet metal supply and return trunks that were never designed to be cleaned, and in most homes, they have not been.

The Rock River valley geography creates humidity swings that promote interior duct condensation and mold risk in basement plenum sections, especially in homes where original single-pane windows were replaced with insulated glass without upgrading the HVAC airflow balance. **Unbalanced duct systems in high-humidity basements** accumulate moisture-laden debris at a faster rate than homes on drier ground.

Rockford Air Duct Pros has served the Loves Park area since 2014, scheduling appointments in this community regularly and maintaining short response times without the per-mile surcharges that out-of-area contractors add to Loves Park estimates.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
- Short paragraphs: 2-3 sentences max
