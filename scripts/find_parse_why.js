const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const pos = code.indexOf('function parseWhyUsFromContent');
console.log('parseWhyUsFromContent at:', pos);
console.log(code.substring(pos, pos + 250));

