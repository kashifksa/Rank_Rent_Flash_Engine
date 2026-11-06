const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const faqMatches = [ ...html.matchAll(/class="[^"]*faq[^"]*"/gi) ].map(m => m.index);
console.log('FAQ matches:', faqMatches);

if (faqMatches.length > 0) {
  const p = faqMatches[0];
  console.log('FAQ snippet:');
  console.log(html.substring(p - 150, p + 1500));
}

const ctaMatches = [ ...html.matchAll(/class="[^"]*cta[^"]*"/gi) ].map(m => m.index);
console.log('CTA matches:', ctaMatches);
if (ctaMatches.length > 0) {
  const p = ctaMatches[ctaMatches.length - 1]; // bottom CTA
  console.log('CTA snippet:');
  console.log(html.substring(p - 150, p + 1500));
}

