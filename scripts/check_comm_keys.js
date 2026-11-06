global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

const comm = window.BUILDER_PAGES_DATA['commercial-hvac-duct-cleaning'];
console.log('Commercial section keys:');
Object.keys(comm.sections).forEach(k => console.log('  -', k));

