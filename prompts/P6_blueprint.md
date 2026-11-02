# P6 — Generate master_site_blueprint.json
# Flash Engine | RUNS ONCE PER PROJECT — NEVER REPEAT
# Read master_brief.json AND topical_authority.json before running

## TASK
Generate the complete site blueprint. Every page in every phase gets a
full blueprint entry. This is the master architecture document.

Blog category hub pages must be included in the site architecture section.
Each `blog_categories` entry from topical_authority.json becomes a hub URL
(e.g., /blog/consumer-guides/) that category posts link back to.

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
  "blog_categories": [
    {
      "name": "",
      "slug": "",
      "url": "/blog/[category-slug]/",
      "description": "",
      "supporting_service": ""
    }
  ],
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
      "category": "(blog pages only — from topical_authority.json)",
      "category_slug": "(blog pages only — from topical_authority.json)",
      "sections": [],
      "word_count_target": 0,
      "status": "planned"
    }
  ],
  "site_architecture": {
    "homepage_links_to": [],
    "hub_pages": [],
    "location_hub": "",
    "blog_category_hubs": [
      "/blog/consumer-guides/",
      "/blog/air-quality-ducts/",
      "/blog/methods-equipment/",
      "/blog/dryer-vent-safety/"
    ]
  }
}

## SELF-CHECK before outputting
- [ ] Every page from topical_authority.json has a blueprint entry
- [ ] Each page has correct schema_types for its page_type
- [ ] internal_links_to only references page_ids in this same blueprint
- [ ] No duplicate slugs
- [ ] Every blog page carries the correct category and category_slug from topical_authority.json
- [ ] blog_category_hubs lists all category slugs from topical_authority.json blog_categories
- [ ] Output is valid JSON

## REMINDER
This prompt runs ONCE. Save the output immediately as master_site_blueprint.json.
Do NOT re-run this prompt for individual pages.
