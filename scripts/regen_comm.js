const fs = require('fs');
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const commHtml = originalHtml.replace('loadSelectedPage("homepage");', 'loadSelectedPage("commercial-hvac-duct-cleaning");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section4.html', commHtml, 'utf-8');
console.log('Regenerated test_commercial_section4.html successfully!');

