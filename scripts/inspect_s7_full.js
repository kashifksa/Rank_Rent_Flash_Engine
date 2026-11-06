const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_section7_extracted.html', 'utf-8');

const styleEnd = html.indexOf('</style>');
console.log('=== CSS STYLES ===');
console.log(html.substring(0, styleEnd + 8));

console.log('\n=== SECTION HTML ===');
console.log(html.substring(html.indexOf('<section')));

