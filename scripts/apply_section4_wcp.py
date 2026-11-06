import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add WCP CSS right before .svc-section
wcp_css = """
    /* ========================================================
       CORNERSTONE WHY CHOOSE US / TRUST PILLARS (SECTION 4)
       ======================================================== */
    .wcp-section {
      width: 100%;
      padding: 76px 24px 70px;
      background: var(--surface-container-low);
      position: relative;
    }
    .wcp-container {
      max-width: 1200px;
      margin: 0 auto;
    }
    .wcp-heading {
      text-align: center;
      color: var(--on-surface);
      font-size: clamp(24px, 2.8vw, 36px);
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.02em;
      margin: 0 0 48px 0;
    }
    .wcp-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 22px;
    }
    @keyframes wcpSpin {
      100% { transform: rotate(360deg); }
    }
    .wcp-card {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 36px 22px 30px;
      background: #ffffff;
      border: 1px solid var(--outline-variant);
      border-radius: 18px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
      text-align: center;
      overflow: hidden;
      transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
      cursor: pointer;
    }
    .wcp-card::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(150deg, rgba(var(--accent-rgb), 0.08), transparent 55%);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.35s ease;
    }
    .wcp-card::after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: var(--secondary-container);
      transform: scaleX(0.7);
      transform-origin: center;
      transition: transform 0.35s ease;
      border-radius: 0 0 4px 4px;
    }
    .wcp-card:hover {
      transform: translateY(-7px);
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.12);
      border-color: rgba(var(--accent-rgb), 0.45);
    }
    .wcp-card:hover::before { opacity: 1; }
    .wcp-card:hover::after  { transform: scaleX(1); }
    .wcp-icon {
      position: relative;
      display: grid;
      place-items: center;
      width: 86px;
      height: 86px;
      flex: 0 0 86px;
      margin-bottom: 20px;
      border-radius: 50%;
      background: rgba(var(--accent-rgb), 0.12);
      color: var(--secondary-container);
      transition: transform 0.35s ease, box-shadow 0.35s ease;
    }
    .wcp-icon::before {
      content: "";
      position: absolute;
      inset: 7px;
      border: 1px dashed rgba(var(--accent-rgb), 0.45);
      border-radius: 50%;
      animation: wcpSpin 20s linear infinite;
    }
    .wcp-card:hover .wcp-icon {
      transform: translateY(-3px) scale(1.07);
      box-shadow: 0 12px 22px rgba(var(--accent-rgb), 0.25);
    }
    .wcp-icon svg {
      position: relative;
      z-index: 1;
      width: 40px;
      height: 40px;
    }
    .wcp-title {
      margin: 0;
      color: var(--on-surface);
      font-size: 16px;
      font-weight: 800;
      line-height: 1.35;
    }
    .wcp-line {
      width: 28px;
      height: 3px;
      margin: 12px auto 14px;
      border-radius: 10px;
      background: var(--secondary-container);
      transition: width 0.35s ease;
    }
    .wcp-card:hover .wcp-line { width: 52px; }
    .wcp-text {
      margin: 0;
      color: var(--on-surface-variant);
      font-size: 14px;
      line-height: 1.65;
    }
    @media (max-width: 1024px) {
      .wcp-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 18px;
      }
    }
    @media (max-width: 640px) {
      .wcp-grid {
        grid-template-columns: 1fr !important;
        gap: 16px;
      }
      .wcp-card { padding: 30px 20px 26px; }
    }
"""

anchor_css = "/* ========================================================\n   CORNERSTONE INTERACTIVE SERVICES GRID (SECTION 3)"
if anchor_css in code:
    code = code.replace(anchor_css, wcp_css + "\n" + anchor_css)
    print("1. Injected WCP CSS.")
else:
    print("Warning: anchor_css not found!")

# 2. Add Section 4: Why Choose Us in Sidebar
old_sidebar = """        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Services Grid Variant</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="services-var-grid" onclick="setSectionVariant('services', 'grid')">Kadence Grid</button>
            <button class="variation-pill active" id="services-var-cornerstone" onclick="setSectionVariant('services', 'cornerstone')">Cornerstone</button>
            <button class="variation-pill" id="services-var-bento" onclick="setSectionVariant('services', 'bento')">Bento Grid</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            Animated rotating icon rings with responsive multi-service cards.
          </div>
        </div>"""

new_sidebar = """        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Services Grid Variant</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="services-var-grid" onclick="setSectionVariant('services', 'grid')">Kadence Grid</button>
            <button class="variation-pill active" id="services-var-cornerstone" onclick="setSectionVariant('services', 'cornerstone')">Cornerstone</button>
            <button class="variation-pill" id="services-var-bento" onclick="setSectionVariant('services', 'bento')">Bento Grid</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            Animated rotating icon rings with responsive multi-service cards.
          </div>
        </div>

        <!-- Section 4: Why Choose Us / Trust Pillars Variant -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Section 4: Why Choose Us</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="why-var-kadence" onclick="setSectionVariant('why', 'kadence')">Kadence Standard</button>
            <button class="variation-pill active" id="why-var-cornerstone" onclick="setSectionVariant('why', 'cornerstone')">Cornerstone</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            4-pillar trust card grid with spinning icon badges &amp; expanding accents.
          </div>
        </div>"""

if old_sidebar in code:
    code = code.replace(old_sidebar, new_sidebar)
    print("2. Added Section 4: Why Choose Us in sidebar.")
else:
    print("Warning: old_sidebar not found!")

# 3. Update sectionVariants state & setSectionVariant function
target_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      reviews: "cards"
    };"""

replacement_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      why: "cornerstone",
      reviews: "cards"
    };"""

if target_sec_state in code:
    code = code.replace(target_sec_state, replacement_sec_state)
    print("3. Updated sectionVariants.why state.")
else:
    print("Warning: target_sec_state not found!")

target_set_var = """        hero: ['split', 'denton'],
        intro: ['callout', 'denton'],
        services: ['grid', 'cornerstone', 'bento', 'strips'],
        reviews: ['cards', 'split', 'wall']"""

replacement_set_var = """        hero: ['split', 'denton'],
        intro: ['callout', 'denton'],
        services: ['grid', 'cornerstone', 'bento', 'strips'],
        why: ['kadence', 'cornerstone'],
        reviews: ['cards', 'split', 'wall']"""

if target_set_var in code:
    code = code.replace(target_set_var, replacement_set_var)
    print("4. Updated setSectionVariant handler to include why.")
else:
    print("Warning: target_set_var not found!")

# 4. Add parseWhyUsFromContent helper right after parseServicesFromContent
parse_why_helper = """
    function parseWhyUsFromContent(rawSec, pageKey) {
      const defaultPillars = [
        {
          title: "Genuinely Local – Not a Call Center",
          desc: "Dispatched directly from Winnebago County. You speak directly with our local certified technicians—never an out-of-state call center."
        },
        {
          title: "NADCA Certified Source Removal",
          desc: "We adhere strictly to ACR-2021 source removal standards using 5,000 CFM negative air pressure and mechanical brush scouring."
        },
        {
          title: "No Surprise Bills – Ever",
          desc: "All estimates are approved in writing before work begins. Strictly zero hidden disposal fees, hookup charges, or bait-and-switch upsells."
        },
        {
          title: "We Treat Your Home Like Our Own",
          desc: "Protective drop cloths, clean indoor booties, and register magnetic seals protect your living space with zero interior blowback."
        }
      ];

      if (!rawSec) return { heading: "Why Rockford Property Owners Choose Us", items: defaultPillars };

      const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
      const lines = cleanMd.split(String.fromCharCode(10));
      let heading = "";
      const parsedItems = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!heading && line.startsWith("## ")) {
          heading = line.replace(/^##[ \\t]+/, "").trim();
        }
        const bMatch = line.match(/^[-*][ \\t]+\\*\\*([^*]+)\\*\\*[: \\t]*(.*)$/);
        if (bMatch) {
          parsedItems.push({
            title: bMatch[1].replace(/:$/, "").trim(),
            desc: bMatch[2].trim()
          });
        }
      }

      if (parsedItems.length < 3) {
        return {
          heading: (heading && !heading.toLowerCase().includes("technical")) ? heading : "Why Rockford Property Owners Choose Us",
          items: defaultPillars
        };
      }

      return {
        heading: heading || "Why Rockford Property Owners Choose Us",
        items: parsedItems
      };
    }
"""

anchor_helper = "    function parseServicesFromContent(rawSec) {"
if anchor_helper in code:
    code = code.replace(anchor_helper, parse_why_helper + "\n" + anchor_helper)
    print("5. Added parseWhyUsFromContent helper.")
else:
    print("Warning: anchor_helper not found!")

# 5. Insert dedicated branch for Why Choose Us right after branch D (Intro)
target_after_d = "        // E. STEP-BY-STEP PROCESS SECTION (HOW IT WORKS STEP LIST)"

why_us_branch = """        // D2. WHY CHOOSE US / TRUST PILLARS SECTION (SECTION 4 - CORNERSTONE .wcp-section)
        else if (key.includes('why-us') || key.includes('why_us') || key.includes('why-choose') || key.includes('why_choose')) {
          if (sectionVariants.why === 'cornerstone') {
            const whyData = parseWhyUsFromContent(rawSec, pageKey);
            const wcpIcons = [
              `<svg viewBox="0 0 24 24"><path d="M12 3 4 6v5c0 5.25 3.5 10.15 8 11.35C16.5 21.15 20 16.25 20 11V6L12 3Z" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"></path><path d="m9 12 2 2 4-4" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"></path></svg>`,
              `<svg viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="1.2"></rect><path d="M8 7h8M8 11h8M8 15h5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"></path></svg>`,
              `<svg viewBox="0 0 24 24"><path d="M13 2 4.5 13.5H12L11 22l8.5-11.5H12.5L13 2Z" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round" stroke-linecap="round"></path></svg>`,
              `<svg viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5V21a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V10.5Z" fill="currentColor" opacity="0.15" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"></path><circle cx="12" cy="13" r="2" fill="none" stroke="currentColor" stroke-width="1.3"></circle><path d="M12 15v3" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"></path></svg>`
            ];

            const colCount = whyData.items.length === 3 ? 3 : (whyData.items.length === 2 ? 2 : 4);
            const gridStyle = `grid-template-columns: repeat(${colCount}, minmax(0, 1fr));`;

            let cardsHtml = '';
            whyData.items.forEach((item, idx) => {
              const iconSvg = wcpIcons[idx % wcpIcons.length];
              cardsHtml += `
                <div class="wcp-card">
                  <div class="wcp-icon" aria-hidden="true">
                    ${iconSvg}
                  </div>
                  <h3 class="wcp-title" contenteditable="true">${item.title}</h3>
                  <div class="wcp-line"></div>
                  <p class="wcp-text" contenteditable="true">${item.desc}</p>
                </div>
              `;
            });

            html += `
              <section class="wcp-section" id="sec-${key}">
                <div class="wcp-container">
                  <h2 class="wcp-heading" contenteditable="true">${whyData.heading}</h2>
                  <div class="wcp-grid" style="${gridStyle}">
                    ${cardsHtml}
                  </div>
                </div>
              </section>
            `;
          } else {
            // Kadence Standard Why Us Section
            html += `
              <section class="section" style="background-color: var(--surface-container-low);" id="sec-${key}">
                <div class="container">
                  <div style="max-width: 860px; margin: 0 auto;">
                    ${secHTML}
                  </div>
                </div>
              </section>
            `;
          }
        }
"""

if target_after_d in code:
    code = code.replace(target_after_d, why_us_branch + "\n        " + target_after_d)
    print("6. Added dedicated Why Choose Us branch in renderCurrentPage().")
else:
    print("Warning: target_after_d not found!")

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved generate_studio_builder_v4.py successfully!")
