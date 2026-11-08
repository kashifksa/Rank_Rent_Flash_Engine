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
    label: 'Hero', variants: ['full', 'split', 'centered'],
    render(m, c) {
      const title = m.h1 || m.h2 || c.page.title;
      const paras = m.paras.filter(p => !/\|/.test(p));
      const line = m.paras.find(p => /\|/.test(p));
      let chips = (c.merged || []).slice(0, 4);
      if (!chips.length && line) chips = line.split('|').map(s => s.trim()).filter(s => s && !/^direct|\d{3}[-\s)]/i.test(s)).slice(0, 4);
      const img = c.img();
      const btn2 = m.btn2 || 'See Our Services';
      const nextHref = c.nextSid ? '#sec-' + c.nextSid : '#';
      const copy = '<h1>' + inline(title) + '</h1>' + paras.slice(0, 2).map(p => '<p>' + inline(p) + '</p>').join('') +
        '<div class="btns">' + callBtn(c) + '<a class="btn btn-ghost" href="' + nextHref + '">' + esc(btn2) + '</a></div>' +
        (chips.length ? '<div class="proof">' + chips.map(x => '<span class="chip">' + icon('check') + ' ' + esc(x) + '</span>').join('') + '</div>' : '');
      if (c.variant === 'split') {
        return '<div class="hero hero--split"><div class="wrap"><div>' + copy + '</div>' +
          (img ? '<img class="hero-img" src="' + esc(img.src) + '" alt="' + esc(img.alt) + '">' : '<div class="hero-img"></div>') + '</div></div>';
      }
      if (c.variant === 'centered') return '<div class="hero hero--centered"><div class="wrap">' + copy + '</div></div>';
      return '<div class="hero hero--full" style="--hero-img:url(\'' + esc(img ? img.src : '') + '\')"><div class="wrap">' + copy + '</div></div>';
    }
  };

  BLOCKS.split = {
    label: 'Text + image', variants: ['image-right', 'image-left', 'text-only'],
    render(m, c) {
      const img = c.img();
      const bullets = m.bullets.length ? m.bullets : (m.items || []).map(i => ({ label: i.title, text: (i.paras || [])[0] || '' }));
      const list = bullets.length ? '<ul class="checks">' + bullets.map(b => '<li><span class="tick">' + icon('check') + '</span><div>' +
        (b.label ? '<strong>' + inline(b.label) + '</strong> ' : '') + inline(b.text) + '</div></li>').join('') + '</ul>' : '';
      const copy = '<div><h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') + list +
        (m.cta ? '<p style="margin-top:18px">' + callBtn(c) + '</p>' : '') + '</div>';
      const cls = c.variant === 'text-only' || !img ? 'text-only' : (c.variant === 'image-left' ? 'rev' : '');
      return '<div class="wrap"><div class="split ' + cls + '">' + copy +
        (cls === 'text-only' ? '' : '<div class="split-media"><img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '"></div>') + '</div></div>';
    }
  };

  BLOCKS.cards = {
    label: 'Cards', variants: ['icons', 'grid', 'list'],
    render(m, c) {
      let items = (m.items || []).slice();
      if (!items.length && m.bullets.length) items = m.bullets.map(b => ({ title: b.label || b.text, paras: b.label ? [b.text] : [], facts: [], bullets: [] }));
      const intro = m.paras[0];
      const cards = items.map(it => {
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
        const inner = (c.variant === 'list' ? '<div><h3>' + inline(it.title) + '</h3>' : '<h3>' + inline(it.title) + '</h3>') +
          body.map(p => '<p>' + inline(p) + '</p>').join('') + (bl ? '<ul style="margin:6px 0 0;padding-left:18px;color:var(--muted)">' + bl + '</ul>' : '') + fx +
          (cta ? '<a class="more" href="' + tel(c) + '">' + esc(cta) + ' &rarr;</a>' : '') + (c.variant === 'list' ? '</div>' : '');
        return '<article class="card">' + (loc ? '<span class="loc">' + inline(loc.text) + '</span>' : '') + (c.variant === 'grid' ? '' : ic) + inner + '</article>';
      }).join('');
      const wrapCls = c.variant === 'list' ? 'cards-list' : ('grid ' + (c.variant === 'icons' ? 'cards-icons' : ''));
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="' + wrapCls + '">' + cards + '</div></div>';
    }
  };

  BLOCKS.steps = {
    label: 'Process steps', variants: ['timeline', 'table'],
    render(m, c) {
      const intro = m.paras[0];
      let rows = [];
      if (m.table) rows = m.table.rows.map(r => ({ title: r[0], text: r[1] || '', time: r[2] || '' }));
      else rows = (m.items || []).map(i => ({ title: i.title, text: (i.paras || []).join(' '), time: '' }));
      const strip = s => String(s || '').replace(/\*\*/g, '');
      if (c.variant === 'table' && m.table) {
        return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + B.tableHtml(m.table) + '</div>';
      }
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, intro) + '<div class="steps">' + rows.map((r, i) =>
        '<div class="step"><div class="n">' + (i + 1) + '</div><h3>' + inline(strip(r.title)) + '</h3><p>' + inline(r.text) + '</p>' +
        (r.time ? '<span class="time">' + esc(strip(r.time)) + '</span>' : '') + '</div>').join('') + '</div></div>';
    }
  };

  BLOCKS.table = {
    label: 'Comparison table', variants: ['cmp'],
    render(m, c) {
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="cmp">' + B.tableHtml(m.table) + '</div>' +
        (m.paras.length > 1 ? '<p style="margin-top:18px;color:var(--muted)">' + inline(m.paras.slice(1).join(' ')) + '</p>' : '') +
        '<p style="text-align:center;margin-top:26px">' + callBtn(c) + '</p></div>';
    }
  };

  BLOCKS.reviews = {
    label: 'Reviews', variants: ['cards', 'featured'],
    render(m, c) {
      const stars = n => '<div class="stars">' + '\u2605'.repeat(n || 5) + '</div>';
      const card = (q, big) => '<article class="card rev' + (big ? ' big' : '') + '">' + stars(q.rating) + '<q>' + inline('\u201c' + q.text + '\u201d') + '</q>' +
        '<div class="who"><span class="av">' + esc((q.author || '?').trim().charAt(0)) + '</span><div><b>' + esc(q.author) + '</b><small>' + esc(q.loc) + '</small></div></div></article>';
      const qs = m.quotes || [];
      const body = c.variant === 'featured' && qs.length > 1
        ? '<div class="rev-featured">' + card(qs[0], true) + '<div class="stack">' + qs.slice(1).map(q => card(q)).join('') + '</div></div>'
        : '<div class="grid">' + qs.map(q => card(q)).join('') + '</div>';
      const tail = m.paras.length > 1 ? '<p style="text-align:center;margin-top:26px;color:var(--muted)">' + inline(m.paras[m.paras.length - 1]) + '</p>' : '';
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras.length ? m.paras[0] : '') + body + tail + '</div>';
    }
  };

  BLOCKS.faq = {
    label: 'FAQ', variants: ['two-col', 'accordion'],
    render(m, c) {
      const list = (m.items || []).map((it, i) => '<details' + (i === 0 ? ' open' : '') + '><summary>' + inline(it.title) + '</summary><div class="ans">' + (it.paras || []).map(p => '<p>' + inline(p) + '</p>').join('') + '</div></details>').join('');
      if (c.variant === 'accordion') return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="faq-wrap one"><div>' + list + '</div></div></div>';
      return '<div class="wrap"><div class="faq-wrap"><div class="faq-side">' + (c.eyebrow ? '<span class="eyebrow">' + esc(c.eyebrow) + '</span>' : '') +
        '<h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + (m.paras[0] ? '<p style="color:var(--muted)">' + inline(m.paras[0]) + '</p>' : '') + '<p>' + callBtn(c) + '</p></div><div>' + list + '</div></div></div>';
    }
  };

  BLOCKS.cta = {
    label: 'Call to action', variants: ['box', 'band'],
    render(m, c) {
      const paras = m.paras.slice();
      const note = paras.length > 1 ? paras.pop() : '';
      const inner = '<div class="cta-inner"><h2>' + inline(m.h2 || m.h1 || '') + '</h2>' + paras.map(p => '<p>' + inline(p) + '</p>').join('') +
        '<p style="margin-top:24px">' + callBtn(c) + '</p>' + (note ? '<div class="cta-note">' + inline(note) + '</div>' : '') + '</div>';
      if (c.variant === 'band') return '<div class="cta-band">' + inner + '</div>';
      return '<div class="wrap"><div class="cta-box">' + inner + '</div></div>';
    }
  };

  BLOCKS.badges = {
    label: 'Badges / credentials', variants: ['grid'],
    render(m, c) {
      let items = (m.items || []).map(i => ({ t: i.title, d: (i.paras || [])[0] || '' }));
      if (!items.length) items = (m.bullets || []).map(b => ({ t: b.label || b.text, d: b.label ? b.text : '' }));
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="badges">' + items.map(i =>
        '<div class="badge"><span class="ic">' + icon(pickIcon(i.t)) + '</span><b>' + inline(i.t) + '</b>' + (i.d ? '<span>' + inline(i.d) + '</span>' : '') + '</div>').join('') + '</div></div>';
    }
  };

  BLOCKS.area = {
    label: 'Service area + map', variants: ['map'],
    render(m, c) {
      const tags = (m.bullets || []).map(b => '<span class="tag">' + inline((b.label ? b.label + ' ' : '') + b.text) + '</span>').join('');
      const q = encodeURIComponent(c.nap.address || (c.brief.city + ', ' + c.brief.state));
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, '') + '<div class="area"><div>' + m.paras.map(p => '<p>' + inline(p) + '</p>').join('') +
        (tags ? '<div class="tags">' + tags + '</div>' : '') + '<p style="margin-top:22px">' + callBtn(c) + '</p></div>' +
        '<iframe loading="lazy" title="Service area map" src="https://www.google.com/maps?q=' + q + '&z=10&output=embed"></iframe></div></div>';
    }
  };

  BLOCKS.gallery = {
    label: 'Before / after', variants: ['cards'],
    render(m, c) {
      const b = c.pick(/contaminated|before|dirty/i), a = c.pick(/sanitized|after|clean/i);
      const it = m.items || [];
      const fig = (img, tag, cap, cls) => '<figure class="' + cls + '">' + (img ? '<img src="' + esc(img.src) + '" alt="' + esc(img.alt) + '">' : '<div style="aspect-ratio:4/3"></div>') +
        '<span class="tagb">' + tag + '</span><figcaption><strong>' + inline(cap.title || '') + '</strong><br>' + inline((cap.paras || [])[0] || '') + '</figcaption></figure>';
      const stats = (m.bullets || []).map(x => {
        const mm = (x.text || x.label).match(/^([+\-]?[\d.,]+%?)\s*(.*)$/);
        return mm ? '<div><b>' + esc(mm[1]) + '</b>' + inline(mm[2]) + '</div>' : '';
      }).join('');
      return '<div class="wrap">' + head(c.eyebrow, m.h2 || m.h1, m.paras[0]) + '<div class="ba">' + fig(b, 'BEFORE', it[0] || {}, 'before') + fig(a, 'AFTER', it[1] || {}, 'after') + '</div>' +
        (stats ? '<div class="stats">' + stats + '</div>' : '') + '</div>';
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
