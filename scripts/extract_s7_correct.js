const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const posStyle = html.indexOf('<style>.comp-section');
console.log('posStyle:', posStyle);

const secStart = html.indexOf('<section class="comp-section"', posStyle);
console.log('secStart:', secStart);

const secEnd = html.indexOf('</section>', secStart);
console.log('secEnd:', secEnd);

const compFull = html.substring(posStyle, secEnd + 10);
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_section7_extracted.html', compFull, 'utf-8');
console.log('Saved Section 7 extracted HTML (length: ' + compFull.length + ')');

