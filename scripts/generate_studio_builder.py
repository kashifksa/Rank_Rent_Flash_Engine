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
  <title>Rank & Rent Studio Builder — Universal Page Customizer</title>
  
  <!-- Google Fonts: Inter, Montserrat, Plus Jakarta Sans, Outfit -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  
  <style>
    /* ==========================================================================
       STUDIO BUILDER APP CHASSIS (APPLICATION UI)
       ========================================================================== */
    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    :root {
      --app-bg: #0f1117;
      --app-sidebar-bg: #161822;
      --app-border: #262a3b;
      --app-text: #e2e8f0;
      --app-text-muted: #8b95a5;
      --app-accent: #3b82f6;
      --app-accent-hover: #2563eb;
      --app-header-h: 56px;
      --app-sidebar-w: 360px;
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

    /* Top Application Bar */
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
      font-weight: 800;
      font-size: 16px;
      color: white;
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
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

    /* Viewport Controls */
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

    .viewport-btn:hover {
      color: #fff;
    }

    .viewport-btn.active {
      background: var(--app-sidebar-bg);
      color: #fff;
      box-shadow: 0 1px 4px rgba(0,0,0,0.4);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .action-btn {
      padding: 7px 14px;
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
      background: #1e2230;
      color: #cbd5e1;
      border: 1px solid var(--app-border);
    }

    .action-btn.secondary:hover {
      background: #282d3f;
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

    /* Main Workspace Layout */
    .app-workspace {
      display: flex;
      flex: 1;
      height: calc(100vh - var(--app-header-h));
      overflow: hidden;
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

    .form-group:last-child {
      margin-bottom: 0;
    }

    .form-label {
      display: block;
      font-size: 12px;
      font-weight: 600;
      color: #cbd5e1;
      margin-bottom: 6px;
    }

    .form-select, .form-input {
      width: 100%;
      background: #0f1117;
      border: 1px solid var(--app-border);
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 12px;
      color: #e2e8f0;
      outline: none;
      transition: border-color 0.15s;
    }

    .form-select:focus, .form-input:focus {
      border-color: var(--app-accent);
    }

    /* Archetype Switcher Grid */
    .archetype-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .archetype-card {
      background: #0f1117;
      border: 1px solid var(--app-border);
      border-radius: 6px;
      padding: 10px 6px;
      text-align: center;
      cursor: pointer;
      transition: all 0.15s;
    }

    .archetype-card:hover {
      border-color: #475569;
    }

    .archetype-card.active {
      border-color: var(--app-accent);
      background: rgba(59, 130, 246, 0.1);
    }

    .archetype-icon {
      font-size: 18px;
      margin-bottom: 4px;
    }

    .archetype-name {
      font-size: 11px;
      font-weight: 700;
      color: #fff;
    }

    /* Switch Toggles */
    .toggle-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 7px 0;
      border-bottom: 1px solid rgba(255,255,255,0.04);
    }

    .toggle-row:last-child {
      border-bottom: none;
    }

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

    .toggle-switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    .toggle-slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
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

    input:checked + .toggle-slider {
      background-color: var(--app-accent);
    }

    input:checked + .toggle-slider:before {
      transform: translateX(16px);
    }

    /* Section Order / Visibility Pills */
    .section-pill-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .section-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #0f1117;
      border: 1px solid var(--app-border);
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }

    .section-item-left {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .drag-handle {
      color: #64748b;
      cursor: grab;
      font-size: 13px;
    }

    /* Canvas Area */
    .app-canvas-container {
      flex: 1;
      background: #090a0f;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 24px;
      overflow-y: auto;
    }

    .app-viewport-frame {
      background: #ffffff;
      border-radius: 8px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
      transition: width 0.3s ease;
      width: 100%;
      max-width: 1280px;
      min-height: 800px;
      color: #1a1c1d;
      position: relative;
    }

    /* Mobile Frame Styling */
    .app-viewport-frame.mobile {
      max-width: 375px;
      border: 12px solid #1e2230;
      border-radius: 40px;
      overflow: hidden;
      box-shadow: 0 25px 60px rgba(0,0,0,0.8);
    }

    .app-viewport-frame.tablet {
      max-width: 768px;
    }

    .app-viewport-frame.laptop {
      max-width: 1024px;
    }

    /* Dynamic Archetype Styles Injected via JS into #theme-overrides */
  </style>
  
  <style id="theme-overrides">
    /* Initial Theme Settings */
  </style>
</head>
<body>

  <!-- Top App Navigation -->
  <header class="app-header">
    <div class="app-branding">
      <div class="app-logo">⚡</div>
      <div class="app-title-group">
        <h1>Rank & Rent Studio Builder <span class="app-badge">Kadence v2 Master</span></h1>
      </div>
    </div>

    <!-- Viewport Switcher -->
    <div class="viewport-controls">
      <button class="viewport-btn active" onclick="setViewport('desktop', this)">🖥️ Desktop</button>
      <button class="viewport-btn" onclick="setViewport('laptop', this)">💻 Laptop</button>
      <button class="viewport-btn" onclick="setViewport('tablet', this)">📱 Tablet</button>
      <button class="viewport-btn" onclick="setViewport('mobile', this)">📲 Mobile</button>
    </div>

    <!-- Actions -->
    <div class="header-actions">
      <button class="action-btn secondary" onclick="exportKadenceBlocks()">📋 Copy Gutenberg HTML</button>
      <button class="action-btn primary" onclick="exportFullHTML()">📥 Export Full HTML</button>
    </div>
  </header>

  <!-- Main Workspace -->
  <div class="app-workspace">
    
    <!-- Sidebar Control Panel -->
    <aside class="app-sidebar">
      
      <!-- Section 1: Page Selector -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Active Page & Blueprint</div>
        <div class="form-group">
          <label class="form-label" for="page-select">Select Page to Customize:</label>
          <select id="page-select" class="form-select" onchange="loadSelectedPage(this.value)">
            <option value="homepage">🏠 Homepage (Residential & Hub)</option>
            <option value="about">ℹ️ About Us (E-E-A-T & Credentials)</option>
            <option value="contact">📞 Contact Us (Dispatch & Form)</option>
            <option value="air-duct-cleaning-loves-park-il">📍 Loves Park Location Page</option>
            <option value="commercial-hvac-duct-cleaning">🏢 Commercial HVAC Duct Cleaning</option>
            <option value="dryer-vent-cleaning-and-lint-removal">🌀 Dryer Vent Cleaning & Lint Removal</option>
          </select>
        </div>
        <div id="page-meta-badge" style="font-size: 11px; color: #94a3b8; background: #0f1117; padding: 6px 8px; border-radius: 4px; border: 1px solid var(--app-border);">
          Target Keyword: <strong id="meta-kw" style="color: #60a5fa;">air duct cleaning rockford</strong>
        </div>
      </div>

      <!-- Section 2: Design Archetypes -->
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

      <!-- Section 3: Interactive Component Toggles -->
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
          <span class="toggle-label">Floating Mobile Call Bar</span>
          <label class="toggle-switch">
            <input type="checkbox" id="toggle-mobile-bar" checked onchange="toggleFeature('mobile-bar', this.checked)">
            <span class="toggle-slider"></span>
          </label>
        </div>
      </div>

      <!-- Section 4: Typography & Styling -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Typography & Palette</div>
        <div class="form-group">
          <label class="form-label" for="font-family-select">Heading Font:</label>
          <select id="font-family-select" class="form-select" onchange="setFontFamily(this.value)">
            <option value="'Montserrat', sans-serif">Montserrat (Industrial Heavy)</option>
            <option value="'Plus Jakarta Sans', sans-serif">Plus Jakarta Sans (Modern Clean)</option>
            <option value="'Outfit', sans-serif">Outfit (Bold Geometric)</option>
            <option value="'Inter', sans-serif">Inter (Utilitarian Precision)</option>
          </select>
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

      <!-- Section 5: Section Visibility Manager -->
      <div class="sidebar-section">
        <div class="sidebar-section-title">Page Section Visibility</div>
        <div class="section-pill-list" id="section-visibility-list">
          <!-- Dynamically populated per page -->
        </div>
      </div>

    </aside>

    <!-- Canvas Render Frame -->
    <main class="app-canvas-container">
      <div class="app-viewport-frame desktop" id="viewport-frame">
        <div id="page-render-target">
          <!-- Rendered Page Content -->
        </div>
      </div>
    </main>

  </div>

  <!-- Embedded Compiled Data for All 6 Pages -->
  <script>
""" + builder_data_js + """
  </script>

  <!-- Builder Application Logic -->
  <script>
    // State
    let currentActivePage = "homepage";
    let currentArchetype = "industrial";
    let currentBaMode = "cards";
    let activeFeatures = {
      radar: false,
      winner: true,
      conduit: false,
      spotlight: true,
      mobileBar: true
    };
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
      document.getElementById('primary-color-picker').value = preset.primary.startsWith('#') ? preset.primary : '#121315';
      document.getElementById('accent-color-picker').value = preset.accent.startsWith('#') ? preset.accent : '#fd761a';
      document.getElementById('font-family-select').value = preset.fontHeading;

      applyThemeStyles();
    }

    function setFontFamily(font) {
      ARCHETYPES[currentArchetype].fontHeading = font;
      applyThemeStyles();
    }

    function updateCustomColors() {
      ARCHETYPES[currentArchetype].primary = document.getElementById('primary-color-picker').value;
      ARCHETYPES[currentArchetype].accent = document.getElementById('accent-color-picker').value;
      applyThemeStyles();
    }

    function applyThemeStyles() {
      const preset = ARCHETYPES[currentArchetype];
      const styleEl = document.getElementById('theme-overrides');
      styleEl.innerHTML = `
        :root {
          --primary: ${preset.primary};
          --secondary-container: ${preset.accent};
          --accent: ${preset.accent};
          --font-heading: ${preset.fontHeading};
          --radius-default: ${preset.radius};
        }
        .builder-page h1, .builder-page h2, .builder-page h3 {
          font-family: ${preset.fontHeading} !important;
        }
        .btn-primary {
          background-color: ${preset.accent} !important;
          color: #ffffff !important;
          border-radius: ${preset.radius} !important;
        }
        .highlight-border {
          border-color: ${preset.accent} !important;
        }
      `;
    }

    function setBaMode(mode) {
      currentBaMode = mode;
      const cardsBtn = document.getElementById('ba-cards-btn');
      const sliderBtn = document.getElementById('ba-slider-btn');
      if (mode === 'cards') {
        cardsBtn.style.background = '#2563eb';
        cardsBtn.style.color = '#fff';
        sliderBtn.style.background = '#1e2230';
        sliderBtn.style.color = '#cbd5e1';
      } else {
        sliderBtn.style.background = '#2563eb';
        sliderBtn.style.color = '#fff';
        cardsBtn.style.background = '#1e2230';
        cardsBtn.style.color = '#cbd5e1';
      }
      renderCurrentPage();
    }

    function toggleFeature(feature, isChecked) {
      activeFeatures[feature] = isChecked;
      renderCurrentPage();
    }

    function loadSelectedPage(pageId) {
      currentActivePage = pageId;
      const pageData = window.BUILDER_PAGES_DATA[pageId];
      if (!pageData) return;

      // Update badge
      const kw = pageData.meta.target_keyword || pageData.meta.primary_keyword || "N/A";
      document.getElementById('meta-kw').innerText = kw;

      // Reset section visibility list
      const visList = document.getElementById('section-visibility-list');
      visList.innerHTML = '';
      sectionVisibility[pageId] = sectionVisibility[pageId] || {};

      Object.keys(pageData.sections).forEach(secKey => {
        if (sectionVisibility[pageId][secKey] === undefined) {
          sectionVisibility[pageId][secKey] = true;
        }
        const item = document.createElement('div');
        item.className = 'section-item';
        item.innerHTML = `
          <div class="section-item-left">
            <span class="drag-handle">⠿</span>
            <span>${secKey.replace(/_/g, ' ').toUpperCase()}</span>
          </div>
          <input type="checkbox" ${sectionVisibility[pageId][secKey] ? 'checked' : ''} onchange="toggleSection('${secKey}', this.checked)">
        `;
        visList.appendChild(item);
      });

      renderCurrentPage();
    }

    function toggleSection(secKey, visible) {
      sectionVisibility[currentActivePage][secKey] = visible;
      renderCurrentPage();
    }

    // Markdown Parser Helper for Sections
    function parseMarkdownToHTML(md) {
      let html = md
        .replace(/^### (.*$)/gim, '<h3 style="font-size: 1.25rem; font-weight: 700; margin: 16px 0 8px; color: var(--primary);">$1</h3>')
        .replace(/^## (.*$)/gim, '<h2 style="font-size: 1.75rem; font-weight: 800; margin: 24px 0 12px; color: var(--primary);">$1</h2>')
        .replace(/^# (.*$)/gim, '<h1 style="font-size: 2.25rem; font-weight: 800; margin-bottom: 16px; color: var(--primary); line-height: 1.2;">$1</h1>')
        .replace(/\\*\\*(.*?)\\*\\*/gim, '<strong style="color: var(--primary);">$1</strong>')
        .replace(/\\*(.*?)\\*/gim, '<em>$1</em>')
        .replace(/\\[([^\\]]+)\\]\\(([^\\)]+)\\)/gim, '<a href="$2" style="color: var(--accent); text-decoration: underline; font-weight: 600;">$1</a>')
        .replace(/\\n\\n/gim, '</p><p style="margin-bottom: 14px; font-size: 1rem; line-height: 1.6; color: #374151;">')
        .replace(/^> (.*$)/gim, '<blockquote style="border-left: 4px solid var(--accent); padding-left: 16px; margin: 16px 0; font-style: italic; color: #4b5563;">$1</blockquote>');
      
      // Handle tables
      if (html.includes('|')) {
        const lines = html.split('\\n');
        let inTable = false;
        let tableHTML = '<div style="overflow-x: auto; margin: 20px 0;"><table style="width: 100%; border-collapse: collapse; font-size: 14px;">';
        let newLines = [];
        
        for (let line of lines) {
          if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
            if (!inTable) { inTable = true; }
            if (line.includes('---')) continue; // separator
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

      return `<p style="margin-bottom: 14px; font-size: 1rem; line-height: 1.6; color: #374151;">${html}</p>`;
    }

    function renderCurrentPage() {
      const pageData = window.BUILDER_PAGES_DATA[currentActivePage];
      if (!pageData) return;

      const container = document.getElementById('page-render-target');
      let html = `<div class="builder-page" style="padding-bottom: 60px;">`;

      // Header Navigation Bar Simulation
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

      // Render Each Section
      const secKeys = Object.keys(pageData.sections);
      secKeys.forEach(key => {
        if (sectionVisibility[currentActivePage] && sectionVisibility[currentActivePage][key] === false) {
          return;
        }

        const rawSec = pageData.sections[key];
        const secHTML = parseMarkdownToHTML(rawSec);

        // Section Container
        let bgStyle = "background: #ffffff;";
        if (key.includes('hero')) {
          bgStyle = "background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%); padding: 50px 32px;";
        } else if (key.includes('trust') || key.includes('cta')) {
          bgStyle = "background: #f1f5f9; padding: 36px 32px;";
        } else {
          bgStyle = "padding: 40px 32px; border-bottom: 1px solid #f1f5f9;";
        }

        html += `
          <section id="sec-${key}" style="${bgStyle}">
            <div style="max-width: 1100px; margin: 0 auto; position: relative;">
        `;

        // If Before/After section, handle slider mode
        if (key.includes('before') || key.includes('after')) {
          if (currentBaMode === 'slider') {
            html += `
              <h2 style="font-size: 1.75rem; font-weight: 800; margin-bottom: 16px; color: var(--primary);">Verified Borescope Before & After Inspection</h2>
              <div style="position: relative; width: 100%; max-width: 800px; height: 420px; margin: 24px auto; overflow: hidden; border-radius: 8px; border: 2px solid #e2e8f0; user-select: none;">
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

        // Add Winner Ribbon if enabled & comparison section
        if (activeFeatures.winner && key.includes('comparison')) {
          html += `
            <div style="position: absolute; top: 10px; right: 20px; background: #eab308; color: #000; font-weight: 800; font-size: 10px; padding: 4px 10px; border-radius: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
              ★ NADCA CERTIFIED ADVANTAGE
            </div>
          `;
        }

        html += `
            </div>
          </section>
        `;
      });

      // Mobile Bottom Bar if active
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
    }

    function exportKadenceBlocks() {
      const pageData = window.BUILDER_PAGES_DATA[currentActivePage];
      let blocks = `<!-- wp:kadence/rowlayout -->\\n`;
      Object.keys(pageData.sections).forEach(key => {
        if (sectionVisibility[currentActivePage] && sectionVisibility[currentActivePage][key] === false) return;
        blocks += `<!-- wp:kadence/column {"section":"${key}"} -->\\n`;
        blocks += parseMarkdownToHTML(pageData.sections[key]);
        blocks += `\\n<!-- /wp:kadence/column -->\\n`;
      });
      blocks += `<!-- /wp:kadence/rowlayout -->`;

      navigator.clipboard.writeText(blocks).then(() => {
        alert("Kadence Gutenberg Block HTML copied to clipboard!");
      });
    }

    function exportFullHTML() {
      const container = document.getElementById('page-render-target');
      const fullHTML = `<!DOCTYPE html>\\n<html lang="en">\\n<head>\\n  <meta charset="UTF-8">\\n  <title>${window.BUILDER_PAGES_DATA[currentActivePage].title}</title>\\n  <style>${document.getElementById('theme-overrides').innerHTML}</style>\\n</head>\\n<body>\\n${container.innerHTML}\\n</body>\\n</html>`;
      
      const blob = new Blob([fullHTML], { type: 'text/html' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `${currentActivePage}.html`;
      a.click();
    }

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {
      setArchetype('industrial');
      loadSelectedPage('homepage');
      setBaMode('cards');
    });
  </script>
</body>
</html>
"""

out_builder = os.path.join(base_dir, "studio_builder.html")
with open(out_builder, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated {out_builder} ({len(html_content)} bytes)")

