import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

pos1 = code.find('// F. PREMIUM COMPARISON TABLE')
pos2 = code.find('// G. BEFORE & AFTER SECTION')

new_branch_f = """// F. PREMIUM COMPARISON TABLE (SECTION 7 - CORNERSTONE .comp-section)
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
        }

        """

if pos1 != -1 and pos2 != -1:
    code = code[:pos1] + new_branch_f + code[pos2:]
    print("Replaced Branch F successfully!")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(code)
else:
    print("Failed to find bounds for Branch F!")

