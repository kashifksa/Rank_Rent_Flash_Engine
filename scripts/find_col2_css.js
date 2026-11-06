const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const regex = /\.kadence-column53_c2a037-4b[^{]*\{[^}]*\}/g;
const matches = html.match(regex);
console.log('CSS for column 2:', matches);

// Also search for id53_741617-4a
const rowCss = html.match(/\.kb-row-layout-id53_741617-4a[^{]*\{[^}]*\}/g);
console.log('CSS for row layout:', rowCss);

