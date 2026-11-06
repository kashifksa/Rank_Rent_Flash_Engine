const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_section6_extracted.html', 'utf-8');

const styleMatches = html.match(/<style>([\s\S]*?)<\/style>/g);
console.log('Styles count:', styleMatches ? styleMatches.length : 0);
if (styleMatches) {
  styleMatches.forEach((s, i) => {
    console.log(`\n=== STYLE ${i} ===`);
    console.log(s.replace(/<\/?style>/g, '').substring(0, 1500));
  });
}

const sectionMatch = html.match(/<section[^>]*>([\s\S]*?)<\/section>/);
if (sectionMatch) {
  console.log('\n=== SECTION HTML (snippet) ===');
  console.log(sectionMatch[0].substring(0, 1200));
}

