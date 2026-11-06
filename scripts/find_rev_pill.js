const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const regex = /reviews/gi;
let match;
while ((match = regex.exec(code)) !== null) {
  if (code.substring(match.index - 50, match.index + 50).includes('variation-pill') || code.substring(match.index - 50, match.index + 50).includes('form-group')) {
    console.log('Found sidebar reviews at:', match.index);
    console.log(code.substring(match.index - 100, match.index + 350));
    break;
  }
}

