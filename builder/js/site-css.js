/* site-css.js : stylesheet shared by every template (templates only change CSS variables + default variants). */
window.Builder = window.Builder || {};
window.Builder.SITE_CSS = `
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:var(--font-b);color:var(--text);background:var(--bg);line-height:1.65;font-size:16px}
h1,h2,h3,h4{font-family:var(--font-h);color:var(--heading);line-height:1.2;margin:0 0 .5em;letter-spacing:-.015em}
h1{font-size:clamp(2rem,4.2vw,3.2rem);font-weight:800}h2{font-size:clamp(1.6rem,3vw,2.3rem);font-weight:800}h3{font-size:1.2rem;font-weight:700}
p{margin:0 0 1em}a{color:inherit}img{max-width:100%;display:block}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.sec{padding:var(--pad) 0}
.sec.pad-compact{padding:calc(var(--pad)*.55) 0}.sec.pad-roomy{padding:calc(var(--pad)*1.45) 0}
.sec.w-wide .wrap{max-width:1400px}.sec.w-narrow .wrap{max-width:960px}
.sec.al-left .head{text-align:left;margin-left:0}.sec.al-center .head{text-align:center}
.sec.nohover .card:hover,.sec.nohover .dba-card:hover{transform:none;box-shadow:0 8px 24px rgba(0,0,0,.05)}
/* entrance animations (runtime adds .in when the section scrolls into view) */
.js-anim [data-anim]{transition:opacity var(--ad,.6s) ease var(--adl,0s),transform var(--ad,.6s) cubic-bezier(.16,1,.3,1) var(--adl,0s)}
.js-anim [data-anim]:not(.in){opacity:0}
.js-anim [data-anim="rise"]:not(.in){transform:translateY(36px)}
.js-anim [data-anim="slide-left"]:not(.in){transform:translateX(-56px)}
.js-anim [data-anim="slide-right"]:not(.in){transform:translateX(56px)}
.js-anim [data-anim="zoom"]:not(.in){transform:scale(.92)}
.js-anim [data-anim="stagger"] :is(.grid,.steps,.badges,.dba-grid,.stats,.stack)>*{transition:opacity .55s ease,transform .6s cubic-bezier(.16,1,.3,1)}
.js-anim [data-anim="stagger"]:not(.in) :is(.grid,.steps,.badges,.dba-grid,.stats,.stack)>*{opacity:0;transform:translateY(28px)}
.js-anim [data-anim="stagger"].in :is(.grid,.steps,.badges,.dba-grid,.stats,.stack)>*:nth-child(2){transition-delay:.1s}
.js-anim [data-anim="stagger"].in :is(.grid,.steps,.badges,.dba-grid,.stats,.stack)>*:nth-child(3){transition-delay:.2s}
.js-anim [data-anim="stagger"].in :is(.grid,.steps,.badges,.dba-grid,.stats,.stack)>*:nth-child(4){transition-delay:.3s}
.js-anim [data-anim="stagger"].in :is(.grid,.steps,.badges,.dba-grid,.stats,.stack)>*:nth-child(n+5){transition-delay:.4s}
@media (prefers-reduced-motion:reduce){.js-anim [data-anim]{opacity:1!important;transform:none!important;transition:none!important}}
.sec-hero{padding:0}
.bg-light{background:var(--surface)}
.bg-dark{background:var(--dark);color:#cbd5e1}.bg-dark h1,.bg-dark h2,.bg-dark h3,.bg-dark h4{color:#fff}
.bg-accent{background:var(--accent);color:#fff}.bg-accent h2,.bg-accent h3{color:#fff}
.eyebrow{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);background:rgba(var(--accent-rgb),.12);padding:6px 14px;border-radius:999px;margin-bottom:14px}
.head{text-align:center;max-width:760px;margin:0 auto 44px}.head p{color:var(--muted);font-size:1.05rem}
.bg-dark .head p{color:#94a3b8}
.btn{display:inline-flex;align-items:center;gap:8px;padding:14px 26px;border-radius:var(--radius);font-weight:700;text-decoration:none;border:2px solid transparent;transition:transform .18s,box-shadow .18s,background .18s;cursor:pointer;font-size:1rem}
.btn:hover{transform:translateY(-2px)}
.btn-primary{background:var(--accent);color:#fff;box-shadow:0 8px 22px rgba(var(--accent-rgb),.32)}
.btn-ghost{border-color:currentColor;background:transparent}
.btn svg{width:18px;height:18px}
svg{width:1em;height:1em}
.ic{display:inline-grid;place-items:center;width:56px;height:56px;border-radius:50%;background:rgba(var(--accent-rgb),.12);color:var(--accent)}
.ic svg{width:26px;height:26px}
/* header */
.hdr{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.hdr .wrap{display:flex;align-items:center;justify-content:space-between;height:74px}
.hdr .logo{margin-right:clamp(16px, 2.5vw, 36px);flex-shrink:0}
.logo{font-family:var(--font-h);font-weight:800;font-size:1.25rem;text-decoration:none;color:var(--heading)}
.nav{display:flex;align-items:center;gap:clamp(10px, 1.6vw, 20px);flex-wrap:nowrap}
.nav>a,.dd>a{color:#334155;font-weight:600;font-size:14.5px;text-decoration:none;transition:color .15s}
.nav>a:hover,.dd:hover>a{color:var(--accent)}
.dd{position:relative;display:inline-flex}.dd>a{padding:14px 0;display:inline-flex;align-items:center;gap:5px}
.caret{font-size:9px;color:#94a3b8;transition:transform .2s,color .15s;display:inline-block}.dd:hover .caret{transform:rotate(180deg);color:var(--accent)}
.dd-menu{display:none;position:absolute;top:100%;left:0;min-width:300px;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 16px 36px rgba(0,0,0,.14);padding:8px 0;z-index:60;animation:ddIn .18s cubic-bezier(.16,1,.3,1)}
@keyframes ddIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.dd:hover .dd-menu{display:block}
.dd-menu a{display:block;padding:11px 20px;color:#1e293b;font-size:13.5px;text-decoration:none;white-space:nowrap;transition:background .15s,color .15s,padding-left .15s}
.dd-menu a:hover{background:#f8fafc;color:var(--accent);padding-left:24px}
.hdr .btn{padding:9px 18px;font-size:14px}
.hdr-call{display:none}
.mnav{display:none}
@media (max-width:767px){.nav{display:none}.hdr-call{display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;padding:8px 14px;border-radius:var(--radius);font-size:13px}
.mnav{display:block;position:relative}.mnav summary{list-style:none;cursor:pointer;font-weight:700;padding:8px 10px}.mnav summary::-webkit-details-marker{display:none}
.mnav div{position:absolute;right:0;top:100%;background:#fff;border:1px solid var(--line);border-radius:12px;min-width:240px;padding:8px 0;box-shadow:0 16px 36px rgba(0,0,0,.15)}.mnav a{display:block;padding:10px 18px;text-decoration:none;color:#1e293b;font-size:14px}}
/* hero */
.hero{position:relative;color:#fff}
.hero .proof{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:700;padding:7px 14px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);color:#fff}
.hero .btns{display:flex;flex-wrap:wrap;gap:14px;margin-top:28px}
.hero--full{min-height:640px;display:flex;align-items:center;background:linear-gradient(180deg,rgba(var(--dark-rgb),.62),rgba(var(--dark-rgb),.86)),var(--hero-img) center/cover no-repeat,var(--dark);text-align:center}
.hero--full .wrap{max-width:900px;padding:90px 24px}.hero--full h1,.hero--centered h1{color:#fff}.hero--full .proof,.hero--full .btns,.hero--centered .proof,.hero--centered .btns{justify-content:center}
.hero--full p,.hero--centered p{font-size:1.15rem;color:#e2e8f0}
.hero--centered{background:linear-gradient(135deg,var(--dark),var(--primary));text-align:center}.hero--centered .wrap{max-width:900px;padding:96px 24px}
.hero--split{background:linear-gradient(180deg,var(--surface),var(--bg));color:var(--text)}
.hero--split .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center;padding:84px 24px}
.hero--split h1{color:var(--heading)}.hero--split p{color:var(--muted);font-size:1.1rem}
.hero--split .chip{background:rgba(var(--accent-rgb),.1);border-color:rgba(var(--accent-rgb),.3);color:var(--heading)}
.hero--split .btn-ghost{color:var(--heading)}
.hero-img{border-radius:calc(var(--radius)*1.6);aspect-ratio:3/2;object-fit:cover;width:100%;box-shadow:0 24px 60px rgba(0,0,0,.2);background:linear-gradient(135deg,var(--surface),var(--line))}
@media (max-width:900px){.hero--split .wrap{grid-template-columns:1fr;padding:56px 20px}.hero--full{min-height:520px}}
/* split */
.split{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}.split.rev .split-media{order:-1}.split.text-only{grid-template-columns:1fr}
.split-media img{width:100%;border-radius:calc(var(--radius)*1.6);box-shadow:0 18px 44px rgba(0,0,0,.14);aspect-ratio:4/3;object-fit:cover}
.checks{list-style:none;padding:0;margin:18px 0 0;display:grid;gap:12px}
.checks li{display:flex;gap:12px;align-items:flex-start}.checks .tick{flex:0 0 24px;width:24px;height:24px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center}.checks .tick svg{width:14px;height:14px}
@media (max-width:900px){.split{grid-template-columns:1fr}.split.rev .split-media{order:0}}
/* cards */
.grid{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(270px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--radius)*1.5);padding:28px 24px;box-shadow:0 8px 24px rgba(0,0,0,.05);transition:transform .25s,box-shadow .25s,border-color .25s;display:flex;flex-direction:column;gap:10px}
.card:hover{transform:translateY(-6px);box-shadow:0 20px 44px rgba(0,0,0,.12);border-color:rgba(var(--accent-rgb),.5)}
.card p{color:var(--muted);margin:0;font-size:.97rem}.card h3{margin:6px 0 0}
.card .more{margin-top:auto;padding-top:10px;color:var(--accent);font-weight:700;text-decoration:none;font-size:.9rem}
.cards-icons .card{align-items:center;text-align:center}
.cards-list{display:grid;gap:16px}.cards-list .card{flex-direction:row;align-items:flex-start;gap:20px}.cards-list .ic{flex:0 0 56px}
.facts{display:grid;gap:12px;margin-top:6px}.fact{border-left:3px solid var(--line);padding-left:12px}.fact.last{border-left-color:var(--accent)}
.fact b{display:block;font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted)}.fact span{font-size:.95rem;color:var(--muted)}
.loc{font-size:11px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--accent)}
.bg-dark .card{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12)}.bg-dark .card p,.bg-dark .fact span{color:#cbd5e1}
/* steps */
.steps{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));counter-reset:s}
.step{position:relative;background:var(--card);border:1px solid var(--line);border-radius:calc(var(--radius)*1.5);padding:28px 24px 24px}
.step .n{width:42px;height:42px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;font-weight:800;margin-bottom:14px}
.step p{color:var(--muted);margin:0 0 12px}.time{display:inline-block;background:rgba(var(--accent-rgb),.12);color:var(--accent);font-weight:700;font-size:12.5px;padding:5px 12px;border-radius:999px}
/* table */
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:calc(var(--radius)*1.5);background:var(--card)}
table{width:100%;border-collapse:collapse;min-width:640px;font-size:.95rem}
th{background:var(--dark);color:#fff;text-align:left;padding:16px 18px;font-size:12.5px;letter-spacing:.05em;text-transform:uppercase}
td{padding:15px 18px;border-top:1px solid var(--line);vertical-align:top}
td:first-child{font-weight:700;color:var(--heading)}
.cmp td:nth-child(2),.cmp th:nth-child(2){background:rgba(var(--accent-rgb),.1);font-weight:700}.cmp th:nth-child(2){background:var(--accent)}
/* reviews */
.stars{color:#f59e0b;letter-spacing:2px;font-size:1.1rem}
.rev .who{display:flex;align-items:center;gap:12px;margin-top:auto;padding-top:8px}
.av{width:42px;height:42px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;font-weight:800}
.who b{display:block;font-size:.92rem}.who small{color:var(--muted)}
.rev q{quotes:none;display:block;color:var(--text);font-size:1rem}
.rev-featured{display:grid;grid-template-columns:1.3fr 1fr;gap:24px}.rev-featured .big q{font-size:1.25rem;line-height:1.55}.rev-featured .stack{display:grid;gap:16px}
@media (max-width:900px){.rev-featured{grid-template-columns:1fr}}
/* faq */
.faq-wrap{display:grid;grid-template-columns:1fr 1.5fr;gap:48px;align-items:start}.faq-wrap.one{grid-template-columns:1fr;max-width:860px;margin:0 auto}
.faq-side{position:sticky;top:100px}
details{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--radius)*1.5);margin-bottom:12px;overflow:hidden;transition:border-color .2s}
details[open]{border-color:var(--accent)}summary{cursor:pointer;list-style:none;padding:18px 22px;font-weight:700;display:flex;justify-content:space-between;gap:16px;align-items:center;color:var(--heading)}
summary::-webkit-details-marker{display:none}summary::after{content:"+";font-size:1.4rem;color:var(--accent);transition:transform .25s}details[open] summary::after{transform:rotate(45deg)}
details .ans{padding:0 22px 20px;color:var(--muted)}
@media (max-width:900px){.faq-wrap{grid-template-columns:1fr}.faq-side{position:static}}
/* cta */
.cta-band{background:linear-gradient(135deg,var(--dark),var(--primary));color:#e2e8f0;text-align:center;padding:72px 24px}.cta-band h2{color:#fff}
.cta-box{background:linear-gradient(135deg,var(--dark),var(--primary));color:#e2e8f0;text-align:center;border-radius:calc(var(--radius)*2.4);padding:64px 32px;position:relative;overflow:hidden}.cta-box h2{color:#fff}
.cta-box::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 85% 10%,rgba(var(--accent-rgb),.28),transparent 45%)}.cta-box>*{position:relative}
.cta-inner{max-width:760px;margin:0 auto}.cta-note{margin-top:20px;font-size:.9rem;color:#94a3b8}
.sec-cta{padding:calc(var(--pad)*.8) 0}.sec-cta.is-band{padding:0}
/* badges */
.badges{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
.badge{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--radius)*1.5);padding:22px 18px;text-align:center}
.badge .ic{margin-bottom:10px}.badge b{display:block;color:var(--heading)}.badge span{font-size:.9rem;color:var(--muted)}
/* area */
.area{display:grid;grid-template-columns:1fr 1.2fr;gap:36px;align-items:stretch}
.area iframe{width:100%;min-height:340px;height:100%;border:0;border-radius:calc(var(--radius)*1.5);box-shadow:0 12px 30px rgba(0,0,0,.12)}
.tags{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}.tag{background:rgba(var(--accent-rgb),.1);color:var(--heading);padding:7px 14px;border-radius:999px;font-size:.88rem;font-weight:600}
@media (max-width:900px){.area{grid-template-columns:1fr}}
/* gallery */
.ba{display:grid;grid-template-columns:1fr 1fr;gap:24px}.ba figure{margin:0;position:relative;border-radius:calc(var(--radius)*1.5);overflow:hidden;background:var(--dark)}
.ba img{width:100%;aspect-ratio:4/3;object-fit:cover}.ba figcaption{padding:16px 18px;background:var(--card);border:1px solid var(--line);border-top:0;color:var(--muted);font-size:.95rem}
.ba .tagb{position:absolute;top:14px;left:14px;font-size:11px;font-weight:800;letter-spacing:.07em;padding:5px 12px;border-radius:6px;color:#fff;background:#dc2626}.ba .after .tagb{background:#059669}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px;margin-top:28px;background:var(--dark);border-radius:calc(var(--radius)*1.5);padding:26px}
.stats div{color:#94a3b8;font-size:.85rem}.stats b{display:block;font-size:1.7rem;color:var(--accent);font-family:var(--font-h)}
@media (max-width:700px){.ba{grid-template-columns:1fr}}
/* article */
.article{max-width:820px;margin:0 auto}.article h2{margin-top:1.4em}.article ul,.article ol{padding-left:1.3em}.article li{margin-bottom:.4em}
.article blockquote{border-left:4px solid var(--accent);margin:1.2em 0;padding:.4em 1em;color:var(--muted);font-style:italic;background:var(--surface);border-radius:0 8px 8px 0}
.article .tbl{margin:1.2em 0}.byline{color:var(--muted);font-size:.9rem}
.lead{font-size:1.2rem;color:var(--muted)}
/* forms */
.form{background:var(--card);border:1px solid var(--line);border-radius:calc(var(--radius)*1.6);padding:30px;display:grid;gap:14px;box-shadow:0 14px 36px rgba(0,0,0,.08)}
.form label{font-size:12px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:5px}
.form input,.form select,.form textarea{width:100%;padding:12px 14px;border:1px solid var(--line);border-radius:var(--radius);font:inherit;background:#fff}
.nap{display:grid;grid-template-columns:1fr 1fr;gap:36px}@media (max-width:900px){.nap{grid-template-columns:1fr}}
/* footer */
.ftr{background:var(--dark);color:#94a3b8;padding:56px 0 24px;margin-top:0}.ftr h4{color:#fff;font-size:.95rem;margin-bottom:12px}
.ftr .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:32px}.ftr a{display:block;color:#94a3b8;text-decoration:none;margin-bottom:8px;font-size:.92rem}.ftr a:hover{color:#fff}
.ftr .copy{border-top:1px solid rgba(255,255,255,.1);margin-top:34px;padding-top:18px;font-size:.85rem}
@media (max-width:800px){.ftr .cols{grid-template-columns:1fr 1fr}}
/* gallery: Denton split cards + wipe slider */
.dba-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.dba-card{position:relative;border-radius:18px;overflow:hidden;box-shadow:0 12px 32px rgba(0,0,0,.08);aspect-ratio:4/3;background:#0f172a;border:1px solid rgba(0,0,0,.08);transition:transform .3s cubic-bezier(.16,1,.3,1),box-shadow .3s}
.dba-card:hover{transform:translateY(-5px);box-shadow:0 20px 48px rgba(0,0,0,.16)}
.dba-card img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s ease}.dba-card:hover img{transform:scale(1.04)}
.dba-card figcaption{position:absolute;left:0;right:0;bottom:0;padding:34px 16px 14px;color:#fff;font-size:.85rem;font-weight:700;background:linear-gradient(to top,rgba(0,0,0,.9),transparent)}
.dba-card{margin:0}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:20px;margin-top:36px;background:#0f172a;color:#fff;border-radius:16px;padding:26px 32px;box-shadow:0 12px 32px rgba(15,23,42,.15)}
.metrics div{border-right:1px solid rgba(255,255,255,.1);padding-right:16px;color:#94a3b8;font-size:.8rem;line-height:1.4}.metrics div:last-child{border:0}
.metrics b{display:block;font-size:1.85rem;color:var(--accent);font-family:var(--font-h);letter-spacing:-.02em;line-height:1.1;margin-bottom:4px}
@media (max-width:1024px){.dba-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media (max-width:640px){.dba-grid{grid-template-columns:1fr}}
.ba-tabs{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:22px}
.ba-tab{padding:9px 18px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--muted);font:inherit;font-weight:700;font-size:.85rem;cursor:pointer;transition:all .2s}
.ba-tab.on{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 4px 14px rgba(var(--accent-rgb),.35)}
.ba-slider{--pos:50%;position:relative;max-width:960px;aspect-ratio:2/1;margin:0 auto;overflow:hidden;border-radius:16px;box-shadow:0 16px 40px rgba(0,0,0,.2);background:#0f172a}
.ba-slider img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ba-slider .aft{clip-path:inset(0 calc(100% - var(--pos)) 0 0)}
.ba-slider .bar{position:absolute;top:0;bottom:0;left:var(--pos);width:3px;background:#fff;box-shadow:0 0 14px rgba(0,0,0,.6);transform:translateX(-50%)}
.ba-slider .tg{position:absolute;top:14px;padding:6px 14px;border-radius:6px;font-size:11px;font-weight:800;letter-spacing:.06em;color:#fff;z-index:2}.ba-slider .tg.b{right:14px;background:rgba(220,38,38,.95)}.ba-slider .tg.a{left:14px;background:rgba(16,185,129,.95)}
.ba-range{position:absolute;left:8%;right:8%;bottom:16px;width:84%;z-index:3;accent-color:var(--accent)}
.ba-cap{text-align:center;color:var(--muted);margin:14px auto 0;max-width:760px;font-size:.95rem}
/* hero effects */
.hero{overflow:hidden}.hero>.wrap{position:relative;z-index:2}
.hero[data-fx]::before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none}
.hero[data-fx="airflow"]::before{background:repeating-linear-gradient(115deg,transparent 0 60px,rgba(255,255,255,.08) 60px 62px,transparent 62px 140px);background-size:280px 100%;animation:fxAir 7s linear infinite}
@keyframes fxAir{to{background-position:280px 0}}
.hero[data-fx="motes"]::before{background-image:radial-gradient(circle,rgba(255,255,255,.6) 1.5px,transparent 2px),radial-gradient(circle,rgba(var(--accent-rgb),.7) 2px,transparent 3px);background-size:90px 90px,140px 140px;background-position:0 0,40px 60px;animation:fxMote 14s linear infinite;opacity:.55}
@keyframes fxMote{to{background-position:0 -180px,40px -220px}}
.hero[data-fx="blueprint"]::before{background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:40px 40px;animation:fxGrid 20s linear infinite}
@keyframes fxGrid{to{background-position:0 400px,400px 0}}
.hero--split[data-fx]::before{filter:invert(1);opacity:.35}
.logo{display:inline-flex;align-items:center;gap:10px}.logo img{height:var(--logo-h,44px);width:auto;display:block}
.ftr .logo img{height:calc(var(--logo-h,44px)*.9);margin-bottom:12px}
.callbar{display:none}
@media (max-width:767px){.callbar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:70;background:var(--accent);color:#fff;justify-content:center;align-items:center;gap:8px;padding:14px;font-weight:800;text-decoration:none}body{padding-bottom:54px}}
`;

