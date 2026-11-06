const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const pos = html.indexOf('.aws-section');
console.log(html.substring(pos + 2400, pos + 5000));

