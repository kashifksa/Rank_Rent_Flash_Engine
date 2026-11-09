/* content.js : markdown <-> section model. Plain script (works on file://). */
(function () {
  const B = (window.Builder = window.Builder || {});

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function inline(s) {
    let t = esc(s);
    t = t.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, lbl, u) => '<a href="' + u.replace(/^\/?index\.html(?=#|$)/i, '/') + '">' + lbl + '</a>')
         .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
         .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    return t;
  }
  function stripComments(md) { return String(md || '').replace(/<!--[\s\S]*?-->/g, ''); }

  function splitRow(row) {
    return row.replace(/^\|/, '').replace(/\|\s*$/, '').split('|').map(c => c.trim());
  }
  function parseTable(rows) {
    const clean = rows.filter(r => !/^\|[\s:|-]+\|?$/.test(r));
    if (!clean.length) return null;
    return { head: splitRow(clean[0]), rows: clean.slice(1).map(splitRow) };
  }
  function tableHtml(t) {
    if (!t) return '';
    return '<div class="tbl"><table><thead><tr>' + t.head.map(h => '<th>' + inline(h) + '</th>').join('') +
      '</tr></thead><tbody>' + t.rows.map(r => '<tr>' + r.map(c => '<td>' + inline(c) + '</td>').join('') + '</tr>').join('') +
      '</tbody></table></div>';
  }

  function mdToHtml(md) {
    const lines = stripComments(md).split(/\r?\n/);
    const out = [];
    let i = 0;
    const isBlockStart = l => /^(#{1,4}\s|\||[-*]\s|\d+\.\s|>)/.test(l);
    while (i < lines.length) {
      const l = lines[i].trim();
      if (!l || /^---+$/.test(l)) { i++; continue; }
      let m = l.match(/^(#{1,4})\s+(.*)$/);
      if (m) { const n = Math.min(4, Math.max(2, m[1].length)); out.push('<h' + n + '>' + inline(m[2]) + '</h' + n + '>'); i++; continue; }
      if (l.startsWith('|')) {
        const rows = [];
        while (i < lines.length && lines[i].trim().startsWith('|')) { rows.push(lines[i].trim()); i++; }
        out.push(tableHtml(parseTable(rows))); continue;
      }
      if (/^[-*]\s+/.test(l)) {
        const it = [];
        while (i < lines.length && /^[-*]\s+/.test(lines[i].trim())) { it.push(lines[i].trim().replace(/^[-*]\s+/, '')); i++; }
        out.push('<ul>' + it.map(x => '<li>' + inline(x) + '</li>').join('') + '</ul>'); continue;
      }
      if (/^\d+\.\s+/.test(l)) {
        const it = [];
        while (i < lines.length && /^\d+\.\s+/.test(lines[i].trim())) { it.push(lines[i].trim().replace(/^\d+\.\s+/, '')); i++; }
        out.push('<ol>' + it.map(x => '<li>' + inline(x) + '</li>').join('') + '</ol>'); continue;
      }
      if (l.startsWith('>')) {
        const q = [];
        while (i < lines.length && lines[i].trim().startsWith('>')) { q.push(lines[i].trim().replace(/^>\s?/, '')); i++; }
        out.push('<blockquote>' + q.map(inline).join('<br>') + '</blockquote>'); continue;
      }
      const p = [];
      while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i].trim()) && !/^---+$/.test(lines[i].trim())) { p.push(lines[i].trim()); i++; }
      if (!p.length) { i++; continue; }
      out.push('<p>' + inline(p.join(' ')) + '</p>');
    }
    return out.join('\n');
  }

  function parseBullet(text) {
    const m = text.match(/^\*\*([^*]+?)\*\*[:\s\-]*(.*)$/);
    if (m) return { label: m[1].replace(/:$/, '').trim(), text: m[2].trim() };
    return { label: '', text: text.trim() };
  }

  /** Parse one section's markdown into an editable model. */
  function parseSection(md) {
    const lines = stripComments(md).split(/\r?\n/);
    const m = { h1: '', h2: '', paras: [], bullets: [], items: [], table: null, quotes: [], facts: [], cta: '' };
    let cur = null, q = null, tableRows = [];
    const flushQuote = () => { if (q) { m.quotes.push(q); q = null; } };
    const flushTable = () => { if (tableRows.length) { m.table = parseTable(tableRows); tableRows = []; } };
    for (const raw of lines) {
      const l = raw.trim();
      if (!l) { flushQuote(); flushTable(); continue; }
      if (/^---+$/.test(l)) continue;
      if (l.startsWith('|')) { tableRows.push(l); continue; } else flushTable();
      if (l.startsWith('### ')) { flushQuote(); cur = { title: l.slice(4).replace(/[*_#]/g, '').trim(), paras: [], bullets: [], facts: [] }; m.items.push(cur); continue; }
      if (l.startsWith('## ')) { flushQuote(); if (!m.h2) m.h2 = l.slice(3).replace(/[*#]/g, '').trim(); continue; }
      if (l.startsWith('# ')) { flushQuote(); m.h1 = l.slice(2).replace(/[*#]/g, '').trim(); continue; }
      if (l.startsWith('>')) {
        const t = l.replace(/^>\s?/, '').trim();
        if (!q) q = { text: '', author: '', loc: '', rating: 5 };
        if (/^[★\u2605]+$/.test(t)) { q.rating = t.length; }
        else if (/^[-\u2013]\s+/.test(t)) {
          const a = t.replace(/^[-\u2013]\s+/, ''); const idx = a.indexOf(',');
          q.author = (idx > -1 ? a.slice(0, idx) : a).trim(); q.loc = idx > -1 ? a.slice(idx + 1).trim() : '';
        } else q.text += (q.text ? ' ' : '') + t.replace(/^["\u201c]+|["\u201d]+$/g, '');
        continue;
      }
      flushQuote();
      let mm;
      if ((mm = l.match(/^[-*]\s+(.*)$/)) || (mm = l.match(/^\d+\.\s+(.*)$/))) {
        (cur ? cur.bullets : m.bullets).push(parseBullet(mm[1]));
        continue;
      }
      if ((mm = l.match(/^\*\*([^*:]+):\*\*\s*(.*)$/))) { (cur || m).facts.push({ label: mm[1].trim(), text: mm[2].trim() }); continue; }
      if ((mm = l.match(/^\*\*(.+)\*\*$/))) { m.cta = mm[1].trim(); continue; }
      (cur ? cur.paras : m.paras).push(l);
    }
    flushQuote(); flushTable();
    return m;
  }

  function serializeSection(m) {
    const o = [];
    if (m.h1) o.push('# ' + m.h1, '');
    if (m.h2) o.push('## ' + m.h2, '');
    (m.paras || []).forEach(p => o.push(p, ''));
    (m.facts || []).forEach(f => o.push('**' + f.label + ':** ' + f.text));
    if ((m.facts || []).length) o.push('');
    (m.bullets || []).forEach(b => o.push('- ' + (b.label ? '**' + b.label + ':** ' : '') + b.text));
    if ((m.bullets || []).length) o.push('');
    if (m.table) {
      o.push('| ' + m.table.head.join(' | ') + ' |', '|' + m.table.head.map(() => '---').join('|') + '|');
      m.table.rows.forEach(r => o.push('| ' + r.join(' | ') + ' |'));
      o.push('');
    }
    (m.items || []).forEach(it => {
      o.push('### ' + it.title);
      (it.facts || []).forEach(f => o.push('**' + f.label + ':** ' + f.text));
      (it.paras || []).forEach(p => o.push(p, ''));
      (it.bullets || []).forEach(b => o.push('- ' + (b.label ? '**' + b.label + ':** ' : '') + b.text));
      o.push('');
    });
    (m.quotes || []).forEach(q => {
      o.push('> "' + q.text + '"', '> - ' + q.author + (q.loc ? ', ' + q.loc : ''), '> ' + '\u2605'.repeat(q.rating || 5), '');
    });
    if (m.cta) o.push('**' + m.cta + '**', '');
    return o.join('\n').replace(/\n{3,}/g, '\n\n').trim() + '\n';
  }

  B.esc = esc; B.inline = inline; B.mdToHtml = mdToHtml; B.tableHtml = tableHtml;
  B.parseSection = parseSection; B.serializeSection = serializeSection;
})();

