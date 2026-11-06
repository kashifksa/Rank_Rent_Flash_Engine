const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const pos = code.indexOf('// E. STEP-BY-STEP PROCESS SECTION');
const endPos = code.indexOf('// F. PREMIUM COMPARISON TABLE', pos);
console.log('Branch E from', pos, 'to', endPos);
console.log(code.substring(pos, endPos));

