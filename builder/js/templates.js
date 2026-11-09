/* templates.js : a template = theme tokens + default layout variant per block type. Add a new template = add one object. */
(function () {
  const B = (window.Builder = window.Builder || {});
  B.FONTS = {
    technical: { h: 'Montserrat', b: 'Inter', label: 'Industrial Tech (Montserrat + Inter)', q: 'family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600;700' },
    trade: { h: 'Oswald', b: 'Roboto', label: 'Rugged Trade (Oswald + Roboto)', q: 'family=Oswald:wght@500;600;700&family=Roboto:wght@400;500;700' },
    modern: { h: 'Poppins', b: 'Open Sans', label: 'Friendly Modern (Poppins + Open Sans)', q: 'family=Poppins:wght@600;700;800&family=Open+Sans:wght@400;600;700' },
    editorial: { h: 'Plus Jakarta Sans', b: 'Inter', label: 'Architectural Clean (Plus Jakarta Sans + Inter)', q: 'family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700' }
  };
  B.TEMPLATES = {
    cornerstone: {
      name: 'Cornerstone ProFlow', badge: 'Full-bleed authority',
      desc: 'Full-bleed photo hero, icon cards, timeline process, two-column FAQ, boxed CTA.',
      theme: { primary: '#121315', accent: '#fd761a', font: 'technical', radius: 8, density: 'balanced' },
      variants: { hero: 'full', split: 'image-right', cards: 'icons', steps: 'timeline', reviews: 'cards', faq: 'two-col', cta: 'box', gallery: 'cards', badges: 'grid', area: 'map', table: 'cmp' },
      motion: { anim: 'rise', fx: 'airflow' },
      header: 'classic', skin: ''
    },
    keystone: {
      name: 'Keystone Classic', badge: 'Kadence split',
      desc: 'Split hero with photo, plain card grid, table process, accordion FAQ, full-width CTA band.',
      theme: { primary: '#0a2540', accent: '#0066cc', font: 'modern', radius: 6, density: 'balanced' },
      variants: { hero: 'split', split: 'image-left', cards: 'grid', steps: 'table', reviews: 'cards', faq: 'accordion', cta: 'band', gallery: 'slider', badges: 'grid', area: 'map', table: 'cmp' },
      motion: { anim: 'fade', fx: 'none' },
      header: 'topbar', skin: ''
    },
    industrial: {
      name: 'Modern Industrial', badge: 'Stitch palette',
      desc: 'Stitch-style palette and type: centered dark hero, list cards, timeline, featured review, boxed CTA.',
      theme: { primary: '#131b2e', accent: '#d95d0f', font: 'editorial', radius: 12, density: 'spacious' },
      variants: { hero: 'centered', split: 'image-right', cards: 'list', steps: 'timeline', reviews: 'featured', faq: 'accordion', cta: 'box', gallery: 'cards', badges: 'grid', area: 'map', table: 'cmp' },
      motion: { anim: 'stagger', fx: 'blueprint' },
      header: 'dark', skin: ''
    },
    bold: {
      name: 'Bold Trade', badge: 'Rugged high-contrast',
      desc: 'Dark header, uppercase condensed headings, square corners, amber accent bars, angled full-bleed hero, hard-shadow cards.',
      theme: { primary: '#111418', accent: '#f5a400', font: 'trade', radius: 2, density: 'balanced' },
      variants: { hero: 'full', split: 'image-left', cards: 'grid', steps: 'timeline', reviews: 'cards', faq: 'two-col', cta: 'band', gallery: 'cards', badges: 'grid', area: 'map', table: 'cmp' },
      motion: { anim: 'slide-left', fx: 'none' },
      header: 'dark', skin: 'bold'
    },
    clean: {
      name: 'Clean Local', badge: 'Friendly light',
      desc: 'Info top bar, split hero with soft glow, large rounded cards, tinted sections, pill buttons, featured review, accordion FAQ.',
      theme: { primary: '#10343a', accent: '#0b7d6a', font: 'modern', radius: 18, density: 'spacious' },
      variants: { hero: 'split', split: 'image-right', cards: 'icons', steps: 'timeline', reviews: 'featured', faq: 'accordion', cta: 'box', gallery: 'cards', badges: 'grid', area: 'map', table: 'cmp' },
      motion: { anim: 'rise', fx: 'none' },
      header: 'topbar', skin: 'clean'
    }
  };
  B.DENSITY = { compact: 52, balanced: 76, spacious: 100 };
})();

