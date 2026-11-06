import os
import json

base_dir = r"D:\Projects\Rank_Rent_Flash_Engine"
data_js_path = os.path.join(base_dir, "scripts", "builder_data.js")
builder_data_js = open(data_js_path, encoding="utf-8").read() if os.path.exists(data_js_path) else "window.BUILDER_PAGES_DATA = {};"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rank & Rent Studio Page Builder v2 — Pro Visual Editor</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Montserrat:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@600;700;800&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  
  <style>
    /* ==========================================================================
       APP CHASSIS & PRO LAYOUT (DARK THEME IDE)
       ========================================================================== */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --app-bg: #0b0d14;
      --app-sidebar-bg: #121520;
      --app-panel-bg: #181c2b;
      --app-border: #23293f;
      --app-text: #e2e8f0;
      --app-text-muted: #8492a6;
      --app-accent: #3b82f6;
      --app-accent-hover: #2563eb;
      --app-header-h: 56px;
      --app-sidebar-w: 380px;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--app-bg);
      color: var(--app-text);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }

    /* Top Navigation Toolbar */
    .app-header {
      height: var(--app-header-h);
      background: var(--app-sidebar-bg);
      border-bottom: 1px solid var(--app-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 100;
      flex-shrink: 0;
    }

    .app-branding {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .app-logo {
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, #3b82f6, #ec4899);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: 16px;
      color: white;
      box-shadow: 0 2px 10px rgba(59, 130, 246, 0.4);
    }

    .app-title-group h1 {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .app-badge {
      font-size: 10px;
      background: rgba(59, 130, 246, 0.15);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.3);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }

    /* Viewport Selector */
    .viewport-controls {
      display: flex;
      align-items: center;
      background: var(--app-bg);
      border: 1px solid var(--app-border);
      border-radius: 8px;
      padding: 3px;
      gap: 4px;
    }

    .viewport-btn {
      background: none;
      border: none;
      color: var(--app-text-muted);
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }

    .viewport-btn:hover { color: #fff; }
    .viewport-btn.active {
      background: var(--app-panel-bg);
      color: #fff;
      box-shadow: 0 1px 4px rgba(0,0,0,0.5);
    }

    /* Header Actions */
    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .action-btn {
      padding: 7px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      border: none;
      transition: all 0.15s ease;
    }

    .action-btn.secondary {
      background: var(--app-panel-bg);
      color: #cbd5e1;
      border: 1px solid var(--app-border);
    }

    .action-btn.secondary:hover {
      background: #23293f;
      color: #fff;
    }

    .action-btn.primary {
      background: #2563eb;
      color: #fff;
    }

    .action-btn.primary:hover {
      background: #1d4ed8;
      box-shadow: 0 2px 10px rgba(37, 99, 235, 0.4);
    }

    .action-btn.code-toggle {
      background: #1e1b4b;
      color: #a5b4fc;
      border: 1px solid #3730a3;
    }

    .action-btn.code-toggle:hover {
      background: #312e81;
      color: #fff;
    }

    /* Main Workspace Layout */
    .app-workspace {
      display: flex;
      flex: 1;
      height: calc(100vh - var(--app-header-h));
      overflow: hidden;
      position: relative;
    }

    /* Sidebar Customizer */
    .app-sidebar {
      width: var(--app-sidebar-w);
      background: var(--app-sidebar-bg);
      border-right: 1px solid var(--app-border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      overflow-y: auto;
    }

    .sidebar-section {
      padding: 16px;
      border-bottom: 1px solid var(--app-border);
    }

    .sidebar-section-title {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #94a3b8;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .form-group {
      margin-bottom: 12px;
    }
    .form-group:last-child { margin-bottom: 0; }

    .form-label {
      display: block;
      font-size: 12px;
      font-weight: 600;
      color: #cbd5e1;
      margin-bottom: 6px;
    }

    .form-select, .form-input {
      width: 100%;
      background: #0b0d14;
      border: 1px solid var(--app-border);
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 12px;
      color: #e2e8f0;
      outline: none;
      transition: border-color 0.15s;
    }
    .form-select:focus, .form-input:focus { border-color: var(--app-accent); }

    /* Archetype Switcher Grid */
    .archetype-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .archetype-card {
      background: #0b0d14;
      border: 1px solid var(--app-border);
      border-radius: 6px;
      padding: 10px 4px;
      text-align: center;
      cursor: pointer;
      transition: all 0.15s;
    }
    .archetype-card:hover { border-color: #475569; }
    .archetype-card.active {
      border-color: var(--app-accent);
      background: rgba(59, 130, 246, 0.12);
    }

    .archetype-icon { font-size: 18px; margin-bottom: 4px; }
    .archetype-name { font-size: 11px; font-weight: 700; color: #fff; }

    /* Template Variation Selector Tabs */
    .variation-pill-group {
      display: flex;
      background: #0b0d14;
      border: 1px solid var(--app-border);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
      margin-bottom: 8px;
    }

    .variation-pill {
      flex: 1;
      border: none;
      background: none;
      color: var(--app-text-muted);
      font-size: 11px;
      font-weight: 600;
      padding: 5px 4px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s;
      text-align: center;
    }
    .variation-pill:hover { color: #fff; }
    .variation-pill.active {
      background: var(--app-panel-bg);
      color: #60a5fa;
      box-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }

    /* Switch Toggles */
    .toggle-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 7px 0;
      border-bottom: 1px solid rgba(255,255,255,0.04);
    }
    .toggle-row:last-child { border-bottom: none; }

    .toggle-label {
      font-size: 12px;
      color: #cbd5e1;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 36px;
      height: 20px;
    }

    .toggle-switch input { opacity: 0; width: 0; height: 0; }
    .toggle-slider {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: #334155;
      transition: .2s;
      border-radius: 20px;
    }
    .toggle-slider:before {
      position: absolute;
      content: "";
      height: 14px;
      width: 14px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .2s;
      border-radius: 50%;
    }
    input:checked + .toggle-slider { background-color: var(--app-accent); }
    input:checked + .toggle-slider:before { transform: translateX(16px); }

    /* Section Reorder / Visibility Manager */
    .section-pill-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .section-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #0b0d14;
      border: 1px solid var(--app-border);
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }

    .section-item-left {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .reorder-btns {
      display: flex;
      align-items: center;
      gap: 2px;
    }

    .reorder-btn {
      background: #1a1e2e;
      border: 1px solid var(--app-border);
      color: #94a3b8;
      font-size: 10px;
      width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      cursor: pointer;
    }
    .reorder-btn:hover { color: #fff; background: #262c42; }

    /* Canvas Area */
    .app-canvas-container {
      flex: 1;
      background: #07080c;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 24px;
      overflow-y: auto;
      position: relative;
    }

    .app-viewport-frame {
      background: #ffffff;
      border-radius: 8px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.6);
      transition: width 0.3s ease;
      width: 100%;
      max-width: 1280px;
      min-height: 800px;
      color: #1a1c1d;
      position: relative;
    }

    .app-viewport-frame.mobile {
      max-width: 375px;
      border: 12px solid #1e2230;
      border-radius: 40px;
      overflow: hidden;
      box-shadow: 0 25px 70px rgba(0,0,0,0.9);
    }
    .app-viewport-frame.tablet { max-width: 768px; }
    .app-viewport-frame.laptop { max-width: 1024px; }

    /* Live Editable Highlight */
    [contenteditable="true"]:hover {
      outline: 2px dashed #3b82f6 !important;
      outline-offset: 4px;
      cursor: text;
    }
    [contenteditable="true"]:focus {
      outline: 2px solid #2563eb !important;
      outline-offset: 4px;
      background: rgba(59, 130, 246, 0.05);
    }

    /* Live Kadence Split-Code Drawer */
    .code-drawer {
      position: absolute;
      top: 0;
      right: -550px;
      width: 540px;
      height: 100%;
      background: #0f111a;
      border-left: 1px solid var(--app-border);
      box-shadow: -10px 0 30px rgba(0,0,0,0.7);
      transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
      z-index: 90;
    }

    .code-drawer.open { right: 0; }

    .code-drawer-header {
      padding: 12px 16px;
      background: #141724;
      border-bottom: 1px solid var(--app-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .code-drawer-title {
      font-size: 12px;
      font-weight: 700;
      color: #cbd5e1;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .code-view-pre {
      flex: 1;
      overflow: auto;
      padding: 16px;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 11px;
      line-height: 1.5;
      color: #93c5fd;
      background: #08090f;
      white-space: pre-wrap;
      word-break: break-all;
    }

    /* Texture Patterns */
    .texture-dots {
      background-image: radial-gradient(rgba(0,0,0,0.06) 1px, transparent 1px) !important;
      background-size: 16px 16px !important;
    }
    .texture-grid {
      background-image: linear-gradient(to right, rgba(0,0,0,0.04) 1px, transparent 1px), linear-gradient(to bottom, rgba(0,0,0,0.04) 1px, transparent 1px) !important;
      background-size: 24px 24px !important;
    }
  </style>

  <style id="theme-overrides"></style>
</head>
<body>

  <!-- Top App Navigation -->
  <header class="app-header">
    <div class="app-branding">
      <div class="app-logo">⚡</div>
      <div class="app-title-group">
        <h1>Rank & Rent Studio Builder <span class="app-badge">Pro v2</span></h1>
      </div>
    </div>

    <!-- Viewport Switcher -->
    <div class="viewport-controls">
      <button class="viewport-btn active" onclick="setViewport('desktop', this)">🖥️ Desktop</button>
      <button class="viewport-btn" onclick="setViewport('laptop', this)">💻 Laptop</button>
      <button class="viewport-btn" onclick="setViewport('tablet', this)">📱 Tablet</button>
      <button class="viewport-btn" onclick="setViewport('mobile', this)">📲 Mobile</button>
    </div>

    <!-- Header Actions -->
    <div class="header-actions">
      <button class="action-btn code-toggle" onclick="toggleCodeDrawer()"><code>&lt;/&gt;</code> Kadence Code</button>
      <button class="action-btn secondary" onclick="exportKadenceBlocks()">📋 Copy Blocks</button>
      <button class="action-btn primary" onclick="exportFullHTML()">📥 Export HTML</button>
    </div>
  </header>

  <!-- Main Workspace -->
  <div class="app-workspace">
    
    <!-- Sidebar Control Panel -->
    <aside class="app-sidebar">
      
      <!-- 1. Page Selector -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Active Blueprint Page</div>
        <div class="form-group">
          <select id="page-select" class="form-select" onchange="loadSelectedPage(this.value)">
            <option value="homepage">🏠 Homepage (Residential Hub)</option>
            <option value="about">ℹ️ About Us (E-E-A-T & Credentials)</option>
            <option value="contact">📞 Contact Us (Dispatch & Form)</option>
            <option value="air-duct-cleaning-loves-park-il">📍 Loves Park Location Page</option>
            <option value="commercial-hvac-duct-cleaning">🏢 Commercial HVAC Duct Cleaning</option>
            <option value="dryer-vent-cleaning-and-lint-removal">🌀 Dryer Vent Cleaning & Lint Removal</option>
          </select>
        </div>
        <div id="page-meta-badge" style="font-size: 11px; color: #94a3b8; background: #0b0d14; padding: 6px 8px; border-radius: 4px; border: 1px solid var(--app-border);">
          Target: <strong id="meta-kw" style="color: #60a5fa;">air duct cleaning rockford</strong>
        </div>
      </div>

      <!-- 2. Design Archetype (1-Click DNA) -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Design Archetype (1-Click DNA)</div>
        <div class="archetype-grid">
          <div class="archetype-card active" id="arch-industrial" onclick="setArchetype('industrial')">
            <div class="archetype-icon">🏗️</div>
            <div class="archetype-name">Industrial</div>
          </div>
          <div class="archetype-card" id="arch-emergency" onclick="setArchetype('emergency')">
            <div class="archetype-icon">🚨</div>
            <div class="archetype-name">Emergency</div>
          </div>
          <div class="archetype-card" id="arch-architectural" onclick="setArchetype('architectural')">
            <div class="archetype-icon">🏛️</div>
            <div class="archetype-name">Architectural</div>
          </div>
        </div>
      </div>

      <!-- 3. Section Variation Templates (Borrowed from Tailblocks & Shuffle) -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Layout Template Variants</div>
        
        <div class="form-group">
          <label class="form-label">Hero Section Template:</label>
          <div class="variation-pill-group">
            <button class="variation-pill active" id="hero-var-split" onclick="setSectionVariant('hero', 'split')">Split Form</button>
            <button class="variation-pill" id="hero-var-banner" onclick="setSectionVariant('hero', 'banner')">Wide Banner</button>
            <button class="variation-pill" id="hero-var-alert" onclick="setSectionVariant('hero', 'alert')">Emergency</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Services Grid Template:</label>
          <div class="variation-pill-group">
            <button class="variation-pill active" id="services-var-grid" onclick="setSectionVariant('services', 'grid')">3-Col Cards</button>
            <button class="variation-pill" id="services-var-bento" onclick="setSectionVariant('services', 'bento')">Bento Grid</button>
            <button class="variation-pill" id="services-var-strips" onclick="setSectionVariant('services', 'strips')">H-Strips</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Social Proof / Reviews Template:</label>
          <div class="variation-pill-group">
            <button class="variation-pill active" id="reviews-var-cards" onclick="setSectionVariant('reviews', 'cards')">Review Cards</button>
            <button class="variation-pill" id="reviews-var-split" onclick="setSectionVariant('reviews', 'split')">Before/After</button>
            <button class="variation-pill" id="reviews-var-wall" onclick="setSectionVariant('reviews', 'wall')">Proof Wall</button>
          </div>
        </div>
      </div>

      <!-- 4. Interactive Feature Controls -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Component Feature Controls</div>
        
        <div class="toggle-row">
          <span class="toggle-label">Before/After View Mode</span>
          <div style="display: flex; gap: 4px;">
            <button id="ba-cards-btn" class="action-btn secondary" style="padding: 3px 8px; font-size: 10px;" onclick="setBaMode('cards')">Cards</button>
            <button id="ba-slider-btn" class="action-btn secondary" style="padding: 3px 8px; font-size: 10px;" onclick="setBaMode('slider')">Slider</button>
          </div>
        </div>

        <div class="toggle-row">
          <span class="toggle-label">Live Radar Beacons</span>
          <label class="toggle-switch">
            <input type="checkbox" id="toggle-radar" onchange="toggleFeature('radar', this.checked)">
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row">
          <span class="toggle-label">Winner Ribbon & Border</span>
          <label class="toggle-switch">
            <input type="checkbox" id="toggle-winner" checked onchange="toggleFeature('winner', this.checked)">
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row">
          <span class="toggle-label">Process Conduit Track</span>
          <label class="toggle-switch">
            <input type="checkbox" id="toggle-conduit" onchange="toggleFeature('conduit', this.checked)">
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row">
          <span class="toggle-label">Card Cursor Spotlight</span>
          <label class="toggle-switch">
            <input type="checkbox" id="toggle-spotlight" checked onchange="toggleFeature('spotlight', this.checked)">
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="toggle-row">
          <span class="toggle-label">Mobile Sticky Call Bar</span>
          <label class="toggle-switch">
            <input type="checkbox" id="toggle-mobile-bar" checked onchange="toggleFeature('mobileBar', this.checked)">
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>

      <!-- 5. Spacing, Geometry & Palette Inspector -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Design Engine & Geometry</div>
        
        <div class="form-group">
          <label class="form-label">Density / Section Padding:</label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="spacing-compact" onclick="setSpacing('compact')">Compact</button>
            <button class="variation-pill active" id="spacing-balanced" onclick="setSpacing('balanced')">Balanced</button>
            <button class="variation-pill" id="spacing-spacious" onclick="setSpacing('spacious')">Spacious</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Corner Radius:</label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="radius-sharp" onclick="setCornerRadius('0px')">Sharp (0)</button>
            <button class="variation-pill active" id="radius-clean" onclick="setCornerRadius('4px')">Clean (4)</button>
            <button class="variation-pill" id="radius-round" onclick="setCornerRadius('8px')">Round (8)</button>
            <button class="variation-pill" id="radius-pill" onclick="setCornerRadius('999px')">Pill</button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Background Texture:</label>
          <div class="variation-pill-group">
            <button class="variation-pill active" id="texture-solid" onclick="setTexture('solid')">Solid</button>
            <button class="variation-pill" id="texture-dots" onclick="setTexture('dots')">Dots</button>
            <button class="variation-pill" id="texture-grid" onclick="setTexture('grid')">Blueprint</button>
          </div>
        </div>

        <div class="form-group" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <div>
            <label class="form-label">Primary Color:</label>
            <input type="color" id="primary-color-picker" value="#121315" style="width: 100%; height: 32px; border: none; border-radius: 4px; cursor: pointer; background: none;" onchange="updateCustomColors()">
          </div>
          <div>
            <label class="form-label">Accent Color:</label>
            <input type="color" id="accent-color-picker" value="#fd761a" style="width: 100%; height: 32px; border: none; border-radius: 4px; cursor: pointer; background: none;" onchange="updateCustomColors()">
          </div>
        </div>
      </div>

      <!-- 6. Section Reordering & Visibility Manager (Borrowed from Puck / Gutenberg) -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">
          <span>Section Order & Visibility</span>
          <span style="font-size: 10px; color: #64748b;">(Reorder & Toggle)</span>
        </div>
        <div class="section-pill-list" id="section-order-list">
          <!-- Dynamically populated -->
        </div>
      </div>

    </aside>

    <!-- Center Canvas Preview Frame -->
    <main class="app-canvas-container">
      <div class="app-viewport-frame desktop" id="viewport-frame">
        <div id="page-render-target">
          <!-- Rendered Page Content -->
        </div>
      </div>
    </main>

    <!-- Slide-Out Kadence Gutenberg Split-Code Drawer -->
    <div class="code-drawer" id="code-drawer">
      <div class="code-drawer-header">
        <div class="code-drawer-title">
          <span>🧱 Kadence Gutenberg Block Markup</span>
        </div>
        <div style="display: flex; gap: 6px;">
          <button class="action-btn primary" style="padding: 4px 10px; font-size: 11px;" onclick="copyCodeDrawer()">Copy Code</button>
          <button class="action-btn secondary" style="padding: 4px 8px; font-size: 11px;" onclick="toggleCodeDrawer()">✕</button>
        </div>
      </div>
      <pre class="code-view-pre" id="code-drawer-content"></pre>
    </div>

  </div>

  <!-- Embedded Compiled Data for All 6 Pages -->
  <script>
""" + builder_data_js + """
  </script>

  <!-- Pro Builder Application Logic -->
  <script>
    // App State
    let currentActivePage = "homepage";
    let currentArchetype = "industrial";
    let currentBaMode = "cards";
    let activeDensity = "balanced";
    let activeCornerRadius = "4px";
    let activeTexture = "solid";

    let sectionVariants = {
      hero: "split",
      services: "grid",
      reviews: "cards"
    };

    let activeFeatures = {
      radar: false,
      winner: true,
      conduit: false,
      spotlight: true,
      mobileBar: true
    };

    let pageSectionOrder = {};
    let sectionVisibility = {};

    // Archetype Presets
    const ARCHETYPES = {
      industrial: {
        primary: "#121315",
        accent: "#fd761a",
        bg: "#f9f9fa",
        cardBg: "#ffffff",
        border: "#e5e7eb",
        fontHeading: "'Montserrat', sans-serif",
        radius: "4px"
      },
      emergency: {
        primary: "#7f1d1d",
        accent: "#dc2626",
        bg: "#fff5f5",
        cardBg: "#ffffff",
        border: "#fecaca",
        fontHeading: "'Outfit', sans-serif",
        radius: "6px"
      },
      architectural: {
        primary: "#0f172a",
        accent: "#059669",
        bg: "#f8fafc",
        cardBg: "#ffffff",
        border: "#e2e8f0",
        fontHeading: "'Plus Jakarta Sans', sans-serif",
        radius: "8px"
      }
    };

    function setViewport(size, btn) {
      document.querySelectorAll('.viewport-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const frame = document.getElementById('viewport-frame');
      frame.className = `app-viewport-frame ${size}`;
    }

    function setArchetype(type) {
      currentArchetype = type;
      document.querySelectorAll('.archetype-card').forEach(c => c.classList.remove('active'));
      const activeEl = document.getElementById(`arch-${type}`);
      if (activeEl) activeEl.classList.add('active');

      const preset = ARCHETYPES[type];
      document.getElementById('primary-color-picker').value = preset.primary;
      document.getElementById('accent-color-picker').value = preset.accent;
      activeCornerRadius = preset.radius;

      applyThemeStyles();
      renderCurrentPage();
    }

    function setSectionVariant(section, variant) {
      sectionVariants[section] = variant;
      const group = {
        hero: ['split', 'banner', 'alert'],
        services: ['grid', 'bento', 'strips'],
        reviews: ['cards', 'split', 'wall']
      }[section];

      group.forEach(v => {
        const btn = document.getElementById(`${section}-var-${v}`);
        if (btn) btn.classList.toggle('active', v === variant);
      });

      renderCurrentPage();
    }

    function setSpacing(density) {
      activeDensity = density;
      ['compact', 'balanced', 'spacious'].forEach(d => {
        document.getElementById(`spacing-${d}`).classList.toggle('active', d === density);
      });
      applyThemeStyles();
    }

    function setCornerRadius(rad) {
      activeCornerRadius = rad;
      const map = { '0px': 'sharp', '4px': 'clean', '8px': 'round', '999px': 'pill' };
      Object.keys(map).forEach(r => {
        document.getElementById(`radius-${map[r]}`).classList.toggle('active', r === rad);
      });
      applyThemeStyles();
    }

    function setTexture(tex) {
      activeTexture = tex;
      ['solid', 'dots', 'grid'].forEach(t => {
        document.getElementById(`texture-${t}`).classList.toggle('active', t === tex);
      });
      const frame = document.getElementById('viewport-frame');
      frame.classList.remove('texture-dots', 'texture-grid');
      if (tex !== 'solid') frame.classList.add(`texture-${tex}`);
    }

    function setBaMode(mode) {
      currentBaMode = mode;
      const cardsBtn = document.getElementById('ba-cards-btn');
      const sliderBtn = document.getElementById('ba-slider-btn');
      if (mode === 'cards') {
        cardsBtn.style.background = '#2563eb';
        cardsBtn.style.color = '#fff';
        sliderBtn.style.background = 'var(--app-panel-bg)';
        sliderBtn.style.color = '#cbd5e1';
      } else {
        sliderBtn.style.background = '#2563eb';
        sliderBtn.style.color = '#fff';
        cardsBtn.style.background = 'var(--app-panel-bg)';
        cardsBtn.style.color = '#cbd5e1';
      }
      renderCurrentPage();
    }

    function toggleFeature(feature, isChecked) {
      activeFeatures[feature] = isChecked;
      renderCurrentPage();
    }

    function updateCustomColors() {
      ARCHETYPES[currentArchetype].primary = document.getElementById('primary-color-picker').value;
      ARCHETYPES[currentArchetype].accent = document.getElementById('accent-color-picker').value;
      applyThemeStyles();
    }

    function applyThemeStyles() {
      const preset = ARCHETYPES[currentArchetype];
      const paddings = {
        compact: "28px 24px",
        balanced: "48px 32px",
        spacious: "72px 40px"
      }[activeDensity];

      const styleEl = document.getElementById('theme-overrides');
      styleEl.innerHTML = `
        :root {
          --primary: ${preset.primary};
          --accent: ${preset.accent};
          --radius-default: ${activeCornerRadius};
          --section-padding: ${paddings};
        }
        .builder-page h1, .builder-page h2, .builder-page h3 {
          font-family: ${preset.fontHeading} !important;
        }
        .builder-section {
          padding: var(--section-padding) !important;
        }
        .btn-primary {
          background-color: ${preset.accent} !important;
          color: #ffffff !important;
          border-radius: ${activeCornerRadius} !important;
        }
        .card-custom {
          border-radius: ${activeCornerRadius} !important;
        }
      `;
    }

    function loadSelectedPage(pageId) {
      currentActivePage = pageId;
      const pageData = window.BUILDER_PAGES_DATA[pageId];
      if (!pageData) return;

      document.getElementById('meta-kw').innerText = pageData.meta.target_keyword || pageData.meta.primary_keyword || "N/A";

      // Initialize Section Ordering & Visibility
      if (!pageSectionOrder[pageId]) {
        pageSectionOrder[pageId] = Object.keys(pageData.sections);
      }
      if (!sectionVisibility[pageId]) {
        sectionVisibility[pageId] = {};
        pageSectionOrder[pageId].forEach(k => sectionVisibility[pageId][k] = true);
      }

      renderSectionOrderUI();
      renderCurrentPage();
    }

    function renderSectionOrderUI() {
      const listEl = document.getElementById('section-order-list');
      listEl.innerHTML = '';
      const order = pageSectionOrder[currentActivePage];

      order.forEach((secKey, idx) => {
        const item = document.createElement('div');
        item.className = 'section-item';
        item.innerHTML = `
          <div class="section-item-left">
            <input type="checkbox" ${sectionVisibility[currentActivePage][secKey] ? 'checked' : ''} onchange="toggleSection('${secKey}', this.checked)">
            <span>${secKey.replace(/_/g, ' ').toUpperCase()}</span>
          </div>
          <div class="reorder-btns">
            <button class="reorder-btn" onclick="moveSection('${secKey}', -1)" ${idx === 0 ? 'disabled style="opacity:0.3;"' : ''}>▲</button>
            <button class="reorder-btn" onclick="moveSection('${secKey}', 1)" ${idx === order.length - 1 ? 'disabled style="opacity:0.3;"' : ''}>▼</button>
          </div>
        `;
        listEl.appendChild(item);
      });
    }

    function moveSection(secKey, direction) {
      const order = pageSectionOrder[currentActivePage];
      const index = order.indexOf(secKey);
      if (index === -1) return;
      const newIndex = index + direction;
      if (newIndex < 0 || newIndex >= order.length) return;

      order.splice(index, 1);
      order.splice(newIndex, 0, secKey);

      renderSectionOrderUI();
      renderCurrentPage();
    }

    function toggleSection(secKey, visible) {
      sectionVisibility[currentActivePage][secKey] = visible;
      renderCurrentPage();
    }

    // Markdown Parser
    function parseMarkdownToHTML(md) {
      let html = md
        .replace(/^### (.*$)/gim, '<h3 contenteditable="true" style="font-size: 1.25rem; font-weight: 700; margin: 16px 0 8px; color: var(--primary);">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 contenteditable="true" style="font-size: 1.75rem; font-weight: 800; margin: 24px 0 12px; color: var(--primary);">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1 contenteditable="true" style="font-size: 2.25rem; font-weight: 800; margin-bottom: 16px; color: var(--primary); line-height: 1.2;">$1</h1>')
        .replace(/\\*\\*(.*?)\\*\\*/gim, '<strong style="color: var(--primary);">$1</strong>')
        .replace(/\\*(.*?)\\*/gim, '<em>$1</em>')
        .replace(/\\[([^\\]]+)\\]\\(([^\\)]+)\\)/gim, '<a href="$2" style="color: var(--accent); text-decoration: underline; font-weight: 600;">$1</a>')
        .replace(/\\n\\n/gim, '</p><p contenteditable="true" style="margin-bottom: 14px; font-size: 1rem; line-height: 1.6; color: #374151;">')
        .replace(/^> (.*$)/gim, '<blockquote style="border-left: 4px solid var(--accent); padding-left: 16px; margin: 16px 0; font-style: italic; color: #4b5563;">$1</blockquote>');
      
      if (html.includes('|')) {
        const lines = html.split('\\n');
        let inTable = false;
        let tableHTML = '<div style="overflow-x: auto; margin: 20px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 14px;">';
        let newLines = [];
        
        for (let line of lines) {
          if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
            if (!inTable) inTable = true;
            if (line.includes('---')) continue;
            const cells = line.split('|').slice(1, -1);
            tableHTML += '<tr style="border-bottom: 1px solid #e5e7eb;">';
            cells.forEach(c => {
              tableHTML += `<td style="padding: 10px 14px; text-align: left;">${c.trim()}</td>`;
            });
            tableHTML += '</tr>';
          } else {
            if (inTable) {
              tableHTML += '</table></div>';
              newLines.push(tableHTML);
              inTable = false;
            }
            newLines.push(line);
          }
        }
        if (inTable) tableHTML += '</table></div>';
        html = newLines.join('\\n');
      }

      return `<p contenteditable="true" style="margin-bottom: 14px; font-size: 1rem; line-height: 1.6; color: #374151;">${html}</p>`;
    }

    // Render Canvas
    function renderCurrentPage() {
      if (!currentActivePage || !window.BUILDER_PAGES_DATA || !window.BUILDER_PAGES_DATA[currentActivePage] || !pageSectionOrder[currentActivePage]) return;
      const pageData = window.BUILDER_PAGES_DATA[currentActivePage];

      const container = document.getElementById('page-render-target');
      let html = `<div class="builder-page" style="padding-bottom: 60px;">`;

      // Header Navigation
      html += `
        <nav style="display: flex; align-items: center; justify-content: space-between; padding: 18px 32px; border-bottom: 1px solid #e5e7eb; background: #ffffff;">
          <div style="font-weight: 800; font-size: 18px; color: var(--primary);">Rockford Air Duct Pros</div>
          <div style="display: flex; align-items: center; gap: 20px; font-size: 13px; font-weight: 600;">
            <a href="#" style="color: #374151; text-decoration: none;">Services</a>
            <a href="#" style="color: #374151; text-decoration: none;">About</a>
            <a href="#" style="color: #374151; text-decoration: none;">Reviews</a>
            <a href="#" style="color: #374151; text-decoration: none;">Service Area</a>
            <a href="tel:8155550142" class="btn-primary" style="padding: 8px 16px; text-decoration: none; font-weight: 700;">(815) 555-0142</a>
          </div>
        </nav>
      `;

      // Render Reordered Sections
      const order = pageSectionOrder[currentActivePage];
      order.forEach(key => {
        if (sectionVisibility[currentActivePage] && sectionVisibility[currentActivePage][key] === false) return;

        const rawSec = pageData.sections[key];
        const secHTML = parseMarkdownToHTML(rawSec);

        let bgStyle = "background: #ffffff;";
        if (key.includes('hero')) {
          bgStyle = "background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);";
        } else if (key.includes('trust') || key.includes('cta')) {
          bgStyle = "background: #f1f5f9;";
        }

        html += `
          <section id="sec-${key}" class="builder-section" style="${bgStyle}; border-bottom: 1px solid #f1f5f9;">
            <div style="max-width: 1100px; margin: 0 auto; position: relative;">
        `;

        // Variant logic for Hero
        if (key.includes('hero')) {
          if (sectionVariants.hero === 'split') {
            html += `
              <div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 40px; align-items: center;">
                <div>${secHTML}</div>
                <div class="card-custom" style="background: #ffffff; padding: 24px; border: 2px solid var(--accent); box-shadow: 0 10px 30px rgba(0,0,0,0.08);">
                  <h3 style="font-size: 16px; font-weight: 800; margin-bottom: 8px; color: var(--primary);">Instant Inspection Booking</h3>
                  <p style="font-size: 12px; color: #64748b; margin-bottom: 16px;">Schedule verified camera documentation before & after cleaning.</p>
                  <input type="text" placeholder="Your Name" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12px;">
                  <input type="tel" placeholder="Phone Number" style="width: 100%; padding: 8px; margin-bottom: 12px; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 12px;">
                  <button class="btn-primary" style="width: 100%; padding: 10px; font-weight: 700; border: none; cursor: pointer;">Call (815) 555-0142</button>
                </div>
              </div>
            `;
          } else if (sectionVariants.hero === 'alert') {
            html += `
              <div style="background: #fef2f2; border-left: 5px solid #dc2626; padding: 14px 20px; margin-bottom: 24px; border-radius: 4px;">
                <strong style="color: #991b1b; font-size: 13px;">🚨 Emergency Dispatch Alert:</strong>
                <span style="color: #7f1d1d; font-size: 13px; margin-left: 6px;">Same-day service slots available for urgent airflow or soot contamination calls in Winnebago County.</span>
              </div>
              ${secHTML}
            `;
          } else {
            html += secHTML;
          }
        }
        // Before/After Section Logic
        else if (key.includes('before') || key.includes('after')) {
          if (currentBaMode === 'slider') {
            html += `
              <h2 contenteditable="true" style="font-size: 1.75rem; font-weight: 800; margin-bottom: 16px; color: var(--primary);">Verified Borescope Before & After Inspection</h2>
              <div style="position: relative; width: 100%; max-width: 800px; height: 420px; margin: 24px auto; overflow: hidden; border-radius: ${activeCornerRadius}; border: 2px solid #e2e8f0; user-select: none;">
                <img src="images/homepage/contaminated-air-duct-interior-rockford-residence.webp" alt="Before Cleaning" style="position: absolute; top:0; left:0; width:100%; height:100%; object-fit: cover;">
                <div id="slider-reveal" style="position: absolute; top:0; left:0; width: 50%; height:100%; overflow: hidden; border-right: 3px solid #ffffff; box-shadow: 2px 0 10px rgba(0,0,0,0.3);">
                  <img src="images/homepage/sanitized-bare-metal-air-duct-rockford-residence.webp" alt="After Cleaning" style="position: absolute; top:0; left:0; width: 800px; height:100%; object-fit: cover;">
                </div>
                <input type="range" min="0" max="100" value="50" style="position: absolute; bottom: 15px; left: 10%; width: 80%; z-index: 10;" oninput="document.getElementById('slider-reveal').style.width = this.value + '%'">
              </div>
            `;
          } else {
            html += secHTML;
          }
        } else {
          html += secHTML;
        }

        // Winner Ribbon & Border
        if (activeFeatures.winner && key.includes('comparison')) {
          html += `
            <div style="position: absolute; top: 10px; right: 20px; background: #eab308; color: #000; font-weight: 800; font-size: 10px; padding: 4px 10px; border-radius: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
              ★ NADCA CERTIFIED ADVANTAGE
            </div>
          `;
        }

        // Radar Beacon Marker
        if (activeFeatures.radar && (key.includes('map') || key.includes('area') || key.includes('hero'))) {
          html += `
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 14px; font-size: 11px; font-weight: 700; color: var(--accent);">
              <span style="display: inline-block; width: 10px; height: 10px; background: var(--accent); border-radius: 50%; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3); animation: pulse 2s infinite;"></span>
              Live Service Truck Dispatched in Rockford Area
            </div>
          `;
        }

        html += `
            </div>
          </section>
        `;
      });

      // Mobile Bottom Sticky Bar
      if (activeFeatures.mobileBar) {
        html += `
          <div style="position: fixed; bottom: 0; left: 0; right: 0; background: var(--primary); color: #fff; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; z-index: 999; border-top: 2px solid var(--accent);">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; color: #94a3b8;">Direct Local Dispatch</div>
              <div style="font-size: 14px; font-weight: 700;">(815) 555-0142</div>
            </div>
            <a href="tel:8155550142" class="btn-primary" style="padding: 8px 16px; text-decoration: none; font-size: 12px; font-weight: 700;">Call Now</a>
          </div>
        `;
      }

      html += `</div>`;
      container.innerHTML = html;
      updateLiveCodeDrawer();
    }

    // Kadence Code Generator
    function generateKadenceBlocksString() {
      const pageData = window.BUILDER_PAGES_DATA[currentActivePage];
      let blocks = `<!-- wp:kadence/rowlayout {"uniqueID":"sec_main","columns":1} -->\\n`;
      const order = pageSectionOrder[currentActivePage];

      order.forEach(key => {
        if (sectionVisibility[currentActivePage] && sectionVisibility[currentActivePage][key] === false) return;
        blocks += `  <!-- wp:kadence/column {"id":"${key}"} -->\\n`;
        blocks += `    <!-- SECTION: ${key} -->\\n`;
        blocks += `    ${parseMarkdownToHTML(pageData.sections[key]).replace(/contenteditable="true"/g, '')}\\n`;
        blocks += `  <!-- /wp:kadence/column -->\\n\\n`;
      });

      blocks += `<!-- /wp:kadence/rowlayout -->`;
      return blocks;
    }

    function toggleCodeDrawer() {
      const drawer = document.getElementById('code-drawer');
      drawer.classList.toggle('open');
      if (drawer.classList.contains('open')) {
        updateLiveCodeDrawer();
      }
    }

    function updateLiveCodeDrawer() {
      const pre = document.getElementById('code-drawer-content');
      if (pre) {
        pre.innerText = generateKadenceBlocksString();
      }
    }

    function copyCodeDrawer() {
      navigator.clipboard.writeText(generateKadenceBlocksString()).then(() => {
        alert("Kadence Gutenberg Block markup copied to clipboard!");
      });
    }

    function exportKadenceBlocks() {
      copyCodeDrawer();
    }

    function exportFullHTML() {
      const container = document.getElementById('page-render-target');
      const pageData = window.BUILDER_PAGES_DATA[currentActivePage];
      const fullHTML = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${pageData.meta.meta_title || pageData.title}</title>
  <meta name="description" content="${pageData.meta.meta_description || ''}">
  <style>
    ${document.getElementById('theme-overrides').innerHTML}
    body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; color: #1a1c1d; }
    *, *::before, *::after { box-sizing: border-box; }
    a { color: inherit; }
  </style>
</head>
<body>
${container.innerHTML.replace(/contenteditable="true"/g, '')}
</body>
</html>`;
      
      const blob = new Blob([fullHTML], { type: 'text/html' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${currentActivePage}_production.html`;
      a.click();
    }

    // App Init
    window.addEventListener('DOMContentLoaded', () => {
      loadSelectedPage('homepage');
      setArchetype('industrial');
      setBaMode('cards');
      setSpacing('balanced');
      setCornerRadius('4px');
    });
  </script>
</body>
</html>
"""

out_builder = os.path.join(base_dir, "studio_builder.html")
with open(out_builder, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated updated {out_builder} ({len(html_content)} bytes)")

