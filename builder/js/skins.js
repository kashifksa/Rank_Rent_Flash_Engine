/* skins.js : a SKIN is the design layer of a template (header style, buttons, cards, headings, section rhythm).
   A template picks one with `skin: 'id'`. Add a skin = add one entry here. Skins only restyle: structure, SEO and sections never change. */
(function () {
  const B = (window.Builder = window.Builder || {});

  /* header variants available to every template (template.header = 'classic' | 'topbar' | 'dark') */
  B.SKIN_BASE_CSS = `
.topbar{background:var(--dark);color:#cbd5e1;font-size:13px}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:38px;flex-wrap:wrap}
.topbar a{color:#fff;text-decoration:none;font-weight:700}.topbar a+a{margin-left:18px}.topbar a:hover{text-decoration:underline}
@media (max-width:767px){.topbar{display:none}}
.hdr-dark{background:rgba(var(--dark-rgb),.97);border-bottom:1px solid rgba(255,255,255,.08)}
.hdr-dark .logo{color:#fff}.hdr-dark .nav>a,.hdr-dark .dd>a{color:#e2e8f0}
.hdr-dark .nav>a:hover,.hdr-dark .dd:hover>a{color:var(--accent)}.hdr-dark .caret{color:#94a3b8}.hdr-dark .mnav summary{color:#fff;border-color:rgba(255,255,255,.22)}
.hdr-decker{border-bottom:0;background:#fff}
.hdr-decker .deck-top .wrap{display:flex;align-items:center;justify-content:space-between;height:78px;gap:18px}
.hdr-decker .deck-info{display:flex;align-items:center;gap:22px}
.hdr-decker .deck-pill{display:flex;align-items:center;gap:10px;font-size:13px;line-height:1.25}
.hdr-decker .deck-pill svg{width:22px;height:22px;color:var(--accent);flex-shrink:0}
.hdr-decker .deck-pill small{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.hdr-decker .deck-pill b{color:var(--heading);font-size:13.5px}
.hdr-decker .deck-nav{background:var(--dark);border-top:1px solid rgba(255,255,255,.08)}
.hdr-decker .deck-nav .wrap{display:flex;align-items:center;justify-content:space-between;height:50px}
.hdr-decker .deck-nav .nav>a,.hdr-decker .deck-nav .dd>a{color:#f1f5f9;font-size:14px;font-weight:700;padding:14px 4px}
.hdr-decker .deck-nav .nav>a:hover,.hdr-decker .deck-nav .dd:hover>a{color:var(--accent)}
.hdr-decker .deck-mail{color:#cbd5e1;font-size:13px;text-decoration:none;font-weight:600}
@media (max-width:767px){.hdr-decker .deck-info,.hdr-decker .deck-nav{display:none}.hdr-decker .deck-top .wrap{height:70px;padding:0 14px}}
.hdr-floating{background:transparent;border-bottom:0;backdrop-filter:none;padding:14px 16px 0}
.hdr-floating .wrap{background:rgba(255,255,255,.95);backdrop-filter:blur(12px);border:1px solid var(--line);border-radius:999px;box-shadow:0 14px 36px rgba(0,0,0,.08);padding:0 18px 0 24px;height:68px}
@media (max-width:767px){.hdr-floating{padding:8px 10px 0}.hdr-floating .wrap{height:60px;padding:0 12px 0 16px}}
/* new hero variants: dispatch, bento, docked */
.hero--dispatch{background:linear-gradient(110deg,rgba(var(--dark-rgb),.92) 38%,rgba(var(--dark-rgb),.70)),var(--hero-img) center/cover no-repeat,var(--dark);padding:76px 0}
.hero--dispatch .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:44px;align-items:center}
.hero--dispatch h1{color:#fff}.hero--dispatch p{color:#e2e8f0;font-size:1.1rem}
.hero-dcard{background:#fff;color:var(--text);border-radius:calc(var(--radius)*1.6);padding:30px 28px;box-shadow:0 24px 60px rgba(0,0,0,.35);border-top:5px solid var(--accent)}
.hero-dcard .hd-top{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.07em;color:var(--accent);margin-bottom:8px}
.hero-dcard .hd-dot{width:9px;height:9px;border-radius:50%;background:#16a34a;box-shadow:0 0 0 4px rgba(22,163,74,.2)}
.hero-dcard h3{color:var(--heading);margin:0 0 12px;font-size:1.25rem}
.hero-dcard .hd-phone{display:flex;align-items:center;gap:10px;font-family:var(--font-h);font-size:1.45rem;font-weight:800;color:var(--heading);text-decoration:none;padding:12px 16px;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);margin-bottom:16px}
.hero-dcard .hd-phone svg{color:var(--accent);width:22px;height:22px}
.hero-dcard .hd-list{list-style:none;padding:0;margin:0 0 20px;display:grid;gap:10px;font-size:.94rem;color:var(--text)}
.hero-dcard .hd-list li{display:flex;align-items:center;gap:10px}
.hero-dcard .hd-list .tick{width:22px;height:22px;border-radius:50%;background:rgba(var(--accent-rgb),.14);color:var(--accent);display:grid;place-items:center;flex-shrink:0}
.hero-dcard .hd-list .tick svg{width:13px;height:13px}
.hero-dcard .hd-btn{width:100%;justify-content:center}
@media (max-width:900px){.hero--dispatch .wrap{grid-template-columns:1fr;padding:20px 24px}}
.hero--bento{background:var(--bg);color:var(--text);padding:36px 0 56px}
.hero--bento .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;align-items:stretch}
.hero--bento .bento-main{background:var(--surface);border:1px solid var(--line);border-radius:calc(var(--radius)*1.6);padding:48px 42px;display:flex;flex-direction:column;justify-content:center}
.hero--bento h1{color:var(--heading)}.hero--bento p{color:var(--muted);font-size:1.08rem}
.hero--bento .btn-ghost{color:var(--heading)}
.hero--bento .bento-side{display:grid;grid-template-rows:1fr auto;gap:20px}
.hero--bento .bento-photo{border-radius:calc(var(--radius)*1.6);overflow:hidden;min-height:260px;background:var(--dark)}
.hero--bento .bento-photo img{width:100%;height:100%;object-fit:cover}
.hero--bento .bento-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:14px}
.hero--bento .bento-tile{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--radius)*1.2);padding:16px;display:flex;flex-direction:column;gap:8px}
.hero--bento .bento-tile .ic{width:40px;height:40px}.hero--bento .bento-tile b{font-size:.88rem;color:var(--heading);line-height:1.3}
@media (max-width:900px){.hero--bento .wrap{grid-template-columns:1fr}.hero--bento .bento-main{padding:32px 24px}}
.hero--docked{background:linear-gradient(180deg,rgba(var(--dark-rgb),.76),rgba(var(--dark-rgb),.94)),var(--hero-img) center/cover no-repeat,var(--dark);padding:80px 0 44px}
.hero--docked .dock-copy{max-width:820px}
.hero--docked h1{color:#fff}.hero--docked p{color:#e2e8f0;font-size:1.12rem}
.hero-dock{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-top:48px;background:rgba(255,255,255,.08);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.16);border-radius:calc(var(--radius)*1.4);padding:20px}
.hero-dock .dock-item{display:flex;align-items:center;gap:12px;color:#fff;font-size:.93rem}
.hero-dock .dock-item .ic{width:44px;height:44px;flex-shrink:0;background:var(--accent);color:var(--btn-fg,#fff)}
/* new card variants: numbered & stripe */
.cards-numbered .cnum-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.cards-numbered .cnum{font-family:var(--font-h);font-size:1.65rem;font-weight:800;color:var(--accent);opacity:.85;letter-spacing:-.03em}
.cards-numbered .card{border-bottom:4px solid var(--accent)}
.cards-stripe{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:20px}
.cards-stripe .card{flex-direction:row;align-items:flex-start;gap:18px;border-left:5px solid var(--accent)}
.cards-stripe .card .ic{flex:0 0 52px;width:52px;height:52px}
@media (max-width:640px){.cards-stripe{grid-template-columns:1fr}}
/* new step variants: rail & track */
.steps-rail{display:grid;grid-template-columns:.9fr 1.3fr;gap:48px;align-items:start}
.steps-rail .rail-side{position:sticky;top:100px}
.steps-rail .rail-list{display:grid;gap:18px;position:relative;padding-left:22px;border-left:3px solid rgba(var(--accent-rgb),.3)}
.steps-rail .rail-item{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--radius)*1.4);padding:22px 24px;display:flex;gap:18px;align-items:flex-start}
.steps-rail .rail-item .n{width:42px;height:42px;border-radius:var(--radius);background:var(--accent);color:var(--btn-fg,#fff);display:grid;place-items:center;font-weight:800;flex-shrink:0}
.steps-rail .rail-body h3{margin:0 0 6px}.steps-rail .rail-body p{margin:0 0 8px;color:var(--muted)}
@media (max-width:900px){.steps-rail{grid-template-columns:1fr}.steps-rail .rail-side{position:static}}
.steps-track .step{text-align:center;border-top:4px solid var(--accent)}
.steps-track .step .n{margin-inline:auto}
`;

  B.SKINS = {
    /* Bold Trade: rugged, high contrast, square corners, hard shadows, amber on charcoal (dark text on amber for contrast) */
    bold: `
.skin-bold h1,.skin-bold h2,.skin-bold h3{text-transform:uppercase;letter-spacing:.01em;font-weight:700}
.skin-bold h1{font-size:clamp(2.2rem,5vw,3.8rem)}
.skin-bold h2::after{content:"";display:block;width:64px;height:5px;background:var(--accent);margin:14px 0 0}
.skin-bold .head{text-align:left;max-width:820px;margin-left:0}
.skin-bold .sec.al-center .head{text-align:center;margin-inline:auto}.skin-bold .sec.al-center .head h2::after{margin-inline:auto}
.skin-bold .hero h1::after,.skin-bold .cta-box h2::after,.skin-bold .cta-band h2::after{margin-inline:auto}
.skin-bold .eyebrow{background:var(--accent);color:#111418;border-radius:0;letter-spacing:.14em;padding:5px 12px;font-size:11px}
.skin-bold .btn{border-radius:0;text-transform:uppercase;letter-spacing:.06em;font-weight:800}
.skin-bold .btn-primary{color:#111418;box-shadow:none}
.skin-bold .card,.skin-bold .step,.skin-bold .badge,.skin-bold .faq-wrap details,.skin-bold .mnav summary,.skin-bold .tbl,.skin-bold .form,.skin-bold .chip,.skin-bold .time,.skin-bold .tag,.skin-bold .ba-tab{border-radius:0}
.skin-bold .card{border-top:5px solid var(--accent);box-shadow:none}
.skin-bold .card:hover{transform:translateY(-4px);box-shadow:8px 8px 0 rgba(17,20,24,.12)}
.skin-bold .card .more,.skin-bold .loc,.skin-bold .time{color:#7a4f00}
.skin-bold .ic,.skin-bold .step .n,.skin-bold .tick,.skin-bold .av{border-radius:0;background:var(--accent);color:#111418}
.skin-bold .hero--full{clip-path:polygon(0 0,100% 0,100% 93%,0 100%);padding-bottom:36px;background:linear-gradient(180deg,rgba(var(--dark-rgb),.72),rgba(var(--dark-rgb),.92)),var(--hero-img) center/cover no-repeat,var(--dark)}
.skin-bold .bg-light{background:#eceef1}
.skin-bold .split-media img{border-radius:0;box-shadow:12px 12px 0 var(--accent)}
.skin-bold .hero-img,.skin-bold .dba-card,.skin-bold .ba-slider,.skin-bold .metrics,.skin-bold .stats{border-radius:0}
.skin-bold .bg-accent,.skin-bold .bg-accent h2,.skin-bold .bg-accent h3{color:#111418}
.skin-bold .cta-band{border-top:6px solid var(--accent)}
.skin-bold .cmp th:nth-child(2){color:#111418}
.skin-bold .faq-wrap summary{text-transform:uppercase;letter-spacing:.03em}
.skin-bold .ftr{border-top:6px solid var(--accent)}
.skin-bold .callbar{color:#111418}
.skin-bold .tag{background:rgba(var(--accent-rgb),.18)}
`,
    /* Clean Local: light, friendly, big soft radius, tinted sections, pill buttons, no hard borders */
    clean: `
.skin-clean{--tint:rgba(var(--accent-rgb),.09)}
.skin-clean h1,.skin-clean h2{font-weight:700;letter-spacing:-.02em}
.skin-clean .bg-light{background:linear-gradient(180deg,#f3faf8,#eaf5f2)}
.skin-clean .eyebrow{background:transparent;padding:0;color:var(--accent);letter-spacing:.12em}
.skin-clean .eyebrow::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--accent);margin-right:8px}
.skin-clean .btn{border-radius:999px;padding:14px 30px}
.skin-clean .card,.skin-clean .step,.skin-clean .badge,.skin-clean .tbl,.skin-clean .form{border:0;border-radius:24px;box-shadow:0 10px 36px rgba(16,52,58,.08)}
.skin-clean .card:hover{transform:translateY(-6px);box-shadow:0 22px 52px rgba(16,52,58,.14)}
.skin-clean .faq-wrap details{border:1px solid rgba(var(--accent-rgb),.18);border-radius:20px}
.skin-clean .ic{width:64px;height:64px;border-radius:20px;background:var(--tint)}
.skin-clean .step .n{border-radius:14px}
.skin-clean .hero--split{background:radial-gradient(circle at 88% 12%,rgba(var(--accent-rgb),.16),transparent 42%),radial-gradient(circle at 5% 92%,rgba(var(--accent-rgb),.10),transparent 40%),#fff}
.skin-clean .hero-img,.skin-clean .split-media img{border-radius:32px}
.skin-clean .hero-img{box-shadow:0 30px 70px rgba(16,52,58,.22)}
.skin-clean .cta-box{border-radius:36px}
.skin-clean .dba-card,.skin-clean .ba-slider,.skin-clean .metrics,.skin-clean .stats{border-radius:24px}
.skin-clean .tag{background:var(--tint)}
.skin-clean .topbar{background:var(--accent)}
.skin-clean .ftr{border-radius:40px 40px 0 0}
`,
    /* Executive Contractor: navy + brick red, double-decker nav, dispatch card hero, numbered index cards, sticky rail process */
    authority: `
.skin-authority h1,.skin-authority h2{letter-spacing:-.02em}
.skin-authority .eyebrow{border-radius:4px;background:rgba(var(--accent-rgb),.12);color:var(--accent);font-weight:800}
.skin-authority .card{border-radius:8px;box-shadow:0 10px 28px rgba(12,30,53,.06)}
.skin-authority .bg-light{background:#f1f5f9}
.skin-authority .cta-band{border-top:5px solid var(--accent)}
`,
    /* Rapid Dispatch: high-urgency cobalt & slate, docked trust strip, horizontal stripe cards, connected step track */
    emergency: `
.skin-emergency h1,.skin-emergency h2,.skin-emergency h3{letter-spacing:-.01em}
.skin-emergency .topbar{background:var(--accent);color:#fff;font-weight:700}
.skin-emergency .eyebrow{background:var(--accent);color:#fff;border-radius:6px}
.skin-emergency .bg-light{background:#eef2ff}
.skin-emergency .card{border-radius:10px;box-shadow:0 8px 24px rgba(15,23,42,.07)}
`,
    /* Modern Architectural: warm stone palette, floating pill navbar, bento hero, soft borderless surfaces */
    bento: `
.skin-bento{--bg:#f7f5f0;--surface:#efeae1;--card:#ffffff;--line:#e4ddd1}
.skin-bento .bg-light{background:#efeae1}
.skin-bento .card,.skin-bento .step,.skin-bento .badge,.skin-bento .rail-item{border:1px solid #e4ddd1;border-radius:22px;box-shadow:0 8px 28px rgba(28,25,23,.05)}
.skin-bento .btn{border-radius:999px}
.skin-bento .hero-img,.skin-bento .split-media img,.skin-bento .dba-card{border-radius:24px}
.skin-bento .cta-box{border-radius:32px}
`
  };
})();

