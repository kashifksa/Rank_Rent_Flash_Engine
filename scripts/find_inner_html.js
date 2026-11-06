const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const matches = html.match(/[a-zA-Z0-9_$.]+\.innerHTML\s*=/g);
console.log('innerHTML targets:', matches);

