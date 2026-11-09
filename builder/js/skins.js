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
.hdr-dark .nav>a:hover,.hdr-dark .dd:hover>a{color:var(--accent)}.hdr-dark .caret{color:#94a3b8}.hdr-dark .mnav summary{color:#fff}
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
.skin-bold .card,.skin-bold .step,.skin-bold .badge,.skin-bold details,.skin-bold .tbl,.skin-bold .form,.skin-bold .chip,.skin-bold .time,.skin-bold .tag,.skin-bold .ba-tab{border-radius:0}
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
.skin-bold summary{text-transform:uppercase;letter-spacing:.03em}
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
.skin-clean details{border:1px solid rgba(var(--accent-rgb),.18);border-radius:20px}
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
`
  };
})();
