const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

const regex = /<script\b[^>]*>/gi;
let match;
while ((match = regex.exec(html)) !== null) {
  console.log('Found script tag at index:', match.index);
  console.log(html.substring(match.index, match.index + 120));
}
