# P7 Service — Section 05: Process
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

## SECTION RULES — Process (Section 5 of 10)
Word budget: 80-120 words

H2: How Our {PRIMARY_SERVICE} Process Works in {CITY}

First sentence (answer-first rule): State how many steps and approximate total timeframe.

Then EXACTLY 3 steps in table format (preferred for AI extraction):

| Step | What Happens | Timeframe |
|------|--------------|-----------|
| **1. [Bold Title]** | 20-30 word description | [timeframe] |
| **2. [Bold Title]** | 20-30 word description | [timeframe] |
| **3. [Bold Title]** | 20-30 word description | [timeframe] |

Step 1: Initial contact / assessment
Step 2: On-site evaluation / proposal
Step 3: Work completed / follow-up

SECTION PARITY: All 3 step descriptions within ±2% word count.

SELF-CHECK before outputting:
- [ ] H2 matches exactly: "How Our {PRIMARY_SERVICE} Process Works in {CITY}"
- [ ] Answer-first opening sentence present
- [ ] Exactly 3 steps in table format
- [ ] All step descriptions within ±2% word count
- [ ] Total 80-120 words

## GOLDEN EXAMPLE
<!-- Golden example generated from: service_page_example.md -->
<!-- Section 05 — injected by inject_golden_examples.py -->

## How Our Air Duct Cleaning Process Works in Rockford

Our residential air duct cleaning follows a three-step process that typically takes two to four hours for an average Rockford home, from initial setup through final camera verification.

| Step | What Happens | Timeframe |
|------|--------------|-----------|
| **1. Pre-Cleaning Camera Inspection** | A flexible camera is inserted into your supply and return trunks to document existing conditions and identify any blockages, collapsed flex sections, or moisture damage before work begins. | 20-30 minutes |
| **2. Negative Air Source Removal** | Our NADCA-certified technicians connect a commercial-grade negative air machine to your main trunk line and systematically clean every supply and return branch using agitation tools and HEPA-filtered vacuum extraction. | 90-150 minutes |
| **3. Post-Cleaning Verification and Documentation** | A second camera pass confirms the full duct interior is clear. Registers are reinstalled, the system is tested at normal operation, and you receive a copy of before-and-after documentation. | 20-30 minutes |

## OUTPUT RULES
- Output ONLY the section content in Markdown
- Start directly with the content — no intro, no "Here is the section:" preamble
- No pricing, no em-dashes (—), no separator lines (---)
- Bold ONE key phrase per paragraph
