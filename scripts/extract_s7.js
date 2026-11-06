const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const posStart = html.indexOf('.comp-section');
console.log('posStart of .comp-section:', posStart);

// Let's find the closing of this section
const secStart = html.lastIndexOf('<section class="comp-section"', posStart + 2000);
console.log('secStart:', secStart);

const secEnd = html.indexOf('</section>', secStart);
console.log('secEnd:', secEnd);

const compFull = html.substring(posStart - 100, secEnd + 10);
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_section7_extracted.html', compFull, 'utf-8');
console.log('Saved Section 7 extracted HTML (length: ' + compFull.length + ')');

