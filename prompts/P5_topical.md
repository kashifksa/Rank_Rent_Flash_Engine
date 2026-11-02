# P5 — Generate topical_authority.json
# Flash Engine | Output: topical_authority.json
# Read master_brief.json before running this prompt

## TASK
Using master_brief.json, generate the complete topical authority publishing roadmap.
This file defines every page to be built, in priority order, AND the blog category taxonomy.

## INPUT REQUIRED
Paste before submitting:
=== MASTER_BRIEF.JSON ===
[paste full master_brief.json here]

## RULES

### Phase Architecture
- Phase 1: homepage + primary service page + about + contact + primary city location page
- Phase 2: secondary service pages
- Phase 3: expansion city location pages (one per expansion_cities entry)
- Phase 4: high-volume problem & decision guides (how often, signs of, what is, cost factors — no pricing)
- Phase 5: informational blog posts (strictly informational — how to, signs of, guide to, what is, when to, why does)

### Blog Post Rules
- Blog post keywords MUST NOT overlap with any service or location page keyword
- No two blog posts may share the same intent angle
- All blog keywords must be informational intent — never transactional

### Blog Category Rules — REQUIRED
Every blog post (phase 4 and 5) MUST be assigned to one of the blog categories defined in `blog_categories`.
Assign each blog post a `"category"` (category name) and `"category_slug"` (URL-safe slug).
Blog categories must map to their supporting money service page.
Define 3–5 topic-cluster categories based on the services in master_brief.json.

## OUTPUT FORMAT
Output ONLY valid JSON. No markdown fences, no explanation.

{
  "blog_categories": [
    {
      "name": "Category Name",
      "slug": "category-slug",
      "description": "One sentence describing what posts in this category cover.",
      "supporting_service": "page_id of the service page this silo supports"
    }
  ],
  "pages": [
    {
      "page_id": "unique-slug",
      "page_type": "service | location | blog | about | contact | homepage",
      "phase": 1,
      "priority": 1,
      "target_keyword": "",
      "h1_title": "",
      "parent_service": "",
      "city": "",
      "category": "Category Name (blog pages only — omit for service/location pages)",
      "category_slug": "category-slug (blog pages only — omit for service/location pages)",
      "status": "planned"
    }
  ]
}

## SELF-CHECK before outputting
- [ ] Phase 1 contains: homepage, primary service, about, contact, primary location
- [ ] All blog post keywords are informational intent (how to / signs of / guide to)
- [ ] No blog keyword overlaps with any service or location page keyword
- [ ] Every blog post has both "category" and "category_slug" fields populated
- [ ] blog_categories array has 3–5 entries, each with supporting_service pointing to a real page_id
- [ ] Output is valid JSON
