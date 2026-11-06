const fs = require('fs');
const code = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/generate_studio_builder_v4.py', 'utf-8');

const sIdx = code.indexOf('Section 4: Why Choose Us');
console.log('Section 4 in code:', sIdx !== -1);
console.log(code.substring(sIdx - 50, sIdx + 450));

