const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const pos1 = code.indexOf('let sectionVariants = {');
console.log(code.substring(pos1, pos1 + 200));

const pos2 = code.indexOf('function setSectionVariant(');
console.log(code.substring(pos2, pos2 + 400));

