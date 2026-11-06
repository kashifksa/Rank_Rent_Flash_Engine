const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const pos = html.indexOf('function loadSelectedPage(pageId)');
console.log(html.substring(pos, pos + 600));

