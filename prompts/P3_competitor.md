# P3 — Competitor Intelligence Report
# Flash Engine | Output: JSON object saved to competitor_intelligence.json

## TASK
Analyze the top local competitors for the niche and city below.
Output a structured JSON report.

## VARIABLES — fill before submitting
{PRIMARY_SERVICE} = [fill in]
{CITY} = [fill in]
{STATE} = [fill in]

## OUTPUT FORMAT
Output ONLY valid JSON. No markdown fences, no explanation.

{
  "niche": "{PRIMARY_SERVICE}",
  "city": "{CITY}",
  "competitors": [
    {
      "rank": 1,
      "name": "competitor name",
      "url": "domain.com",
      "strengths": ["strength1", "strength2"],
      "weaknesses": ["weakness1", "weakness2"],
      "content_gaps": ["topic not covered 1", "topic not covered 2"]
    }
  ],
  "serp_overview": "description of what dominates the SERP",
  "ranking_difficulty": "low | medium | high",
  "quick_win_keywords": ["kw1", "kw2", "kw3"],
  "differentiation_angles": ["angle1", "angle2", "angle3"]
}

## SELF-CHECK before outputting
- [ ] At least 3 competitors listed
- [ ] content_gaps filled for each competitor — these drive the content plan
- [ ] Output is valid JSON
