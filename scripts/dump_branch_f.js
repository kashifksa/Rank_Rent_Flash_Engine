const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const pos1 = code.indexOf('// F. PREMIUM COMPARISON TABLE');
const pos2 = code.indexOf('// G. BEFORE & AFTER SECTION');
console.log('pos1:', pos1, 'pos2:', pos2);
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/old_branch_f.txt', code.substring(pos1, pos2), 'utf-8');
console.log('Wrote old_branch_f.txt, length:', pos2 - pos1);

