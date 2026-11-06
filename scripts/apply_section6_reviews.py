import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Reviews CSS right before .proc-section
test_css = """
    /* ========================================================
       CORNERSTONE CUSTOMER REVIEWS / SOCIAL PROOF (SECTION 6)
       ======================================================== */
    .test-section {
      width: 100%;
      padding: 84px 24px 80px;
      background: linear-gradient(180deg, var(--surface-container-low) 0%, var(--background) 100%);
      position: relative;
    }
    .test-container {
      max-width: 1200px;
      margin: 0 auto;
    }
    .test-header {
      text-align: center;
      margin-bottom: 52px;
    }
    .test-eyebrow {
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
    .test-eyebrow svg {
      width: 14px;
      height: 14px;
      fill: currentColor;
    }
    .test-heading {
      color: var(--on-surface);
      font-size: clamp(24px, 2.8vw, 36px);
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.02em;
      margin: 0 0 14px 0;
    }
    .test-subtitle {
      color: var(--on-surface-variant);
      font-size: 15px;
      line-height: 1.6;
      margin: 0 auto;
      max-width: 680px;
    }
    .test-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 24px;
    }
    .test-card {
      position: relative;
      display: flex;
      flex-direction: column;
      padding: 36px 30px;
      background: #ffffff;
      border: 1px solid var(--outline-variant);
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
      transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }
    .test-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.09);
      border-color: rgba(var(--accent-rgb), 0.4);
    }
    .test-stars {
      display: flex;
      gap: 4px;
      color: #f59e0b;
      margin-bottom: 20px;
    }
    .test-stars svg {
      width: 18px;
      height: 18px;
      fill: currentColor;
    }
    .test-quote {
      color: var(--on-surface-variant);
      font-size: 14.5px;
      line-height: 1.68;
      margin: 0 0 24px 0;
      flex-grow: 1;
    }
    .test-meta {
      display: flex;
      align-items: center;
      gap: 14px;
      border-top: 1px solid var(--outline-variant);
      padding-top: 20px;
    }
    .test-avatar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 44px;
      height: 44px;
      flex: 0 0 44px;
      border-radius: 50%;
      background: rgba(var(--accent-rgb), 0.12);
      color: var(--secondary-container);
      font-weight: 800;
      font-size: 14px;
      border: 1px solid rgba(var(--accent-rgb), 0.25);
    }
    .test-author-info {
      flex: 1;
      min-width: 0;
    }
    .test-author-name {
      display: block;
      color: var(--on-surface);
      font-size: 15px;
      font-weight: 800;
      line-height: 1.3;
      margin: 0 0 3px 0;
    }
    .test-author-loc {
      display: block;
      color: var(--on-surface-variant);
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    @media (max-width: 960px) {
      .test-grid {
        grid-template-columns: 1fr;
        gap: 20px;
      }
      .test-card {
        padding: 28px 22px;
      }
    }
"""

anchor_css = "    /* ========================================================\n       CORNERSTONE STEP-BY-STEP PROCESS SECTION (SECTION 5)"
if anchor_css in code:
    code = code.replace(anchor_css, test_css + "\n" + anchor_css)
    print("1. Injected Reviews CSS.")
else:
    print("Warning: anchor_css not found!")

# 2. Add Section 6 in Sidebar right after Section 5
old_s5_sidebar = """        <!-- Section 5: Step-by-Step Process Variant -->
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

new_s6_sidebar = old_s5_sidebar + """

        <!-- Section 6: Customer Reviews & Social Proof Variant -->
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

if old_s5_sidebar in code:
    code = code.replace(old_s5_sidebar, new_s6_sidebar)
    print("2. Added Section 6 in sidebar.")
else:
    print("Warning: old_s5_sidebar not found!")

# 3. Update sectionVariants state & setSectionVariant function
target_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      why: "cornerstone",
      process: "cornerstone",
      reviews: "cards"
    };"""

replacement_sec_state = """    let sectionVariants = {
      hero: "denton",
      intro: "denton",
      services: "cornerstone",
      why: "cornerstone",
      process: "cornerstone",
      reviews: "cornerstone"
    };"""

if target_sec_state in code:
    code = code.replace(target_sec_state, replacement_sec_state)
    print("3. Updated sectionVariants.reviews state.")
else:
    print("Warning: target_sec_state not found!")

target_set_var = """        why: ['kadence', 'cornerstone'],
        process: ['kadence', 'cornerstone'],
        reviews: ['cards', 'split', 'wall']"""

replacement_set_var = """        why: ['kadence', 'cornerstone'],
        process: ['kadence', 'cornerstone'],
        reviews: ['kadence', 'cornerstone']"""

if target_set_var in code:
    code = code.replace(target_set_var, replacement_set_var)
    print("4. Updated setSectionVariant handler to include reviews.")
else:
    print("Warning: target_set_var not found!")

# 4. Add parseReviewsFromContent helper
parse_rev_helper = """
    function parseReviewsFromContent(rawSec) {
      const defaultReviews = [
        {
          author: "Marcus T.",
          loc: "Verified Homeowner • Loves Park (Forest Hills)",
          initials: "MT",
          quote: "After purchasing our 1970s ranch home in Loves Park, the dust blowing through registers was unbearable. They showed us endoscope video before and after. The difference was night and day, and our furnace runs noticeably quieter."
        },
        {
          author: "Sarah and David K.",
          loc: "Verified Homeowners • Rockford (Edgebrook)",
          initials: "SK",
          quote: "We got caught two years ago by a forty-nine dollar coupon company that blew dust into our master bedroom. These technicians brought real truck-mounted 5,000 CFM negative air equipment and sealed every register. Honest flat rate honored."
        },
        {
          author: "Elena R.",
          loc: "Verified Homeowner • Machesney Park",
          initials: "ER",
          quote: "Called early in the morning after noticing a musty odor whenever the air conditioner cycled on. They had a certified two-man crew at our home by early afternoon. The botanical spray smelled natural and clean."
        }
      ];

      if (!rawSec) return { heading: "What Winnebago County Homeowners Say", subhead: "Authentic reviews from verified local property owners.", reviews: defaultReviews };

      const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
      const lines = cleanMd.split(String.fromCharCode(10));
      let heading = "";
      let subhead = "";
      const parsedReviews = [];

      let curRev = null;

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        if (!heading && line.startsWith("## ")) {
          heading = line.replace(/^##[ \\t]+/, "").trim();
          continue;
        }

        if (!subhead && !curRev && !line.startsWith("#")) {
          subhead = line;
          continue;
        }

        // Match H3: ### Location or Author
        if (line.startsWith("### ")) {
          if (curRev && curRev.quote) parsedReviews.push(curRev);
          const locOrName = line.replace(/^###[ \\t]+/, "").trim();
          curRev = {
            loc: locOrName,
            author: "",
            initials: "",
            quote: ""
          };
          continue;
        }

        if (line.toLowerCase().startsWith("rating:")) {
          continue;
        }

        if (line.toLowerCase().startsWith("reviewer:")) {
          if (curRev) {
            const fullReviewer = line.replace(/^reviewer:\\s*/i, "").trim();
            const parts = fullReviewer.split(",");
            curRev.author = parts[0].trim();
            if (parts.length > 1) {
              curRev.loc = parts.slice(1).join(",").trim() + (curRev.loc ? " • " + curRev.loc : "");
            }
            const nameParts = curRev.author.split(/\\s+/).filter(Boolean);
            if (nameParts.length >= 2) {
              curRev.initials = (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase();
            } else if (nameParts.length === 1) {
              curRev.initials = nameParts[0].substring(0, 2).toUpperCase();
            }
          }
          continue;
        }

        // Append to quote
        if (curRev) {
          if (!curRev.quote) {
            curRev.quote = line;
          } else {
            curRev.quote += " " + line;
          }
        }
      }

      if (curRev && curRev.quote) parsedReviews.push(curRev);

      parsedReviews.forEach(r => {
        if (!r.author) {
          r.author = r.loc || "Verified Customer";
          r.loc = "Verified Customer";
        }
        if (!r.initials) {
          const parts = r.author.split(/\\s+/).filter(Boolean);
          r.initials = parts.length >= 2 ? (parts[0][0] + parts[1][0]).toUpperCase() : r.author.substring(0, 2).toUpperCase();
        }
      });

      return {
        heading: heading || "What Property Owners Say",
        subhead: subhead || "Authentic customer reviews from verified local service calls.",
        reviews: parsedReviews.length > 0 ? parsedReviews : defaultReviews
      };
    }
"""

anchor_rev_helper = "    function parseProcessFromContent(rawSec) {"
if anchor_rev_helper in code:
    code = code.replace(anchor_rev_helper, parse_rev_helper + "\n" + anchor_rev_helper)
    print("5. Added parseReviewsFromContent helper.")
else:
    print("Warning: anchor_rev_helper not found!")

# 5. Replace Branch H in renderCurrentPage()
old_branch_h = """        // H. CUSTOMER REVIEWS / SOCIAL PROOF (5-STAR CARDS)
        else if (key.includes('testimonial') || key.includes('reviews')) {
          html += `
            <section class="section" style="background-color: var(--surface-container-low);" id="sec-${key}">
              <div class="container">
                <h2 contenteditable="true">What Rockford and Winnebago County Customers Say</h2>
                <div class="grid md:grid-cols-3" style="margin-top: var(--stack-md);">
                  <div class="card">
                    <div style="color: #F59E0B; font-size: 1.1rem; margin-bottom: 8px;">★★★★★</div>
                    <p contenteditable="true">"Marcus and Dave were courteous, professional, and walked me through the video camera footage. The air inside our Rolling Green home feels noticeable crisper!"</p>
                    <strong style="font-size: 13px; color: var(--primary);">— Sarah M., Rolling Green Neighborhood</strong>
                  </div>
                  <div class="card">
                    <div style="color: #F59E0B; font-size: 1.1rem; margin-bottom: 8px;">★★★★★</div>
                    <p contenteditable="true">"Super thorough negative air hookup. No dust escaped into our living room, and the botanical fog left a clean herbal scent. Highly recommend!"</p>
                    <strong style="font-size: 13px; color: var(--primary);">— James T., Loves Park Resident</strong>
                  </div>
                  <div class="card">
                    <div style="color: #F59E0B; font-size: 1.1rem; margin-bottom: 8px;">★★★★★</div>
                    <p contenteditable="true">"Honest flat-rate quote from start to finish. They showed up right on time, explained the NADCA standards, and gave us complete peace of mind."</p>
                    <strong style="font-size: 13px; color: var(--primary);">— Brian K., Machesney Park Homeowner</strong>
                  </div>
                </div>
              </div>
            </section>
          `;
        }"""

new_branch_h = """        // H. CUSTOMER REVIEWS / SOCIAL PROOF (SECTION 6 - CORNERSTONE .test-section)
        else if (key.includes('testimonial') || key.includes('reviews')) {
          const revData = parseReviewsFromContent(rawSec);

          if (sectionVariants.reviews === 'cornerstone') {
            const starSvg = `<svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
            const fiveStars = starSvg + starSvg + starSvg + starSvg + starSvg;

            let cardsHtml = '';
            revData.reviews.forEach(rev => {
              cardsHtml += `
                <article class="test-card">
                  <div class="test-stars">
                    ${fiveStars}
                  </div>
                  <p class="test-quote" contenteditable="true">"${rev.quote}"</p>
                  <div class="test-meta">
                    <div class="test-avatar">${rev.initials}</div>
                    <div class="test-author-info">
                      <span class="test-author-name" contenteditable="true">${rev.author}</span>
                      <span class="test-author-loc" contenteditable="true">${rev.loc}</span>
                    </div>
                  </div>
                </article>
              `;
            });

            html += `
              <section class="test-section" id="sec-${key}">
                <div class="test-container">
                  <div class="test-header">
                    <span class="test-eyebrow">
                      <svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                      Customer Reviews
                    </span>
                    <h2 class="test-heading" contenteditable="true">${revData.heading}</h2>
                    <p class="test-subtitle" contenteditable="true">${revData.subhead}</p>
                  </div>

                  <div class="test-grid">
                    ${cardsHtml}
                  </div>
                </div>
              </section>
            `;
          } else {
            // Kadence Standard Reviews Cards
            let cardsHtml = '';
            revData.reviews.forEach(rev => {
              cardsHtml += `
                <div class="card">
                  <div style="color: #F59E0B; font-size: 1.1rem; margin-bottom: 8px;">★★★★★</div>
                  <p contenteditable="true">"${rev.quote}"</p>
                  <strong style="font-size: 13px; color: var(--primary);">— ${rev.author}, ${rev.loc}</strong>
                </div>
              `;
            });

            html += `
              <section class="section" style="background-color: var(--surface-container-low);" id="sec-${key}">
                <div class="container">
                  <h2 contenteditable="true">${revData.heading}</h2>
                  <div class="grid md:grid-cols-3" style="margin-top: var(--stack-md);">
                    ${cardsHtml}
                  </div>
                </div>
              </section>
            `;
          }
        }"""

if old_branch_h in code:
    code = code.replace(old_branch_h, new_branch_h)
    print("6. Replaced Branch H with Cornerstone Reviews implementation.")
else:
    print("Warning: old_branch_h not found!")

with open(script_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved generate_studio_builder_v4.py successfully!")

