const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const pos = html.indexOf('.test-section');
console.log(html.substring(pos + 1700, pos + 3200));

