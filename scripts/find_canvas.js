const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
console.log('canvas match:', html.match(/id=["']canvas["'][^>]*>/));
console.log('preview match:', html.match(/id=["']preview[^"']*["'][^>]*>/));

