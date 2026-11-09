/* blocks.js : one renderer per block type. Each block has variants; model comes from Builder.parseSection. */
(function () {
  const B = (window.Builder = window.Builder || {});
  const esc = B.esc, inline = B.inline;

  const ICONS = {
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    check: '<polyline points="20 6 9 17 4 12"/>',
    home: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    building: '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    flame: '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.1.4-2.3 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    camera: '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    drop: '<path d="M12 2.7l5.7 5.7a8 8 0 1 1-11.4 0z"/>',
    wind: '<path d="M9.6 4.6A2 2 0 1 1 11 8H2m10.6 11.4A2 2 0 1 0 14 16H2m15.7-8.3A2.5 2.5 0 1 1 19.5 12H2"/>',
    clock: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    star: '<polygon points="12 2 15 9 22 9.3 16.5 14 18.5 21 12 17 5.5 21 7.5 14 2 9.3 9 9"/>',
    tool: '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
    phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    pin: '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    award: '<circle cx="12" cy="8" r="7"/><polyline points="8.2 13.9 7 23 12 20 17 23 15.8 13.9"/>',
    users: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>',
    arrow: '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>'
  };
  function icon(n) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + (ICONS[n] || ICONS.check) + '</svg>'; }
  function pickIcon(t) {
    t = (t || '').toLowerCase();
    if (/commercial|facility|rooftop|building|institution/.test(t)) return 'building';
    if (/residential|home|house/.test(t)) return 'home';
    if (/dryer|lint|fire|exhaust|burn/.test(t)) return 'flame';
    if (/camera|video|inspect|borescope|optic|verif/.test(t)) return 'camera';
    if (/sanitiz|fog|botanical|antimicrob|mold|clean air/.test(t)) return 'drop';
    if (/negative|vacuum|hepa|airflow|air |duct/.test(t)) return 'wind';
    if (/certif|nadca|licen|credential|award|accredit/.test(t)) return 'award';
    if (/team|technician|local|communit|people|owner/.test(t)) return 'users';
    if (/time|same|next-day|dispatch|hour|fast|window|min/.test(t)) return 'clock';
    if (/repair|replace|equipment|tool|brush/.test(t)) return 'tool';
    if (/insur|guarant|safe|protect|trust|contain/.test(t)) return 'shield';
    return 'check';
  }

  const tel = c => 'tel:' + String(c.phone || '').replace(/[^\d+]/g, '');
  const head = (eyebrow, h, sub) =>
    '<div class="head">' + (eyebrow ? '<span class="eyebrow">' + esc(eyebrow) + '</span>' : '') +
    '<h2>' + inline(h || '') + '</h2>' + (sub ? '<p>' + inline(sub) + '</p>' : '') + '</div>';
  const callBtn = (c, cls) => '<a class="btn ' + (cls || 'btn-primary') + '" href="' + tel(c) + '">' + icon('phone') + ' Call ' + esc(c.phone) + '</a>';
  const ucfirst = s => (s || '').charAt(0).toUpperCase() + (s || '').slice(1);

  const BLOCKS = {};

  BLOCKS.hero = {
    label: 'Hero', variants: ['full', 'split', 'centered', 'dispatch', 'bento', 'docked', 'magazine', 'dossier'],
    render(m, c) {
      const title = m.h1 || m.h2 || c.page.title;
      const paras = m.paras.filter(p => !/\|/.test(p));
      const line = m.paras.find(p => /\|/.test(p));
      let chips = (c.merged || []).slice(0, 4);
      if (!chips.length && line) chips = line.split('|').map(s => s.trim()).filter(s => s && !/^direct|\d{3}[-\s)]/i.test(s)).slice(0, 4);
      if (!chips.length && (c.brief.credentials || []).length) chips = c.brief.credentials.slice(0, 4);
      const img = c.img();
      const btn2 = m.btn2 || 'See Our Services';
      const fx = c.fx && c.fx !== 'none' ? ' data-fx="' + esc(c.fx) + '"' : '';
      const nextHref = c.nextSid ? '#sec-' + c.nextSid : '#';
      const city = c.page.city || c.brief.city || '';
      const copy = '<h1>' + inline(title) + '</h1>' + paras.slice(0, 2).map(p => '<p>' + inline(p) + '</p>').join('') +
        '<div class="btns">' + callBtn(c) + '<a class="btn btn-ghost" href="' + nextHref + '">' + esc(btn2) + '</a></div>' +
        (chips.length ? '<div class="proof">' + chips.map(x => '<span class="chip">' + icon('check') + ' ' + esc(x) + '</span>').join('') + '</div>' : '');
      if (c.variant === 'split') {
        return '<div class="hero hero--split"' + fx + '><div class="wrap"><div>' + copy + '</div>' +
          (img ? '<img class="hero-img" src="' + esc(img.src) + '" alt="' + esc(img.alt) + '">' : '<div class="hero-img"></div>') + '</div></div>';
      }
      if (c.variant === 'centered') return '<div class="hero hero--centered"' + fx + '><div class="wrap">' + copy + '</div></div>';
      if (c.variant === 'dispatch') {
        const list = (chips.length ? chips : ['Licensed & Insured', 'Same or Next-Day Dispatch', 'Written Scope Before Work']).map(x =>
          '<li><span class="tick">' + icon('check') + '</span><span>' + esc(x) + '</span></li>').join('');
        const dcard = '<aside class="hero-dcard"><div class="hd-top"><span class="hd-dot"></span><span>Direct Local Dispatch' + (city ? ' &middot; ' + esc(city) : '') + '</span></div>' +
          '<h3>Speak With a Certified Specialist</h3><a class="hd-phone" href="' + tel(c) + '">' + icon('phone') + ' ' + esc(c.phone) + '</a>' +
          '<ul class="hd-list">' + list + '</ul><a class="btn btn-primary hd-btn" href="' + tel(c) + '">Request Immediate Dispatch</a></aside>';
        return '<div class="hero hero--dispatch"' + fx + ' style="--hero-img:url(\'' + esc(img ? img.src : '') + '\')"><div class="wrap"><div class="hd-copy">' +
          (city ? '<span class="eyebrow">' + esc(city + (c.brief.state ? ', ' + c.brief.state : '')) + '</span>' : '') +
          '<h1>' + inline(title) + '</h1>' + paras.slice(0, 2).map(p => '<p>' + inline(p) + '</p>').join('') +
          '<div class="btns">' + callBtn(c) + '<a class="btn btn-ghost" href="' + nextHref + '">' + esc(btn2) + '</a></div></div>' + dcard + '</div></div>';
      }
      if (c.variant === 'bento') {
        const tiles = (chips.length ? chips : ['Certified Technicians', 'Same-Day Availability']).slice(0, 3).map(x =>
          '<div class="bento-tile"><span class="ic">' + icon(pickIcon(x)) + '</span><b>' + esc(x) + '</b></div>').join('');
        return '<div class="hero hero--bento"' + fx + '><div class="wrap"><div class="bento-main">' +
          (city ? '<span class="eyebrow">' + esc(city + (c.brief.state ? ', ' + c.brief.state : '')) + '</span>' : '') +
          '<h1>' + inline(title) + '</h1>' + paras.slice(0, 2).map(p => '<p>' + inline(p) + '</p>').join('') +
          '<div class="btns">' + callBtn(c) + '<a class="btn btn-ghost" href="' + nextHref + '">' + esc(btn2) + '</a></div></div>' +
          '<div class="bento-side">' + (img ? '<div class="bento-photo"><img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '"></div>' : '') +
          '<div class="bento-tiles">' + tiles + '</div></div></div></div>';
      }
      if (c.variant === 'docked') {
        const dock = (chips.length ? chips : ['Certified Specialists', 'Local Dispatch', 'Written Scope']).slice(0, 4).map(x =>
          '<div class="dock-item"><span class="ic">' + icon(pickIcon(x)) + '</span><b>' + esc(x) + '</b></div>').join('');
        return '<div class="hero hero--docked"' + fx + ' style="--hero-img:url(\'' + esc(img ? img.src : '') + '\')"><div class="wrap"><div class="dock-copy">' +
          '<h1>' + inline(title) + '</h1>' + paras.slice(0, 2).map(p => '<p>' + inline(p) + '</p>').join('') +
          '<div class="btns">' + callBtn(c) + '<a class="btn btn-ghost" href="' + nextHref + '">' + esc(btn2) + '</a></div></div>' +
          '<div class="hero-dock">' + dock + '</div></div></div>';
      }
      if (c.variant === 'magazine') {
        const specs = (chips.length ? chips : ['Certified Field Technicians', 'Same or Next-Day Dispatch', 'Written Scope Before Work', 'Verified Containment']).slice(0, 4).map((x, i) =>
          '<div class="mag-spec"><span class="mag-idx">[' + String(i + 1).padStart(2, '0') + ']</span><b>' + esc(x) + '</b></div>').join('');
        return '<div class="hero hero--magazine"' + fx + '><div class="wrap">' +
          '<div class="mag-meta"><span>01 // FIELD DISPATCH</span><span>' + esc((city ? city + (c.brief.state ? ', ' + c.brief.state : '') : c.nap.company_name).toUpperCase()) + '</span><span>DIRECT LINE: ' + esc(c.phone) + '</span></div>' +
          '<div class="mag-grid"><div class="mag-copy"><h1>' + inline(title) + '</h1>' +
          '<div class="mag-lead">' + paras.slice(0, 2).map(p => '<p>' + inline(p) + '</p>').join('') + '</div>' +
          '<div class="btns">' + callBtn(c) + '<a class="btn btn-ghost" href="' + nextHref + '">' + esc(btn2) + '</a></div></div>' +
          '<div class="mag-visual">' + (img ? '<div class="mag-frame"><img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '"><div class="mag-cap">FIG. 01 &mdash; ' + esc(img.alt || c.page.title) + '</div></div>' : '') +
          '</div></div><div class="mag-bar">' + specs + '</div></div></div>';
      }
      if (c.variant === 'dossier') {
        const specs = (chips.length ? chips : ['Certified Field Technicians', 'Same or Next-Day Dispatch', 'Written Scope Before Work', 'Verified Source Removal']).slice(0, 4).map((x, i) =>
          '<div class="dos-cell"><span class="dos-k">SPEC // 0' + (i + 1) + '</span><b>' + esc(x) + '</b></div>').join('');
        return '<div class="hero hero--dossier"' + fx + '><div class="wrap"><div class="dos-grid"><div class="dos-left">' +
          '<div class="dos-tag"><span class="dos-dot"></span><span>FIELD DOSSIER // ' + esc((city ? city + (c.brief.state ? ', ' + c.brief.state : '') : c.nap.company_name).toUpperCase()) + '</span></div>' +
          '<h1>' + inline(title) + '</h1>' +
          '<div class="dos-lead">' + paras.slice(0, 2).map(p => '<p>' + inline(p) + '</p>').join('') + '</div>' +
          '<div class="btns">' + callBtn(c) + '<a class="btn btn-ghost" href="' + nextHref + '">' + esc(btn2) + '</a></div>' +
          '<div class="dos-matrix">' + specs + '</div></div>' +
          '<div class="dos-right"><div class="dos-viewport"><span class="ret tl">+</span><span class="ret tr">+</span><span class="ret bl">+</span><span class="ret br">+</span>' +
          (img ? '<img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '">' : '') +
          '<div class="dos-readout"><div><small>DIRECT DISPATCH TELEMETRY</small><b>' + esc(c.phone) + '</b></div><span>ACTIVE</span></div></div></div></div></div></div>';
      }
      return '<div class="hero hero--full"' + fx + ' style="--hero-img:url(\'' + esc(img ? img.src : '') + '\')"><div class="wrap">' + copy + '</div></div>';
    }
  };

  BLOCKS.split = {
    label: 'Text + image', variants: ['image-right', 'image-left', 'text-only', 'frame', 'diagnostic', 'spotlight'],
    render(m, c) {
      const img = c.img();
      const bullets = m.bullets.length ? m.bullets : (m.items || []).map(i => ({ label: i.title, text: (i.paras || [])[0] || '' }));
      const list = bullets.length ? '<ul class="checks">' + bullets.map(b => '<li><span class="tick">' + icon('check') + '</span><div>' +
        (b.label ? '<strong>' + inline(b.label) + '</strong> ' : '') + inline(b.text) + '</div></li>').join('') + '</ul>' : '';
      const copy = '<div><h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') + list +
        (m.cta ? '<p style="margin-top:18px">' + callBtn(c) + '</p>' : '') + '</div>';
      if (c.variant === 'frame' && img) {
        return '<div class="wrap"><div class="split split-frame">' + copy +
          '<div class="split-media"><div class="arch-frame"><div class="arch-top"><span>FIELD DOCUMENTATION</span><span>' + esc(c.page.city || c.brief.city || '') + '</span></div>' +
          '<img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '"><div class="arch-cap">' + esc(img.alt || m.h2 || '') + '</div></div></div></div></div>';
      }
      if (c.variant === 'diagnostic') {
        const sym = (bullets.length ? bullets.map(b => (b.label ? b.label + ': ' : '') + b.text) : m.paras.slice(0, 2)).slice(0, 4);
        const symHtml = sym.map((s, i) => '<div class="diag-chip"><span class="diag-code">DIAG-0' + (i + 1) + '</span><p>' + inline(s) + '</p></div>').join('');
        return '<div class="wrap"><div class="split-diagnostic"><div class="diag-panel"><div class="diag-bar"><span>DIAGNOSTIC BRIEFING</span><span>STATUS: CRITICAL CHECK</span></div>' +
          '<h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') +
          '<div class="diag-cta">' + callBtn(c) + '</div></div>' +
          '<div class="diag-visual">' + (img ? '<div class="diag-img"><img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '"><span class="diag-badge">FIELD INSPECTION VISUAL</span></div>' : '') +
          '<div class="diag-chips">' + symHtml + '</div></div></div></div>';
      }
      if (c.variant === 'spotlight') {
        return '<div class="wrap"><div class="split-spotlight"><div class="spot-head"><span class="eyebrow">' + esc(c.eyebrow || 'REGIONAL DISPATCH BRIEF') + '</span><h2>' + inline(m.h2 || m.h1 || '') + '</h2></div>' +
          '<div class="spot-body">' + (img ? '<div class="spot-media"><img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '"><div class="spot-cap">' + esc(img.alt || '') + '</div></div>' : '') +
          '<div class="spot-copy">' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') + list + '<div style="margin-top:20px">' + callBtn(c) + '</div></div></div></div></div>';
      }
      const cls = c.variant === 'text-only' || !img ? 'text-only' : (c.variant === 'image-left' ? 'rev' : '');
      return '<div class="wrap"><div class="split ' + cls + '">' + copy +
        (cls === 'text-only' ? '' : '<div class="split-media"><img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '"></div>') + '</div></div>';
    }
  };

  BLOCKS.cards = {
    label: 'Cards', variants: ['icons', 'grid', 'list', 'numbered', 'stripe', 'ledger', 'bento-mosaic', 'pillars', 'dossier-cards'],
    render(m, c) {
      let items = (m.items || []).slice();
      if (!items.length && m.bullets.length) items = m.bullets.map(b => ({ title: b.label || b.text, paras: b.label ? [b.text] : [], facts: [], bullets: [] }));
      const intro = m.paras[0];
      if (c.variant === 'bento-mosaic') {
        const mcards = items.map((it, idx) => {
          const paras = (it.paras || []);
          const cta = paras.find(p => /^(schedule|request|call|get)/i.test(p));
          const body = paras.filter(p => p !== cta);
          return '<article class="bm-card' + (idx === 0 ? ' bm-hero' : '') + '"><div class="bm-top"><span class="bm-idx">SVC // 0' + (idx + 1) + '</span><span class="ic">' + icon(pickIcon(it.title)) + '</span></div>' +
            '<h3>' + inline(it.title) + '</h3>' + body.map(p => '<p>' + inline(p) + '</p>').join('') +
            '<a class="bm-link" href="' + tel(c) + '">' + esc(cta || 'Schedule Service') + ' &rarr;</a></article>';
        }).join('');
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="cards-bento-mosaic">' + mcards + '</div></div>';
      }
      if (c.variant === 'pillars') {
        const rows = items.map((it, idx) => {
          const paras = (it.paras || []);
          return '<article class="pillar-row"><div class="pil-num"><span>0' + (idx + 1) + '</span><span class="ic">' + icon(pickIcon(it.title)) + '</span></div>' +
            '<div class="pil-title"><h3>' + inline(it.title) + '</h3></div>' +
            '<div class="pil-body">' + paras.map(p => '<p>' + inline(p) + '</p>').join('') + '</div></article>';
        }).join('');
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="cards-pillars">' + rows + '</div></div>';
      }
      if (c.variant === 'dossier-cards') {
        const dcards = items.map((it, idx) => {
          const facts = it.facts || [];
          const loc = facts.find(f => /neighbou?rhood|location/i.test(f.label));
          const rest = facts.filter(f => f !== loc);
          const paras = (it.paras || []);
          const fx = rest.length ? '<div class="dc-facts">' + rest.map((f, i) => '<div class="dc-fact' + (i === rest.length - 1 ? ' dc-result' : '') + '"><small>' + esc(f.label) + '</small><div>' + inline(f.text) + '</div></div>').join('') + '</div>' : '';
          return '<article class="dc-card"><div class="dc-hdr"><span>CASE FILE #0' + (idx + 1) + '</span>' + (loc ? '<span class="dc-loc">' + inline(loc.text) + '</span>' : '<span>VERIFIED LOG</span>') + '</div>' +
            '<div class="dc-body"><h3>' + inline(it.title) + '</h3>' + paras.map(p => '<p>' + inline(p) + '</p>').join('') + fx + '</div></article>';
        }).join('');
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="cards-dossier">' + dcards + '</div></div>';
      }
      const cards = items.map((it, idx) => {
        const facts = it.facts || [];
        const loc = facts.find(f => /neighbou?rhood|location/i.test(f.label));
        const rest = facts.filter(f => f !== loc);
        const paras = (it.paras || []);
        const cta = paras.find(p => /^(schedule|request|call|get)\b/i.test(p));
        const body = paras.filter(p => p !== cta);
        const bl = (it.bullets || []).map(b => '<li>' + (b.label ? '<strong>' + inline(b.label) + ':</strong> ' : '') + inline(b.text) + '</li>').join('');
        const fx = rest.length ? '<div class="facts">' + rest.map((f, i) => '<div class="fact' + (i === rest.length - 1 && /result/i.test(f.label) ? ' last' : '') + '"><b>' + esc(f.label) + '</b><span>' + inline(f.text) + '</span></div>').join('') + '</div>' : '';
        const showIcon = !rest.length;
        const ic = showIcon ? '<span class="ic">' + icon(pickIcon(it.title)) + '</span>' : '';
        const numBadge = (c.variant === 'numbered' || c.variant === 'ledger') ? '<div class="cnum-top"><span class="cnum">[' + String(idx + 1).padStart(2, '0') + ']</span>' + ic + '</div>' : '';
        const useBodyWrap = c.variant === 'list' || c.variant === 'stripe';
        const inner = (useBodyWrap ? '<div><h3>' + inline(it.title) + '</h3>' : '<h3>' + inline(it.title) + '</h3>') +
          body.map(p => '<p>' + inline(p) + '</p>').join('') + (bl ? '<ul style="margin:6px 0 0;padding-left:18px;color:var(--muted)">' + bl + '</ul>' : '') + fx +
          (cta ? '<a class="more" href="' + tel(c) + '">' + esc(cta) + ' &rarr;</a>' : '') + (useBodyWrap ? '</div>' : '');
        const lead = (c.variant === 'numbered' || c.variant === 'ledger') ? numBadge : (c.variant === 'grid' ? '' : ic);
        return '<article class="card">' + (loc ? '<span class="loc">' + inline(loc.text) + '</span>' : '') + lead + inner + '</article>';
      }).join('');
      const wrapCls = c.variant === 'list' ? 'cards-list' : c.variant === 'stripe' ? 'cards-stripe' : c.variant === 'ledger' ? 'cards-ledger' : ('grid ' + (c.variant === 'icons' ? 'cards-icons' : c.variant === 'numbered' ? 'cards-numbered' : ''));
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="' + wrapCls + '">' + cards + '</div></div>';
    }
  };

  BLOCKS.steps = {
    label: 'Process steps', variants: ['timeline', 'table', 'rail', 'track', 'spec', 'chevron'],
    render(m, c) {
      const intro = m.paras[0];
      let rows = [];
      if (m.table) rows = m.table.rows.map(r => ({ title: r[0], text: r[1] || '', time: r[2] || '' }));
      else rows = (m.items || []).map(i => ({ title: i.title, text: (i.paras || []).join(' '), time: '' }));
      const strip = s => String(s || '').replace(/\*\*/g, '');
      if (c.variant === 'table' && m.table) {
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + B.tableHtml(m.table) + '</div>';
      }
      if (c.variant === 'rail') {
        return '<div class="wrap"><div class="steps-rail"><div class="rail-side">' +
          (c.eyebrow ? '<span class="eyebrow">' + esc(c.eyebrow) + '</span>' : '') +
          '<h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + (intro ? '<p style="color:var(--muted)">' + inline(intro) + '</p>' : '') +
          '<p style="margin-top:20px">' + callBtn(c) + '</p></div><div class="rail-list">' +
          rows.map((r, i) => '<div class="rail-item"><div class="n">' + String(i + 1).padStart(2, '0') + '</div><div class="rail-body"><h3>' +
            inline(strip(r.title)) + '</h3><p>' + inline(r.text) + '</p>' + (r.time ? '<span class="time">' + esc(strip(r.time)) + '</span>' : '') + '</div></div>').join('') +
          '</div></div></div>';
      }
      if (c.variant === 'spec') {
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="steps-spec">' + rows.map((r, i) =>
          '<div class="spec-row"><div class="spec-idx">PHASE // ' + String(i + 1).padStart(2, '0') + '</div><div class="spec-title"><h3>' + inline(strip(r.title)) + '</h3>' +
          (r.time ? '<span class="time">' + esc(strip(r.time)) + '</span>' : '') + '</div><div class="spec-desc"><p>' + inline(r.text) + '</p></div></div>').join('') + '</div></div>';
      }
      if (c.variant === 'chevron') {
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="steps-chevron">' + rows.map((r, i) =>
          '<div class="chev-step"><div class="chev-top"><span class="chev-stage">STAGE 0' + (i + 1) + '</span>' +
          (r.time ? '<span class="chev-time">' + esc(strip(r.time)) + '</span>' : '') + '</div>' +
          '<h3>' + inline(strip(r.title)) + '</h3><p>' + inline(r.text) + '</p></div>').join('') + '</div></div>';
      }
      const cls = c.variant === 'track' ? 'steps steps-track' : 'steps';
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="' + cls + '">' + rows.map((r, i) =>
        '<div class="step"><div class="n">' + (i + 1) + '</div><h3>' + inline(strip(r.title)) + '</h3><p>' + inline(r.text) + '</p>' +
        (r.time ? '<span class="time">' + esc(strip(r.time)) + '</span>' : '') + '</div>').join('') + '</div></div>';
    }
  };

  BLOCKS.table = {
    label: 'Comparison table', variants: ['cmp', 'matrix'],
    render(m, c) {
      if (c.variant === 'matrix' && m.table) {
        const ths = (m.table.headers || []).map((h, i) => '<th class="' + (i === 1 ? 'mx-win' : '') + '">' + (i === 1 ? '<span class="mx-tag">OUR STANDARD</span>' : '') + inline(h) + '</th>').join('');
        const trs = (m.table.rows || []).map(r => '<tr>' + r.map((cell, i) => '<td class="' + (i === 0 ? 'mx-feat' : i === 1 ? 'mx-win' : '') + '">' + inline(cell) + '</td>').join('') + '</tr>').join('');
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) +
          '<div class="cmp-matrix"><div class="tbl"><table><thead><tr>' + ths + '</tr></thead><tbody>' + trs + '</tbody></table></div>' +
          '<div class="mx-foot"><span>' + inline(m.paras[1] || 'Verified equipment and certified source-removal protocols on every dispatch.') + '</span>' + callBtn(c) + '</div></div></div>';
      }
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="cmp">' + B.tableHtml(m.table) + '</div>' +
        (m.paras.length > 1 ? '<p style="margin-top:18px;color:var(--muted)">' + inline(m.paras.slice(1).join(' ')) + '</p>' : '') +
        '<p style="text-align:center;margin-top:26px">' + callBtn(c) + '</p></div>';
    }
  };

  BLOCKS.reviews = {
    label: 'Reviews', variants: ['cards', 'featured', 'wall'],
    render(m, c) {
      const stars = n => '<div class="stars">' + '\u2605'.repeat(n || 5) + '</div>';
      const card = (q, big) => '<article class="card rev' + (big ? ' big' : '') + '">' + stars(q.rating) + '<q>' + inline('\u201c' + q.text + '\u201d') + '</q>' +
        '<div class="who"><span class="av">' + esc((q.author || '?').trim().charAt(0)) + '</span><div><b>' + esc(q.author) + '</b><small>' + esc(q.loc) + '</small></div></div></article>';
      let qs = (m.quotes || []).slice();
      if (!qs.length && (m.items || []).length) {
        qs = m.items.map(it => {
          let rating = 5, author = it.title || '', loc = '', texts = [];
          (it.paras || []).forEach(p => {
            let m1;
            if ((m1 = p.match(/^rating:\s*([\d.]+)/i))) { rating = Math.round(parseFloat(m1[1])) || 5; }
            else if ((m1 = p.match(/^reviewer:\s*(.+)$/i))) {
              const raw = m1[1].trim(), idx = raw.indexOf(',');
              author = (idx > -1 ? raw.slice(0, idx) : raw).trim();
              const sub = idx > -1 ? raw.slice(idx + 1).trim() : '';
              loc = it.title && sub && !sub.includes(it.title) ? (sub + ' · ' + it.title) : (sub || it.title || '');
            } else { texts.push(p.replace(/^["\u201c]+|["\u201d]+$/g, '')); }
          });
          return { text: texts.join(' '), author: author, loc: loc, rating: rating };
        }).filter(q => q.text);
      }
            if (c.variant === 'wall') {
        const wcards = qs.map((q, i) => '<article class="wall-card"><div class="wall-top">' + stars(q.rating) + '<span class="wall-v">VERIFIED CLIENT // 0' + (i + 1) + '</span></div>' +
          '<q>' + inline('“' + q.text + '”') + '</q><div class="wall-who"><span class="av">' + esc((q.author || '?').trim().charAt(0)) + '</span><div><b>' + esc(q.author) + '</b><small>' + esc(q.loc) + '</small></div></div></article>').join('');
        return '<div class="wrap"><div class="wall-banner"><div><span class="eyebrow">' + esc(c.eyebrow || 'CLIENT TELEMETRY') + '</span><h2>' + inline(m.h2 || m.h1 || '') + '</h2>' +
          (m.paras[0] ? '<p>' + inline(m.paras[0]) + '</p>' : '') + '</div><div class="wall-score"><div class="ws-num">5.0</div><div><div class="stars">★★★★★</div><small>Verified Local Reviews</small></div></div></div>' +
          '<div class="wall-grid">' + wcards + '</div></div>';
      }
      const body = c.variant === 'featured' && qs.length > 1
        ? '<div class="rev-featured">' + card(qs[0], true) + '<div class="stack">' + qs.slice(1).map(q => card(q)).join('') + '</div></div>'
        : '<div class="grid">' + qs.map(q => card(q)).join('') + '</div>';
      const tail = m.paras.length > 1 ? '<p style="text-align:center;margin-top:26px;color:var(--muted)">' + inline(m.paras[m.paras.length - 1]) + '</p>' : '';
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras.length ? m.paras[0] : '') + body + tail + '</div>';
    }
  };

  BLOCKS.faq = {
    label: 'FAQ', variants: ['two-col', 'accordion', 'numbered-grid'],
    render(m, c) {
      const list = (m.items || []).map((it, i) => '<details' + (i === 0 ? ' open' : '') + '><summary>' + inline(it.title) + '</summary><div class="ans">' + (it.paras || []).map(p => '<p>' + inline(p) + '</p>').join('') + '</div></details>').join('');
            if (c.variant === 'numbered-grid') {
        const gitems = (m.items || []).map((it, i) => '<details class="faq-ncard"' + (i < 2 ? ' open' : '') + '><summary><span class="fn-idx">Q.0' + (i + 1) + '</span><span class="fn-q">' + inline(it.title) + '</span></summary><div class="ans">' + (it.paras || []).map(p => '<p>' + inline(p) + '</p>').join('') + '</div></details>').join('');
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="faq-wrap faq-ngrid">' + gitems + '</div></div>';
      }
      if (c.variant === 'accordion') return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="faq-wrap one"><div>' + list + '</div></div></div>';
      return '<div class="wrap"><div class="faq-wrap"><div class="faq-side">' + (c.eyebrow ? '<span class="eyebrow">' + esc(c.eyebrow) + '</span>' : '') +
        '<h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + (m.paras[0] ? '<p style="color:var(--muted)">' + inline(m.paras[0]) + '</p>' : '') + '<p>' + callBtn(c) + '</p></div><div>' + list + '</div></div></div>';
    }
  };

  BLOCKS.cta = {
    label: 'Call to action', variants: ['box', 'band', 'split-ticket'],
    render(m, c) {
      const paras = m.paras.slice();
      const note = paras.length > 1 ? paras.pop() : '';
      const inner = '<div class="cta-inner"><h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + paras.map(p => '<p>' + inline(p) + '</p>').join('') +
        '<p style="margin-top:24px">' + callBtn(c) + '</p>' + (note ? '<div class="cta-note">' + inline(note) + '</div>' : '') + '</div>';
            if (c.variant === 'split-ticket') {
        return '<div class="wrap"><div class="cta-ticket"><div class="ct-left"><span class="ct-tag">DIRECT FIELD DISPATCH</span><h2>' + inline(m.h2 || m.h1 || '') + '</h2>' +
          paras.map(p => '<p>' + inline(p) + '</p>').join('') + (note ? '<div class="ct-note">' + inline(note) + '</div>' : '') + '</div>' +
          '<div class="ct-right"><span class="ct-label">IMMEDIATE DISPATCH LINE</span><a class="ct-phone" href="' + tel(c) + '">' + esc(c.phone) + '</a>' +
          '<p>Speak directly with our local dispatch desk</p>' + callBtn(c) + '</div></div></div>';
      }
      if (c.variant === 'band') return '<div class="cta-band">' + inner + '</div>';
      return '<div class="wrap"><div class="cta-box">' + inner + '</div></div>';
    }
  };

  BLOCKS.badges = {
    label: 'Badges / credentials', variants: ['grid', 'seal-strip'],
    render(m, c) {
      let items = (m.items || []).map(i => ({ t: i.title, d: (i.paras || [])[0] || '' }));
      if (!items.length) items = (m.bullets || []).map(b => ({ t: b.label || b.text, d: b.label ? b.text : '' }));
            if (c.variant === 'seal-strip') {
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="badges-seals">' + items.map((i, idx) =>
          '<div class="seal-card"><div class="seal-emblem"><span class="ic">' + icon(pickIcon(i.t)) + '</span><small>CERT // 0' + (idx + 1) + '</small></div>' +
          '<div class="seal-body"><b>' + inline(i.t) + '</b>' + (i.d ? '<span>' + inline(i.d) + '</span>' : '') + '</div></div>').join('') + '</div></div>';
      }
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="badges">' + items.map(i =>
        '<div class="badge"><span class="ic">' + icon(pickIcon(i.t)) + '</span><b>' + inline(i.t) + '</b>' + (i.d ? '<span>' + inline(i.d) + '</span>' : '') + '</div>').join('') + '</div></div>';
    }
  };

  BLOCKS.area = {
    label: 'Service area + map', variants: ['map', 'radar'],
    render(m, c) {
      const allBullets = (m.bullets || []).concat(...(m.items || []).map(it => it.bullets || []));
      const tags = allBullets.map(b => '<span class="tag">' + inline((b.label ? b.label + ': ' : '') + b.text) + '</span>').join('');
      const itemParas = (m.items || []).filter(it => (it.paras || []).length).map(it =>
        '<p style="margin:12px 0 0;font-size:.93rem;color:var(--muted)"><strong style="color:var(--heading)">' + inline(it.title) + ':</strong> ' + it.paras.map(p => inline(p)).join(' &middot; ') + '</p>'
      ).join('');
      const q = encodeURIComponent(c.nap.address || (c.brief.city + ', ' + c.brief.state));
            if (c.variant === 'radar') {
        const rtags = allBullets.map(b => '<span class="tag radar-tag">' + icon('pin') + ' ' + inline((b.label ? b.label + ': ' : '') + b.text) + '</span>').join('');
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, '') + '<div class="area-radar">' +
          '<div class="radar-map"><div class="radar-bar"><span>LIVE COVERAGE RADAR</span><span>' + esc(c.brief.city + ', ' + c.brief.state) + '</span></div>' +
          '<iframe loading="lazy" title="Service area map" src="https://www.google.com/maps?q=' + q + '&z=10&output=embed"></iframe></div>' +
          '<div class="radar-board"><div class="radar-intro">' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') + '</div>' +
          (rtags ? '<div class="tags radar-tags">' + rtags + '</div>' : '') + '<div class="radar-meta">' + itemParas + '</div>' +
          '<div style="margin-top:20px">' + callBtn(c) + '</div></div></div></div>';
      }
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, '') + '<div class="area"><div>' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') +
        (tags ? '<div class="tags">' + tags + '</div>' : '') + itemParas + '<p style="margin-top:22px">' + callBtn(c) + '</p></div>' +
        '<iframe loading="lazy" title="Service area map" src="https://www.google.com/maps?q=' + q + '&z=10&output=embed"></iframe></div></div>';
    }
  };

  BLOCKS.gallery = {
    label: 'Before / after', variants: ['cards', 'slider', 'filmstrip'],
    render(m, c) {
      const cards = c.galleryCards(m), pairs = c.galleryPairs(m);
      const metrics = (m.bullets || []).map(x => {
        const mm = (x.text || x.label).match(/^([+\-]?[\d.,]+%?)\s*(.*)$/);
        return mm ? '<div><b>' + esc(mm[1]) + '</b>' + inline(mm[2]) + '</div>' : '';
      }).join('');
      const strip = metrics ? '<div class="metrics">' + metrics + '</div>' : '';
      const h = head(c.eyebrow, m.h2 || m.h1, m.paras[0]);
            if (c.variant === 'filmstrip' && cards.length) {
        const plates = cards.map((k, i) => '<figure class="film-plate"><div class="fp-bar"><span>EVIDENCE PLATE // 0' + (i + 1) + '</span><span>VERIFIED</span></div>' +
          '<img src="' + esc(c.src(k.img)) + '" alt="' + esc(k.alt || '') + '" loading="lazy">' +
          (k.caption ? '<figcaption>' + inline(k.caption) + '</figcaption>' : '') + '</figure>').join('');
        return '<div class="wrap">' + h + '<div class="film-grid">' + plates + '</div>' + strip + '</div>';
      }
      let mode = c.variant;
      if (mode === 'slider' && !pairs.length) mode = 'cards';
      if (mode === 'cards' && !cards.length && pairs.length) mode = 'slider';
      if (mode === 'slider') {
        const tabs = pairs.length > 1 ? '<div class="ba-tabs">' + pairs.map((p, i) => '<button type="button" class="ba-tab' + (i ? '' : ' on') + '" data-i="' + i + '">' + esc(p.label || ('Case ' + (i + 1))) + '</button>').join('') + '</div>' : '';
        const cases = pairs.map((p, i) => '<div class="ba-case"' + (i ? ' hidden' : '') + '><div class="ba-slider"><img src="' + esc(c.src(p.before)) + '" alt="Before cleaning"><img class="aft" src="' + esc(c.src(p.after)) + '" alt="After cleaning">' +
          '<span class="tg a">AFTER</span><span class="tg b">BEFORE</span><span class="bar"></span><input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Before and after slider"></div>' +
          (p.caption ? '<p class="ba-cap">' + inline(p.caption) + '</p>' : '') + '</div>').join('');
        return '<div class="wrap">' + h + '<div class="ba-wrap">' + tabs + cases + '</div>' + strip + '</div>';
      }
      const figs = cards.map(k => '<figure class="dba-card"><img src="' + esc(c.src(k.img)) + '" alt="' + esc(k.alt || '') + '" loading="lazy">' +
        (k.caption ? '<figcaption>' + inline(k.caption) + '</figcaption>' : '') + '</figure>').join('');
      return '<div class="wrap">' + h + (figs ? '<div class="dba-grid">' + figs + '</div>' : '<p style="text-align:center;color:var(--muted)">Add before / after images in the editor.</p>') + strip + '</div>';
    }
  };

  BLOCKS.article = {
    label: 'Article text', variants: ['default'],
    render(m, c) {
      return '<div class="wrap"><div class="article">' + (m.h2 ? '<h2>' + inline(m.h2) + '</h2>' : '') + B.mdToHtml(B.serializeSection(Object.assign({}, m, { h1: '', h2: '' }))) + '</div></div>';
    }
  };

  BLOCKS.postHeader = {
    label: 'Post header', variants: ['default'],
    render(m, c) {
      return '<div class="wrap"><div class="article"><span class="eyebrow">Guide</span><h1>' + inline(m.h1 || m.h2 || c.page.title) + '</h1>' +
        (m.paras[0] ? '<p class="lead">' + inline(m.paras[0]) + '</p>' : '') + m.paras.slice(1).map(p => '<p class="byline">' + inline(p) + '</p>').join('') + '</div></div>';
    }
  };

  BLOCKS.form = {
    label: 'Contact form', variants: ['card'],
    render(m, c) {
      const f = (l, t, extra) => '<div><label>' + l + '</label><input type="' + (t || 'text') + '" ' + (extra || '') + '></div>';
      return '<div class="wrap"><div class="split"><div><h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') + '</div>' +
        '<form class="form" onsubmit="event.preventDefault();alert(\'Thanks! We will call you shortly.\')">' + f('Full name', 'text', 'required') + f('Phone number', 'tel', 'required') + f('Service address') +
        '<div><label>Service needed</label><select><option>Residential duct cleaning</option><option>Commercial HVAC</option><option>Dryer vent</option><option>Camera inspection</option></select></div>' +
        '<div><label>Details</label><textarea rows="3"></textarea></div><button class="btn btn-primary" type="submit">Request a call back</button></form></div></div>';
    }
  };

  BLOCKS.nap = {
    label: 'NAP / hours', variants: ['default'],
    render(m, c) {
      const q = encodeURIComponent(c.nap.address || '');
      return '<div class="wrap"><div class="nap"><div class="article" style="margin:0">' + (m.h2 ? '<h2>' + inline(m.h2) + '</h2>' : '') +
        B.mdToHtml(B.serializeSection(Object.assign({}, m, { h1: '', h2: '' }))) + '<p>' + callBtn(c) + '</p></div>' +
        '<iframe style="width:100%;min-height:360px;border:0;border-radius:14px" loading="lazy" title="Map" src="https://www.google.com/maps?q=' + q + '&z=14&output=embed"></iframe></div></div>';
    }
  };

  B.BLOCKS = BLOCKS; B.icon = icon;
})();

