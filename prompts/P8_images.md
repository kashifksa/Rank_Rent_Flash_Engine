# P8 — Generate Image Plan
# Flash Engine | Runs once per page after content is approved

## TASK
Generate the image plan for the page below.
Output image_plan_[slug].json.

## VARIABLES — fill before submitting
PAGE_ID = [fill in — from topical_authority.json]
PAGE_TYPE = [service | location | blog | about]
{PRIMARY_SERVICE} = [fill in]
{CITY} = [fill in]

## INPUT REQUIRED
=== PAGE_CONTENT_[SLUG].MD ===
[paste the approved page content here]

## RULES
- Max 13-15 images per session (quota limit)
- NO AI-generated map images — use Google Maps iframe instead
- NO 3D rendered star images — use CSS text stars
- Image filenames: lowercase words only, NO digits, hyphens between words
  GOOD: roof-repair-austin-hero.webp
  BAD:  roof_repair_1.webp | roofRepairAustin2.jpg
- Alt text must include local identifier: "[action] in [neighborhood], {CITY}, {STATE}"
- Priority order: hero image first, then section images, then supporting

## OUTPUT FORMAT
Output ONLY valid JSON.

{
  "page_id": "",
  "slug": "",
  "images": [
    {
      "slot": "section-name",
      "filename": "descriptive-words-city.webp",
      "alt_text": "descriptive alt with city and neighborhood",
      "prompt": "detailed AI generation prompt for this image",
      "priority": 1,
      "wp_media_id": null
    }
  ]
}

## SELF-CHECK before outputting
- [ ] No digits in any filename
- [ ] Every alt_text contains {CITY} or a neighborhood name
- [ ] No map images in the list (use iframe note instead)
- [ ] Total images <= 15
- [ ] Output is valid JSON
