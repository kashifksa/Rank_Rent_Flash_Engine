/* site.js : state, section resolution and full-page HTML assembly (used by preview AND export). */
(function () {
  const B = (window.Builder = window.Builder || {});
  const D = () => window.BUILDER_DATA;
  const esc = B.esc;

  B.state = { template: 'cornerstone', theme: {}, pages: {} };

  const EYEBROW = {
    'services-grid': 'Our Services', '03_services_grid': 'Our Services', '03_services_overview': 'Our Services',
    'why-us': 'Why Choose Us', '04_why_choose_us': 'Why Choose Us',
    'process': 'How It Works', '05_process': 'How It Works',
    'testimonials': 'Customer Reviews', '06_local_proof': 'Local Reviews', '04_local_proof': 'Local Reviews',
    'faq': 'FAQ', '09_faq': 'FAQ', '07_faq': 'FAQ', '05_local_faq': 'FAQ',
    'awards': 'Certifications', 'comparison-table': 'How We Compare', 'before-after': 'Verified Work',
    'case-studies': 'Real Projects', 'service-area': 'Service Area', '07_service_area': 'Service Area', '06_service_area': 'Service Area',
    '04_credentials_display': 'Credentials', '06_trust_signals': 'Trust Signals', '03_team_credentials': 'Our Technicians'
  };
  const SPECIAL = { '01_header': 'postHeader', '01_contact_hero': 'hero', '02_contact_form': 'form', '03_nap_block': 'nap', '07_service_area_nap': 'area' };

  B.pageIds = () => Object.keys(D().pages);
  B.page = pid => D().pages[pid];
  B.ps = function (pid) {
    const s = B.state.pages;
    if (!s[pid]) s[pid] = { order: null, hidden: {}, variants: {}, bg: {}, images: {}, models: {}, srcHash: {}, added: {}, opts: {} };
    if (!s[pid].srcHash) s[pid].srcHash = {};
    if (!s[pid].opts) s[pid].opts = {};
    return s[pid];
  };
  B.fileName = function (pid) {
    const p = B.page(pid);
    if (p.type === 'homepage') return 'index.html';
    return ((p.slug && p.slug !== '/') ? p.slug : pid).replace(/^\/|\/$/g, '') + '.html';
  };
  B.sectionList = function (pid) {
    const ps = B.ps(pid), base = Object.keys(B.page(pid).sections);
    if (!ps.order) return base.concat(Object.keys(ps.added).filter(k => base.indexOf(k) < 0));
    const keep = ps.order.filter(k => base.indexOf(k) > -1 || ps.added[k]);
    base.forEach(k => { if (keep.indexOf(k) < 0) keep.push(k); });
    return keep;
  };
  B.sectionMd = (pid, sid) => B.ps(pid).added[sid] || B.page(pid).sections[sid] || '';
  B._cache = {};
  B.hash = function (s) { let h = 5381; s = String(s); for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0; return String(h); };
  /* read-only model (parsed from the .md; never persisted unless edited) */
  B.getModel = function (pid, sid) {
    const ps = B.ps(pid);
    if (ps.models[sid]) return ps.models[sid];
    const k = pid + '|' + sid;
    if (!B._cache[k]) B._cache[k] = B.parseSection(B.sectionMd(pid, sid));
    return B._cache[k];
  };
  /* writable model: first edit snapshots the model and remembers which source text it came from */
  B.editModel = function (pid, sid) {
    const ps = B.ps(pid);
    if (!ps.models[sid]) {
      ps.models[sid] = JSON.parse(JSON.stringify(B.getModel(pid, sid)));
      ps.srcHash[sid] = B.hash(B.sectionMd(pid, sid));
    }
    return ps.models[sid];
  };
  B.resetSection = function (pid, sid) { const ps = B.ps(pid); delete ps.models[sid]; delete ps.srcHash[sid]; delete B._cache[pid + '|' + sid]; };
  B.hasEdits = (pid, sid) => !!B.ps(pid).models[sid];
  /* drop edits whose source .md changed since (files win, so content never silently drifts) */
  B.reconcile = function () {
    let dropped = 0;
    Object.keys(B.state.pages).forEach(pid => {
      if (!B.page(pid)) { delete B.state.pages[pid]; return; }
      const ps = B.ps(pid);
      Object.keys(ps.models).forEach(sid => {
        if (ps.added[sid]) return;
        if (ps.srcHash[sid] !== B.hash(B.sectionMd(pid, sid))) { delete ps.models[sid]; delete ps.srcHash[sid]; dropped++; }
      });
    });
    return dropped;
  };
  B.sectionSchema = function (pid, sid) {
    const t = B.page(pid).type, sp = D().schema[t];
    return sp ? sp.sections.find(s => s.id === sid) : null;
  };
  B.sectionType = function (pid, sid) {
    const s = B.sectionSchema(pid, sid);
    if (s && s.render) return s.render;
    if (SPECIAL[sid]) return SPECIAL[sid];
    if (/faq/.test(sid)) return 'faq';
    if (/cta/.test(sid)) return 'cta';
    return 'article';
  };
  B.sectionLabel = function (pid, sid) {
    const s = B.sectionSchema(pid, sid);
    if (s && s.label) return s.label;
    return sid.replace(/^\d+_/, '').replace(/[-_]/g, ' ').replace(/\b\w/g, x => x.toUpperCase());
  };
  B.tpl = () => B.TEMPLATES[B.state.template] || B.TEMPLATES.cornerstone;
  B.variantsFor = type => (B.BLOCKS[type] || B.BLOCKS.article).variants;
  B.getVariant = function (pid, sid) {
    const type = B.sectionType(pid, sid), list = B.variantsFor(type), tpl = B.tpl();
    const v = B.ps(pid).variants[sid] || (tpl.sectionVariants && tpl.sectionVariants[sid]) || tpl.variants[type];
    return list.indexOf(v) > -1 ? v : list[0];
  };
  B.theme = function () { return Object.assign({}, B.tpl().theme, B.state.theme || {}); };

  /* per-section options (animation, spacing, width, alignment, hover, hero effect) */
  const OPT_DEFAULTS = { anim: 'auto', speed: 'normal', delay: 0, pad: 'auto', width: 'auto', align: 'auto', hover: 'on', fx: 'auto' };
  B.getOpts = (pid, sid) => Object.assign({}, OPT_DEFAULTS, B.ps(pid).opts[sid] || {});
  B.effAnim = o => o.anim !== 'auto' ? o.anim : (B.theme().anim || (B.tpl().motion || {}).anim || 'none');
  B.effFx = o => o.fx !== 'auto' ? o.fx : (B.theme().fx || (B.tpl().motion || {}).fx || 'none');

  /* brand: webp logo + favicon */
  B.brand = () => Object.assign({ logoSrc: 'auto', logoData: '', height: 56, mode: 'auto', favicon: true, footer: true }, B.state.brand || {});
  B.logoUrl = function (preview, dark) {
    const b = B.brand(), d = D().brand || {};
    if (b.logoSrc === 'none') return '';
    if (b.logoSrc === 'upload' && b.logoData) return b.logoData;
    const f = (dark && d.logoLight) ? d.logoLight : d.logo;
    return f ? (preview ? '../' : '') + f : '';
  };
  B.faviconUrl = function (preview) {
    const b = B.brand(), d = D().brand || {};
    return b.favicon && d.favicon ? (preview ? '../' : '') + d.favicon : '';
  };

  function hexRgb(h) {
    h = (h || '#000').replace('#', ''); if (h.length === 3) h = h.split('').map(x => x + x).join('');
    const n = parseInt(h, 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function lum(h) { const [r, g, b] = hexRgb(h); return (0.299 * r + 0.587 * g + 0.114 * b) / 255; }
  function relLum(h) {
    const c = hexRgb(h).map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }

  B.cssVars = function () {
    const t = B.theme(), f = B.FONTS[t.font] || B.FONTS.technical;
    const [ar, ag, ab] = hexRgb(t.accent), [pr, pg, pb] = hexRgb(t.primary);
    const al = relLum(t.accent), btnFg = (1.05 / (al + 0.05)) >= 4.5 ? '#ffffff' : '#111418';
    const pad = B.DENSITY[t.density] || 76;
    return ':root{--primary:' + t.primary + ';--dark:' + t.primary + ';--dark-rgb:' + pr + ',' + pg + ',' + pb + ';--accent:' + t.accent + ';--accent-rgb:' + ar + ',' + ag + ',' + ab + ';--btn-fg:' + btnFg +
      ';--logo-h:' + (B.brand().height || 56) + 'px;--heading:' + (lum(t.primary) < 0.4 ? t.primary : '#0f172a') + ';--text:#334155;--muted:#64748b;--bg:#fff;--surface:#f8fafc;--card:#fff;--line:#e2e8f0;--radius:' + t.radius + 'px;--pad:' + pad +
      'px;--font-h:"' + f.h + '",sans-serif;--font-b:"' + f.b + '",sans-serif}';
  };

  /* images */
  function imgSrc(page, filename, base) {
    const dir = (page.img_dir || 'images/homepage').replace(/^images\//, '');
    return base + dir + '/' + filename;
  }
  function makeImageCtx(pid, base, used) {
    const page = B.page(pid), imgs = B.contentImages(pid);
    const mk = i => ({ src: imgSrc(page, i.filename, base), alt: i.alt_text || page.title, file: i.filename });
    return {
      pick: re => { const i = imgs.find(x => re.test(x.filename) || re.test(x.slot || '')); return i ? mk(i) : null; },
      forSection: (sid, type) => {
        const ov = B.ps(pid).images[sid];
        if (ov === 'none') return null;
        if (ov) { const i = imgs.find(x => x.filename === ov); return i ? mk(i) : null; }
        let i = null;
        if (type === 'hero') i = imgs.find(x => x.slot === 'hero') || imgs[0];
        else if (type === 'split') {
          i = imgs.find(x => !used[x.filename] && /intro|primary|diagnos|local|context|origin|team|community|story|equipment/.test((x.slot || '') + x.filename)) ||
              imgs.find(x => !used[x.filename] && x.slot !== 'hero');
        }
        if (i) used[i.filename] = true;
        return i ? mk(i) : null;
      }
    };
  }
  B.contentImages = pid => (B.page(pid).images || []).filter(i => !/logo|favicon/i.test((i.slot || '') + ' ' + (i.filename || '')));
  B.imageOptions = pid => B.contentImages(pid).map(i => ({ file: i.filename, alt: i.alt_text || i.filename }));

  function mergedChips(pid) {
    const m = B.page(pid).merged || {}, k = Object.keys(m)[0];
    if (!k) return [];
    const mod = B.parseSection(m[k]);
    return mod.bullets.map(b => (b.label ? b.label + ' ' : '') + b.text).filter(Boolean);
  }

  /* alternate plain / light backgrounds, counting only normal content sections (stable for partial re-render) */
  function autoBg(pid, sid, type) {
    if (type === 'hero' || type === 'cta') return 'none';
    const ps = B.ps(pid); let n = 0;
    for (const s of B.sectionList(pid)) {
      if (ps.hidden[s]) continue;
      if (s === sid) break;
      const t = B.sectionType(pid, s);
      if (t !== 'hero' && t !== 'cta') n++;
    }
    return n % 2 ? 'light' : 'none';
  }

  function renderSection(pid, sid, i, ctxBase, selected) {
    const type = B.sectionType(pid, sid), block = B.BLOCKS[type] || B.BLOCKS.article;
    const model = B.getModel(pid, sid), variant = B.getVariant(pid, sid), ps = B.ps(pid);
    const order = B.sectionList(pid).filter(s => !ps.hidden[s]);
    const next = order[order.indexOf(sid) + 1];
    const c = Object.assign({}, ctxBase, {
      fx: type === 'hero' ? B.effFx(B.getOpts(pid, sid)) : 'none', variant, sid, nextSid: next, eyebrow: model.eyebrow === 'none' ? '' : (model.eyebrow != null ? model.eyebrow : (EYEBROW[sid] || '')),
      img: () => ctxBase.imgs.forSection(sid, type), pick: ctxBase.imgs.pick,
      merged: type === 'hero' ? mergedChips(pid) : []
    });
    let inner;
    try { inner = block.render(model, c); } catch (e) { inner = '<div class="wrap"><p style="color:#b91c1c">Render error in ' + esc(sid) + ': ' + esc(e.message) + '</p></div>'; }
    let bg = ps.bg[sid] || 'auto';
    if (bg === 'auto') bg = autoBg(pid, sid, type);
    const o = B.getOpts(pid, sid), anim = B.effAnim(o);
    const cls = 'sec sec-' + type + ' bg-' + bg + (type === 'cta' && variant === 'band' ? ' is-band' : '') + (selected === sid ? ' is-selected' : '') +
      (o.pad === 'compact' ? ' pad-compact' : o.pad === 'roomy' ? ' pad-roomy' : '') + (o.width === 'wide' ? ' w-wide' : o.width === 'narrow' ? ' w-narrow' : '') +
      (o.align === 'left' ? ' al-left' : o.align === 'center' ? ' al-center' : '') + (o.hover === 'off' ? ' nohover' : '') + (ctxBase.instant ? ' in' : '');
    const dur = { fast: '.35s', normal: '.6s', slow: '1.05s' }[o.speed] || '.6s';
    const aa = anim && anim !== 'none' ? ' data-anim="' + anim + '" style="--ad:' + dur + ';--adl:' + (Number(o.delay) || 0) + 's"' : '';
    return '<section class="' + cls + '" id="sec-' + esc(sid) + '" data-sec="' + esc(sid) + '"' + aa + '>' + inner + '</section>';
  }
  B.renderSectionHtml = function (pid, sid, opts) {
    opts = opts || {};
    const base = B.siteCtx(pid, opts.preview);
    base.instant = !!opts.instant;
    return renderSection(pid, sid, 0, base, opts.selected);
  };

  B.siteCtx = function (pid, preview) {
    const d = D(), page = B.page(pid);
    const base = preview ? '../images/' : 'images/', imgs = B.contentImages(pid);
    const num = s => parseInt((String(s).match(/(\d+)$/) || [0, 0])[1], 10);
    const pretty = s => String(s).replace(/[-_]+/g, ' ').trim().replace(/\b\w/g, x => x.toUpperCase());
    return {
      page, pid, nap: d.nap, brief: d.brief, phone: d.nap.phone, preview: !!preview,
      imgs: makeImageCtx(pid, base, {}), altCounter: { n: 0 },
      src: f => imgSrc(page, f, base),
      galleryCards: m => Array.isArray(m.cards) ? m.cards :
        imgs.filter(i => /^before-after-\d+$/.test(i.slot || '')).sort((a, b) => num(a.slot) - num(b.slot)).map(i => ({ img: i.filename, alt: i.alt_text || '', caption: '' })),
      galleryPairs: m => {
        if (Array.isArray(m.pairs)) return m.pairs;
        const map = {};
        imgs.forEach(i => {
          const s = i.slot || '';
          if (/^before-after-\d+$/.test(s) || !/(before|after)/.test(s)) return;
          const key = s.replace(/before|after/g, '').replace(/-+/g, '-').replace(/^-|-$/g, '');
          (map[key] = map[key] || {})[/before/.test(s) ? 'before' : 'after'] = i.filename;
        });
        return Object.keys(map).filter(k => map[k].before && map[k].after).map((k, n) => ({ before: map[k].before, after: map[k].after, label: 'Case ' + String(n + 1).padStart(2, '0') + ': ' + pretty(k || 'Service'), caption: '' }));
      }
    };
  };

  function header(pid, preview) {
    const d = D(), nap = d.nap, pages = Object.values(d.pages);
    const svc = pages.filter(p => p.type === 'service'), loc = pages.filter(p => p.type === 'location');
    const blog = pages.find(p => p.type === 'blog'), about = pages.find(p => p.type === 'about'), contact = pages.find(p => p.type === 'contact');
    const home = pages.find(p => p.type === 'homepage');
    const hasRev = home && home.sections && home.sections['testimonials'];
    const dd = (label, items, href) => '<div class="dd"><a href="' + href + '">' + label + ' <span class="caret">&#9660;</span></a><div class="dd-menu">' +
      items.map(p => '<a href="' + B.fileName(p.id) + '">' + esc(p.nav || p.title) + '</a>').join('') + '</div></div>';
    const homeHref = preview ? 'index.html' : '/';
    const links = [
      '<a href="' + homeHref + '">Home</a>',
      svc.length ? dd('Services', svc, homeHref + '#sec-services-grid') : '',
      loc.length ? dd('Locations', loc, homeHref + '#sec-service-area') : '',
      blog ? '<a href="' + B.fileName(blog.id) + '">Blog</a>' : '',
      hasRev ? '<a href="' + homeHref + '#sec-testimonials">Reviews</a>' : '',
      about ? '<a href="' + B.fileName(about.id) + '">About</a>' : '',
      contact ? '<a href="' + B.fileName(contact.id) + '">Contact</a>' : ''
    ].filter(Boolean);
    const tel = 'tel:' + nap.phone.replace(/[^\d+]/g, '');
    const hv = B.tpl().header || 'classic';
    const lg = B.logoUrl(preview, hv === 'dark'), bm = B.brand().mode, mode = bm === 'auto' ? (lg ? 'logo' : 'text') : bm;
    const logoInner = (lg && mode !== 'text' ? '<img src="' + esc(lg) + '" alt="' + esc(nap.company_name) + ' logo">' : '') + ((mode !== 'logo' || !lg) ? '<span>' + esc(nap.company_name) + '</span>' : '');
    if (hv === 'console') {
      const cred = (d.brief.credentials && d.brief.credentials[0]) || 'Certified Specialists';
      return '<div class="console-strip"><div class="wrap"><span>SYS.STATUS // ACTIVE FIELD DISPATCH</span><span>ZONE: ' + esc((d.brief.city + ', ' + d.brief.state).toUpperCase()) + '</span><span>ACCREDITATION: ' + esc(cred.toUpperCase()) + '</span></div></div>' +
        '<header class="hdr hdr-console"><div class="wrap"><a class="logo" href="' + homeHref + '">' + logoInner + '</a>' +
        '<nav class="nav console-nav">' + links.join('') + '</nav>' +
        '<a class="console-cta" href="' + tel + '"><span class="c-dot"></span><div><small>DIRECT DISPATCH</small><b>' + esc(nap.phone) + '</b></div></a>' +
        '<a class="hdr-call" href="' + tel + '">' + B.icon('phone') + ' Call</a>' +
        '<details class="mnav"><summary>Menu</summary><div>' + links.join('') + '</div></details></div></header>';
    }
    if (hv === 'gridline') {
      return '<header class="hdr hdr-gridline"><div class="wrap"><a class="logo gl-cell gl-logo" href="' + homeHref + '">' + logoInner + '</a>' +
        '<nav class="nav gl-cell gl-nav">' + links.join('') + '</nav>' +
        '<a class="gl-cta" href="' + tel + '"><small>DIRECT DISPATCH</small><b>' + esc(nap.phone) + ' &rarr;</b></a>' +
        '<a class="hdr-call" href="' + tel + '">' + B.icon('phone') + ' Call</a>' +
        '<details class="mnav"><summary>Menu</summary><div>' + links.join('') + '</div></details></div></header>';
    }
    if (hv === 'decker') {
      const cred = (d.brief.credentials && d.brief.credentials[0]) || 'Licensed & Insured';
      return '<header class="hdr hdr-decker"><div class="deck-top"><div class="wrap"><a class="logo" href="' + homeHref + '">' + logoInner + '</a>' +
        '<div class="deck-info"><div class="deck-pill">' + B.icon('pin') + '<div><small>Service Area</small><b>' + esc(d.brief.city + ', ' + d.brief.state) + '</b></div></div>' +
        '<div class="deck-pill">' + B.icon('shield') + '<div><small>Accreditation</small><b>' + esc(cred) + '</b></div></div>' +
        '<a class="btn btn-primary" href="' + tel + '">' + B.icon('phone') + ' ' + esc(nap.phone) + '</a></div>' +
        '<a class="hdr-call" href="' + tel + '">' + B.icon('phone') + ' Call</a>' +
        '<details class="mnav"><summary>Menu</summary><div>' + links.join('') + '</div></details></div></div>' +
        '<div class="deck-nav"><div class="wrap"><nav class="nav">' + links.join('') + '</nav>' +
        (nap.email ? '<a class="deck-mail" href="mailto:' + esc(nap.email) + '">' + esc(nap.email) + '</a>' : '') + '</div></div></header>';
    }
    const topbar = hv === 'topbar' ? '<div class="topbar"><div class="wrap"><span>Serving ' + esc(d.brief.city) + ', ' + esc(d.brief.state) + ' and nearby communities</span><span><a href="' + tel + '">Call ' + esc(nap.phone) + '</a>' + (nap.email ? '<a href="mailto:' + esc(nap.email) + '">' + esc(nap.email) + '</a>' : '') + '</span></div></div>' : '';
    const hcls = hv === 'dark' ? ' hdr-dark' : hv === 'floating' ? ' hdr-floating' : '';
    return topbar + '<header class="hdr' + hcls + '"><div class="wrap"><a class="logo" href="' + homeHref + '">' + logoInner + '</a><nav class="nav">' + links.join('') +
      '<a class="btn btn-primary" href="' + tel + '">' + esc(nap.phone) + '</a></nav>' +
      '<a class="hdr-call" href="' + tel + '">' + B.icon('phone') + ' Call</a>' +
      '<details class="mnav"><summary>Menu</summary><div>' + links.join('') + '</div></details></div></header>';
  }
  function footer(preview) {
    const d = D(), nap = d.nap, pages = Object.values(d.pages), homeHref = preview ? 'index.html' : '/';
    const list = t => pages.filter(p => p.type === t).map(p => '<a href="' + B.fileName(p.id) + '">' + esc(p.nav || p.title) + '</a>').join('');
    const flg = B.brand().footer ? B.logoUrl(preview, true) : '';
    const tel = 'tel:' + nap.phone.replace(/[^\d+]/g, '');
    if (B.tpl().skin === 'blueprint') {
      return '<footer class="ftr ftr-blueprint"><div class="wrap"><div class="ftr-banner"><div><small>24/7 FIELD DISPATCH DESK // ' + esc((d.brief.city + ', ' + d.brief.state).toUpperCase()) + '</small><h3>Ready to Schedule Your Inspection?</h3></div>' +
        '<a class="btn btn-primary" href="' + tel + '">' + B.icon('phone') + ' Call ' + esc(nap.phone) + '</a></div>' +
        '<div class="cols"><div>' + (flg ? '<a class="logo" href="' + homeHref + '"><img src="' + esc(flg) + '" alt="' + esc(nap.company_name) + '"></a>' : '') + '<h4>' + esc(nap.company_name) + '</h4><p>' + esc(d.brief.niche) + ' in ' + esc(d.brief.city) + ', ' + esc(d.brief.state) +
        '.</p><p>' + esc(nap.address) + '</p></div><div><h4>Services</h4>' + list('service') + '</div><div><h4>Locations</h4>' + list('location') +
        '</div><div><h4>Direct Telemetry</h4><a href="' + tel + '">' + esc(nap.phone) + '</a><a href="mailto:' + esc(nap.email) + '">' + esc(nap.email) + '</a></div></div>' +
        '<div class="copy">&copy; ' + new Date().getFullYear() + ' ' + esc(nap.company_name) + '. All rights reserved.</div></div></footer>' +
        '<a class="callbar" href="' + tel + '">' + B.icon('phone') + ' Call ' + esc(nap.phone) + '</a>';
    }
    return '<footer class="ftr"><div class="wrap"><div class="cols"><div>' + (flg ? '<a class="logo" href="' + homeHref + '"><img src="' + esc(flg) + '" alt="' + esc(nap.company_name) + '"></a>' : '') + '<h4>' + esc(nap.company_name) + '</h4><p>' + esc(d.brief.niche) + ' in ' + esc(d.brief.city) + ', ' + esc(d.brief.state) +
      '.</p><p>' + esc(nap.address) + '</p></div><div><h4>Services</h4>' + list('service') + '</div><div><h4>Locations</h4>' + list('location') +
      '</div><div><h4>Contact</h4><a href="tel:' + nap.phone.replace(/[^\d+]/g, '') + '">' + esc(nap.phone) + '</a><a href="mailto:' + esc(nap.email) + '">' + esc(nap.email) + '</a></div></div>' +
      '<div class="copy">&copy; ' + new Date().getFullYear() + ' ' + esc(nap.company_name) + '. All rights reserved.</div></div></footer>' +
      '<a class="callbar" href="tel:' + nap.phone.replace(/[^\d+]/g, '') + '">' + B.icon('phone') + ' Call ' + esc(nap.phone) + '</a>';
  }

  const PREVIEW_JS = '(function(){var st=document.createElement("style");st.textContent="[data-sec]{cursor:pointer}[data-sec]:hover{outline:2px dashed rgba(var(--accent-rgb),.65);outline-offset:-2px}.is-selected{outline:3px solid var(--accent)!important;outline-offset:-3px}";document.head.appendChild(st);' +
    'document.addEventListener("click",function(e){var a=e.target.closest("a");if(a){e.preventDefault();var h=a.getAttribute("href")||"";if(h.indexOf("#")===0){var el=h.length>1?document.querySelector(h):null;if(el)el.scrollIntoView({behavior:"smooth",block:"start"});return}if(!h||h.indexOf("tel:")===0||h.indexOf("mailto:")===0||/^https?:/.test(h))return;parent.postMessage({b5:"nav",href:h},"*");return}var s=e.target.closest("[data-sec]");if(s){e.preventDefault();parent.postMessage({b5:"select",sid:s.getAttribute("data-sec")},"*")}},true);' +
    'window.addEventListener("message",function(ev){var d=ev.data||{};if(d.b5==="replace"){var el=document.querySelector("[data-sec=\\""+d.sid+"\\"]");if(el){el.outerHTML=d.html}}' +
    'if(d.b5==="replay"){var r=document.querySelector("[data-sec=\\""+d.sid+"\\"]");if(r){r.classList.remove("in");void r.offsetWidth;setTimeout(function(){r.classList.add("in")},80)}}' +
    'if(d.b5==="setScroll"){window.scrollTo(0,d.y||0)}if(d.b5==="select"){document.querySelectorAll(".is-selected").forEach(function(x){x.classList.remove("is-selected")});var t=document.querySelector("[data-sec=\\""+d.sid+"\\"]");if(t){t.classList.add("is-selected");if(d.scroll)t.scrollIntoView({behavior:"smooth",block:"start"})}}});' +
    'var tk=0;window.addEventListener("scroll",function(){if(tk)return;tk=1;requestAnimationFrame(function(){tk=0;parent.postMessage({b5:"scroll",y:window.scrollY},"*")})});})();';

  const RUNTIME_JS = '(function(){if(/^https?:/.test(location.protocol)&&/\\/index\\.html$/i.test(location.pathname)){try{history.replaceState(null,"",location.pathname.replace(/index\\.html$/i,"")+location.search+location.hash)}catch(e){}}' +
    'var d=document;d.documentElement.classList.add("js-anim");function chk(){var l=d.querySelectorAll("[data-anim]:not(.in)");for(var i=0;i<l.length;i++){var r=l[i].getBoundingClientRect();if(r.top<innerHeight*0.92&&r.bottom>0)l[i].classList.add("in")}}' +
    'addEventListener("scroll",chk,{passive:true});addEventListener("resize",chk);addEventListener("load",chk);setTimeout(chk,60);setTimeout(chk,500);' +
    'd.addEventListener("input",function(e){var t=e.target;if(t.classList&&t.classList.contains("ba-range")){t.closest(".ba-slider").style.setProperty("--pos",t.value+"%")}});' +
    'd.addEventListener("click",function(e){var b=e.target.closest(".ba-tab");if(!b)return;var w=b.closest(".ba-wrap");w.querySelectorAll(".ba-tab").forEach(function(x){x.classList.toggle("on",x===b)});w.querySelectorAll(".ba-case").forEach(function(c,i){c.hidden=(String(i)!==b.getAttribute("data-i"))})});})();';

  B.buildDocument = function (pid, opts) {
    opts = opts || {};
    const d = D(), page = B.page(pid), meta = page.meta || {}, f = B.FONTS[B.theme().font] || B.FONTS.technical;
    const ps = B.ps(pid), base = B.siteCtx(pid, opts.preview);
    const body = B.sectionList(pid).filter(s => !ps.hidden[s]).map((sid, i) => renderSection(pid, sid, i, base, opts.selected)).join('\n');
    const title = meta.meta_title || page.title, desc = meta.meta_description || '';
    const canon = meta.canonical || (d.nap.website ? d.nap.website.replace(/\/$/, '') + '/' + (page.type === 'homepage' ? '' : B.fileName(pid).replace('.html', '/')) : '');
    const ld = meta.schema ? '<script type="application/ld+json">' + JSON.stringify(meta.schema).replace(/<\/script/gi, '<\\/script') + '</script>' : '';
    return '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
      '<title>' + esc(title) + '</title><meta name="description" content="' + esc(desc) + '">' + (canon ? '<link rel="canonical" href="' + esc(canon) + '">' : '') +
      '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' +
      (B.faviconUrl(opts.preview) ? '<link rel="icon" type="image/webp" href="' + esc(B.faviconUrl(opts.preview)) + '">' : '') + '<link href="https://fonts.googleapis.com/css2?' + f.q + '&display=swap" rel="stylesheet"><style>' + B.cssVars() + B.SITE_CSS + (B.SKIN_BASE_CSS || '') + ((B.SKINS || {})[B.tpl().skin] || '') + '</style>' + ld + '</head><body class="skin-' + (B.tpl().skin || 'base') + '">' +
      header(pid, opts.preview) + '<main>' + body + '</main>' + footer(opts.preview) +
      '<script>' + RUNTIME_JS + '<\/script>' + (opts.preview ? '<script>' + PREVIEW_JS + '<\/script>' : '') + '</body></html>';
  };

  /* public API for the orchestrator */
  B.prepGallery = function (pid, sid, m) {
    const c = B.siteCtx(pid, true);
    if (!Array.isArray(m.cards)) m.cards = c.galleryCards(m).map(x => Object.assign({}, x));
    if (!Array.isArray(m.pairs)) m.pairs = c.galleryPairs(m).map(x => Object.assign({}, x));
  };
  B.exportPage = pid => B.buildDocument(pid, { preview: false });
  B.exportAll = function () { const o = {}; B.pageIds().forEach(p => { o[B.fileName(p)] = B.exportPage(p); }); return o; };
  B.setTemplate = function (id, keepEdits) {
    if (!B.TEMPLATES[id]) return;
    B.state.template = id; B.state.theme = {};
    if (!keepEdits) Object.values(B.state.pages).forEach(p => { p.variants = {}; p.bg = {}; });
  };
})();
