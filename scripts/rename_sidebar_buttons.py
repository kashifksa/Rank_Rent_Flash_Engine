script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the buttons for Hero Section Design
old_hero_group = """        <!-- Hero Architecture Selector -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Hero Section Design</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">PROFLOW ADDED</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill active" id="hero-var-split" onclick="setSectionVariant('hero', 'split')">Hostinger V-Split</button>
            <button class="variation-pill" id="hero-var-denton" onclick="setSectionVariant('hero', 'denton')">Denton ProFlow Full-Bleed</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            Enforced symmetrically across Home, Services &amp; Location pages.
          </div>
        </div>"""

new_hero_group = """        <!-- Hero Architecture Selector -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Hero Section Design</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="hero-var-split" onclick="setSectionVariant('hero', 'split')">Kadence Split</button>
            <button class="variation-pill active" id="hero-var-denton" onclick="setSectionVariant('hero', 'denton')">Cornerstone</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            Enforced symmetrically across Home, Services &amp; Location pages.
          </div>
        </div>"""

# Replace Section 2 Problem / Diagnostic
old_sec2_group = """        <!-- Section 2: Problem / Diagnostic Section Variant -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Section 2: Problem / Diagnostic</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">PROFLOW ADDED</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="intro-var-callout" onclick="setSectionVariant('intro', 'callout')">Standard Callout Row</button>
            <button class="variation-pill active" id="intro-var-denton" onclick="setSectionVariant('intro', 'denton')">Denton ProFlow Diagnostic</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            2-column diagnostic proof card + docked 4-pillar trust badge ribbon.
          </div>
        </div>"""

new_sec2_group = """        <!-- Section 2: Problem / Diagnostic Section Variant -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Section 2: Problem / Diagnostic</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="intro-var-callout" onclick="setSectionVariant('intro', 'callout')">Kadence Callout</button>
            <button class="variation-pill active" id="intro-var-denton" onclick="setSectionVariant('intro', 'denton')">Cornerstone</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            2-column diagnostic proof card + docked 4-pillar trust badge ribbon.
          </div>
        </div>"""

if old_hero_group in content:
    content = content.replace(old_hero_group, new_hero_group)
    print("Replaced Hero Architecture Selector successfully.")
else:
    print("Warning: old_hero_group not found!")

if old_sec2_group in content:
    content = content.replace(old_sec2_group, new_sec2_group)
    print("Replaced Section 2 Selector successfully.")
else:
    print("Warning: old_sec2_group not found!")

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated generate_studio_builder_v4.py saved.")

