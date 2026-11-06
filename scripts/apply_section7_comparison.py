import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Comparison CSS right before .test-section
comp_css = """
    /* ========================================================
       CORNERSTONE COMPARISON BENCHMARK TABLE (SECTION 7)
       ======================================================== */
    .comp-section {
      width: 100%;
      padding: 84px 24px 80px;
      background: #091730;
      color: #ffffff;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .comp-section::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image: radial-gradient(circle, rgba(255, 255, 255, 0.06) 1.5px, transparent 1.5px);
      background-size: 24px 24px;
      pointer-events: none;
    }
    .comp-container {
      max-width: 1100px;
      margin: 0 auto;
      position: relative;
      z-index: 1;
    }
    .comp-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.1);
      color: var(--secondary-container);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 20px;
      border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .comp-eyebrow svg {
      width: 14px;
      height: 14px;
    }
    .comp-heading {
      color: #ffffff;
      font-size: clamp(24px, 3.2vw, 36px);
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.02em;
      margin: 0 0 16px 0;
    }
    .comp-text {
      color: #cbd5e1;
      font-size: 15px;
      line-height: 1.65;
      margin: 0 auto 36px;
      max-width: 760px;
    }
    .comp-table-wrap {
      width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      border-radius: 18px;
      border: 1px solid rgba(255, 255, 255, 0.14);
      margin: 0 0 24px 0;
      background: rgba(11, 26, 44, 0.7);
      backdrop-filter: blur(14px);
      box-shadow: 0 24px 48px rgba(0, 0, 0, 0.35);
    }
    .comp-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      min-width: 720px;
    }
    .comp-table th {
      padding: 18px 20px;
      font-size: 12.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.04);
      border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }
    .comp-table th.col-proflow {
      color: #ffffff;
      background: rgba(var(--accent-rgb), 0.18);
      border-bottom: 2px solid var(--secondary-container);
    }
    .comp-table td {
      padding: 16px 20px;
      font-size: 14px;
      line-height: 1.5;
      color: #cbd5e1;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }
    .comp-table tr:last-child td {
      border-bottom: none;
    }
    .comp-table tr:nth-child(even) td {
      background: rgba(255, 255, 255, 0.02);
    }
    .comp-table tr td.cell-feature {
      font-weight: 700;
      color: #ffffff;
      width: 26%;
    }
    .comp-table tr td.cell-proflow {
      background: rgba(var(--accent-rgb), 0.08);
      font-weight: 700;
      color: #ffffff;
      width: 32%;
      border-left: 1px solid rgba(var(--accent-rgb), 0.2);
      border-right: 1px solid rgba(var(--accent-rgb), 0.2);
    }
    .comp-table tr td.cell-other {
      width: 21%;
    }
    .pill-yes {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 9999px;
      background: rgba(74, 222, 128, 0.18);
      color: #4ade80;
      border: 1px solid rgba(74, 222, 128, 0.35);
      font-size: 11.5px;
      font-weight: 800;
      margin-right: 6px;
    }
    .pill-warn {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 9999px;
      background: rgba(250, 204, 21, 0.18);
      color: #facc15;
      border: 1px solid rgba(250, 204, 21, 0.35);
      font-size: 11.5px;
      font-weight: 800;
      margin-right: 6px;
    }
    .pill-no {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 9999px;
      background: rgba(248, 113, 113, 0.18);
      color: #f87171;
      border: 1px solid rgba(248, 113, 113, 0.35);
      font-size: 11.5px;
      font-weight: 800;
      margin-right: 6px;
    }
    .comp-legend {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 22px;
      flex-wrap: wrap;
      color: #94a3b8;
      font-size: 12.5px;
      margin-bottom: 32px;
    }
    .comp-legend-item {
      display: inline-flex;
      align-items: center;
      gap: 7px;
    }
    .comp-btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 15px 34px;
      border-radius: 14px;
      background: var(--secondary-container);
      color: #0b1f5e;
      font-weight: 800;
      font-size: 15px;
      text-decoration: none;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
      transition: all 0.25s ease;
    }
    .comp-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 16px 36px rgba(var(--accent-rgb), 0.4);
      filter: brightness(1.1);
    }
    .comp-btn svg {
      width: 18px;
      height: 18px;
      stroke: currentColor;
      fill: none;
      stroke-width: 2.5;
    }
"""

anchor_css = "    /* ========================================================\n       CORNERSTONE CUSTOMER REVIEWS / SOCIAL PROOF (SECTION 6)"
if anchor_css in code:
    code = code.replace(anchor_css, comp_css + "\n" + anchor_css)
    print("1. Injected Comparison Table CSS.")
else:
    print("Warning: anchor_css not found!")

# 2. Add Section 7 in Sidebar right after Section 6
old_s6_sidebar = """        <!-- Section 6: Customer Reviews & Social Proof Variant -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Section 6: Customer Reviews</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="reviews-var-kadence" onclick="setSectionVariant('reviews', 'kadence')">Kadence Standard</button>
            <button class="variation-pill active" id="reviews-var-cornerstone" onclick="setSectionVariant('reviews', 'cornerstone')">Cornerstone</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            5-star rating cards with initials avatar &amp; verified neighborhood tags.
          </div>
        </div>"""

new_s7_sidebar = old_s6_sidebar + """

        <!-- Section 7: Comparison Benchmark Table Variant -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Section 7: Comparison Table</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="comp-var-kadence" onclick="setSectionVariant('comp', 'kadence')">Kadence Standard</button>
            <button class="variation-pill active" id="comp-var-cornerstone" onclick="setSectionVariant('comp', 'cornerstone')">Cornerstone</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            Dark frosted glass comparison table with highlighted column &amp; glowing pills.
          </div>
        </div>"""

if old_s6_sidebar in code:
    code = code.replace(old_s6_sidebar, new_s7_sidebar)
    print("2. Added Section 7 in sidebar.")
else:
    print("Warning: old_s6_sidebar not found!")

# 3. Update sectionVariants state & setSectionVariant function
target_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      why: "cornerstone",
      process: "cornerstone",
      reviews: "cornerstone"
    };"""

replacement_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      why: "cornerstone",
      process: "cornerstone",
      reviews: "cornerstone",
      comp: "cornerstone"
    };"""

if target_sec_state in code:
    code = code.replace(target_sec_state, replacement_sec_state)
    print("3. Updated sectionVariants.comp state.")
else:
    print("Warning: target_sec_state not found!")

target_set_var = """        process: ['kadence', 'cornerstone'],
        reviews: ['kadence', 'cornerstone']"""

replacement_set_var = """        process: ['kadence', 'cornerstone'],
        reviews: ['kadence', 'cornerstone'],
        comp: ['kadence', 'cornerstone']"""

if target_set_var in code:
    code = code.replace(target_set_var, replacement_set_var)
    print("4. Updated setSectionVariant handler to include comp.")
else:
    print("Warning: target_set_var not found!")

# 4. Add parseComparisonFromContent helper
parse_comp_helper = """
    function parseComparisonFromContent(rawSec) {
      const defaultData = {
        heading: "The Quality Standard of Care: Comparison Benchmark",
        subhead: "Before hiring an air duct cleaning contractor in Rockford, examine how certified full-system decontamination compares against discount coupon companies and DIY attempts.",
        headers: ["Inspection & Cleaning Factor", "Rockford Air Duct Pros", "Budget Forty-Nine Dollar Coupon Vans", "DIY Shop-Vac Attempt"],
        rows: [
          {
            feature: "Vacuum Airflow Capacity",
            pro: "5,000 CFM Sealed Negative Air",
            other: "Portable 150 CFM Shop-Vac",
            diy: "Under 100 CFM Standard Vacuum"
          },
          {
            feature: "Mechanical Brush Agitation",
            pro: "360-Degree Rotary Motorized Scrubbing",
            other: "Compressed Air Wand Only",
            diy: "Manual Hand Brush Near Register Grille"
          },
          {
            feature: "Technician Accreditation",
            pro: "NADCA ASCS Certified Technicians",
            other: "Uncertified Subcontractors",
            diy: "Uncertified Homeowner"
          },
          {
            feature: "Live Video Verification",
            pro: "High-Definition Borescope Before & After",
            other: "Refuse to Show Duct Interior",
            diy: "Limited Flashlight View Only"
          },
          {
            feature: "Pricing Transparency",
            pro: "Upfront Flat-Rate Quotes with Zero Surcharges",
            other: "Low Bait-and-Switch Rate with High Upsells",
            diy: "Tool Rental Costs & Damaged Duct Vents"
          }
        ]
      };

      if (!rawSec) return defaultData;

      const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
      const lines = cleanMd.split(String.fromCharCode(10));
      let heading = "";
      let subhead = "";
      const tableLines = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        if (!heading && line.startsWith("## ")) {
          heading = line.replace(/^##[ \\t]+/, "").trim();
          continue;
        }

        if (!subhead && !line.startsWith("#") && !line.startsWith("|")) {
          subhead = line;
          continue;
        }

        if (line.startsWith("|")) {
          tableLines.push(line);
        }
      }

      if (tableLines.length < 3) return defaultData;

      const headerCells = tableLines[0].split("|").map(c => c.trim()).filter(Boolean);
      const rows = [];

      for (let i = 2; i < tableLines.length; i++) {
        const cells = tableLines[i].split("|").map(c => c.trim()).filter(Boolean);
        if (cells.length >= 2) {
          rows.push({
            feature: cells[0],
            pro: cells[1] || "",
            other: cells[2] || "",
            diy: cells[3] || ""
          });
        }
      }

      return {
        heading: heading || defaultData.heading,
        subhead: subhead || defaultData.subhead,
        headers: headerCells.length >= 3 ? headerCells : defaultData.headers,
        rows: rows.length > 0 ? rows : defaultData.rows
      };
    }
"""

anchor_comp_helper = "    function parseReviewsFromContent(rawSec) {"
if anchor_comp_helper in code:
    code = code.replace(anchor_comp_helper, parse_comp_helper + "\n" + anchor_comp_helper)
    print("5. Added parseComparisonFromContent helper.")
else:
    print("Warning: anchor_comp_helper not found!")

# 5. Replace Branch F in renderCurrentPage()
old_branch_f = """        // F. PREMIUM COMPARISON TABLE (HOSTINGER HIGHLIGHT-COL TABLE)
        else if (key.includes('comparison')) {
          html += `
            <section class="section" style="background-color: var(--surface-container-low);" id="sec-${key}">
              <div class="container">
                <div style="text-align: center; max-width: 750px; margin: 0 auto var(--stack-lg);">
                  <h2 contenteditable="true">Why Rockford Homeowners and Contractors Choose Us</h2>
                  <p contenteditable="true">Compare our verified mechanical source removal standards against uncertified bait-and-switch operations.</p>
                </div>

                <div style="overflow-x: auto; margin-top: var(--stack-md);">
                  <table class="premium-table">
                    <thead>
                      <tr>
                        <th>Standard Feature</th>
                        <th class="highlight-col">Rockford Air Duct Pros</th>
                        <th>$99 "Blow & Go" Operators</th>
                        <th>DIY Shop Vac Attempt</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Source Removal Protocol</td>
                        <td class="highlight-col"><span class="check-icon">✓</span> NADCA ACR 2021 Standard</td>
                        <td><span class="cross-icon">✕</span> Uncertified blow & go</td>
                        <td>N/A</td>
                      </tr>
                      <tr>
                        <td>Vacuum Suction Velocity</td>
                        <td class="highlight-col"><span class="check-icon">✓</span> 5,000 CFM Negative Pressure</td>
                        <td><span class="cross-icon">✕</span> Handheld carpet vacuum</td>
                        <td><span class="cross-icon">✕</span> 120 CFM shop vac</td>
                      </tr>
                      <tr>
                        <td>Borescope Video Inspection</td>
                        <td class="highlight-col"><span class="check-icon">✓</span> Before & After Recorded Proof</td>
                        <td><span class="cross-icon">✕</span> None (bait-and-switch)</td>
                        <td><span class="cross-icon">✕</span> None</td>
                      </tr>
                      <tr>
                        <td>Antimicrobial Sanitizer</td>
                        <td class="highlight-col"><span class="check-icon">✓</span> EPA-Registered Botanical</td>
                        <td><span class="cross-icon">✕</span> Synthetic perfumed mist</td>
                        <td><span class="cross-icon">✕</span> None</td>
                      </tr>
                      <tr>
                        <td>Transparent Flat-Rate Quote</td>
                        <td class="highlight-col"><span class="check-icon">✓</span> Written binding quote</td>
                        <td><span class="cross-icon">✕</span> Hidden per-vent charges</td>
                        <td>Equipment rental + time</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          `;
        }"""

new_branch_f = """        // F. PREMIUM COMPARISON TABLE (SECTION 7 - CORNERSTONE .comp-section)
        else if (key.includes('comparison') || key.includes('compare')) {
          const compData = parseComparisonFromContent(rawSec);

          if (sectionVariants.comp === 'cornerstone') {
            const h0 = compData.headers[0] || 'Feature / Standard';
            const h1 = compData.headers[1] || `${pageData.company_name || 'Rockford Air Duct Pros'}`;
            const h2 = compData.headers[2] || 'Discount Contractors';
            const h3 = compData.headers[3] || 'DIY Attempt';

            let rowsHtml = '';
            compData.rows.forEach(r => {
              rowsHtml += `
                <tr>
                  <td class="cell-feature" contenteditable="true">${r.feature}</td>
                  <td class="cell-proflow" contenteditable="true"><span class="pill-yes">✓ Standard</span> ${r.pro}</td>
                  <td class="cell-other" contenteditable="true"><span class="pill-warn">! Risk</span> ${r.other}</td>
                  <td class="cell-other" contenteditable="true"><span class="pill-no">✗ Limited</span> ${r.diy}</td>
                </tr>
              `;
            });

            html += `
              <section class="comp-section" id="sec-${key}">
                <div class="comp-container">
                  <span class="comp-eyebrow">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M16 3h5v5M8 21H3v-5M12 12V3M12 12v18M12 12H3M12 12h18"></path>
                    </svg>
                    Compare Standards
                  </span>
                  <h2 class="comp-heading" contenteditable="true">${compData.heading}</h2>
                  <p class="comp-text" contenteditable="true">${compData.subhead}</p>

                  <div class="comp-table-wrap">
                    <table class="comp-table">
                      <thead>
                        <tr>
                          <th>${h0}</th>
                          <th class="col-proflow">${h1}</th>
                          <th>${h2}</th>
                          <th>${h3}</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${rowsHtml}
                      </tbody>
                    </table>
                  </div>

                  <div class="comp-legend">
                    <span class="comp-legend-item"><span class="pill-yes">✓ Standard</span> Certified NADCA source removal protocol</span>
                    <span class="comp-legend-item"><span class="pill-warn">! Risk</span> Subcontracted, unverified or coupon bait-and-switch</span>
                    <span class="comp-legend-item"><span class="pill-no">✗ Limited</span> Dangerous blowback or equipment damage</span>
                  </div>

                  <div style="margin-top: 14px;">
                    <a href="tel:${pageData.phone || '(815) 555-0142'}" class="comp-btn">
                      <span>Call Now: ${pageData.phone || '(815) 555-0142'}</span>
                      <svg viewBox="0 0 24 24"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                    </a>
                  </div>
                </div>
              </section>
            `;
          } else {
            // Kadence Standard Comparison Table
            let rowsHtml = '';
            compData.rows.forEach(r => {
              rowsHtml += `
                <tr>
                  <td>${r.feature}</td>
                  <td class="highlight-col"><span class="check-icon">✓</span> ${r.pro}</td>
                  <td><span class="cross-icon">✕</span> ${r.other}</td>
                  <td>${r.diy}</td>
                </tr>
              `;
            });

            html += `
              <section class="section" style="background-color: var(--surface-container-low);" id="sec-${key}">
                <div class="container">
                  <div style="text-align: center; max-width: 750px; margin: 0 auto var(--stack-lg);">
                    <h2 contenteditable="true">${compData.heading}</h2>
                    <p contenteditable="true">${compData.subhead}</p>
                  </div>

                  <div style="overflow-x: auto; margin-top: var(--stack-md);">
                    <table class="premium-table">
                      <thead>
                        <tr>
                          <th>${compData.headers[0] || 'Feature'}</th>
                          <th class="highlight-col">${compData.headers[1] || 'Our Team'}</th>
                          <th>${compData.headers[2] || 'Discount Contractors'}</th>
                          <th>${compData.headers[3] || 'DIY'}</th>
                        </tr>
                      </thead>
                      <tbody>
                        ${rowsHtml}
                      </tbody>
                    </table>
                  </div>
                </div>
              </section>
            `;
          }
        }"""

if old_branch_f in code:
    code = code.replace(old_branch_f, new_branch_f)
    print("6. Replaced Branch F with Cornerstone Comparison implementation.")
else:
    print("Warning: old_branch_f not found!")

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved generate_studio_builder_v4.py successfully!")

