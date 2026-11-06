---
name: page-builder
description: Rank & Rent Studio Page Builder for visually customizing, styling, reordering, and exporting Kadence Gutenberg blocks and HTML pages with maximum design options.
---

# Rank & Rent Studio Page Builder Pro (v2)

This skill governs the visual customization, layout variation switching, section reordering, and block/HTML export for all pages in the Rank & Rent pipeline.

## When to Use This Skill
- When previewing, customizing, or editing any Phase page (`homepage`, `about`, `contact`, `location`, `service`, `blog`).
- When switching section layout templates (Split Form vs. Wide Banner vs. Emergency Alert; 3-Col Cards vs. Bento Grid vs. Horizontal Strips).
- When toggling between visual design archetypes (`Industrial`, `Emergency`, `Architectural`).
- When adjusting geometry (Corner Radius: Sharp, Clean, Round, Pill; Density: Compact, Balanced, Spacious).
- When reordering sections visually using Up/Down arrows.
- When live-editing text on the canvas (`contenteditable`).
- When inspecting or exporting clean Kadence WordPress Gutenberg blocks or standalone HTML for production deployment.

## Core Capabilities & Features

### 1. Launching the Visual Builder
Open [`studio_builder.html`](file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html) directly in any browser:
```powershell
Start-Process "D:\Projects\Rank_Rent_Flash_Engine\studio_builder.html"
```

### 2. Available Design Archetypes
- **Industrial Clean (Default):**
  - Primary: Deep Charcoal (`#121315`)
  - Accent: High-Vis Industrial Orange (`#fd761a`)
  - Typography: Montserrat (Headings) + Inter (Body)
  - Grounded 4px radius, technical inspection badges
- **Emergency 24/7:**
  - Primary: Deep Crimson (`#7f1d1d`)
  - Accent: Alert Red / Amber (`#dc2626` / `#f59e0b`)
  - Typography: Outfit (Headings) + Inter (Body)
  - Urgency dispatch banner, prominent click-to-call
- **Architectural Modern:**
  - Primary: Dark Slate (`#0f172a`)
  - Accent: Emerald Green (`#059669`)
  - Typography: Plus Jakarta Sans (Headings) + Inter (Body)
  - Minimalist airy spacing, refined 8px rounded corners

### 3. Section Template Variations (Borrowed from Modern UI Libraries)
- **Hero Section:**
  - `Split Form`: High-conversion lead generation form alongside copy and trust signals.
  - `Wide Banner`: Full-width visual presentation with prominent badges.
  - `Emergency Alert`: High-urgency alert strip for immediate dispatch services.
- **Services Grid:**
  - `3-Col Cards`: Clean 3-column elevated feature cards.
  - `Bento Grid`: 1 Large featured service card + 3 compact satellite cards.
  - `Horizontal Strips`: Full-width technical service strips.
- **Reviews & Social Proof:**
  - `Review Cards`: Standard 3-column customer review cards with star ratings.
  - `Before/After Proof`: Visual borescope inspection imagery paired with quote.
  - `Proof Wall`: Dense customer sentiment wall.

### 4. Interactive Component Toggles
- **Before/After View:** Draggable wipe slider vs. side-by-side cards.
- **Live Radar Beacons:** Pulsing real-time geographic radar markers.
- **Winner Ribbon:** Highlighted gold badge and accent border.
- **Process Conduit Track:** Animated glowing line connecting workflow steps.
- **Card Cursor Spotlight:** Dynamic radial gradient highlight tracking pointer.
- **Mobile Sticky Call Bar:** Fixed bottom call bar on mobile viewports.

### 5. Geometry & Density Tuner
- **Spacing Density:** `Compact` (tight padding), `Balanced` (standard), `Spacious` (airy luxury).
- **Corner Radius:** `Sharp (0px)`, `Clean (4px)`, `Round (8px)`, `Pill (999px)`.
- **Background Texture:** `Solid Clean`, `Subtle Blueprint Dots`, `Technical Grid`.

### 6. Section Reordering & In-Line Editing
- **Up / Down Reorder Arrows:** Reorder any section in the DOM in real-time.
- **Click-to-Edit (`contenteditable`):** Click on any headline or paragraph on the canvas to edit wording in-place.

### 7. Live Kadence Gutenberg Split-Code Drawer
- Click **`</> Kadence Code`** to open the real-time block code view.
- 1-click **"Copy Code"** formats blocks ready for WordPress `safe_publish()`.
