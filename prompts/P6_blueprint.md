# P6 — Generate master_site_blueprint.json
# Flash Engine | RUNS ONCE PER PROJECT — NEVER REPEAT
# Read master_brief.json AND topical_authority.json before running

## TASK
Generate the complete site blueprint. Every page in every phase gets a
full blueprint entry. This is the master architecture document.

## INPUTS REQUIRED
=== MASTER_BRIEF.JSON ===
[paste here]

=== TOPICAL_AUTHORITY.JSON ===
[paste here]

## OUTPUT FORMAT
Output ONLY valid JSON. No markdown fences.

{
  "site_name": "",
  "domain": "",
  "pages": [
    {
      "page_id": "",
      "page_type": "",
      "phase": 1,
      "slug": "",
      "h1": "",
      "meta_title": "",
      "meta_description": "",
      "target_keyword": "",
      "secondary_keywords": [],
      "schema_types": [],
      "internal_links_to": [],
      "sections": [],
      "word_count_target": 0,
      "status": "planned"
    }
  ],
  "site_architecture": {
    "homepage_links_to": [],
    "hub_pages": [],
    "location_hub": ""
  }
}

## SELF-CHECK before outputting
- [ ] Every page from topical_authority.json has a blueprint entry
- [ ] Each page has correct schema_types for its page_type
- [ ] internal_links_to only references page_ids in this same blueprint
- [ ] No duplicate slugs
- [ ] Output is valid JSON

## REMINDER
This prompt runs ONCE. Save the output immediately as master_site_blueprint.json.
Do NOT re-run this prompt for individual pages.
