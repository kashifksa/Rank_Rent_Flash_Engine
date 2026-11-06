const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const regex = /service-area|service_area|map/gi;
let match;
while ((match = regex.exec(code)) !== null) {
  if (code.substring(match.index - 50, match.index + 50).includes('else if') || code.substring(match.index - 50, match.index + 50).includes('includes(')) {
    console.log('Found service-area branch at:', match.index);
    console.log(code.substring(match.index - 50, match.index + 350));
    break;
  }
}

