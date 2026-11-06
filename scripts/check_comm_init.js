const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section4.html', 'utf-8');
console.log('Has commercial in init:', html.includes('commercial-hvac-duct-cleaning'));
const pos = html.indexOf('function initBuilder()');
console.log(html.substring(pos, pos + 400));

