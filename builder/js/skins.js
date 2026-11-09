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
/* architectural gridline header, magazine hero, ledger grid, frame split, spec steps */
.hdr-gridline{background:var(--bg);border-top:3px solid var(--heading);border-bottom:2px solid var(--heading);backdrop-filter:none}
.hdr-gridline .wrap{max-width:1320px;padding:0;height:78px;display:grid;grid-template-columns:auto 1fr auto;align-items:stretch}
.hdr-gridline .gl-cell{display:flex;align-items:center;padding:0 28px;border-right:1.5px solid var(--heading)}
.hdr-gridline .gl-logo{margin:0}
.hdr-gridline .gl-nav{justify-content:center;gap:26px}
.hdr-gridline .gl-nav>a,.hdr-gridline .gl-nav .dd>a{text-transform:uppercase;letter-spacing:.08em;font-size:12px;font-weight:800;color:var(--heading)}
.hdr-gridline .gl-cta{display:flex;flex-direction:column;justify-content:center;padding:0 32px;background:var(--accent);color:var(--btn-fg,#fff);text-decoration:none;transition:background .2s}
.hdr-gridline .gl-cta small{font-size:10px;letter-spacing:.14em;font-weight:800;opacity:.88}
.hdr-gridline .gl-cta b{font-family:var(--font-h);font-size:1.15rem;font-weight:800;letter-spacing:-.01em}
.hdr-gridline .gl-cta:hover{background:var(--heading);color:#fff}
@media (max-width:767px){.hdr-gridline .wrap{display:flex;justify-content:space-between;align-items:center;height:68px;padding:0 14px}.hdr-gridline .gl-cell{border:0;padding:0}.hdr-gridline .gl-nav,.hdr-gridline .gl-cta{display:none}}
.hero--magazine{background:var(--bg);color:var(--text);padding:0 0 56px;border-bottom:2px solid var(--heading)}
.hero--magazine .wrap{max-width:1320px}
.hero--magazine .mag-meta{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:14px 0;border-bottom:1.5px solid var(--heading);font-size:11.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--heading)}
.hero--magazine .mag-grid{display:grid;grid-template-columns:1.18fr .82fr;gap:44px;align-items:center;padding:46px 0 38px}
.hero--magazine h1{color:var(--heading);font-size:clamp(2.4rem,4.8vw,4.1rem);line-height:1.06;letter-spacing:-.025em;margin-bottom:.45em}
.hero--magazine .mag-lead p{color:var(--text);font-size:1.08rem;max-width:640px}
.hero--magazine .btn-ghost{color:var(--heading);border-color:var(--heading)}
.hero--magazine .mag-frame{border:2px solid var(--heading);background:var(--card);padding:12px;box-shadow:12px 12px 0 var(--heading)}
.hero--magazine .mag-frame img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
.hero--magazine .mag-cap{padding:10px 4px 2px;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);border-top:1px solid var(--line);margin-top:10px}
.hero--magazine .mag-bar{display:grid;grid-template-columns:repeat(4,1fr);border:2px solid var(--heading);background:var(--dark);color:#fff}
.hero--magazine .mag-spec{padding:18px 20px;border-right:1px solid rgba(255,255,255,.16);display:flex;flex-direction:column;gap:4px}
.hero--magazine .mag-spec:last-child{border-right:0}
.hero--magazine .mag-idx{font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--accent)}
.hero--magazine .mag-spec b{font-size:.92rem;line-height:1.3;color:#f8fafc}
@media (max-width:900px){.hero--magazine .mag-grid{grid-template-columns:1fr;gap:28px}.hero--magazine .mag-bar{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.hero--magazine .mag-bar{grid-template-columns:1fr}.hero--magazine .mag-meta{font-size:10px}}
.split-frame .arch-frame{border:2px solid var(--heading);background:var(--card);padding:14px;box-shadow:10px 10px 0 var(--accent)}
.split-frame .arch-top{display:flex;justify-content:space-between;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding-bottom:10px;margin-bottom:10px;border-bottom:1.5px solid var(--heading);color:var(--heading)}
.split-frame .arch-frame img{border-radius:0;box-shadow:none;aspect-ratio:4/3;object-fit:cover;width:100%}
.split-frame .arch-cap{padding-top:10px;margin-top:10px;border-top:1px solid var(--line);font-size:12px;color:var(--muted);font-weight:600}
.cards-ledger{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));border-top:2px solid var(--heading);border-left:2px solid var(--heading)}
.cards-ledger .card{border:0;border-right:2px solid var(--heading);border-bottom:2px solid var(--heading);border-radius:0;box-shadow:none;padding:32px 28px;background:transparent;transition:background .2s,color .2s}
.cards-ledger .card:hover{transform:none;background:var(--card);box-shadow:inset 0 -5px 0 var(--accent)}
.cards-ledger .cnum-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid var(--line)}
.cards-ledger .cnum{font-family:var(--font-h);font-size:1.1rem;font-weight:800;color:var(--accent);letter-spacing:.05em}
.cards-ledger .ic{width:42px;height:42px;border-radius:0;border:1.5px solid var(--heading);background:var(--card);color:var(--heading)}
.steps-spec{border-top:2px solid var(--heading)}
.steps-spec .spec-row{display:grid;grid-template-columns:160px 1fr 1.5fr;gap:28px;align-items:baseline;padding:26px 0;border-bottom:1.5px solid var(--heading)}
.steps-spec .spec-idx{font-size:12px;font-weight:800;letter-spacing:.12em;color:var(--accent);text-transform:uppercase}
.steps-spec .spec-title h3{margin:0 0 6px;font-size:1.25rem}
.steps-spec .spec-desc p{margin:0;color:var(--muted)}
@media (max-width:820px){.steps-spec .spec-row{grid-template-columns:1fr;gap:8px}}
/* --- Precision Blueprint Dossier: 14 Unique Section Layouts --- */
.console-strip{background:#070d17;color:#94a3b8;font-size:11px;font-weight:700;letter-spacing:.12em;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.08)}
.console-strip .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.hdr-console{background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:2px solid var(--dark)}
.hdr-console .wrap{height:80px;gap:20px}
.hdr-console .console-nav{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:6px 18px;gap:20px}
.hdr-console .console-cta{display:flex;align-items:center;gap:12px;background:var(--dark);color:#fff;padding:10px 18px;border-radius:8px;text-decoration:none;border:2px solid var(--dark);transition:transform .15s,background .15s}
.hdr-console .console-cta:hover{background:var(--accent);border-color:var(--accent);transform:translateY(-1px)}
.hdr-console .console-cta small{display:block;font-size:10px;letter-spacing:.12em;color:#93c5fd;font-weight:700}
.hdr-console .console-cta b{font-size:1rem;font-family:var(--font-h)}
.hdr-console .c-dot{width:10px;height:10px;border-radius:50%;background:#22c55e;box-shadow:0 0 0 4px rgba(34,197,94,.25)}
@media (max-width:960px){.console-strip{display:none}.hdr-console .console-nav,.hdr-console .console-cta{display:none}}

/* 1. Hero Dossier */
.hero--dossier{background:radial-gradient(circle at 85% 20%,rgba(var(--accent-rgb),.14),transparent 45%),linear-gradient(180deg,#0b1320 0%,#111c2d 100%);color:#fff;padding:64px 0 72px;border-bottom:3px solid var(--accent)}
.hero--dossier h1{color:#fff;font-size:clamp(2.2rem,4vw,3.35rem);line-height:1.08;margin-bottom:18px}
.hero--dossier p{color:#cbd5e1;font-size:1.06rem}
.dos-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.dos-tag{display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);padding:7px 14px;border-radius:6px;font-size:11px;font-weight:800;letter-spacing:.12em;color:#93c5fd;margin-bottom:18px}
.dos-dot{width:8px;height:8px;border-radius:50%;background:#38bdf8}
.dos-matrix{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:28px;padding-top:24px;border-top:1px solid rgba(255,255,255,.14)}
.dos-cell{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-left:3px solid var(--accent);padding:12px 14px;border-radius:6px}
.dos-k{display:block;font-size:10px;font-weight:800;letter-spacing:.12em;color:#60a5fa;margin-bottom:3px}
.dos-cell b{font-size:.9rem;color:#f8fafc;display:block;line-height:1.35}
.dos-viewport{position:relative;background:#070d17;border:2px solid rgba(255,255,255,.22);border-radius:10px;padding:14px;box-shadow:0 28px 60px rgba(0,0,0,.45)}
.dos-viewport img{width:100%;height:390px;object-fit:cover;border-radius:6px;display:block}
.dos-viewport .ret{position:absolute;color:#60a5fa;font-family:monospace;font-weight:700;font-size:16px;line-height:1;pointer-events:none}
.dos-viewport .ret.tl{top:4px;left:6px}.dos-viewport .ret.tr{top:4px;right:6px}.dos-viewport .ret.bl{bottom:64px;left:6px}.dos-viewport .ret.br{bottom:64px;right:6px}
.dos-readout{margin-top:12px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:6px;padding:12px 16px;display:flex;justify-content:space-between;align-items:center}
.dos-readout small{display:block;font-size:10px;letter-spacing:.12em;color:#94a3b8;font-weight:700}
.dos-readout b{font-size:1.1rem;color:#fff;font-family:var(--font-h)}
.dos-readout > span{background:rgba(34,197,94,.18);color:#4ade80;border:1px solid rgba(34,197,94,.4);font-size:11px;font-weight:800;padding:4px 10px;border-radius:99px;letter-spacing:.08em}
@media (max-width:960px){.dos-grid{grid-template-columns:1fr}.dos-matrix{grid-template-columns:1fr}}

/* 2. Split Diagnostic */
.split-diagnostic{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:start}
.diag-panel{background:var(--card);border:1.5px solid var(--line);border-top:4px solid var(--accent);border-radius:var(--radius);padding:34px;box-shadow:0 12px 32px rgba(15,23,42,.05)}
.diag-bar{display:flex;justify-content:space-between;font-size:11px;font-weight:800;letter-spacing:.12em;color:var(--accent);padding-bottom:14px;margin-bottom:18px;border-bottom:1px dashed var(--line)}
.diag-img{position:relative;border-radius:var(--radius);overflow:hidden;border:1.5px solid var(--line);margin-bottom:16px}
.diag-img img{width:100%;height:280px;object-fit:cover;display:block}
.diag-badge{position:absolute;top:12px;left:12px;background:rgba(11,19,32,.88);color:#fff;font-size:10px;font-weight:800;letter-spacing:.12em;padding:6px 12px;border-radius:4px}
.diag-chips{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.diag-chip{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--dark);border-radius:6px;padding:12px 14px}
.diag-code{display:block;font-size:10px;font-weight:800;letter-spacing:.1em;color:var(--accent);margin-bottom:4px}
.diag-chip p{margin:0;font-size:.86rem;line-height:1.45;color:var(--text);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
@media (max-width:960px){.split-diagnostic,.diag-chips{grid-template-columns:1fr}}

/* 3. Cards Bento Mosaic */
.cards-bento-mosaic{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.bm-card{background:var(--card);border:1.5px solid var(--line);border-radius:var(--radius);padding:28px;display:flex;flex-direction:column;transition:transform .2s,border-color .2s,box-shadow .2s}
.bm-card:hover{transform:translateY(-3px);border-color:var(--accent);box-shadow:0 16px 36px rgba(15,23,42,.08)}
.bm-card.bm-hero{grid-column:span 2;background:var(--dark);color:#fff;border-color:var(--dark)}
.bm-card.bm-hero h3{color:#fff;font-size:1.45rem}
.bm-card.bm-hero p{color:#cbd5e1}
.bm-card.bm-hero .bm-idx{color:#60a5fa}
.bm-card.bm-hero .ic{background:rgba(255,255,255,.1);color:#fff}
.bm-card.bm-hero .bm-link{color:#60a5fa}
.bm-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.bm-idx{font-size:11px;font-weight:800;letter-spacing:.14em;color:var(--accent)}
.bm-link{margin-top:auto;padding-top:14px;font-weight:700;color:var(--accent);text-decoration:none;font-size:.92rem}
@media (max-width:960px){.cards-bento-mosaic{grid-template-columns:1fr}.bm-card.bm-hero{grid-column:span 1}}

/* 4. Cards Pillars (Why Choose Us) */
.cards-pillars{display:flex;flex-direction:column;gap:14px}
.pillar-row{display:grid;grid-template-columns:120px 260px 1fr;gap:28px;align-items:center;background:var(--card);border:1.5px solid var(--line);border-radius:var(--radius);padding:22px 28px;transition:border-color .2s}
.pillar-row:hover{border-color:var(--accent)}
.pil-num{display:flex;align-items:center;gap:14px}
.pil-num > span:first-child{font-family:var(--font-h);font-size:1.75rem;font-weight:800;color:var(--accent);line-height:1}
.pil-num .ic{margin:0;width:42px;height:42px}
.pil-title h3{margin:0;font-size:1.15rem}
.pil-body p{margin:0;color:var(--text);font-size:.96rem}
@media (max-width:900px){.pillar-row{grid-template-columns:1fr;gap:12px}}

/* 5. Split Spotlight (Local Context) */
.split-spotlight{background:var(--dark);color:#fff;border-radius:calc(var(--radius) + 4px);padding:44px;box-shadow:0 24px 54px rgba(11,19,32,.18)}
.spot-head{margin-bottom:28px;padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,.14)}
.spot-head h2{color:#fff;margin:8px 0 0}
.spot-body{display:grid;grid-template-columns:.95fr 1.05fr;gap:36px;align-items:center}
.spot-media{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.16);border-radius:var(--radius);overflow:hidden}
.spot-media img{width:100%;height:340px;object-fit:cover;display:block}
.spot-cap{padding:10px 14px;font-size:12px;color:#94a3b8;border-top:1px solid rgba(255,255,255,.1)}
.spot-copy p{color:#e2e8f0}
@media (max-width:900px){.spot-body{grid-template-columns:1fr}.split-spotlight{padding:26px}}

/* 6. Gallery Filmstrip (Before & After) */
.film-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px}
.film-plate{margin:0;background:#0b1320;color:#fff;border-radius:var(--radius);overflow:hidden;border:2px solid #1e293b;box-shadow:0 14px 32px rgba(11,19,32,.14)}
.fp-bar{display:flex;justify-content:space-between;padding:10px 16px;font-size:11px;font-weight:800;letter-spacing:.12em;color:#60a5fa;background:#070d17;border-bottom:1px solid rgba(255,255,255,.1)}
.film-plate img{width:100%;height:240px;object-fit:cover;display:block}
.film-plate figcaption{padding:14px 16px;font-size:.9rem;color:#cbd5e1}

/* 7. Cards Dossier (Case Studies) */
.cards-dossier{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
.dc-card{background:var(--card);border:1.5px solid var(--line);border-radius:var(--radius);overflow:hidden;display:flex;flex-direction:column}
.dc-hdr{background:var(--dark);color:#fff;padding:12px 20px;display:flex;justify-content:space-between;align-items:center;font-size:11px;font-weight:800;letter-spacing:.1em}
.dc-loc{background:var(--accent);color:#fff;padding:3px 9px;border-radius:4px}
.dc-body{padding:24px}
.dc-facts{display:flex;flex-direction:column;gap:10px;margin-top:14px}
.dc-fact{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--dark);padding:10px 14px;border-radius:5px;font-size:.9rem}
.dc-fact small{display:block;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:3px}
.dc-fact.dc-result{border-left-color:#16a34a;background:rgba(22,163,74,.06)}
.dc-fact.dc-result small{color:#15803d}

/* 8. Table Matrix (Comparison Table) */
.cmp-matrix .mx-win{background:rgba(var(--accent-rgb),.08);font-weight:600;border-left:2px solid var(--accent);border-right:2px solid var(--accent)}
.cmp-matrix thead th.mx-win{background:var(--accent);color:#fff;position:relative}
.mx-tag{display:block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.9;margin-bottom:2px}
.mx-feat{font-weight:700;color:var(--heading)}
.mx-foot{margin-top:18px;background:var(--card);border:1.5px solid var(--line);border-radius:var(--radius);padding:18px 24px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}

/* 9. Steps Chevron (Process) */
.steps-chevron{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.chev-step{background:var(--card);border:1.5px solid var(--line);border-top:4px solid var(--accent);border-radius:var(--radius);padding:24px;position:relative}
.chev-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.chev-stage{font-family:var(--font-h);font-size:12px;font-weight:800;letter-spacing:.12em;color:var(--accent)}
.chev-time{font-size:11px;font-weight:700;background:var(--surface);border:1px solid var(--line);padding:3px 9px;border-radius:99px;color:var(--heading)}

/* 10. Badges Seal Strip (Awards & Certifications) */
.badges-seals{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}
.seal-card{display:grid;grid-template-columns:84px 1fr;gap:18px;align-items:center;background:var(--card);border:1.5px solid var(--line);border-radius:var(--radius);padding:20px}
.seal-emblem{background:var(--dark);color:#fff;border-radius:8px;padding:12px 8px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:6px}
.seal-emblem .ic{margin:0;width:36px;height:36px;background:rgba(255,255,255,.12);color:#60a5fa}
.seal-emblem small{font-size:9px;font-weight:800;letter-spacing:.1em;color:#93c5fd}
.seal-body b{display:block;color:var(--heading);font-size:1.02rem;margin-bottom:4px}
.seal-body span{font-size:.88rem;color:var(--muted);line-height:1.45;display:block}

/* 11. Reviews Editorial Wall */
.wall-banner{display:flex;justify-content:space-between;align-items:flex-end;gap:28px;margin-bottom:32px;padding-bottom:22px;border-bottom:2px solid var(--line);flex-wrap:wrap}
.wall-banner h2{margin:6px 0 8px}
.wall-banner p{margin:0;max-width:640px;color:var(--muted)}
.wall-score{display:flex;align-items:center;gap:14px;background:var(--dark);color:#fff;padding:14px 22px;border-radius:var(--radius)}
.ws-num{font-family:var(--font-h);font-size:2.2rem;font-weight:800;line-height:1;color:#fbbf24}
.wall-score small{display:block;font-size:11px;color:#cbd5e1}
.wall-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px}
.wall-card{background:var(--card);border:1.5px solid var(--line);border-radius:var(--radius);padding:26px;display:flex;flex-direction:column;justify-content:space-between}
.wall-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.wall-v{font-size:10px;font-weight:800;letter-spacing:.1em;color:var(--accent);background:rgba(var(--accent-rgb),.1);padding:4px 8px;border-radius:4px}
.wall-card q{font-style:normal;color:var(--heading);font-size:.98rem;line-height:1.6;margin-bottom:18px;display:block;quotes:none}
.wall-card q::before,.wall-card q::after{content:none}
.wall-who{display:flex;align-items:center;gap:12px;padding-top:14px;border-top:1px solid var(--line)}
.wall-who small{display:block;color:var(--muted);font-size:.82rem}

/* 12. Area Radar (Service Area & Map) */
.area-radar{display:grid;grid-template-columns:1fr 1.1fr;gap:32px;align-items:stretch}
.radar-map{background:var(--dark);border-radius:var(--radius);overflow:hidden;border:2px solid var(--dark);display:flex;flex-direction:column}
.radar-bar{display:flex;justify-content:space-between;padding:12px 18px;font-size:11px;font-weight:800;letter-spacing:.12em;color:#60a5fa;background:#070d17}
.radar-map iframe{width:100%;flex:1;min-height:380px;border:0}
.radar-board{background:var(--card);border:1.5px solid var(--line);border-radius:var(--radius);padding:28px;display:flex;flex-direction:column;justify-content:space-between}
.radar-tag{display:inline-flex;align-items:center;gap:6px;background:var(--surface);border:1px solid var(--line)}
.radar-tag svg{width:14px;height:14px;color:var(--accent)}
@media (max-width:900px){.area-radar{grid-template-columns:1fr}}

/* 13. FAQ Numbered Grid */
.faq-ngrid{display:grid !important;grid-template-columns:repeat(2,1fr) !important;gap:18px !important}
.faq-ncard{margin:0 !important;background:var(--card);border:1.5px solid var(--line) !important;border-radius:var(--radius) !important}
.faq-ncard summary{display:flex !important;align-items:center;gap:14px;padding:18px 20px !important}
.fn-idx{font-family:var(--font-h);font-size:12px;font-weight:800;letter-spacing:.1em;background:rgba(var(--accent-rgb),.12);color:var(--accent);padding:5px 10px;border-radius:5px;flex-shrink:0}
.fn-q{flex:1;font-weight:700}
@media (max-width:860px){.faq-ngrid{grid-template-columns:1fr !important}}

/* 14. CTA Split Ticket */
.cta-ticket{display:grid;grid-template-columns:1.3fr .7fr;background:var(--dark);color:#fff;border-radius:calc(var(--radius) + 4px);overflow:hidden;border:2px solid var(--dark);box-shadow:0 24px 56px rgba(11,19,32,.22)}
.ct-left{padding:44px}
.ct-tag{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.14em;color:#60a5fa;margin-bottom:10px}
.ct-left h2{color:#fff;margin-bottom:12px}
.ct-left p{color:#cbd5e1}
.ct-note{margin-top:16px;padding-top:14px;border-top:1px solid rgba(255,255,255,.12);font-size:.88rem;color:#94a3b8}
.ct-right{background:#070d17;border-left:2px dashed rgba(255,255,255,.18);padding:44px 34px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.ct-label{font-size:11px;font-weight:800;letter-spacing:.14em;color:#93c5fd;margin-bottom:8px}
.ct-phone{font-family:var(--font-h);font-size:1.75rem;font-weight:800;color:#fff;text-decoration:none;margin-bottom:8px}
.ct-right p{color:#94a3b8;font-size:.88rem;margin:0 0 18px}
@media (max-width:860px){.cta-ticket{grid-template-columns:1fr}.ct-right{border-left:0;border-top:2px dashed rgba(255,255,255,.18)}}

/* 15. Architectural Footer */
.ftr-blueprint .ftr-banner{display:flex;justify-content:space-between;align-items:center;gap:20px;padding-bottom:32px;margin-bottom:36px;border-bottom:1px solid rgba(255,255,255,.14);flex-wrap:wrap}
.ftr-blueprint .ftr-banner small{display:block;font-size:11px;letter-spacing:.14em;color:#60a5fa;font-weight:800;margin-bottom:4px}
.ftr-blueprint .ftr-banner h3{color:#fff;margin:0;font-size:1.5rem}
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
`,
    /* Swiss Editorial Atelier: warm architectural paper (#f4f0e6), exposed ink hairlines (#141413), serif display headings, ledger grids */
    atelier: `
.skin-atelier{--bg:#f4f0e6;--surface:#ebe5d8;--card:#fbf9f4;--line:#cfc7b6;--text:#292826;--muted:#5c5852}
.skin-atelier .wrap{max-width:1320px}
.skin-atelier h1,.skin-atelier h2{font-weight:700;letter-spacing:-.025em}
.skin-atelier .sec{border-bottom:1.5px solid var(--heading)}
.skin-atelier .bg-light{background:#ebe5d8}
.skin-atelier .head{text-align:left;max-width:none;margin:0 0 40px;padding-bottom:20px;border-bottom:2px solid var(--heading);display:grid;grid-template-columns:220px 1fr;gap:28px;align-items:end}
.skin-atelier .head .eyebrow{margin:0;background:transparent;padding:0;border-radius:0;color:var(--accent);font-size:12px;letter-spacing:.14em}
.skin-atelier .head .eyebrow::before{content:"// "}
.skin-atelier .head h2{ grid-column:2;margin:0;font-size:clamp(1.85rem,3.4vw,2.75rem);line-height:1.08}
.skin-atelier .head p{grid-column:2;margin:10px 0 0;max-width:740px}
@media (max-width:820px){.skin-atelier .head{grid-template-columns:1fr;gap:8px}.skin-atelier .head h2,.skin-atelier .head p{grid-column:1}}
.skin-atelier .btn{border-radius:0;border:2px solid var(--heading);text-transform:uppercase;letter-spacing:.08em;font-size:.86rem;font-weight:800;padding:14px 26px}
.skin-atelier .btn-primary{border-color:var(--heading);box-shadow:5px 5px 0 var(--heading)}
.skin-atelier .btn-primary:hover{transform:translate(-2px,-2px);box-shadow:7px 7px 0 var(--heading)}
.skin-atelier .steps-spec{border-top:0;margin-top:-20px}
.skin-atelier .badges{gap:0;border-top:2px solid var(--heading);border-left:2px solid var(--heading)}
.skin-atelier .badge{border:0;border-right:2px solid var(--heading);border-bottom:2px solid var(--heading);border-radius:0;background:transparent;text-align:left;padding:24px}
.skin-atelier .badge .ic{border-radius:0;border:1.5px solid var(--heading);background:var(--card);color:var(--heading);width:44px;height:44px}
.skin-atelier .card.rev{border:2px solid var(--heading);border-radius:0;box-shadow:6px 6px 0 var(--heading);background:var(--card)}
.skin-atelier .av{border-radius:0;border:1.5px solid var(--heading)}
.skin-atelier .tbl{border:2px solid var(--heading);border-radius:0;box-shadow:8px 8px 0 var(--heading)}
.skin-atelier .faq-wrap details{border:2px solid var(--heading);border-radius:0;background:var(--card);box-shadow:4px 4px 0 var(--heading)}
.skin-atelier .tag{border-radius:0;border:1.5px solid var(--heading);background:var(--card)}
.skin-atelier .area iframe,.skin-atelier .dba-card{border-radius:0;border:2px solid var(--heading);box-shadow:8px 8px 0 var(--heading)}
.skin-atelier .cta-band{border-top:3px solid var(--heading)}
`
  ,    /* Precision Blueprint Dossier: 14 unique section designs, technical telemetry chrome, cool architectural slate & cobalt */
    blueprint: `
.skin-blueprint{--bg:#f4f7fb;--surface:#e8eef6;--card:#ffffff;--line:#cbd5e1;--text:#1e293b;--muted:#475569}
.skin-blueprint .bg-light{background:#e8eef6}
.skin-blueprint .sec{border-bottom:1px solid var(--line)}
.skin-blueprint .head{text-align:left;max-width:none;display:flex;flex-direction:column;align-items:flex-start;margin-bottom:36px}
.skin-blueprint .head p{max-width:720px}
.skin-blueprint .eyebrow{background:rgba(var(--accent-rgb),.1);color:var(--accent);border-left:3px solid var(--accent);border-radius:0 4px 4px 0;font-weight:800;letter-spacing:.12em}
`
  };
})();

