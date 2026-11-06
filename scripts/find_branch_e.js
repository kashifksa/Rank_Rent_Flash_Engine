const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const pos = code.indexOf('// E. STEP-BY-STEP PROCESS SECTION');
console.log(code.substring(pos, pos + 1200));

