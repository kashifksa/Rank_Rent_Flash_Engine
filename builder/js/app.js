/* app.js : editor UI (section list, field editor, live preview, export). */
(function () {
  const B = window.Builder, D = window.BUILDER_DATA, $ = s => document.querySelector(s), esc = B.esc;
  const KEY = 'site_builder_v5::' + (D.brief.project_name || 'project');
  let pid = 'homepage', sel = null, lastY = 0, vp = 'desktop', saveT = null, frameT = null;

  /* ---------- helpers ---------- */
  const pretty = s => String(s).replace(/[-_]/g, ' ').replace(/\b\w/g, x => x.toUpperCase());
  function toast(msg) { const t = $('#toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 2200); }
  function getPath(o, p) { return p.split('.').reduce((a, k) => (a == null ? a : a[k]), o); }
  function setPath(o, p, v) { const k = p.split('.'); const last = k.pop(); const t = k.reduce((a, x) => a[x], o); t[last] = v; }
  function save() { clearTimeout(saveT); saveT = setTimeout(() => { B.state.page = pid; try { localStorage.setItem(KEY, JSON.stringify(B.state)); } catch (e) {} seoRefresh(); }, 250); }

  /* ---------- SEO audit (primary keyword + density, warn-only) ---------- */
  function seoRefresh() {
    if (!B.seoAudit) return;
    const r = B.seoAudit(pid), b = $('#seoScore'); if (!b) return;
    b.textContent = r ? r.score : '-';
    b.className = 'seoScore' + (r ? (r.score >= 85 ? ' good' : r.score >= 60 ? ' mid' : ' bad') : '');
    if (!$('#seoPop').hidden) renderSeo(r);
  }
  function renderSeo(r) {
    r = r || B.seoAudit(pid); const box = $('#seoPop'); if (!r) { box.innerHTML = '<h4>SEO</h4><small>No SEO standards loaded.</small>'; return; }
    const d = r.density, tag = { pass: 'PASS', info: 'INFO', warn: 'WARN', fail: 'FAIL' };
    box.innerHTML = '<h4>SEO audit <small>warn-only, updates as you type</small></h4>' +
      '<div class="kw">Primary keyword: <b>' + esc(r.keyword || '(none)') + '</b>' + (d ? '<br>' + d.total + ' words | exact ' + d.exact + 'x (' + d.exactPct + '%) | variant "' + esc(d.variant) + '" +' + d.variantOnly + 'x | <b>combined ' + d.combinedPct + '%</b> (target ' + d.target[0] + '-' + d.target[1] + '%)' : '') + '</div>' +
      r.checks.map(c => '<div class="seo-row ' + c.status + '"><div class="st">' + tag[c.status] + '</div><div><b>' + esc(c.label) + '</b><span>' + esc(c.detail) + '</span></div></div>').join('') +
      (r.sections.length ? '<div class="seo-heat"><b style="font-size:11px">Keyword density by section</b>' + r.sections.map(s => '<div><span>' + esc(s.label) + '</span><i class="' + (s.flag ? 'over' : '') + '" style="width:' + Math.min(100, s.pct * 25) + '%"></i><span>' + s.pct + '%</span></div>').join('') + '</div>' : '');
  }
  function download(name, text, type) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type: type || 'text/html;charset=utf-8' })); a.download = name; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  }

  /* ---------- preview frame ---------- */
  const frame = () => $('#frame');
  function loadFrame() {
    const f = frame();
    f.onload = () => { try { f.contentWindow.postMessage({ b5: 'setScroll', y: lastY }, '*'); } catch (e) {} };
    f.srcdoc = B.buildDocument(pid, { preview: true, selected: sel });
  }
  function reloadSoon() { clearTimeout(frameT); frameT = setTimeout(loadFrame, 140); }
  function refreshSection() {
    if (!sel) return;
    const html = B.renderSectionHtml(pid, sel, { preview: true, selected: sel, instant: true });
    frame().contentWindow.postMessage({ b5: 'replace', sid: sel, html: html }, '*');
  }

  /* ---------- top bar ---------- */
  function initTop() {
    $('#projName').textContent = D.nap.company_name + ' | ' + D.brief.city + ', ' + D.brief.state;
    $('#tplSel').innerHTML = Object.keys(B.TEMPLATES).map(k => '<option value="' + k + '">' + esc(B.TEMPLATES[k].name) + ' - ' + esc(B.TEMPLATES[k].badge) + '</option>').join('');
    $('#thFont').innerHTML = Object.keys(B.FONTS).map(k => '<option value="' + k + '">' + esc(B.FONTS[k].label) + '</option>').join('');
    const groups = [['homepage', 'Homepage'], ['service', 'Service pages'], ['location', 'Location pages'], ['blog', 'Blog posts'], ['about', 'About'], ['contact', 'Contact']];
    $('#pageSel').innerHTML = groups.map(g => {
      const ps = Object.values(D.pages).filter(p => p.type === g[0]);
      return ps.length ? '<optgroup label="' + g[1] + '">' + ps.map(p => '<option value="' + p.id + '">' + esc(p.nav || p.title) + '</option>').join('') + '</optgroup>' : '';
    }).join('');
    $('#tplSel').onchange = e => { B.setTemplate(e.target.value); toast('Template applied: ' + B.tpl().name + ' (layout choices reset, your text edits kept)'); syncTheme(); renderAll(); save(); };
    $('#pageSel').onchange = e => go(e.target.value);
    $('#vpSeg').onclick = e => {
      const b = e.target.closest('button'); if (!b) return; vp = b.dataset.vp;
      document.querySelectorAll('#vpSeg button').forEach(x => x.classList.toggle('on', x === b));
      $('#frameWrap').style.maxWidth = { desktop: '1440px', tablet: '820px', mobile: '400px' }[vp];
    };
    $('#themeBtn').onclick = () => { const p = $('#themePop'); p.hidden = !p.hidden; $('#seoPop').hidden = true; syncTheme(); };
    $('#seoBtn').onclick = () => { const p = $('#seoPop'); p.hidden = !p.hidden; $('#themePop').hidden = true; if (!p.hidden) renderSeo(); };
    const th = (id, key, cast) => { $(id).oninput = e => { B.state.theme = Object.assign({}, B.state.theme, { [key]: cast ? cast(e.target.value) : e.target.value }); reloadSoon(); save(); }; };
    const thd = (id, key) => { $(id).onchange = e => { const th0 = Object.assign({}, B.state.theme); if (e.target.value === '') delete th0[key]; else th0[key] = e.target.value; B.state.theme = th0; reloadSoon(); save(); }; };
    thd('#thAnim', 'anim'); thd('#thFx', 'fx');
    const br = (k, v) => { B.state.brand = Object.assign({}, B.state.brand, { [k]: v }); reloadSoon(); save(); syncBrand(); };
    $('#thLogoSrc').onchange = e => br('logoSrc', e.target.value);
    $('#thLogoH').oninput = e => br('height', Number(e.target.value));
    $('#thLogoMode').onchange = e => br('mode', e.target.value);
    $('#thFavicon').onchange = e => br('favicon', e.target.checked);
    $('#thFooterLogo').onchange = e => br('footer', e.target.checked);
    $('#thLogoBtn').onclick = () => $('#thLogoFile').click();
    $('#thLogoFile').onchange = e => {
      const f = e.target.files[0]; if (!f) return;
      const r = new FileReader(); r.onload = () => {
        B.state.brand = Object.assign({}, B.state.brand, { logoSrc: 'upload', logoData: r.result });
        toast('Logo loaded (' + Math.round(f.size / 1024) + ' KB' + (f.size > 102400 ? ', over 100 KB: run image_geotagger.py before launch' : '') + ')');
        reloadSoon(); save(); syncBrand();
      }; r.readAsDataURL(f); e.target.value = '';
    };
    th('#thPrimary', 'primary'); th('#thAccent', 'accent'); th('#thFont', 'font'); th('#thRadius', 'radius', Number); th('#thDensity', 'density');
    $('#thReset').onclick = () => { B.state.theme = {}; syncTheme(); reloadSoon(); save(); };
    $('#exportBtn').onclick = e => { e.stopPropagation(); document.querySelector('.menu').classList.toggle('open'); };
    document.addEventListener('click', e => { if (!e.target.closest('.menu')) document.querySelector('.menu').classList.remove('open'); if (!e.target.closest('#themePop') && e.target.id !== 'themeBtn') $('#themePop').hidden = true; });
    $('#exportMenu').onclick = e => {
      const a = e.target.closest('button'); if (!a) return; document.querySelector('.menu').classList.remove('open');
      ({ page: exportThis, all: exportAll, save: saveProject, load: () => $('#fileIn').click(), reset: resetAll })[a.dataset.act]();
    };
    $('#fileIn').onchange = e => {
      const f = e.target.files[0]; if (!f) return;
      const r = new FileReader(); r.onload = () => {
        try { B.state = Object.assign({ template: 'cornerstone', theme: {}, pages: {} }, JSON.parse(r.result)); const n = B.reconcile(); renderAll(); toast('Project loaded' + (n ? ' (' + n + ' edits dropped: source text changed)' : '')); save(); } catch (er) { toast('Invalid project file'); }
      }; r.readAsText(f); e.target.value = '';
    };
  }
  function syncTheme() {
    const t = B.theme();
    $('#tplSel').value = B.state.template;
    $('#thPrimary').value = t.primary; $('#thAccent').value = t.accent; $('#thFont').value = t.font; $('#thRadius').value = t.radius; $('#thDensity').value = t.density;
    $('#tplNote').textContent = B.tpl().name;
    $('#thAnim').value = t.anim || ''; $('#thFx').value = t.fx || '';
    syncBrand();
  }
  function syncBrand() {
    const b = B.brand(), d = D.brand || {};
    $('#thLogoSrc').value = b.logoSrc; $('#thLogoH').value = b.height; $('#thLogoMode').value = b.mode;
    $('#thFavicon').checked = !!b.favicon; $('#thFooterLogo').checked = !!b.footer;
    $('#logoNote').textContent = b.logoSrc === 'upload' && b.logoData ? 'Using the uploaded logo (for the final site, save it as a .webp in images/ and re-compile).'
      : (d.logo ? 'Detected: ' + d.logo : 'No *logo*.webp found in images/. Upload one or add it to images/.') + (d.favicon ? ' | Favicon: ' + d.favicon : '');
  }
  function exportThis() { download(B.fileName(pid), B.exportPage(pid)); toast('Downloaded ' + B.fileName(pid)); }
  function exportAll() {
    const ids = B.pageIds(); ids.forEach((id, i) => setTimeout(() => download(B.fileName(id), B.exportPage(id)), i * 350)); toast('Downloading ' + ids.length + ' pages...');
  }
  function saveProject() { download('builder_state.json', JSON.stringify(B.state, null, 2), 'application/json'); toast('Saved builder_state.json (put it in the project folder)'); }
  function resetAll() {
    if (!confirm('Reset ALL your edits (text, layouts, theme, order)?')) return;
    B.state = { template: B.state.template, theme: {}, pages: {} }; B._cache = {};
    try { localStorage.removeItem(KEY); } catch (e) {}
    syncTheme(); renderAll(); toast('All edits reset');
  }

  /* ---------- navigation ---------- */
  function go(id) { if (!D.pages[id]) return; pid = id; sel = null; lastY = 0; $('#pageSel').value = id; renderAll(); save(); }
  function select(sid, scroll) {
    sel = sid; renderLeft(); renderEditor();
    try { frame().contentWindow.postMessage({ b5: 'select', sid: sid, scroll: !!scroll }, '*'); } catch (e) {}
  }
  window.addEventListener('message', e => {
    const d = e.data || {};
    if (d.b5 === 'select') select(d.sid, false);
    else if (d.b5 === 'scroll') lastY = d.y;
    else if (d.b5 === 'nav') {
      const file = String(d.href).split('#')[0].replace(/^\.?\//, '');
      const hit = B.pageIds().find(p => B.fileName(p) === file);
      if (hit) go(hit); else toast('Link: ' + d.href);
    }
  });

  /* ---------- left: section list ---------- */
  function renderLeft() {
    const list = B.sectionList(pid), ps = B.ps(pid);
    $('#secCount').textContent = list.length + ' sections';
    $('#seclist').innerHTML = list.map((sid, i) => {
      const off = ps.hidden[sid];
      return '<div class="row' + (sid === sel ? ' sel' : '') + (off ? ' off' : '') + '" data-sid="' + esc(sid) + '"><span class="num">' + (i + 1) + '</span>' +
        '<div class="nm"><b>' + esc(B.sectionLabel(pid, sid)) + (B.hasEdits(pid, sid) ? '<span class="dot" title="Edited"></span>' : '') + '</b><small>' + esc(B.sectionType(pid, sid)) + ' / ' + esc(B.getVariant(pid, sid)) + '</small></div>' +
        '<button class="ib" data-a="up" title="Move up"' + (i === 0 ? ' disabled' : '') + '>&uarr;</button><button class="ib" data-a="down" title="Move down"' + (i === list.length - 1 ? ' disabled' : '') + '>&darr;</button>' +
        '<button class="ib" data-a="eye" title="Show / hide">' + (off ? '&#9676;' : '&#9673;') + '</button></div>';
    }).join('');
    const sp = D.schema[B.page(pid).type];
    $('#addbox').innerHTML = sp && sp.flexible
      ? '<select id="addSel">' + (sp.optional_library || []).map(x => '<option value="' + x + '">' + pretty(x) + '</option>').join('') + '<option value="custom_section">Custom section</option></select><button class="btn2" id="addBtn" style="width:100%">+ Add section</button><p style="color:var(--muted);font-size:11px;margin:8px 0 0">Blog posts can have any number of sections. Required: header, FAQ, conclusion.</p>'
      : '<p style="color:var(--muted);font-size:11px;margin:0">Sections follow the live-site schema for this page type. Use the eye icon to hide one, arrows to reorder.</p>';
    const ab = $('#addBtn'); if (ab) ab.onclick = addSection;
  }
  $('#seclist').addEventListener('click', e => {
    const row = e.target.closest('.row'); if (!row) return; const sid = row.dataset.sid, b = e.target.closest('button');
    const ps = B.ps(pid);
    if (b) {
      e.stopPropagation();
      if (b.dataset.a === 'eye') { ps.hidden[sid] = !ps.hidden[sid]; renderLeft(); loadFrame(); save(); return; }
      const list = B.sectionList(pid).slice(), i = list.indexOf(sid), j = b.dataset.a === 'up' ? i - 1 : i + 1;
      if (j < 0 || j >= list.length) return;
      [list[i], list[j]] = [list[j], list[i]]; ps.order = list; renderLeft(); loadFrame(); save(); return;
    }
    select(sid, true);
  });
  function addSection() {
    const lib = $('#addSel').value, ps = B.ps(pid), list = B.sectionList(pid);
    let sid = lib, n = 2; while (list.indexOf(sid) > -1) sid = lib + '_' + n++;
    ps.added[sid] = '## ' + pretty(lib) + '\n\nWrite your text here.\n';
    const at = list.findIndex(s => /faq$/.test(s) || /conclusion/.test(s));
    list.splice(at > -1 ? at : list.length, 0, sid); ps.order = list;
    renderLeft(); loadFrame(); select(sid, false); save(); toast('Section added: ' + pretty(lib));
  }

  /* ---------- right: editor ---------- */
  const inp = (f, label, v, ph) => '<div class="fld"><label>' + label + '</label><input type="text" data-f="' + f + '" value="' + esc(v) + '"' + (ph ? ' placeholder="' + esc(ph) + '"' : '') + '></div>';
  const area = (f, label, v, rows, lines) => '<div class="fld">' + (label ? '<label>' + label + '</label>' : '') + '<textarea rows="' + (rows || 3) + '" data-f="' + f + '"' + (lines ? ' data-lines="1"' : '') + '>' + esc(v) + '</textarea></div>';
  const opt = (v, cur, label) => '<option value="' + esc(v) + '"' + (v === cur ? ' selected' : '') + '>' + esc(label || pretty(v)) + '</option>';
  const act = (a, label, cls) => '<button class="sm ' + (cls || '') + '" data-a="' + a + '">' + label + '</button>';

  function renderEditor() {
    const box = $('#editor');
    if (!sel) { box.innerHTML = '<div class="hint"><b>Pick a section</b><br>Click a section in the list or directly in the preview to edit its text, layout, background and image.<br><br><b>Template</b> changes every default layout at once. <b>Theme</b> changes colors, fonts and spacing for the whole site.</div>'; return; }
    const type = B.sectionType(pid, sel), m = B.getModel(pid, sel), ps = B.ps(pid), cur = B.getVariant(pid, sel), vl = B.variantsFor(type);
    const added = !!ps.added[sel];
    let h = '<div class="eh"><h3>' + esc(B.sectionLabel(pid, sel)) + '</h3><small>' + esc(sel) + ' &middot; ' + esc(type) + '</small><div class="acts">' +
      (B.hasEdits(pid, sel) && !added ? act('reset', 'Reset to source text') : '') + (added ? act('remove', 'Delete section', 'danger') : '') + '</div></div>';

    h += '<div class="grp"><h5>Layout</h5><div class="two">';
    h += '<div class="fld"><label>Layout</label><select data-v="variant"' + (vl.length < 2 ? ' disabled' : '') + '>' + vl.map(v => opt(v, cur)).join('') + '</select></div>';
    h += '<div class="fld"><label>Background</label><select data-v="bg">' + ['auto', 'none', 'light', 'dark', 'accent'].map(v => opt(v, ps.bg[sel] || 'auto')).join('') + '</select></div></div>';
    if (type === 'hero' || type === 'split') {
      h += '<div class="fld"><label>Image</label><select data-v="image">' + opt('auto', ps.images[sel] || 'auto', 'Auto') + opt('none', ps.images[sel] || 'auto', 'No image') +
        B.imageOptions(pid).map(o => opt(o.file, ps.images[sel] || 'auto', o.file.replace(/\.webp$/, '').replace(/-/g, ' '))).join('') + '</select></div>';
    }
    h += '</div>';

    const o = B.getOpts(pid, sel);
    const osel = (k, label, list, v) => '<div class="fld"><label>' + label + '</label><select data-o="' + k + '">' + list.map(x => opt(x[0], String(v), x[1])).join('') + '</select></div>';
    h += '<div class="grp"><h5>Animation &amp; options</h5><div class="two">' +
      osel('anim', 'Entrance animation', [['auto', 'Auto (template)'], ['none', 'None'], ['fade', 'Fade in'], ['rise', 'Rise up'], ['slide-left', 'Slide from left'], ['slide-right', 'Slide from right'], ['zoom', 'Zoom in'], ['stagger', 'Cards one by one']], o.anim) +
      osel('speed', 'Speed', [['fast', 'Fast'], ['normal', 'Normal'], ['slow', 'Slow']], o.speed) + '</div><div class="two">' +
      '<div class="fld"><label>Delay (seconds)</label><input type="text" data-o="delay" value="' + esc(o.delay) + '"></div>' +
      osel('pad', 'Spacing', [['auto', 'Auto'], ['compact', 'Compact'], ['roomy', 'Roomy']], o.pad) + '</div><div class="two">' +
      osel('width', 'Content width', [['auto', 'Standard'], ['narrow', 'Narrow'], ['wide', 'Wide']], o.width) +
      osel('align', 'Heading align', [['auto', 'Auto'], ['left', 'Left'], ['center', 'Center']], o.align) + '</div><div class="two">' +
      osel('hover', 'Card hover lift', [['on', 'On'], ['off', 'Off']], o.hover) +
      (type === 'hero' ? osel('fx', 'Hero effect', [['auto', 'Auto (template)'], ['none', 'None'], ['airflow', 'Airflow'], ['motes', 'Motes'], ['blueprint', 'Blueprint grid']], o.fx) : '<div></div>') +
      '</div>' + act('replay', 'Replay animation') + '</div>';

    if (type === 'article' || type === 'nap') {
      h += '<div class="grp"><h5>Content (markdown)</h5>' + '<div class="fld"><textarea rows="22" data-raw="1">' + esc(B.serializeSection(m)) + '</textarea></div><p style="color:var(--muted);font-size:11px;margin:0">Use ## for headings, - for lists, | for tables. Changes apply when you click away.</p></div>';
      box.innerHTML = h; return;
    }

    h += '<div class="grp"><h5>Headline</h5>';
    const showH1 = m.h1 !== '' || type === 'hero' || type === 'postHeader';
    if (showH1) h += inp('h1', 'Main heading (H1)', m.h1 || m.h2);
    if (m.h2 !== '' || !showH1) h += inp('h2', 'Heading (H2)', m.h2);
    if (['cards', 'steps', 'table', 'reviews', 'faq', 'badges', 'area', 'gallery'].indexOf(type) > -1) h += inp('eyebrow', 'Small label above heading', m.eyebrow || '', 'Auto (type "none" to hide)');
    if (type === 'hero') h += inp('btn2', 'Second button text', m.btn2 || '', 'See Our Services');
    h += '</div>';

    h += '<div class="grp"><h5>Paragraphs</h5>' + (m.paras || []).map((p, i) => '<div class="card"><div class="top"><span>Paragraph ' + (i + 1) + '</span>' + act('del:paras.' + i, 'Remove', 'danger') + '</div>' + area('paras.' + i, '', p, 3) + '</div>').join('') + act('add:paras', '+ Add paragraph') + '</div>';

    if (['cards', 'steps', 'faq', 'badges', 'gallery', 'split'].indexOf(type) > -1 || (m.items || []).length) {
      const isFaq = type === 'faq';
      h += '<div class="grp"><h5>' + (isFaq ? 'Questions' : 'Items') + '</h5>' + (m.items || []).map((it, i) => '<div class="card"><div class="top"><span>' + (isFaq ? 'Question ' : 'Item ') + (i + 1) + '</span><span>' +
        act('up:items.' + i, '&uarr;') + ' ' + act('down:items.' + i, '&darr;') + ' ' + act('del:items.' + i, 'Remove', 'danger') + '</span></div>' +
        inp('items.' + i + '.title', isFaq ? 'Question' : 'Title', it.title) +
        (it.facts || []).map((f, j) => '<div class="two">' + inp('items.' + i + '.facts.' + j + '.label', 'Label', f.label) + inp('items.' + i + '.facts.' + j + '.text', 'Text', f.text) + '</div>').join('') +
        area('items.' + i + '.paras', isFaq ? 'Answer' : 'Text', (it.paras || []).join('\n\n'), 4, true) + '</div>').join('') + act('add:items', isFaq ? '+ Add question' : '+ Add item') + '</div>';
    }
    if (type !== 'faq' && type !== 'hero') {
      h += '<div class="grp"><h5>List points</h5>' + (m.bullets || []).map((b, i) => '<div class="card"><div class="top"><span>Point ' + (i + 1) + '</span>' + act('del:bullets.' + i, 'Remove', 'danger') + '</div><div class="two">' +
        inp('bullets.' + i + '.label', 'Bold label', b.label) + inp('bullets.' + i + '.text', 'Text', b.text) + '</div></div>').join('') + act('add:bullets', '+ Add point') + '</div>';
    }
    if (m.table) {
      h += '<div class="grp"><h5>Table</h5><div class="tbl-ed"><table><tr>' + m.table.head.map((c, j) => '<td><input type="text" data-f="table.head.' + j + '" value="' + esc(c) + '"></td>').join('') + '<td></td></tr>' +
        m.table.rows.map((r, i) => '<tr>' + r.map((c, j) => '<td><input type="text" data-f="table.rows.' + i + '.' + j + '" value="' + esc(c) + '"></td>').join('') + '<td>' + act('del:table.rows.' + i, 'x', 'danger') + '</td></tr>').join('') + '</table></div>' + act('add:table.rows', '+ Add row') + '</div>';
    }
    if (type === 'reviews' || (m.quotes || []).length) {
      h += '<div class="grp"><h5>Reviews</h5>' + (m.quotes || []).map((q, i) => '<div class="card"><div class="top"><span>Review ' + (i + 1) + '</span>' + act('del:quotes.' + i, 'Remove', 'danger') + '</div>' +
        area('quotes.' + i + '.text', '', q.text, 3) + '<div class="two">' + inp('quotes.' + i + '.author', 'Name', q.author) + inp('quotes.' + i + '.loc', 'Location', q.loc) + '</div></div>').join('') + act('add:quotes', '+ Add review') + '</div>';
    }
    if (type === 'gallery') {
      const cc = B.siteCtx(pid, true), cards = cc.galleryCards(m), pairs = cc.galleryPairs(m), imgs = B.imageOptions(pid);
      const isel = (f, v) => '<select data-f="' + f + '">' + imgs.map(i => opt(i.file, v, i.file.replace(/\.webp$/, ''))).join('') + '</select>';
      h += '<div class="grp"><h5>Comparison cards (one image each)</h5>' + cards.map((k, i) => '<div class="card"><div class="top"><span>Card ' + (i + 1) + '</span><span>' +
        act('up:cards.' + i, '&uarr;') + ' ' + act('down:cards.' + i, '&darr;') + ' ' + act('del:cards.' + i, 'Remove', 'danger') + '</span></div>' +
        '<div class="fld"><label>Image</label>' + isel('cards.' + i + '.img', k.img) + '</div>' + inp('cards.' + i + '.alt', 'Alt text', k.alt) + inp('cards.' + i + '.caption', 'Caption (optional)', k.caption || '')).join('</div>') + (cards.length ? '</div>' : '') + act('add:cards', '+ Add card') + '</div>';
      h += '<div class="grp"><h5>Wipe slider cases (before + after)</h5>' + pairs.map((k, i) => '<div class="card"><div class="top"><span>Case ' + (i + 1) + '</span><span>' + act('del:pairs.' + i, 'Remove', 'danger') + '</span></div>' +
        inp('pairs.' + i + '.label', 'Tab label', k.label) + '<div class="two"><div class="fld"><label>Before</label>' + isel('pairs.' + i + '.before', k.before) + '</div><div class="fld"><label>After</label>' + isel('pairs.' + i + '.after', k.after) + '</div></div>' +
        inp('pairs.' + i + '.caption', 'Caption (optional)', k.caption || '')).join('</div>') + (pairs.length ? '</div>' : '') + act('add:pairs', '+ Add case') + '</div>';
    }
    if (m.cta) h += '<div class="grp"><h5>Call line</h5>' + inp('cta', 'Bold call line', m.cta) + '</div>';
    h += '<div class="grp"><h5>Advanced</h5><details style="background:none;border:0"><summary style="padding:0;cursor:pointer;color:var(--muted)">Edit whole section as markdown</summary><div class="fld" style="margin-top:8px"><textarea rows="14" data-raw="1">' + esc(B.serializeSection(m)) + '</textarea></div></details></div>';
    box.innerHTML = h;
  }

  function touch() { renderLeft(); save(); }
  $('#editor').addEventListener('input', e => {
    const el = e.target, f = el.dataset.f;
    if (!sel || !f) return;
    const m = B.editModel(pid, sel);
    if (B.sectionType(pid, sel) === 'gallery') B.prepGallery(pid, sel, m);
    let v = el.value;
    if (el.dataset.lines) v = v.split(/\n\s*\n/).map(s => s.trim()).filter(Boolean);
    if (f === 'h1' && m.h1 === '' && m.h2) setPath(m, 'h2', v); else setPath(m, f, v);
    if ((f === 'eyebrow' || f === 'btn2') && v === '') delete m[f];
    refreshSection(); if (!el._d) { el._d = 1; touch(); } else save();
  });
  $('#editor').addEventListener('change', e => {
    const el = e.target;
    if (el.dataset.raw) {
      const old = B.getModel(pid, sel), nm = B.parseSection(el.value);
      if (old.eyebrow) nm.eyebrow = old.eyebrow; if (old.btn2) nm.btn2 = old.btn2;
      B.editModel(pid, sel); B.ps(pid).models[sel] = nm; refreshSection(); renderEditor(); touch(); return;
    }
    if (el.dataset.o && sel) {
      const ps0 = B.ps(pid), k = el.dataset.o; ps0.opts[sel] = ps0.opts[sel] || {};
      let val = el.value; if (k === 'delay') val = Math.max(0, Number(val) || 0);
      if (val === 'auto' || (k === 'hover' && val === 'on') || (k === 'speed' && val === 'normal') || (k === 'delay' && !val)) delete ps0.opts[sel][k]; else ps0.opts[sel][k] = val;
      refreshSection(); if (/anim|speed|delay/.test(k)) frame().contentWindow.postMessage({ b5: 'replay', sid: sel }, '*'); save(); return;
    }
    const v = el.dataset.v; if (!v || !sel) return; const ps = B.ps(pid);
    if (v === 'variant') ps.variants[sel] = el.value;
    if (v === 'bg') { if (el.value === 'auto') delete ps.bg[sel]; else ps.bg[sel] = el.value; }
    if (v === 'image') { if (el.value === 'auto') delete ps.images[sel]; else ps.images[sel] = el.value; }
    refreshSection(); renderLeft(); save();
  });
  $('#editor').addEventListener('click', e => {
    const b = e.target.closest('button[data-a]'); if (!b || !sel) return;
    const a = b.dataset.a;
    if (a === 'replay') { frame().contentWindow.postMessage({ b5: 'replay', sid: sel }, '*'); return; }
    if (a === 'reset') { B.resetSection(pid, sel); refreshSection(); renderEditor(); touch(); toast('Section reset to source text'); return; }
    if (a === 'remove') {
      const ps = B.ps(pid); delete ps.added[sel]; delete ps.models[sel]; ps.order = B.sectionList(pid).filter(s => s !== sel); sel = null; renderLeft(); renderEditor(); loadFrame(); save(); return;
    }
    const [op, path] = a.split(':'); const m = B.editModel(pid, sel);
    if (B.sectionType(pid, sel) === 'gallery') B.prepGallery(pid, sel, m);
    const parts = path.split('.'), idx = parts.length > 1 && /^\d+$/.test(parts[parts.length - 1]) ? +parts.pop() : null, listPath = parts.join('.'), list = getPath(m, listPath);
    if (op === 'add') {
      if (listPath === 'paras') list.push('');
      else if (listPath === 'items') { const t = list[0]; list.push({ title: 'New item', paras: [''], bullets: [], facts: t && t.facts ? t.facts.map(f => ({ label: f.label, text: '' })) : [] }); }
      else if (listPath === 'bullets') list.push({ label: '', text: '' });
      else if (listPath === 'quotes') list.push({ text: '', author: '', loc: '', rating: 5 });
      else if (listPath === 'table.rows') list.push(m.table.head.map(() => ''));
      else if (listPath === 'cards') { const f = (B.imageOptions(pid)[0] || {}).file || ''; list.push({ img: f, alt: '', caption: '' }); }
      else if (listPath === 'pairs') { const f = (B.imageOptions(pid)[0] || {}).file || ''; list.push({ before: f, after: f, label: 'Case ' + (list.length + 1), caption: '' }); }
    } else if (op === 'del') list.splice(idx, 1);
    else if (op === 'up' && idx > 0) [list[idx - 1], list[idx]] = [list[idx], list[idx - 1]];
    else if (op === 'down' && idx < list.length - 1) [list[idx + 1], list[idx]] = [list[idx], list[idx + 1]];
    refreshSection(); renderEditor(); touch();
  });

  /* ---------- boot ---------- */
  function renderAll() { syncTheme(); renderLeft(); renderEditor(); loadFrame(); seoRefresh(); }
  function boot() {
    let loaded = false;
    try { const s = JSON.parse(localStorage.getItem(KEY) || 'null'); if (s) { B.state = Object.assign({ template: 'cornerstone', theme: {}, pages: {} }, s); loaded = true; } } catch (e) {}
    if (!loaded && D.defaultState) B.state = Object.assign({ template: 'cornerstone', theme: {}, pages: {} }, D.defaultState);
    if (!B.TEMPLATES[B.state.template]) B.state.template = 'cornerstone';
    const dropped = B.reconcile();
    initTop();
    pid = D.pages[B.state.page] ? B.state.page : (D.pages.homepage ? 'homepage' : B.pageIds()[0]);
    $('#pageSel').value = pid;
    renderAll();
    if (dropped) toast(dropped + ' saved edit(s) dropped because the source text changed');
  }
  B.app = { go: go, select: select, get pid() { return pid; }, get sel() { return sel; }, renderAll: renderAll };
  boot();
})();

