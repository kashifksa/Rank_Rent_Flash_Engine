import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Process CSS right before .wcp-section
proc_css = """
    /* ========================================================
       CORNERSTONE STEP-BY-STEP PROCESS SECTION (SECTION 5)
       ======================================================== */
    .proc-section {
      width: 100%;
      padding: 80px 24px 76px;
      background: var(--background);
      position: relative;
    }
    .proc-container {
      max-width: 1200px;
      margin: 0 auto;
    }
    .proc-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
      gap: 48px;
      align-items: center;
    }
    .proc-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      border-radius: 9999px;
      background: rgba(var(--accent-rgb), 0.12);
      color: var(--secondary-container);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 16px;
    }
    .proc-heading {
      color: var(--on-surface);
      font-size: clamp(24px, 2.6vw, 36px);
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.02em;
      margin: 0 0 16px 0;
    }
    .proc-subhead {
      color: var(--on-surface-variant);
      font-size: 15px;
      line-height: 1.65;
      margin: 0 0 32px 0;
      max-width: 620px;
    }
    .proc-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: relative;
    }
    .proc-item {
      display: flex;
      gap: 18px;
      align-items: flex-start;
      position: relative;
      padding: 16px 20px 16px 14px;
      border-radius: 14px;
      background: transparent;
      border: 1px solid transparent;
      transition: all 0.3s ease;
    }
    .proc-item:hover {
      background: #ffffff;
      border-color: var(--outline-variant);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
      transform: translateX(4px);
    }
    .proc-badge-col {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 0 0 44px;
    }
    .proc-badge {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: rgba(var(--accent-rgb), 0.12);
      color: var(--secondary-container);
      border: 2px solid var(--secondary-container);
      display: grid;
      place-items: center;
      font-size: 15px;
      font-weight: 800;
      transition: all 0.3s ease;
      z-index: 2;
    }
    .proc-item:hover .proc-badge {
      background: var(--secondary-container);
      color: #ffffff;
      transform: scale(1.08);
      box-shadow: 0 6px 16px rgba(var(--accent-rgb), 0.3);
    }
    .proc-track {
      position: absolute;
      top: 44px;
      bottom: -20px;
      width: 2px;
      background: repeating-linear-gradient(to bottom, var(--outline-variant) 0, var(--outline-variant) 4px, transparent 4px, transparent 8px);
      z-index: 1;
    }
    .proc-item:last-child .proc-track {
      display: none;
    }
    .proc-body {
      flex: 1;
    }
    .proc-title-wrap {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 6px;
    }
    .proc-title {
      margin: 0;
      color: var(--on-surface);
      font-size: 16.5px;
      font-weight: 800;
      line-height: 1.35;
    }
    .proc-window {
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 9999px;
      background: var(--surface-container-low);
      color: var(--on-surface-variant);
      border: 1px solid var(--outline-variant);
      white-space: nowrap;
    }
    .proc-desc {
      margin: 0;
      color: var(--on-surface-variant);
      font-size: 14px;
      line-height: 1.6;
    }
    .proc-visual {
      position: relative;
      height: 100%;
      min-height: 520px;
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.12);
      border: 1px solid var(--outline-variant);
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      background-size: cover;
      background-position: center;
    }
    .proc-visual::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, rgba(11, 26, 44, 0.92) 0%, rgba(11, 26, 44, 0.35) 55%, transparent 100%);
      pointer-events: none;
    }
    .proc-visual-card {
      position: relative;
      z-index: 2;
      padding: 28px 24px;
      color: #ffffff;
    }
    .proc-visual-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(8px);
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 12px;
      border: 1px solid rgba(255, 255, 255, 0.25);
    }
    .proc-visual-title {
      margin: 0 0 6px 0;
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
    }
    .proc-visual-desc {
      margin: 0;
      font-size: 13.5px;
      line-height: 1.5;
      color: rgba(255, 255, 255, 0.85);
    }

    @media (max-width: 1024px) {
      .proc-grid {
        grid-template-columns: 1fr;
        gap: 40px;
      }
      .proc-visual {
        min-height: 380px;
      }
    }
    @media (max-width: 640px) {
      .proc-section {
        padding: 56px 18px;
      }
      .proc-item {
        padding: 12px 10px;
        gap: 14px;
      }
      .proc-badge {
        width: 38px;
        height: 38px;
        font-size: 13px;
      }
      .proc-track {
        top: 38px;
      }
    }
"""

anchor_css = "    /* ========================================================\n       CORNERSTONE WHY CHOOSE US / TRUST PILLARS (SECTION 4)"
if anchor_css in code:
    code = code.replace(anchor_css, proc_css + "\n" + anchor_css)
    print("1. Injected Process CSS.")
else:
    print("Warning: anchor_css not found!")

# 2. Add Section 5: Process Protocol in Sidebar right after Section 4
old_s4_sidebar = """        <!-- Section 4: Why Choose Us / Trust Pillars Variant -->
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

new_s5_sidebar = old_s4_sidebar + """

        <!-- Section 5: Step-by-Step Process Variant -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Section 5: Process Protocol</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="process-var-kadence" onclick="setSectionVariant('process', 'kadence')">Kadence Standard</button>
            <button class="variation-pill active" id="process-var-cornerstone" onclick="setSectionVariant('process', 'cornerstone')">Cornerstone</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            Connected timeline steps with numbered badges &amp; full-height photo card.
          </div>
        </div>"""

if old_s4_sidebar in code:
    code = code.replace(old_s4_sidebar, new_s5_sidebar)
    print("2. Added Section 5 in sidebar.")
else:
    print("Warning: old_s4_sidebar not found!")

# 3. Update sectionVariants state & setSectionVariant function
target_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      why: "cornerstone",
      reviews: "cards"
    };"""

replacement_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      why: "cornerstone",
      process: "cornerstone",
      reviews: "cards"
    };"""

if target_sec_state in code:
    code = code.replace(target_sec_state, replacement_sec_state)
    print("3. Updated sectionVariants.process state.")
else:
    print("Warning: target_sec_state not found!")

target_set_var = """        services: ['grid', 'cornerstone', 'bento', 'strips'],
        why: ['kadence', 'cornerstone'],
        reviews: ['cards', 'split', 'wall']"""

replacement_set_var = """        services: ['grid', 'cornerstone', 'bento', 'strips'],
        why: ['kadence', 'cornerstone'],
        process: ['kadence', 'cornerstone'],
        reviews: ['cards', 'split', 'wall']"""

if target_set_var in code:
    code = code.replace(target_set_var, replacement_set_var)
    print("4. Updated setSectionVariant handler to include process.")
else:
    print("Warning: target_set_var not found!")

# 4. Add parseProcessFromContent helper
parse_proc_helper = """
    function parseProcessFromContent(rawSec) {
      if (!rawSec) return { heading: "Our 4-Step Cleaning Protocol", subhead: "", steps: [] };

      const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
      const lines = cleanMd.split(String.fromCharCode(10));
      let heading = "";
      let subhead = "";
      const steps = [];

      let currentStep = null;

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        if (!heading && line.startsWith("## ")) {
          heading = line.replace(/^##[ \\t]+/, "").trim();
          continue;
        }

        if (!subhead && !currentStep && !line.startsWith("#") && !line.startsWith("|") && !line.startsWith("-") && !line.startsWith("*") && !line.match(/^\\d+\\./)) {
          subhead = line;
          continue;
        }

        // A. Match table row: | **Phase X: Title** | Description | Window |
        if (line.startsWith("|") && !line.includes("---")) {
          const cells = line.split("|").map(c => c.trim()).filter(Boolean);
          if (cells.length >= 2) {
            const titleRaw = cells[0].replace(/\\*\\*/g, "").trim();
            if (titleRaw.toLowerCase().includes("phase") && !titleRaw.match(/\\d+/) && !cells[0].includes("**")) {
              continue; // Table header row
            }
            if (titleRaw.toLowerCase().includes("stage") && !titleRaw.match(/\\d+/) && !cells[0].includes("**")) {
              continue; // Table header row
            }
            if (titleRaw.toLowerCase().includes("service stage") || titleRaw.toLowerCase().includes("project phase")) {
              continue;
            }
            const cleanTitle = titleRaw.replace(/^(?:Phase|Stage|Step)\\s*\\d+:\\s*/i, "").trim();
            steps.push({
              title: cleanTitle || titleRaw,
              desc: cells[1].trim(),
              window: cells[2] ? cells[2].trim() : ""
            });
            continue;
          }
        }

        // B. Match H3: ### 1. Title or ### Title
        const h3Match = line.match(/^###[ \\t]+(?:\\d+\\.?\\s*)?(.*)$/);
        if (h3Match) {
          if (currentStep) steps.push(currentStep);
          currentStep = {
            title: h3Match[1].replace(/^\\d+\\.\\s*/, "").trim(),
            desc: ""
          };
          continue;
        }

        // C. Match numbered list: 1. **Title:** desc or 1. Title
        const numMatch = line.match(/^(\\d+)\\.\\s+(?:\\*\\*([^*:]+):?\\*\\*)?\\s*(.*)$/);
        if (numMatch && !line.startsWith("#")) {
          if (currentStep) steps.push(currentStep);
          currentStep = {
            title: numMatch[2] ? numMatch[2].trim() : `Step ${numMatch[1]}`,
            desc: numMatch[3] ? numMatch[3].trim() : ""
          };
          continue;
        }

        // Append to current step description
        if (currentStep) {
          if (!currentStep.desc) {
            currentStep.desc = line;
          } else {
            currentStep.desc += " " + line;
          }
        }
      }

      if (currentStep) steps.push(currentStep);

      return { heading: heading || "Our Step-by-Step Protocol", subhead, steps };
    }
"""

anchor_proc_helper = "    function parseWhyUsFromContent(rawSec, pageKey) {"
if anchor_proc_helper in code:
    code = code.replace(anchor_proc_helper, parse_proc_helper + "\n" + anchor_proc_helper)
    print("5. Added parseProcessFromContent helper.")
else:
    print("Warning: anchor_proc_helper not found!")

# 5. Replace Branch E in renderCurrentPage()
old_branch_e = """        // E. STEP-BY-STEP PROCESS SECTION (HOW IT WORKS STEP LIST)
        else if (key.includes('process')) {
          html += `
            <section class="section" id="sec-${key}">
              <div class="container">
                <div style="text-align: center; max-width: 750px; margin: 0 auto var(--stack-lg);">
                  <h2 contenteditable="true">How Our 4-Step Cleaning Process Works</h2>
                  <p contenteditable="true">NADCA certified source removal ensures your ductwork is mechanically scrubbed bare with zero secondary contamination.</p>
                </div>
                <div style="max-width: 820px; margin: 0 auto;">
                  <ol class="step-list">
                    <li class="step-item">
                      <h3 contenteditable="true">Pre-Service Borescope Diagnostic</h3>
                      <p contenteditable="true">Our certified technicians guide a high-resolution video camera through supply and return duct runs to pinpoint dust buildup, pet dander, and airflow restrictions.</p>
                    </li>
                    <li class="step-item">
                      <h3 contenteditable="true">Negative Air Vacuum Containment</h3>
                      <p contenteditable="true">We seal supply registers with magnetic dampers and connect a 5,000 CFM HEPA negative air system to your plenum, pulling high velocity suction through your home.</p>
                    </li>
                    <li class="step-item">
                      <h3 contenteditable="true">High-Torque Mechanical Agitation</h3>
                      <p contenteditable="true">Rotating nylon brush heads and forward-discharging pneumatic air whips scour the interior galvanized steel surfaces to dislodge caked furnace soot and debris.</p>
                    </li>
                    <li class="step-item">
                      <h3 contenteditable="true">Botanical Fogging & Post Verification</h3>
                      <p contenteditable="true">An EPA-registered thyme-derived botanical fog is aerosolized through your trunk lines followed by side-by-side borescope video confirmation.</p>
                    </li>
                  </ol>
                </div>
              </div>
            </section>
          `;
        }"""

new_branch_e = """        // E. STEP-BY-STEP PROCESS SECTION (SECTION 5 - CORNERSTONE SPLIT TIMELINE)
        else if (key.includes('process')) {
          const procData = parseProcessFromContent(rawSec);

          if (sectionVariants.process === 'cornerstone') {
            // Find section image or high-quality photographic fallback
            const procImgPath = (sectionImage ? `${pageData.img_dir}/${sectionImage.filename}` : null) || 
                                (pageData.images && pageData.images.find(img => img.slot.includes('process') || img.slot.includes('tech') || img.slot.includes('inspect')) ? `${pageData.img_dir}/${pageData.images.find(img => img.slot.includes('process') || img.slot.includes('tech') || img.slot.includes('inspect')).filename}` : null) || 
                                "images/homepage/commercial-negative-air-vacuum.webp";
            const procImgAlt = sectionImage ? sectionImage.alt_text : "NADCA Certified Decontamination Equipment";

            let stepsHtml = '';
            procData.steps.forEach((step, idx) => {
              const stepNum = String(idx + 1).padStart(2, '0');
              const windowBadge = step.window ? `<span class="proc-window">⏱ ${step.window}</span>` : '';
              stepsHtml += `
                <div class="proc-item">
                  <div class="proc-badge-col">
                    <div class="proc-badge">${stepNum}</div>
                    <div class="proc-track"></div>
                  </div>
                  <div class="proc-body">
                    <div class="proc-title-wrap">
                      <h3 class="proc-title" contenteditable="true">${step.title}</h3>
                      ${windowBadge}
                    </div>
                    <p class="proc-desc" contenteditable="true">${step.desc}</p>
                  </div>
                </div>
              `;
            });

            html += `
              <section class="proc-section" id="sec-${key}">
                <div class="proc-container">
                  <div class="proc-grid">
                    
                    <!-- Left Column: Timeline Steps -->
                    <div>
                      <div class="proc-eyebrow">
                        <span>●</span> Step-by-Step Protocol
                      </div>
                      <h2 class="proc-heading" contenteditable="true">${procData.heading}</h2>
                      <p class="proc-subhead" contenteditable="true">${procData.subhead || 'Engineered for complete contaminant extraction under negative air pressure with zero interior blowback.'}</p>

                      <div class="proc-list">
                        ${stepsHtml}
                      </div>

                      <div style="margin-top: 32px;">
                        <a href="tel:${pageData.phone || '(815) 555-0142'}" class="btn btn-primary" style="display: inline-flex; align-items: center; gap: 8px; padding: 13px 28px; font-size: 15px;">
                          <span>📞</span> Call Now: ${pageData.phone || '(815) 555-0142'}
                        </a>
                      </div>
                    </div>

                    <!-- Right Column: Full-Height Photographic Card -->
                    <div class="proc-visual" style="background-image: url('${procImgPath}');">
                      <div class="proc-visual-card">
                        <div class="proc-visual-badge">
                          <span>🛡️</span> NADCA ACR-2021 Standard
                        </div>
                        <h4 class="proc-visual-title" contenteditable="true">Certified Source Removal</h4>
                        <p class="proc-visual-desc" contenteditable="true">Every service call is conducted with industrial 5,000 CFM negative containment and documented with endoscope camera verification.</p>
                      </div>
                    </div>

                  </div>
                </div>
              </section>
            `;
          } else {
            // Kadence Standard Process List
            let stepsHtml = '';
            procData.steps.forEach((step, idx) => {
              stepsHtml += `
                <li class="step-item">
                  <h3 contenteditable="true">${step.title}</h3>
                  <p contenteditable="true">${step.desc}</p>
                </li>
              `;
            });

            html += `
              <section class="section" id="sec-${key}">
                <div class="container">
                  <div style="text-align: center; max-width: 750px; margin: 0 auto var(--stack-lg);">
                    <h2 contenteditable="true">${procData.heading}</h2>
                    <p contenteditable="true">${procData.subhead || 'NADCA certified source removal ensures your ductwork is mechanically scrubbed bare.'}</p>
                  </div>
                  <div style="max-width: 820px; margin: 0 auto;">
                    <ol class="step-list">
                      ${stepsHtml}
                    </ol>
                  </div>
                </div>
              </section>
            `;
          }
        }"""

if old_branch_e in code:
    code = code.replace(old_branch_e, new_branch_e)
    print("6. Replaced Branch E with Cornerstone Process implementation.")
else:
    print("Warning: old_branch_e not found!")

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved generate_studio_builder_v4.py successfully!")

