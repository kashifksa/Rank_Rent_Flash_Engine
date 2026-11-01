# P7 Service — Section 03: Services Grid
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

## SECTION RULES — Services Grid (Section 3 of 10)
Word budget: 250-350 words total (3-6 cards)

Write in this order:

H2: Our {CITY} {PRIMARY_SERVICE} Solutions

Then one card per sub-service (3-6 cards from master_brief sub_services list):

### [Sub-service Name]
[40-60 word description of this sub-service]
- What it covers
- Who it helps
- Why {CITY} residents need it
Bold the key term in each card description.

SECTION PARITY RULE: All card descriptions must be within ±2% word count of each other.
Count words in first card, match all others to within ±2%.

No pricing. No "starting at" language.

SELF-CHECK before outputting:
- [ ] H2 matches exactly: "Our {CITY} {PRIMARY_SERVICE} Solutions"
- [ ] 3-6 cards written
- [ ] All card descriptions within ±2% word count of each other
- [ ] One bolded key term per card
- [ ] No pricing

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 03 — injected by inject_golden_examples.py -->

## Our Rockford Air Duct Cleaning Solutions

Every Rockford home has a unique duct system. We offer a complete range of air duct cleaning services sized to residential properties throughout Winnebago County.

### Supply and Return Register Cleaning

**Supply and return registers** are the primary entry and exit points for conditioned air in your home. Our technicians remove each register, vacuum the boot, and clean the inner duct wall within reach before reinstalling. This step alone eliminates the visible dust and debris that recirculates each time your furnace or AC cycles on. Homeowners in Rockford's older neighborhoods notice a measurable reduction in surface dust within days.

### Air Handler and Plenum Cleaning

The **air handler and plenum** are the central collection chambers where return air consolidates before reaching your furnace filter. In Rockford homes built before 1985, these chambers frequently contain decades of compacted fibrous material that standard filter replacement never addresses. Our technicians access and vacuum the plenum interior, the blower compartment, and the evaporator coil housing as part of this service.

### Negative Air Vacuum Trunk Line Cleaning

**Trunk line cleaning** uses a commercial-grade negative air pressure machine connected directly to your main supply trunk to pull contaminants toward the vacuum rather than pushing them through your living space. This method meets the NADCA ACR 2013 standard for source removal. It is the only technique that consistently cleans the full length of galvanized sheet metal trunks common in Rockford's mid-century housing stock.

### Dryer Vent Cleaning and Lint Removal

**Dryer vent lint accumulation** is the leading cause of residential dryer fires according to the U.S. Fire Administration. Our technicians use a rotary brush system to clear lint from the full length of the vent run, including any elbows or offsets. This service is especially important in Rockford homes where original dryer vent runs exceed 15 feet or include more than two 90-degree bends.

### Video Camera Ductwork Inspection

A **before-and-after camera inspection** is included with every duct cleaning appointment. Our technicians insert a flexible camera into your supply and return trunks to document conditions prior to cleaning and again after completion. This footage is your proof of work and your assurance that the cleaning reached the full duct interior, not just the registers you can see.

### Sanitization and Antimicrobial Fogging

**Antimicrobial fogging** applies an EPA-registered sanitizing agent to the interior duct surfaces after the mechanical cleaning is complete. This step reduces mold spores, bacteria, and odor-causing residue that physical vacuuming alone cannot eliminate. It is recommended for Rockford homes with confirmed moisture intrusion, post-flood remediation, or occupants with documented respiratory sensitivities.

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
