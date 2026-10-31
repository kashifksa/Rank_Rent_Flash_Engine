# P2 — Market Intelligence Report
# Flash Engine | Output: JSON object saved to market_intelligence.json

## TASK
Research the market for the niche and city below. Output a structured JSON report.

## VARIABLES — fill before submitting
{PRIMARY_SERVICE} = [fill in]
{CITY} = [fill in]
{STATE} = [fill in]

## OUTPUT FORMAT
Output ONLY valid JSON. No markdown fences, no explanation.

{
  "niche": "{PRIMARY_SERVICE}",
  "city": "{CITY}",
  "state": "{STATE}",
  "market_size": "estimated local demand description",
  "seasonality": "peak and slow seasons",
  "avg_customer_value": "estimated job value range (no $ — write as text)",
  "common_pain_points": ["pain1", "pain2", "pain3"],
  "local_demand_signals": ["signal1", "signal2"],
  "top_keywords": ["kw1", "kw2", "kw3", "kw4", "kw5"],
  "local_challenges": "climate, regulatory, or geographic factors",
  "monetization_notes": "lead rental potential, estimated monthly value"
}

## SELF-CHECK before outputting
- [ ] Output is valid JSON (no trailing commas, all strings quoted)
- [ ] No pricing in dollar amounts — use text descriptions only
- [ ] All fields populated — no empty strings or null values
