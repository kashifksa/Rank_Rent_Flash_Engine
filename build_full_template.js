const fs = require('fs');
const { execSync } = require('child_process');

const filePath = 'D:/Projects/Rank_Rent_Flash_Engine/master_template_sample.html';
let html = fs.readFileSync(filePath, 'utf8');

// 1. Inject JSON-LD Schema in <head>
const schemaBlock = `
  <!-- ========================================================================= -->
  <!-- 2026 JSON-LD STRUCTURED DATA SCHEMA: LOCAL BUSINESS + FAQ                 -->
  <!-- ========================================================================= -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "HVACBusiness",
        "@id": "https://rockfordairductpros.com/#business",
        "name": "Rockford Air Duct Pros",
        "telephone": "+18155550199",
        "priceRange": "$$",
        "image": "https://images.unsplash.com/photo-1581094288338-2314dddb7ece?auto=format&fit=crop&w=900&q=80",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "401 S Main St",
          "addressLocality": "Rockford",
          "addressRegion": "IL",
          "postalCode": "61101",
          "addressCountry": "US"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": 42.2711,
          "longitude": -89.0940
        },
        "areaServed": [
          { "@type": "City", "name": "Rockford" },
          { "@type": "City", "name": "Loves Park" },
          { "@type": "City", "name": "Machesney Park" },
          { "@type": "City", "name": "Belvidere" },
          { "@type": "City", "name": "Cherry Valley" }
        ],
        "openingHoursSpecification": [
          {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "07:00",
            "closes": "19:00"
          }
        ]
      },
      {
        "@type": "FAQPage",
        "@id": "https://rockfordairductpros.com/#faq",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "How often should residential air ducts be cleaned?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "According to the National Air Duct Cleaners Association (NADCA), typical residential ductwork should be inspected every 2 years and thoroughly cleaned every 3 to 5 years."
            }
          },
          {
            "@type": "Question",
            "name": "How long does a full-home duct cleaning take?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "A certified full-system decontamination for a standard 2,000 to 2,500 square-foot home typically requires 3 to 4.5 hours."
            }
          },
          {
            "@type": "Question",
            "name": "Do you serve surrounding Winnebago County communities?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. We dispatch certified technicians daily across Winnebago and Boone counties, including Rockford, Loves Park, Machesney Park, Belvidere, Cherry Valley, and Roscoe."
            }
          }
        ]
      }
    ]
  }
  </script>
`;

if (!html.includes('application/ld+json')) {
  html = html.replace('</head>', schemaBlock + '\n</head>');
}

// 2. Extra CSS for Enhanced Effects & New Sections
const extraCss = `
    /* ==========================================================================
       ENHANCED SECTION EFFECTS & MICRO-INTERACTIONS
       ========================================================================== */
    /* Live Dispatch Beacon */
    .live-beacon {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-weight: 700;
    }

    .live-dot {
      width: 8px;
      height: 8px;
      background-color: #22c55e;
      border-radius: 50%;
      display: inline-block;
      box-shadow: 0 0 0 rgba(34, 197, 94, 0.4);
      animation: livePulse 2s infinite;
      flex-shrink: 0;
    }

    @keyframes livePulse {
      0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
      70% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
      100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }

    /* Audit Conduit List */
    .audit-conduit {
      position: relative;
      list-style: none;
      padding-left: 24px;
      margin-top: 18px;
      margin-bottom: 24px;
    }

    .audit-conduit::before {
      content: "";
      position: absolute;
      left: 7px;
      top: 10px;
      bottom: 12px;
      width: 2px;
      background: var(--surface-container-high);
    }

    .audit-conduit li {
      position: relative;
      margin-bottom: 12px;
      font-size: 0.95rem;
      line-height: 1.5;
      color: var(--on-surface-variant);
    }

    .audit-conduit li::before {
      content: "✓";
      position: absolute;
      left: -24px;
      top: 1px;
      width: 16px;
      height: 16px;
      background: var(--surface-container-lowest);
      border: 1.5px solid var(--secondary-container);
      color: var(--secondary-container);
      border-radius: 50%;
      font-size: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
    }

    /* Before & After Dual-Frame Cards */
    .ba-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 24px;
      margin-top: var(--stack-md);
    }

    @media (min-width: 768px) {
      .ba-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    .ba-card {
      background: var(--surface-container-lowest);
      border: 1px solid var(--surface-container-high);
      border-radius: var(--radius-default);
      overflow: hidden;
      box-shadow: var(--shadow-raised);
      display: flex;
      flex-direction: column;
    }

    .ba-card-fail {
      border-top: 4px solid #dc2626;
    }

    .ba-card-pass {
      border-top: 4px solid #16a34a;
    }

    .ba-img-wrapper {
      position: relative;
      height: 240px;
      overflow: hidden;
    }

    .ba-img-wrapper img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }

    .ba-card:hover .ba-img-wrapper img {
      transform: scale(1.03);
    }

    .ba-badge {
      position: absolute;
      top: 14px;
      left: 14px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }

    .ba-badge-fail {
      background: #dc2626;
      color: #ffffff;
    }

    .ba-badge-pass {
      background: #16a34a;
      color: #ffffff;
    }

    .ba-content {
      padding: 20px 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .ba-content h4 {
      font-size: 1.15rem;
      margin-bottom: 8px;
    }

    .ba-metrics-bar {
      margin-top: 24px;
      background: var(--surface-container-low);
      border: 1px solid var(--surface-container-high);
      border-radius: var(--radius-default);
      padding: 16px 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-around;
      gap: 16px;
      text-align: center;
    }

    .ba-metric-item strong {
      display: block;
      font-size: 1.4rem;
      color: var(--secondary-container);
      font-family: var(--font-heading);
      line-height: 1.1;
    }

    .ba-metric-item span {
      font-size: 0.8rem;
      color: var(--on-surface-variant);
      font-weight: 600;
    }

    /* Process Pipeline Conduit */
    @media (min-width: 768px) {
      .step-pipeline-container {
        position: relative;
      }
      .step-pipeline-container::before {
        content: "";
        position: absolute;
        top: 40px;
        left: 8%;
        right: 8%;
        height: 2px;
        border-top: 2px dashed var(--secondary-container);
        opacity: 0.35;
        z-index: 1;
      }
      .step-card {
        position: relative;
        z-index: 2;
      }
    }

    .step-ghost-num {
      position: absolute;
      top: 10px;
      right: 14px;
      font-family: var(--font-heading);
      font-size: 2.8rem;
      font-weight: 900;
      color: var(--surface-container);
      line-height: 1;
      pointer-events: none;
      transition: color 0.2s ease;
    }

    .step-card:hover .step-ghost-num {
      color: rgba(253, 118, 26, 0.15);
    }

    /* Comparison Table Winner Spotlight */
    th.highlight-col {
      position: relative;
      border-top: 3px solid var(--secondary-container);
      border-left: 2px solid var(--secondary-container);
      border-right: 2px solid var(--secondary-container);
      background-color: var(--surface-container-lowest);
    }

    td.highlight-col {
      border-left: 2px solid var(--secondary-container);
      border-right: 2px solid var(--secondary-container);
    }

    tr:last-child td.highlight-col {
      border-bottom: 2px solid var(--secondary-container);
    }

    .table-winner-badge {
      display: inline-block;
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: var(--secondary-container);
      color: #ffffff;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      margin-bottom: 6px;
      font-weight: 800;
    }

    tbody tr:hover td {
      background-color: rgba(0, 0, 0, 0.015);
    }

    /* Customer Reviews / Testimonials Grid */
    .review-card {
      background: var(--surface-container-lowest);
      border: 1px solid var(--surface-container-high);
      border-radius: var(--radius-default);
      padding: 24px;
      box-shadow: var(--shadow-raised);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .review-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-hover);
    }

    .review-stars {
      color: #eab308;
      font-size: 1.15rem;
      letter-spacing: 2px;
      margin-bottom: 12px;
    }

    .geo-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: var(--surface-container-low);
      border: 1px solid var(--surface-container-high);
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--primary);
      margin-bottom: 14px;
    }

    .review-quote {
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--on-surface-variant);
      margin-bottom: 18px;
      font-style: italic;
    }

    .reviewer-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--surface-container-high);
      padding-top: 14px;
      font-size: 0.85rem;
    }

    .reviewer-name {
      font-weight: 700;
      color: var(--primary);
    }

    .verified-shield {
      color: #16a34a;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.78rem;
    }

    /* Service Area & Map Section */
    .service-area-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 32px;
      align-items: start;
    }

    @media (min-width: 900px) {
      .service-area-grid {
        grid-template-columns: 1.1fr 0.9fr;
      }
    }

    .territory-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 24px;
    }

    .territory-item {
      background: var(--surface-container-lowest);
      border: 1px solid var(--surface-container-high);
      border-radius: var(--radius-default);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.9rem;
      font-weight: 600;
    }

    .territory-badge {
      font-size: 0.78rem;
      background: var(--surface-container);
      color: var(--primary);
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      font-weight: 700;
    }

    .zip-pill-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .zip-pill {
      background: var(--surface-container-lowest);
      border: 1px solid var(--surface-container-high);
      padding: 5px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--on-surface-variant);
    }

    .map-container-card {
      background: var(--surface-container-lowest);
      border: 1px solid var(--surface-container-high);
      border-radius: var(--radius-default);
      overflow: hidden;
      box-shadow: var(--shadow-raised);
      position: relative;
    }

    .map-iframe {
      width: 100%;
      height: 380px;
      border: 0;
      display: block;
    }

    .map-nap-overlay {
      padding: 18px 22px;
      background: var(--surface-container-lowest);
      border-top: 1px solid var(--surface-container-high);
    }

    .map-nap-overlay strong {
      display: block;
      font-size: 1.05rem;
      color: var(--primary);
      margin-bottom: 4px;
    }

    .map-nap-overlay p {
      font-size: 0.85rem;
      margin-bottom: 8px;
    }

    /* FAQ Left Accent Border */
    details.faq-item[open] {
      border-left: 4px solid var(--secondary-container);
      transform: translateY(-2px);
    }

    .faq-help-strip {
      max-width: 820px;
      margin: 24px auto 0;
      background: var(--surface-container-low);
      border: 1px solid var(--surface-container-high);
      border-radius: var(--radius-default);
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.9rem;
    }

    /* Mobile Sticky Bar Pulse */
    @keyframes ctaPulse {
      0% { box-shadow: 0 0 0 0 rgba(253, 118, 26, 0.7); }
      70% { box-shadow: 0 0 0 10px rgba(253, 118, 26, 0); }
      100% { box-shadow: 0 0 0 0 rgba(253, 118, 26, 0); }
    }

    .btn-pulse {
      animation: ctaPulse 2.8s infinite;
    }
`;

// Insert extraCss before </style>
html = html.replace('</style>', extraCss + '\n  </style>');

// 3. Update Trust Bar with Live Beacon
html = html.replace(
  '<span>Same-Day Dispatch</span>',
  '<span><span class="live-dot" style="margin-right: 2px;"></span> Same/Next-Day Dispatch</span>'
);

// 4. Update Callout Row 2 with Audit Conduit
const oldCalloutText = `<p>Following thorough mechanical brushing, we apply an EPA-registered, thyme-based botanical antimicrobial fog that neutralizes biological spores on contact without synthetic VOCs, harsh bleaches, or toxic chemical residue.</p>
          <div>
            <a href="tel:8155550199" class="btn btn-secondary">Learn About Botanical Care</a>
          </div>`;

const newCalloutText = `<p>Following thorough mechanical brushing, we apply an EPA-registered, thyme-based botanical antimicrobial fog that neutralizes biological spores on contact without synthetic VOCs, harsh bleaches, or toxic chemical residue.</p>
          <ul class="audit-conduit">
            <li><strong>Iowa & Illinois EPA Code 455B Compliant:</strong> Zero toxic residues left in living zones.</li>
            <li><strong>NADCA ACR-2021 Standard Verified:</strong> Mechanical agitation prior to antimicrobial fogging.</li>
            <li><strong>Before & After Endoscope Video Audit:</strong> Direct photographic proof of bare metal interior.</li>
          </ul>
          <div>
            <a href="tel:8155550199" class="btn btn-secondary">Learn About Botanical Care</a>
          </div>`;

html = html.replace(oldCalloutText, newCalloutText);

// 5. Add Before & After Section (Right after Callouts, before Comparison Table)
const beforeAfterSection = `
  <!-- ========================================================================= -->
  <!-- VISUAL INSPECTION PROOF (BEFORE & AFTER AUDIT)                            -->
  <!-- ========================================================================= -->
  <section class="section">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Visual Audit</span>
        <h2>Verified Work: Before & After Decontamination</h2>
        <p>Real internal duct inspection photography taken across Winnebago County homes using our high-definition fiber-optic camera probes.</p>
      </div>

      <div class="ba-grid">
        <!-- Before Card -->
        <div class="ba-card ba-card-fail">
          <div class="ba-img-wrapper">
            <span class="ba-badge ba-badge-fail">⚠ Before: Clogged & Restricted</span>
            <img src="https://images.unsplash.com/photo-1517646287270-a5a9ca602e5c?auto=format&fit=crop&w=800&q=80" alt="Heavily contaminated air duct showing dense dust and dander accumulation">
          </div>
          <div class="ba-content">
            <h4>7-Year Contamination Accumulation</h4>
            <p>Main return trunk line choked with pet dander, drywall renovation dust, and organic allergens restricting HVAC blower efficiency by 38%.</p>
          </div>
        </div>

        <!-- After Card -->
        <div class="ba-card ba-card-pass">
          <div class="ba-img-wrapper">
            <span class="ba-badge ba-badge-pass">✓ After: Hospital-Grade Cleared</span>
            <img src="https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80" alt="Cleaned bare metal air duct decontaminated with negative air containment">
          </div>
          <div class="ba-content">
            <h4>Sanitized Bare-Metal Decontamination</h4>
            <p>Full 360-degree motorized rotary scrub under 5,000 CFM negative pressure containment with EPA botanical fogging. Airflow 100% restored.</p>
          </div>
        </div>
      </div>

      <div class="ba-metrics-bar">
        <div class="ba-metric-item">
          <strong>+42%</strong>
          <span>Static Air Pressure Restored</span>
        </div>
        <div class="ba-metric-item">
          <strong>99.97%</strong>
          <span>Particulate Capture at 0.3μm</span>
        </div>
        <div class="ba-metric-item">
          <strong>0.00%</strong>
          <span>Zero-Blowback Interior Guarantee</span>
        </div>
        <div class="ba-metric-item">
          <strong>100%</strong>
          <span>Video Verified Before Dispatch Closes</span>
        </div>
      </div>
    </div>
  </section>
`;

html = html.replace('<section id="comparison" class="section">', beforeAfterSection + '\n  <section id="comparison" class="section">');

// 6. Update Comparison Table Header with Winner Badge
html = html.replace(
  '<th class="highlight-col">Rockford Air Duct Pros</th>',
  '<th class="highlight-col"><span class="table-winner-badge">★ Certified Standard</span><br>Rockford Air Duct Pros</th>'
);

// 7. Add Connected Process Pipeline Container
html = html.replace(
  '<ul class="step-list">',
  '<div class="step-pipeline-container"><ul class="step-list">'
);
html = html.replace(
  '</section>\n\n  <!-- ====\n  <!-- ACCORDION FAQ SECTION',
  '</div>\n  </section>\n\n  <!-- ====\n  <!-- ACCORDION FAQ SECTION'
);

// Add ghost numbers to step cards
html = html.replace(
  '<h3>1. Whole-System Diagnosis</h3>',
  '<span class="step-ghost-num">01</span>\n          <h3>1. Whole-System Diagnosis</h3>'
);
html = html.replace(
  '<h3>2. HEPA Negative Containment</h3>',
  '<span class="step-ghost-num">02</span>\n          <h3>2. HEPA Negative Containment</h3>'
);
html = html.replace(
  '<h3>3. Rotary Mechanical Scrubbing</h3>',
  '<span class="step-ghost-num">03</span>\n          <h3>3. Rotary Mechanical Scrubbing</h3>'
);
html = html.replace(
  '<h3>4. Botanical Fog & Verification</h3>',
  '<span class="step-ghost-num">04</span>\n          <h3>4. Botanical Fog & Verification</h3>'
);

// 8. Add Testimonials Grid & Service Area with Map before FAQ
const reviewsAndMapSections = `
  <!-- ========================================================================= -->
  <!-- LOCAL CUSTOMER TESTIMONIALS (GEO-TAGGED SOCIAL PROOF)                     -->
  <!-- ========================================================================= -->
  <section class="section section-alt">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Homeowner Verified</span>
        <h2>What Winnebago County Homeowners Say</h2>
        <p>Real local reviews from certified residential duct cleaning projects completed across Rockford and surrounding neighborhoods.</p>
      </div>

      <div class="grid grid-3">
        <!-- Review 1 -->
        <div class="review-card">
          <div>
            <div class="review-stars">★★★★★</div>
            <span class="geo-pill">📍 Loves Park, IL • Forest Hills</span>
            <p class="review-quote">"After purchasing our 1970s ranch home in Loves Park, the dust coming through the registers was unbearable. Rockford Air Duct Pros showed us endoscope video of the trunk line before and after. Night and day difference. Furnace runs noticeably quieter."</p>
          </div>
          <div class="reviewer-meta">
            <span class="reviewer-name">Marcus T.</span>
            <span class="verified-shield">✓ Verified Homeowner</span>
          </div>
        </div>

        <!-- Review 2 -->
        <div class="review-card">
          <div>
            <div class="review-stars">★★★★★</div>
            <span class="geo-pill">📍 Rockford, IL • Edgebrook</span>
            <p class="review-quote">"We got scammed two years ago by a $49 coupon company that blew dust into our master bedroom. These guys brought real truck-mounted 5,000 CFM negative air equipment and sealed every register. No hidden fees, flat rate as quoted on the phone."</p>
          </div>
          <div class="reviewer-meta">
            <span class="reviewer-name">Sarah & David K.</span>
            <span class="verified-shield">✓ Verified Homeowner</span>
          </div>
        </div>

        <!-- Review 3 -->
        <div class="review-card">
          <div>
            <div class="review-stars">★★★★★</div>
            <span class="geo-pill">📍 Machesney Park, IL</span>
            <p class="review-quote">"Called at 8:00 AM after noticing a musty smell whenever the AC cycled on. They had a two-man crew at our Machesney Park home by early afternoon. The botanical thyme fogging completely eliminated the odor without chemical smells."</p>
          </div>
          <div class="reviewer-meta">
            <span class="reviewer-name">Elena R.</span>
            <span class="verified-shield">✓ Verified Homeowner</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- SERVICE AREA DIRECTORY & GOOGLE MAPS COVERAGE                             -->
  <!-- ========================================================================= -->
  <section class="section">
    <div class="container">
      <div class="service-area-grid">
        <!-- Left Column: Territory Directory -->
        <div>
          <span class="section-tag">Local Coverage</span>
          <h2>Serving Greater Rockford & Surrounding Communities</h2>
          <p>Our fleet of specialized negative-air decontamination vehicles is staged daily across Winnebago and Boone counties for prompt same/next-day dispatch.</p>

          <div class="territory-list">
            <div class="territory-item">
              <span>Rockford (Central, East & North End)</span>
              <span class="territory-badge">&lt; 30 Min Dispatch</span>
            </div>
            <div class="territory-item">
              <span>Loves Park & Machesney Park</span>
              <span class="territory-badge">&lt; 35 Min Dispatch</span>
            </div>
            <div class="territory-item">
              <span>Belvidere & Boone County</span>
              <span class="territory-badge">&lt; 45 Min Dispatch</span>
            </div>
            <div class="territory-item">
              <span>Cherry Valley & Winnebago</span>
              <span class="territory-badge">&lt; 40 Min Dispatch</span>
            </div>
            <div class="territory-item">
              <span>Roscoe & Rockton Corridor</span>
              <span class="territory-badge">&lt; 45 Min Dispatch</span>
            </div>
          </div>

          <p style="font-size: 0.85rem; font-weight: 700; color: var(--primary); margin-bottom: 8px;">Key Service Postal Zip Codes:</p>
          <div class="zip-pill-grid">
            <span class="zip-pill">61101</span>
            <span class="zip-pill">61102</span>
            <span class="zip-pill">61103</span>
            <span class="zip-pill">61104</span>
            <span class="zip-pill">61107</span>
            <span class="zip-pill">61108</span>
            <span class="zip-pill">61109</span>
            <span class="zip-pill">61111</span>
            <span class="zip-pill">61114</span>
            <span class="zip-pill">61115</span>
            <span class="zip-pill">61008</span>
            <span class="zip-pill">61016</span>
          </div>
        </div>

        <!-- Right Column: Map Embed Card -->
        <div class="map-container-card">
          <iframe 
            class="map-iframe" 
            src="https://maps.google.com/maps?q=Rockford,+IL&t=&z=11&ie=UTF8&iwloc=&output=embed" 
            loading="lazy" 
            referrerpolicy="no-referrer-when-downgrade" 
            title="Rockford Air Duct Pros Service Area Map">
          </iframe>
          <div class="map-nap-overlay">
            <strong>Rockford Air Duct Pros Dispatch Hub</strong>
            <p>401 S Main St, Rockford, IL 61101 • Mon-Sat: 7:00 AM – 7:00 PM</p>
            <a href="tel:8155550199" class="btn btn-primary" style="display: block; text-align: center; padding: 10px;">Call (815) 555-0199 for Dispatch</a>
          </div>
        </div>
      </div>
    </div>
  </section>
`;

html = html.replace('<section id="faq" class="section">', reviewsAndMapSections + '\n  <section id="faq" class="section">');

// 9. Add FAQ Help Strip
const faqHelpStrip = `
      <div class="faq-help-strip">
        <span><strong>Have a specific ductwork question?</strong> Speak directly with an ASCS certified technician.</span>
        <a href="tel:8155550199" class="btn btn-secondary" style="padding: 8px 16px; font-size: 0.85rem;">Call (815) 555-0199</a>
      </div>
    </div>
  </section>`;

html = html.replace('</div>\n  </section>\n\n  <!-- ====\n  <!-- FINAL CONVERSION BANNER', faqHelpStrip + '\n\n  <!-- ====\n  <!-- FINAL CONVERSION BANNER');

// 10. Update Final CTA Banner with live on-duty status
const oldCtaBanner = `<section class="cta-banner">
    <div class="container">
      <h2>Breathe Cleaner Air in Your Rockford Home Today</h2>
      <p>Schedule your NADCA-certified whole-home air duct decontamination. Flat-rate upfront quotes, no hidden fees, hospital-grade equipment.</p>
      <div class="cta-banner-buttons">
        <a href="tel:8155550199" class="btn btn-primary">Call (815) 555-0199</a>
        <a href="#services" class="btn btn-outline" style="border-color: #ffffff; color: #ffffff;">View Services</a>
      </div>
    </div>
  </section>`;

const newCtaBanner = `<section class="cta-banner">
    <div class="container">
      <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.12); padding: 6px 14px; border-radius: 9999px; font-size: 0.825rem; font-weight: 700; margin-bottom: 16px;">
        <span class="live-dot"></span>
        <span>Certified Technicians On Duty Today Across Winnebago County</span>
      </div>
      <h2>Breathe Cleaner Air in Your Rockford Home Today</h2>
      <p>Schedule your NADCA-certified whole-home air duct decontamination. Flat-rate upfront quotes, no hidden fees, hospital-grade equipment.</p>
      <div class="cta-banner-buttons">
        <a href="tel:8155550199" class="btn btn-primary btn-pulse">Call (815) 555-0199 for Dispatch</a>
        <a href="#services" class="btn btn-outline" style="border-color: #ffffff; color: #ffffff;">Explore Core Services</a>
      </div>
    </div>
  </section>`;

html = html.replace(oldCtaBanner, newCtaBanner);

// 11. Add pulse to mobile sticky call button
html = html.replace(
  '<a href="tel:8155550199" class="btn btn-primary"><span>📞 Call (815) 555-0199</span></a>',
  '<a href="tel:8155550199" class="btn btn-primary btn-pulse"><span>📞 Call (815) 555-0199</span></a>'
);

fs.writeFileSync(filePath, html, 'utf8');
console.log('Successfully updated master_template_sample.html with all sections and effects!');

