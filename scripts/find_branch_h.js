const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const pos = code.indexOf('// H. CUSTOMER REVIEWS');
const endPos = code.indexOf('// I. FAQ ACCORDION SECTION', pos);
console.log('Branch H from', pos, 'to', endPos);
console.log(code.substring(pos, endPos));

