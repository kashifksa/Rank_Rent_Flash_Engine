import re
import os

path = r"D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add Denton Hero CSS
denton_css = """
    /* Denton ProFlow Hero Section Styles */
    .denton-hero-text h1 {
      color: #ffffff !important;
      font-size: 2.85rem !important;
      font-weight: 800 !important;
      line-height: 1.2 !important;
      text-shadow: 0 2px 10px rgba(0,0,0,0.6) !important;
      margin-bottom: 16px !important;
      letter-spacing: -0.01em !important;
    }
    .denton-hero-text p {
      color: rgba(255, 255, 255, 0.95) !important;
      font-size: 1.15rem !important;
      line-height: 1.65 !important;
      max-width: 820px !important;
      margin: 0 auto 12px !important;
      text-shadow: 0 1px 5px rgba(0,0,0,0.5) !important;
    }
    .denton-hero-text strong {
      color: #ffffff !important;
    }
    .btn-denton-call:hover {
      background: #2B6CB0 !important;
      border-color: #3182CE !important;
      transform: translateY(-2px) !important;
      box-shadow: 0 6px 24px rgba(43, 108, 176, 0.65) !important;
    }
    @media (max-width: 768px) {
      .denton-proof-bar {
        grid-template-columns: 1fr 1fr !important;
        gap: 10px !important;
      }
      .denton-hero-text h1 {
        font-size: 2rem !important;
      }
    }
    @media (max-width: 480px) {
      .denton-proof-bar {
        grid-template-columns: 1fr !important;
      }
    }
"""

code = code.replace("/* Canvas Texture Styles */", denton_css + "\n    /* Canvas Texture Styles */")

# 2. Update Sidebar to include the 2 Hero Design Options
old_hero_sidebar = """        <!-- Unified Hero Architecture Lock -->
        <div class="form-group">
          <label class="form-label" style="display:flex; justify-content:space-between; align-items:center;">
            <span>Hero Architecture</span>
            <span style="font-size: 10px; color: #10b981; font-weight:700;">🔒 UNIFIED</span>
          </label>
          <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 6px; padding: 8px 10px; font-size: 11px; color: #cbd5e1; line-height: 1.4;">
            <strong style="color: #10b981;">Standardized Homepage Geometry</strong>: Exact 650px desktop height, 2-column split, 3:2 image ratio &amp; Hostinger V-divider enforced across Home, Services &amp; Locations.
          </div>
        </div>"""

new_hero_sidebar = """        <!-- Hero Architecture Selector -->
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

code = code.replace(old_hero_sidebar, new_hero_sidebar)

# 3. Update Hero Section Rendering Logic to support both 'split' and 'denton'
old_hero_render = """        // A. HERO SECTION — UNIFIED HOMEPAGE GEOMETRY (IDENTICAL ACROSS HOME, SERVICES, LOCATIONS)
        if (key.includes('hero') || key.includes('identity')) {
          const heroImgSrc = sectionImage ? `${pageData.img_dir}/${sectionImage.filename}` : "images/homepage/rockford-air-duct-pros-service-van-hero.webp";
          const heroImgAlt = sectionImage ? sectionImage.alt_text : "Rockford Air Duct Pros Service Van";

          // Strict adherence to Homepage 650px Split Hero with Hostinger V-Divider
          html += `
            <section class="hero" id="sec-${key}">
              <div class="container hero-content" style="position: relative; z-index: 2;">
                <div class="hero-text">
                  ${secHTML}
                  <div style="margin-top: var(--stack-md); display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                    <a href="tel:${pageData.phone || '(815) 555-0142'}" class="btn btn-primary ${pulseClass}">Call ${pageData.phone || '(815) 555-0142'}</a>
                    <a href="#booking" class="btn btn-secondary">Get Free Estimate</a>
                  </div>
                </div>
                <div class="hero-image">
                  <img src="${heroImgSrc}" alt="${heroImgAlt}" style="border-radius: var(--radius-md); box-shadow: var(--shadow-raised); width: 100%; aspect-ratio: 3/2; object-fit: cover;">
                </div>
              </div>
              
              <!-- Signature Hostinger V-Shape Geometric Divider -->
              <div class="hero-divider">
                <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                  <path d="M0,60 L600,120 L1200,60 L1200,120 L0,120 Z" class="shape-fill"></path>
                  <path d="M0,60 L600,120 L1200,60" class="shape-stroke"></path>
                </svg>
              </div>
            </section>
          `;
        }"""

new_hero_render = """        // A. HERO SECTION — SUPPORTS HOSTINGER V-SPLIT OR DENTON PROFLOW FULL-BLEED
        if (key.includes('hero') || key.includes('identity')) {
          const heroImgSrc = sectionImage ? `${pageData.img_dir}/${sectionImage.filename}` : "images/homepage/rockford-air-duct-pros-service-van-hero.webp";
          const heroImgAlt = sectionImage ? sectionImage.alt_text : "Rockford Air Duct Pros Service Van";

          if (sectionVariants.hero === 'denton') {
            // DENTON PROFLOW HERO DESIGN (Full-Bleed Photographic Hero with 4-Column Proof Bar)
            html += `
              <section class="hero-denton-wrap" id="sec-${key}" style="position: relative; background: url('${heroImgSrc}') center/cover no-repeat; min-height: 640px; display: flex; flex-direction: column; justify-content: flex-end; padding: 100px 0 36px; overflow: hidden;">
                <!-- Dark Midnight Navy Vignette Overlay -->
                <div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(11, 31, 94, 0.45) 0%, rgba(15, 23, 42, 0.78) 55%, rgba(10, 15, 29, 0.95) 100%); z-index: 1;"></div>
                
                <div class="container" style="position: relative; z-index: 2; width: 100%; text-align: center; max-width: 960px; margin: 0 auto;">
                  <div class="denton-hero-text">
                    ${secHTML}
                  </div>
                  
                  <div style="margin-top: 24px;">
                    <a href="tel:${pageData.phone || '(815) 555-0142'}" class="btn btn-denton-call ${pulseClass}" style="background: rgba(26, 32, 44, 0.88); color: #ffffff; border: 2px solid #2B6CB0; padding: 14px 34px; font-size: 16px; font-weight: 700; border-radius: 8px; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 20px rgba(43, 108, 176, 0.45); transition: all 0.2s ease;">
                      <span>📞 Call Now: ${pageData.phone || '(815) 555-0142'}</span>
                    </a>
                  </div>

                  <!-- Integrated 4-Column Proof Bar (sprinklerrepairdentontx.com structure) -->
                  <div class="denton-proof-bar" style="background: rgba(11, 31, 94, 0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 14px 20px; margin-top: 40px; display: grid; grid-template-columns: repeat(4, 1fr); align-items: center; gap: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.35);">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 6px;">
                      <span style="color: #F59E0B; font-size: 14px; letter-spacing: 1px;">★★★★★</span>
                      <span style="color: #ffffff; font-size: 12px; font-weight: 700; text-transform: uppercase;">5-Star Rated</span>
                    </div>
                    <div style="color: #ffffff; font-size: 12px; font-weight: 700; text-transform: uppercase; border-left: 1px solid rgba(255,255,255,0.15); padding-left: 12px; text-align: center;">
                      NADCA Certified
                    </div>
                    <div style="color: #ffffff; font-size: 12px; font-weight: 700; text-transform: uppercase; border-left: 1px solid rgba(255,255,255,0.15); padding-left: 12px; text-align: center;">
                      Local Experts – Not a Franchise
                    </div>
                    <div style="color: #ffffff; font-size: 12px; font-weight: 700; text-transform: uppercase; border-left: 1px solid rgba(255,255,255,0.15); padding-left: 12px; text-align: center;">
                      No Hidden Fees, Ever
                    </div>
                  </div>
                </div>
              </section>
            `;
          } else {
            // Standard Hostinger 650px Split Hero with V-Divider
            html += `
              <section class="hero" id="sec-${key}">
                <div class="container hero-content" style="position: relative; z-index: 2;">
                  <div class="hero-text">
                    ${secHTML}
                    <div style="margin-top: var(--stack-md); display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                      <a href="tel:${pageData.phone || '(815) 555-0142'}" class="btn btn-primary ${pulseClass}">Call ${pageData.phone || '(815) 555-0142'}</a>
                      <a href="#booking" class="btn btn-secondary">Get Free Estimate</a>
                    </div>
                  </div>
                  <div class="hero-image">
                    <img src="${heroImgSrc}" alt="${heroImgAlt}" style="border-radius: var(--radius-md); box-shadow: var(--shadow-raised); width: 100%; aspect-ratio: 3/2; object-fit: cover;">
                  </div>
                </div>
                
                <!-- Signature Hostinger V-Shape Geometric Divider -->
                <div class="hero-divider">
                  <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                    <path d="M0,60 L600,120 L1200,60 L1200,120 L0,120 Z" class="shape-fill"></path>
                    <path d="M0,60 L600,120 L1200,60" class="shape-stroke"></path>
                  </svg>
                </div>
              </section>
            `;
          }
        }"""

code = code.replace(old_hero_render, new_hero_render)

# 4. Update setSectionVariant in JS to update pill buttons
old_set_variant = """    function setSectionVariant(section, variant) {
      sectionVariants[section] = variant;
      const group = {
        hero: ['split', 'banner', 'alert'],
        services: ['grid', 'bento', 'strips'],
        reviews: ['cards', 'split', 'wall']
      }[section];"""

new_set_variant = """    function setSectionVariant(section, variant) {
      sectionVariants[section] = variant;
      const group = {
        hero: ['split', 'denton'],
        services: ['grid', 'bento', 'strips'],
        reviews: ['cards', 'split', 'wall']
      }[section];"""

code = code.replace(old_set_variant, new_set_variant)

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated generate_studio_builder_v4.py with Denton Hero section successfully")

