const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const pos = code.indexOf('// F. PREMIUM COMPARISON TABLE');
const endPos = code.indexOf('// G. BEFORE & AFTER SECTION', pos);
console.log('Branch F from', pos, 'to', endPos);
console.log(code.substring(pos, endPos));

