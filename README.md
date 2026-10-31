# Rank & Rent Flash Engine

A **Gemini Flash 3.8 optimized** Rank & Rent SEO pipeline.

Runs the full pipeline — research, planning, content writing, images, and publishing — using only **Gemini Flash 3.8**. No Claude, no Gemini Pro required.

---

## How It Works

Classic Rank & Rent pipelines use one large prompt per page (600+ lines). Flash 3.8 struggles with large prompts — it drifts, misses rules, skips sections.

This engine solves that with three mechanisms:

| Mechanism | What it does |
|---|---|
| **Atomic mini-prompts** | One prompt per page section (50-80 lines each) |
| **Golden examples** | Real perfect-output examples embedded in every prompt |
| **Self-check blocks** | Flash validates its own output against a QA checklist before finalizing |

Result: Flash 3.8 produces the same structured, on-rules content as Gemini Pro or Claude Sonnet.

---

## Repo Structure

```
prompts/          8 planning prompts (P1-P6, P8) + atomic P7 section prompts
examples/         Golden output examples (generate with Claude/Pro before first run)
scripts/          All pipeline scripts including orchestrator.py
structure/        Page type structure files (SERVICE, LOCATION, BLOG, ABOUT)
```

---

## Related

- [`Rank_Rent_Starter_Kit`](https://github.com/kashifksa/Rank_Rent_Starter_Kit) — Universal template kit (Gemini Pro + Claude Sonnet edition)

---

## Requirements

- Gemini Flash 3.8 (via Antigravity or Google AI Studio)
- Python 3.10+
- WordPress with Easy MCP AI plugin
- Kadence theme

---

*All project variables (niche, city, NAP) flow from `data.txt` → `master_brief.json`. Nothing is hardcoded.*

