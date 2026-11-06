const fs = require('fs');

const builderData = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js', 'utf-8');
eval(builderData.replace('window.', 'global.'));

const hpSec = global.BUILDER_PAGES_DATA['homepage'].sections['services-grid | BLOCK: CS-02'];
console.log("Raw CS-02 length:", hpSec.length);
console.log("Ends with:\n", hpSec.substring(hpSec.length - 400));

