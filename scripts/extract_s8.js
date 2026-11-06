const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const posStyle = html.indexOf('<style>.aws-section');
console.log('posStyle of .aws-section:', posStyle);

const secStart = html.indexOf('<section class="aws-section"', posStyle);
console.log('secStart:', secStart);

const secEnd = html.indexOf('</section>', secStart);
console.log('secEnd:', secEnd);

const awsFull = html.substring(posStyle, secEnd + 10);
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_section8_extracted.html', awsFull, 'utf-8');
console.log('Saved Section 8 extracted HTML (length: ' + awsFull.length + ')');

