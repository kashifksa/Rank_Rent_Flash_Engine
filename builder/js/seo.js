/* seo.js : live primary-keyword audit. Mirrors scripts/seo_audit.py (same thresholds from seo_standards.json via data.js).
   Works on the CURRENT edited text, so the score updates as you type. WARN-only: it never blocks export. */
(function () {
  const B = window.Builder, D = window.BUILDER_DATA;
  const FILLER = new Set(['in', 'of', 'for', 'and', 'the', 'a', 'an', 'to', 'near', 'at', 'by', 'on', 'with', 'your', 'our', '&']);
  const raw = s => (String(s || '').toLowerCase().match(/[a-z0-9]+(?:'[a-z]+)?/g) || []);
  const ft = t => t.filter(x => !FILLER.has(x));
  const nt = s => ft(raw(s));
  const clean = md => String(md || '').replace(/<!--[\s\S]*?-->/g, ' ').replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/<[^>]+>/g, ' ').replace(/^[\s>#*\-+|:]+/gm, ' ')
    .replace(/[|*_`~#>]/g, ' ').replace(/https?:\/\/\S+/g, ' ').replace(/[\u2014\u2013]/g, ' ').replace(/\s+/g, ' ').trim();
  function count(toks, ph) {
    const n = ph.length; if (!n || toks.length < n) return 0;
    let c = 0, i = 0;
    while (i <= toks.length - n) { let ok = true; for (let j = 0; j < n; j++) if (toks[i + j] !== ph[j]) { ok = false; break; } if (ok) { c++; i += n; } else i++; }
    return c;
  }
  function corePhrase(kt, drop, city, state) {
    const d = new Set(drop || []); raw(city).concat(raw(state)).forEach(x => d.add(x));
    const core = kt.slice(); while (core.length && d.has(core[core.length - 1])) core.pop();
    return core.length > 0 && core.length < kt.length ? core : [];
  }

  /* ---- location pages: doorway guard + local proof (mirrors scripts/seo_local.py) ---- */
  const ROAD_RE = /\b(?:Route|Rt\.?|IL|US|I|State Route|SR|Highway|Hwy|County Road|CR)[ -]?\d{1,3}[A-Z]?\b|\b[A-Z][a-z]+(?: [A-Z][a-z]+)? (?:Road|Rd|Avenue|Ave|Boulevard|Blvd|Parkway|Pkwy|Highway|Drive|Street)\b/g;
  const LM_RE = /\b(?:[A-Z][A-Za-z.'&]+ ){0,3}(?:High School|Middle School|Elementary|Town Hall|Village Hall|City Hall|Library|Park District|Forest Preserve|Fairgrounds|Mall|Shopping Center|Plaza|Hospital|Museum|Golf Course|Community Center|Recreation Center|Sports Complex|Speedway|Ice Arena|Airport|Courthouse|Fire Station|Police Department)\b|\b[A-Z][a-z]+ (?:Park|Preserve|Lake|River|Creek|Heights|Village|Estates|Hills|Grove|Crossing)\b/g;
  const esc = s => String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const shingles = (text, n) => { const t = raw(text), s = new Set(); for (let i = 0; i + n <= t.length; i++) s.add(t.slice(i, i + n).join(' ')); return s; };
  const pageText = pid => clean(B.sectionList(pid).filter(s => !B.ps(pid).hidden[s]).map(s => B.serializeSection(B.getModel(pid, s))).join('\n\n'));

  function localChecks(pid, page, secs, body, rt, rep, sev) {
    const L = Object.assign({ shingle_size: 5, similarity_warn: 0.3, similarity_fail: 0.5, min_landmarks: 2, min_roads: 1, min_city_mentions_per_1000: 4, unique_body_min_words: 700 }, (D.seo || {}).location || {});
    const city = page.city || '', hub = D.brief.city || '', company = D.nap.company_name || '';
    const add = (id, label, status, detail) => rep.checks.push({ id, label, status, detail });
    const plain = clean(body), mine = shingles(plain, L.shingle_size);
    let worst = 0, top = { p: '-', v: 0 };
    B.pageIds().forEach(o => {
      if (o === pid) return;
      const th = shingles(pageText(o), L.shingle_size); let shared = 0; mine.forEach(x => { if (th.has(x)) shared++; });
      const v = shared / Math.max(mine.size, 1); if (v > worst) { worst = v; top = { p: o, v }; }
    });
    add('similarity', 'Unique vs other pages (doorway guard)', worst >= L.similarity_fail ? 'fail' : worst >= L.similarity_warn ? 'warn' : 'pass',
      'Highest overlap ' + (top.v * 100).toFixed(1) + '% with ' + top.p + ' (warn ' + L.similarity_warn * 100 + '%, fail ' + L.similarity_fail * 100 + '%).');
    add('unique_words', 'Body has at least ' + L.unique_body_min_words + ' words', rt.length >= L.unique_body_min_words ? 'pass' : 'warn', rt.length + ' words.');

    const scrub = company ? plain.replace(new RegExp(esc(company), 'gi'), ' ') : plain;
    const roads = [...new Set((scrub.match(ROAD_RE) || []).map(x => x.trim()))].sort();
    const lms = [...new Set((scrub.match(LM_RE) || []).map(x => x.trim()))].filter(x => x !== city && x.toLowerCase() !== hub.toLowerCase() && !/^(our|the) /i.test(x)).sort();
    add('landmarks', 'At least ' + L.min_landmarks + ' local landmarks (FIX 39)', lms.length >= L.min_landmarks ? 'pass' : 'warn', lms.length + ' found: ' + (lms.slice(0, 6).join(', ') || 'none') + '. (Pattern match: confirm they are real places in ' + city + '.)');
    add('roads', 'At least ' + L.min_roads + ' numbered highway / thoroughfare (FIX 39)', roads.length >= L.min_roads ? 'pass' : 'warn', roads.length + ' found: ' + (roads.slice(0, 6).join(', ') || 'none') + '.');

    const noBrand = t => company ? t.replace(new RegExp(esc(company), 'gi'), '') : t, hubRe = new RegExp('\\b' + esc(hub) + '\\b', 'i');
    const heads = []; body.split('\n').forEach(l => { const m = l.match(/^(#{2,3})\s+(.+?)\s*#*\s*$/); if (m) heads.push(clean(m[2])); });
    const leaks = hub ? heads.filter(t => hubRe.test(noBrand(t))) : [];
    const introSec = secs.find(s => /intro/.test(s.sid)), introLeak = hub && introSec && hubRe.test(noBrand(clean(introSec.md)));
    add('hub_leak', 'No hub city (' + hub + ') in H2/H3 or intro (FIX 36)', !leaks.length && !introLeak ? 'pass' : 'fail', !leaks.length && !introLeak ? 'Clean.' : 'Hub city found in: ' + (leaks.slice(0, 3).join(' | ') || 'intro paragraph') + '.');

    const cm = city ? (plain.match(new RegExp(esc(city), 'gi')) || []).length : 0, per1k = cm / Math.max(rt.length, 1) * 1000;
    add('city_mentions', 'City is named naturally and often enough', per1k >= L.min_city_mentions_per_1000 ? 'pass' : 'warn', cm + ' mentions (' + per1k.toFixed(1) + ' per 1000 words, min ' + L.min_city_mentions_per_1000 + ').');
    const proofSec = secs.find(s => /proof|review/.test(s.sid)), cityRe = city ? new RegExp(esc(city), 'i') : null;
    add('local_review', 'City-specific review present', proofSec && cityRe && cityRe.test(clean(proofSec.md)) ? 'pass' : 'warn', proofSec && cityRe && cityRe.test(clean(proofSec.md)) ? 'Found.' : 'No review text in the proof section mentions ' + city + '.');
    const imgs = B.contentImages(pid), ci = imgs.filter(i => cityRe && cityRe.test(i.alt_text || ''));
    add('local_photo', 'Real local photo with city in alt text', ci.length ? 'pass' : 'warn', ci.length + ' of ' + imgs.length + ' images mention ' + city + '. Use genuine, geotagged job photos, not stock.');
    const nb = plain.match(/\b(?:Colonial Village|Meadow|Heights|Estates|Subdivision|neighbou?rhood)\b/g) || [];
    add('neighborhoods', 'Neighbourhood-level detail', nb.length >= 1 ? 'pass' : 'warn', nb.length + ' neighbourhood references.');
    const meta = page.meta || {};
    add('meta_city', 'City in meta title and description', cityRe && cityRe.test(meta.meta_title || '') && cityRe.test(meta.meta_description || '') ? 'pass' : 'warn', 'title: "' + String(meta.meta_title || '').slice(0, 60) + '"');

    const svcSec = secs.find(s => /service/.test(s.sid)), cards = [];
    if (svcSec) svcSec.md.split('\n').forEach(l => { const m = l.match(/^###\s+(.+)/); if (m) cards.push(clean(m[1])); });
    const canon = Object.values(D.pages).filter(p => p.type === 'service').map(p => new Set(ft(raw(p.title))));
    try { const hi0 = (B.getModel('homepage', 'services-grid').items || [])[0]; if (hi0) canon.push(new Set(ft(raw(hi0.title)))); } catch (e) { /* homepage primary service card is canonical too */ }
    const bad = cards.filter(c => { const ct = new Set(ft(raw(c))); return !canon.some(k => [...ct].filter(x => k.has(x)).length / Math.max(ct.size, 1) >= 0.67); });
    add('service_cards', 'Service cards match canonical Phase 1 services (FIX 36)', bad.length ? 'warn' : 'pass', bad.length ? 'Not canonical: ' + bad.join('; ') : 'All cards map to a Phase 1 service.');
  }

  /* ---- Phase 3: word budgets, answer-first, headings, FAQ, schema + NAP (mirrors structure_checks in scripts/seo_audit.py) ---- */
  const digits = s => String(s || '').replace(/\D/g, '');
  const normSid = s => String(s).replace(/^\d+[_-]/, '').replace(/_/g, '-');
  const PHONE_RE = /\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b/g;

  function structureChecks(pid, page, secs, body, rep, sev) {
    const S = (D.seo || {}).structure; if (!S) return;
    const type = page.type, meta = page.meta || {}, add = (id, label, st, detail) => rep.checks.push({ id, label, status: st, detail });
    const okSt = ok => ok ? 'pass' : sev;

    const bud = (S.budgets || {})[type] || {}, counts = {}; let total = 0;
    secs.forEach(s => { const n = raw(clean(s.md)).length; counts[normSid(s.sid)] = n; total += n; });
    if (bud.total) add('word_total', 'Total words within structure target (' + bud.total[0] + '-' + bud.total[1] + ')', okSt(total >= bud.total[0] && total <= bud.total[1]), total + ' words.');
    const bad = [];
    Object.keys(bud).forEach(k => { if (k === 'total' || !(k in counts)) return; const lo = bud[k][0], hi = bud[k][1], n = counts[k]; if ((lo !== null && n < lo) || (hi !== null && n > hi)) bad.push(k + ' ' + n + ' (allowed ' + (lo !== null ? lo : 0) + '-' + (hi !== null ? hi : 'any') + ')'); });
    if (Object.keys(bud).length) add('word_sections', 'Every section within its word budget', okSt(!bad.length), bad.length ? bad.slice(0, 5).join('; ') + (bad.length > 5 ? ' (+' + (bad.length - 5) + ' more)' : '') : 'All sections in range.');

    const af = S.answer_first; let first = '';
    for (const s of secs) {
      for (const blk of s.md.replace(/<!--[\s\S]*?-->/g, '').split(/\n\s*\n/)) { const b = blk.trim(); if (b && !/^[#|\-*>!]/.test(b) && raw(b).length >= 8) { first = clean(b); break; } }
      if (first) break;
    }
    const nfp = raw(first).length;
    if (af) add('answer_first', 'Answer-first opening paragraph (' + af.min_words + '-' + af.max_words + ' words)', okSt(nfp >= af.min_words && nfp <= af.max_words), 'First paragraph is ' + nfp + ' words. AI Overviews and snippets favour a direct answer near the top.');

    const lv = []; body.split('\n').forEach(l => { const m = l.match(/^(#{1,6})\s+/); if (m) lv.push(m[1].length); });
    let h1n = lv.filter(x => x === 1).length, skips = 0, prev = 0;
    lv.forEach(x => { if (prev && x > prev + 1) skips++; prev = x; });
    add('headings', 'One H1, no skipped heading levels', okSt(h1n <= 1 && skips === 0), h1n + ' H1, ' + skips + ' skipped level(s).' + (h1n === 0 ? ' Sections may hold the H1 elsewhere.' : ''));

    const hasList = /^\s*(?:[-*]\s+\S|\d+\.\s+\S)/m.test(body), hasTable = /^\s*\|.+\|\s*$/m.test(body);
    add('parseable', 'Has a list or table (easy for AI answers to cite)', okSt(hasList || hasTable), 'list: ' + (hasList ? 'True' : 'False') + ', table: ' + (hasTable ? 'True' : 'False') + '.');

    const F = S.faq || {}, faq = [];
    if ((F.page_types || []).indexOf(type) > -1) {
      secs.filter(s => /faq/.test(s.sid)).forEach(s => { const parts = s.md.split(/^###\s+(.+)$/m); for (let i = 1; i < parts.length; i += 2) faq.push([clean(parts[i]), raw(clean(parts[i + 1] || '')).length]); });
      const avg = faq.length ? faq.reduce((a, q) => a + q[1], 0) / faq.length : 0;
      add('faq', 'FAQ has ' + F.min_questions + '+ questions with concise answers', okSt(faq.length >= F.min_questions && avg <= F.max_avg_answer_words), faq.length + ' questions, average answer ' + Math.round(avg) + ' words (max ' + F.max_avg_answer_words + ').');
    }

    const sch = meta.schema || {};
    let graph = Array.isArray(sch['@graph']) ? sch['@graph'] : (Array.isArray(sch) ? sch : []);
    if (!graph.length && sch['@type']) graph = [sch];
    const types = new Set(); graph.forEach(g => [].concat(g['@type'] || []).forEach(t => types.add(t)));
    const exp = (S.schema_expected || {})[type] || [], missing = exp.filter(o => !o.some(t => types.has(t))).map(o => o.join(' / '));
    add('schema_types', 'Structured data present for this page type', okSt(graph.length > 0 && !missing.length), 'Found: ' + ([...types].sort().join(', ') || 'none') + '.' + (missing.length ? ' Missing: ' + missing.join('; ') + '.' : ''));
    const faqNode = graph.find(g => g['@type'] === 'FAQPage');
    if (faqNode && (F.page_types || []).indexOf(type) > -1) { const n = (faqNode.mainEntity || []).length; add('schema_faq_match', 'FAQ schema matches the visible FAQ', okSt(n === faq.length), 'Schema has ' + n + ' questions, page shows ' + faq.length + '. Schema must match what users see.'); }

    const bphone = digits(D.nap.phone), bname = (D.nap.company_name || '').trim(), host = u => String(u || '').toLowerCase().replace(/^https?:\/\/(www\.)?/, '').split('/')[0], probs = [];
    graph.forEach(g => [g].concat(g.provider && typeof g.provider === 'object' ? [g.provider] : []).forEach(n => {
      if (n.telephone && [bphone, '1' + bphone].indexOf(digits(n.telephone)) < 0) probs.push('schema phone ' + n.telephone);
      if (['HVACBusiness', 'LocalBusiness', 'Organization'].indexOf(n['@type']) > -1 && n.name && bname && n.name.trim() !== bname) probs.push("schema name '" + n.name + "'");
      if (n.url && D.nap.website && host(n.url) !== host(D.nap.website)) probs.push('schema url ' + n.url);
    }));
    const odd = [...new Set((clean(body).match(PHONE_RE) || []).map(digits))].filter(p => [bphone, '1' + bphone].indexOf(p) < 0);
    if (odd.length) probs.push('page phone(s) ' + odd.sort().join(', '));
    const street = String(D.nap.address || '').split(',')[0].trim(), cb = clean(body);
    if (street && /\b\d{3,5} [NSEW]\.? [A-Z][a-z]+ (?:Rd|Road|St|Street|Ave|Avenue|Blvd|Dr|Drive)\b/.test(cb) && cb.toLowerCase().indexOf(street.toLowerCase()) < 0) probs.push('a street address on the page differs from the brief');
    add('nap', 'Name, address and phone match the brief (schema + page)', probs.length ? 'fail' : 'pass', probs.length ? 'Mismatch: ' + probs.slice(0, 4).join('; ') : 'Consistent.');
  }

  B.seoAudit = function (pid) {
    const std = D.seo || {}, page = B.page(pid); if (!std.primary_keyword || !page) return null;
    const cfg = Object.assign({}, std.primary_keyword, (std.page_type_overrides || {})[page.type] || {});
    const sev = ((std.severity || {}).default) || 'warn';
    const kw = (page.keyword || '').trim();
    const rep = { page_id: pid, keyword: kw, checks: [], sections: [], density: null, score: 0 };
    if (!kw) { rep.checks.push({ id: 'keyword_defined', status: 'fail', label: 'Primary keyword defined', detail: 'No target_keyword in page_meta or topical_authority.json.' }); return rep; }
    const st = (ok) => ok ? 'pass' : sev;
    const add = (id, label, ok, detail) => rep.checks.push({ id, status: st(ok), label, detail });

    const kt = nt(kw), core = cfg.count_variants ? corePhrase(kt, cfg.variant_drop_trailing_tokens, page.city || D.brief.city, D.brief.state) : [];
    const secs = B.sectionList(pid).filter(s => !B.ps(pid).hidden[s]).map(sid => ({ sid, md: B.serializeSection(B.getModel(pid, sid)) }));
    const body = secs.map(s => s.md).join('\n\n');
    const rt = raw(clean(body)), toks = ft(rt), total = rt.length;
    const exact = count(toks, kt), coreTotal = core.length ? count(toks, core) : 0, vOnly = Math.max(coreTotal - exact, 0);
    const exactPct = total ? exact / total * 100 : 0, combPct = total ? (exact + vOnly) / total * 100 : 0;
    rep.density = { total, exact, exactPct: +exactPct.toFixed(2), variant: core.join(' '), variantOnly: vOnly, combinedPct: +combPct.toFixed(2), target: [cfg.density_min, cfg.density_target_max] };

    const lo = cfg.density_min, hi = cfg.density_target_max, wmax = cfg.density_warn_max, fmax = cfg.density_fail_max;
    const hits = exact + vOnly, needMore = Math.max(0, Math.ceil(lo * total / 100) - hits), over = Math.max(0, hits - Math.floor(hi * total / 100));
    let s, det;
    if (combPct < lo) { s = cfg.density_min_severity || sev; det = combPct.toFixed(2) + '% is under ' + lo + '%. Informational only: Google has no density target, so write naturally and keep the topic clear (about ' + needMore + ' more mention(s) would reach ' + lo + '%).'; }
    else if (combPct <= hi) { s = 'pass'; det = combPct.toFixed(2) + '% is within the natural range (' + lo + '-' + hi + '%).'; }
    else if (combPct <= wmax) { s = 'pass'; det = combPct.toFixed(2) + '% is slightly above ' + hi + '% (under the ' + wmax + '% warning line).'; }
    else if (combPct <= fmax) { s = sev; det = combPct.toFixed(2) + '% exceeds ' + wmax + '% and may read as stuffing. Replace about ' + over + ' mention(s) with synonyms or pronouns.'; }
    else { s = 'fail'; det = combPct.toFixed(2) + '% exceeds ' + fmax + '% (stuffing). Replace about ' + over + ' mention(s).'; }
    rep.checks.push({ id: 'density', status: s, label: 'Primary keyword density (exact + core variant)', detail: det + ' Exact only: ' + exactPct.toFixed(2) + '% (' + exact + 'x) of ' + total + ' words.' });

    const has = t => count(nt(t), kt) > 0 || (core.length > 0 && count(nt(t), core) > 0);
    const req = new Set(cfg.required_in || []);
    const heads = []; body.split('\n').forEach(l => { const m = l.match(/^(#{1,6})\s+(.+?)\s*#*\s*$/); if (m) heads.push([m[1].length, clean(m[2])]); });
    const h1 = (heads.find(h => h[0] === 1) || [0, page.meta && page.meta.h1 || ''])[1];
    if (req.has('h1')) add('h1', 'Keyword in H1', !!h1 && count(nt(h1), kt) > 0, h1 ? (count(nt(h1), kt) ? 'Found in H1: "' + h1.slice(0, 70) + '"' : 'Not found. H1: "' + h1.slice(0, 70) + '"') : 'No H1 found.');
    if (req.has('first_words')) { const w = cfg.first_words_window || 100; add('first_words', 'Keyword in first ' + w + ' words', has(rt.slice(0, w).join(' ')), 'Checked the first ' + w + ' body words.'); }
    if (req.has('h2_any')) {
      const h2 = heads.filter(h => h[0] === 2).map(h => h[1]), hit = h2.filter(has), every = h2.length > 2 && hit.length === h2.length;
      add('h2_any', 'Keyword in at least one H2 (not all)', hit.length > 0 && !every, every ? 'Every H2 repeats the keyword (stuffing).' : hit.length + ' of ' + h2.length + ' H2s contain it.');
    }
    const meta = page.meta || {}, mt = meta.meta_title || '', md = meta.meta_description || '';
    if (req.has('meta_title')) {
      add('meta_title', 'Keyword in meta title', has(mt) && mt.length > 0, has(mt) ? 'Keyword present.' : 'Keyword missing from meta title.');
      add('meta_title_len', 'Meta title length (display is pixel-based, ~50-60 chars)', mt.length >= cfg.meta_title_min_chars && mt.length <= cfg.meta_title_max_chars, mt.length + ' chars (target ' + cfg.meta_title_min_chars + '-' + cfg.meta_title_max_chars + '). Google may rewrite titles that are too long or stuffed.');
    }
    if (req.has('meta_description')) {
      add('meta_description', 'Keyword in meta description', has(md) && md.length > 0, has(md) ? 'Keyword present.' : 'Keyword missing from meta description.');
      add('meta_description_len', 'Meta description length (snippet candidate)', md.length >= cfg.meta_description_min_chars && md.length <= cfg.meta_description_max_chars, md.length + ' chars (target ' + cfg.meta_description_min_chars + '-' + cfg.meta_description_max_chars + ').');
    }
    if (req.has('slug')) {
      const slug = meta.slug || page.slug || pid;
      if ((cfg.slug_exempt_page_types || []).indexOf(page.type) > -1 || slug === '/' || slug === '') rep.checks.push({ id: 'slug', status: 'pass', label: 'Keyword in URL slug', detail: 'Exempt (homepage).' });
      else { const set = new Set(nt(slug.replace(/-/g, ' '))), cs = core.length ? core : kt, ov = cs.filter(x => set.has(x)).length / Math.max(cs.length, 1); add('slug', 'Keyword in URL slug', ov >= 0.75, 'Slug "' + slug + '" covers ' + Math.round(ov * 100) + '% of the core keyword words.'); }
    }
    if (req.has('conclusion')) { const last = secs.length ? clean(secs[secs.length - 1].md) : ''; add('conclusion', 'Keyword in conclusion / final CTA', has(last), has(last) ? 'Found.' : 'Not in the last section.'); }

    const imgs = B.contentImages(pid);
    if (imgs.length) { const n = imgs.filter(i => has(i.alt_text || '')).length; add('image_alt', 'Keyword in 1-2 image alts (not all)', n >= cfg.image_alt_min && n <= cfg.image_alt_max, n + ' of ' + imgs.length + ' content image alts contain it.'); }

    const lim = cfg.section_density_max;
    secs.forEach(sc => {
      const sr = raw(clean(sc.md)); if (!sr.length) return;
      const sf = ft(sr), h = Math.max(count(sf, kt), core.length ? count(sf, core) : 0), p = h / sr.length * 100;
      rep.sections.push({ section: sc.sid, label: B.sectionLabel(pid, sc.sid), words: sr.length, hits: h, pct: +p.toFixed(2), flag: p > lim && sr.length >= 40 });
    });
    const overS = rep.sections.filter(x => x.flag).map(x => x.label);
    add('section_density', 'No section above ' + lim + '% keyword density', overS.length === 0, overS.length ? 'Over limit: ' + overS.join(', ') : 'All sections OK.');

    if (page.type === 'location') localChecks(pid, page, secs, body, rt, rep, sev);

    structureChecks(pid, page, secs, body, rep, sev);

    const sc = { pass: 1, info: 1, warn: 0.5, fail: 0 };
    rep.score = Math.round(rep.checks.reduce((a, c) => a + sc[c.status], 0) / rep.checks.length * 100);
    return rep;
  };
})();

