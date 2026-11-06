const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

const s3Start = 252591;
console.log('Script 3 content:');
console.log(html.substring(s3Start));

