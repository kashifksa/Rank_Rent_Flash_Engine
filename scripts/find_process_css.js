const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const regex = /#process[^{]*\{[^}]*\}/g;
const matches = html.match(regex);
console.log('Matches for #process:', matches);

// Also search for classes attached to #process or parent row
const pIdx = html.indexOf('id="process"');
console.log('pIdx context:');
console.log(html.substring(pIdx - 150, pIdx + 300));

