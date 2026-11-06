import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Service Area CSS right before .comp-section
aws_css = """
    /* ========================================================
       CORNERSTONE SERVICE AREA & DISPATCH COVERAGE (SECTION 8)
       ======================================================== */
    .aws-section {
      width: 100%;
      padding: 84px 24px 80px;
      background: var(--surface-container-low);
      position: relative;
    }
    .aws-container {
      max-width: 1200px;
      margin: 0 auto;
      text-align: center;
    }
    .aws-eyebrow {
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
    .aws-eyebrow svg {
      width: 16px;
      height: 16px;
    }
    .aws-heading {
      color: var(--on-surface);
      font-size: clamp(24px, 3vw, 38px);
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.02em;
      margin: 0 0 16px 0;
    }
    .aws-subheading {
      color: var(--on-surface-variant);
      font-size: 15.5px;
      line-height: 1.65;
      margin: 0 auto 40px;
      max-width: 720px;
    }
    .aws-map-container {
      max-width: 1000px;
      width: 100%;
      height: 380px;
      margin: 0 auto 48px;
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
      border: 1px solid var(--outline-variant);
      background: #e2e8f0;
    }
    .aws-layout {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 24px;
      margin-bottom: 40px;
      text-align: center;
    }
    @keyframes awsSlowSpin {
      100% { transform: rotate(360deg); }
    }
    .aws-card {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 32px 22px 28px;
      overflow: hidden;
      border: 1px solid var(--outline-variant);
      border-radius: 20px;
      background: #ffffff;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.04);
      text-decoration: none;
      transition: transform 0.35s ease, box-shadow 0.35s ease, border-color 0.35s ease;
      height: 100%;
    }
    .aws-card-primary {
      grid-column: span 2;
      background: #ffffff;
    }
    .aws-card-secondary {
      grid-column: span 1;
    }
    .aws-card.color-blue   { --card-color: var(--primary);            --card-soft: rgba(var(--accent-rgb), 0.12); }
    .aws-card.color-green  { --card-color: var(--secondary-container);--card-soft: rgba(var(--accent-rgb), 0.12); }
    .aws-card.color-yellow { --card-color: #d97706;                   --card-soft: rgba(217, 119, 6, 0.12); }
    .aws-card.color-purple { --card-color: #7c3aed;                   --card-soft: rgba(124, 58, 237, 0.12); }
    .aws-card.color-teal   { --card-color: #0d9488;                   --card-soft: rgba(13, 148, 136, 0.12); }

    .aws-card::before {
      content: "";
      position: absolute;
      inset: 0;
      opacity: 0;
      background: linear-gradient(150deg, rgba(var(--accent-rgb), 0.08), transparent 50%);
      transition: opacity 0.35s ease;
      pointer-events: none;
    }
    .aws-card::after {
      content: "";
      position: absolute;
      right: 0; bottom: 0; left: 0;
      height: 4px;
      background: var(--card-color);
      transform: scaleX(0.7);
      transform-origin: center;
      transition: transform 0.35s ease;
    }
    .aws-card:hover {
      transform: translateY(-7px);
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.1);
      border-color: rgba(var(--accent-rgb), 0.45);
    }
    .aws-card:hover::before { opacity: 1; }
    .aws-card:hover::after  { transform: scaleX(1); }

    .aws-card__icon {
      position: relative;
      display: grid;
      place-items: center;
      width: 84px;
      height: 84px;
      flex: 0 0 84px;
      margin-bottom: 20px;
      border-radius: 50%;
      background: var(--card-soft);
      color: var(--card-color);
      transition: transform 0.4s ease, box-shadow 0.4s ease;
    }
    .aws-card-primary .aws-card__icon {
      width: 94px;
      height: 94px;
      flex: 0 0 94px;
    }
    .aws-card__icon::before {
      content: "";
      position: absolute;
      inset: 7px;
      border: 1px dashed rgba(var(--accent-rgb), 0.45);
      border-radius: 50%;
      animation: awsSlowSpin 20s linear infinite;
    }
    .aws-card:hover .aws-card__icon {
      transform: translateY(-3px) scale(1.06);
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    }
    .aws-card__icon svg {
      width: 40px;
      height: 40px;
      position: relative;
      z-index: 1;
    }
    .aws-card-primary .aws-card__icon svg {
      width: 46px;
      height: 46px;
    }
    .aws-card__city {
      margin: 0;
      color: var(--on-surface);
      font-size: 19px;
      font-weight: 800;
      line-height: 1.25;
    }
    .aws-card-primary .aws-card__city {
      font-size: 22px;
    }
    .aws-card__line {
      width: 28px;
      height: 3px;
      margin: 12px auto 14px;
      border-radius: 10px;
      background: var(--card-color);
      transition: width 0.35s ease;
    }
    .aws-card:hover .aws-card__line { width: 52px; }
    .aws-card__desc {
      margin: 0 0 14px 0;
      color: var(--on-surface-variant);
      font-size: 13.5px;
      line-height: 1.6;
      flex: 1;
    }
    .aws-card__meta {
      font-size: 12px;
      font-weight: 700;
      color: var(--card-color);
      background: var(--card-soft);
      padding: 4px 12px;
      border-radius: 9999px;
      display: inline-block;
    }
    .aws-card__arrow {
      margin-top: 12px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      font-weight: 800;
      color: var(--secondary-container);
    }
    .aws-card__arrow svg {
      width: 14px;
      height: 14px;
      transition: transform 0.25s ease;
    }
    .aws-card:hover .aws-card__arrow svg {
      transform: translateX(4px);
    }
    .aws-nap-box {
      max-width: 860px;
      margin: 0 auto;
      padding: 22px 30px;
      border-radius: 16px;
      background: #ffffff;
      border: 1px solid var(--outline-variant);
      display: flex;
      justify-content: space-around;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
      font-size: 13.5px;
      color: var(--on-surface-variant);
    }

    @media (max-width: 1024px) {
      .aws-layout {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      .aws-card-primary {
        grid-column: span 2;
      }
    }
    @media (max-width: 640px) {
      .aws-layout {
        grid-template-columns: 1fr;
      }
      .aws-card-primary, .aws-card-secondary {
        grid-column: span 1;
      }
      .aws-map-container {
        height: 280px;
      }
      .aws-nap-box {
        flex-direction: column;
        text-align: center;
      }
    }
"""

anchor_css = "    /* ========================================================\n       CORNERSTONE COMPARISON BENCHMARK TABLE (SECTION 7)"
if anchor_css in code:
    code = code.replace(anchor_css, aws_css + "\n" + anchor_css)
    print("1. Injected Service Area CSS.")
else:
    print("Warning: anchor_css not found!")

# 2. Add Section 8 in Sidebar right after Section 7
old_s7_sidebar = """        <!-- Section 7: Comparison Benchmark Table Variant -->
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

new_s8_sidebar = old_s7_sidebar + """

        <!-- Section 8: Geographic Service Area Variant -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Section 8: Service Area Map</span>
            <span style="font-size: 10px; color: #3b82f6; font-weight:700;">CORNERSTONE</span>
          </label>
          <div class="variation-pill-group">
            <button class="variation-pill" id="area-var-kadence" onclick="setSectionVariant('area', 'kadence')">Kadence Standard</button>
            <button class="variation-pill active" id="area-var-cornerstone" onclick="setSectionVariant('area', 'cornerstone')">Cornerstone</button>
          </div>
          <div style="font-size: 10px; color: var(--app-text-muted); line-height: 1.3; margin-top: 4px;">
            City dispatch card grid with Google Map frame &amp; physical NAP headquarters.
          </div>
        </div>"""

if old_s7_sidebar in code:
    code = code.replace(old_s7_sidebar, new_s8_sidebar)
    print("2. Added Section 8 in sidebar.")
else:
    print("Warning: old_s7_sidebar not found!")

# 3. Update sectionVariants state & setSectionVariant function
target_sec_state = """      reviews: "cornerstone",
      comp: "cornerstone"
    };"""

replacement_sec_state = """      reviews: "cornerstone",
      comp: "cornerstone",
      area: "cornerstone"
    };"""

if target_sec_state in code:
    code = code.replace(target_sec_state, replacement_sec_state)
    print("3. Updated sectionVariants.area state.")
else:
    print("Warning: target_sec_state not found!")

target_set_var = """        reviews: ['kadence', 'cornerstone'],
        comp: ['kadence', 'cornerstone']"""

replacement_set_var = """        reviews: ['kadence', 'cornerstone'],
        comp: ['kadence', 'cornerstone'],
        area: ['kadence', 'cornerstone']"""

if target_set_var in code:
    code = code.replace(target_set_var, replacement_set_var)
    print("4. Updated setSectionVariant handler to include area.")
else:
    print("Warning: target_set_var not found!")

# 4. Add parseServiceAreaFromContent helper
parse_area_helper = """
    function parseServiceAreaFromContent(rawSec, pageKey) {
      const defaultData = {
        heading: "Greater Rockford Service Area and Dispatch Coverage",
        subhead: "Our fleet of specialized negative-air decontamination vehicles is staged daily across Winnebago and Boone counties for prompt same-day and next-day dispatch.",
        primaryCity: {
          name: "Rockford",
          tag: "Winnebago County • Primary Service Hub",
          desc: "Central, East Side, North End, and Midtown. Rapid same-day decontamination with zero travel surcharges.",
          postal: "61101, 61102, 61103, 61104, 61107, 61108, 61109, 61114"
        },
        cities: [
          {
            name: "Loves Park",
            tag: "Winnebago County • Active Service Zone",
            desc: "Forest Hills, Riverside Corridor, and Windsor Road. Under 35-minute mobile dispatch.",
            slug: "air-duct-cleaning-loves-park-il",
            color: "color-green"
          },
          {
            name: "Machesney Park",
            tag: "Winnebago County • Expansion Zone",
            desc: "Harlem Corridor, 173 Commercial Strip, and residential sub-divisions. Fast same-day service.",
            slug: null,
            color: "color-yellow"
          },
          {
            name: "Belvidere",
            tag: "Boone County • Regional Coverage",
            desc: "State Street Corridor, Chrysler plant vicinity, and outlying Boone County homes.",
            slug: null,
            color: "color-purple"
          },
          {
            name: "Cherry Valley",
            tag: "Winnebago County • Rapid Dispatch",
            desc: "Harrison Ave, Perryville Corridor, and Valley Woods residential communities.",
            slug: null,
            color: "color-teal"
          }
        ],
        nap: {
          name: "Rockford Air Duct Pros",
          address: "1111 S Alpine Rd, Rockford, IL 61108",
          phone: "(815) 555-0142",
          hours: "Monday – Saturday: 7:00 AM – 7:00 PM"
        }
      };

      if (!rawSec) return defaultData;

      const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
      const lines = cleanMd.split(String.fromCharCode(10));
      let heading = "";
      let subhead = "";

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        if (!heading && line.startsWith("## ")) {
          heading = line.replace(/^##[ \\t]+/, "").trim();
          continue;
        }

        if (!subhead && !line.startsWith("#") && !line.startsWith("*") && !line.startsWith("-")) {
          subhead = line;
          break;
        }
      }

      return {
        heading: heading || defaultData.heading,
        subhead: subhead || defaultData.subhead,
        primaryCity: defaultData.primaryCity,
        cities: defaultData.cities,
        nap: defaultData.nap
      };
    }
"""

anchor_area_helper = "    function parseComparisonFromContent(rawSec) {"
if anchor_area_helper in code:
    code = code.replace(anchor_area_helper, parse_area_helper + "\n" + anchor_area_helper)
    print("5. Added parseServiceAreaFromContent helper.")
else:
    print("Warning: anchor_area_helper not found!")

# 5. Add Branch J2 for Service Area right after Branch I (FAQ)
target_after_faq = "        // J. BOTTOM CTA SECTION (DARK CHARCOAL GRADIENT)"

service_area_branch = """        // J2. GEOGRAPHIC SERVICE AREA & DISPATCH COVERAGE (SECTION 8 - CORNERSTONE .aws-section)
        else if (key.includes('service-area') || key.includes('service_area') || key.includes('area_nap') || key.includes('coverage')) {
          const areaData = parseServiceAreaFromContent(rawSec, currentActivePage);

          if (sectionVariants.area === 'cornerstone') {
            const pCity = areaData.primaryCity;
            const mapQuery = encodeURIComponent(`${pageData.city || 'Rockford'}, IL`);

            let secondaryCardsHtml = '';
            areaData.cities.forEach(c => {
              const linkAttr = c.slug ? `onclick="loadSelectedPage('${c.slug}')" style="cursor: pointer;"` : '';
              const linkArrow = c.slug ? `
                <span class="aws-card__arrow">
                  <span>Explore City Page</span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                </span>
              ` : `
                <span class="aws-card__arrow" style="opacity: 0.7;">
                  <span>Mobile Dispatch Available</span>
                </span>
              `;

              secondaryCardsHtml += `
                <div class="aws-card aws-card-secondary ${c.color}" ${linkAttr}>
                  <div class="aws-card__icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                  </div>
                  <h3 class="aws-card__city" contenteditable="true">${c.name}</h3>
                  <div class="aws-card__line"></div>
                  <p class="aws-card__desc" contenteditable="true">${c.desc}</p>
                  <span class="aws-card__meta">${c.tag}</span>
                  ${linkArrow}
                </div>
              `;
            });

            html += `
              <section class="aws-section" id="sec-${key}">
                <div class="aws-container">
                  <div style="margin-bottom: 48px;">
                    <span class="aws-eyebrow">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 10c0 6-8 13-8 13s-8-7-8-13a8 8 0 0 1 16 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                      </svg>
                      Where We Serve
                    </span>
                    <h2 class="aws-heading" contenteditable="true">${areaData.heading}</h2>
                    <p class="aws-subheading" contenteditable="true">${areaData.subhead}</p>
                  </div>

                  <!-- Google Maps Verified SAB Frame (CS-11) -->
                  <div class="aws-map-container">
                    <iframe src="https://maps.google.com/maps?q=${mapQuery}&t=&z=11&ie=UTF8&iwloc=&output=embed" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
                  </div>

                  <!-- Location Cards Matrix -->
                  <div class="aws-layout">
                    <!-- Primary City Card (Span 2) -->
                    <div class="aws-card aws-card-primary color-blue">
                      <div class="aws-card__icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                          <polyline points="9 22 9 12 15 12 15 22"></polyline>
                        </svg>
                      </div>
                      <h3 class="aws-card__city" contenteditable="true">${pCity.name}</h3>
                      <div class="aws-card__line"></div>
                      <p class="aws-card__desc" contenteditable="true">${pCity.desc}</p>
                      <span class="aws-card__meta">${pCity.tag}</span>
                      <div style="font-size: 11px; color: var(--on-surface-variant); margin-top: 10px; font-weight: 600;">
                        Serving Zip Codes: ${pCity.postal}
                      </div>
                    </div>

                    ${secondaryCardsHtml}
                  </div>

                  <!-- Physical Dispatch Headquarters NAP Box -->
                  <div class="aws-nap-box">
                    <div><strong>🏢 Company:</strong> ${areaData.nap.name}</div>
                    <div><strong>📍 Address:</strong> ${areaData.nap.address}</div>
                    <div><strong>📞 Phone:</strong> <a href="tel:${areaData.nap.phone}" style="color: var(--primary); font-weight: 700;">${areaData.nap.phone}</a></div>
                    <div><strong>⏱ Hours:</strong> ${areaData.nap.hours}</div>
                  </div>
                </div>
              </section>
            `;
          } else {
            // Kadence Standard Service Area Section
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

if target_after_faq in code:
    code = code.replace(target_after_faq, service_area_branch + "\n        " + target_after_faq)
    print("6. Added Branch J2 for Service Area in renderCurrentPage().")
else:
    print("Warning: target_after_faq not found!")

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved generate_studio_builder_v4.py successfully!")

