global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

const commProof = window.BUILDER_PAGES_DATA['commercial-hvac-duct-cleaning'].sections['06_local_proof'];
console.log('=== Commercial 06_local_proof ===');
console.log(commProof);

const dryerProof = window.BUILDER_PAGES_DATA['dryer-vent-cleaning-and-lint-removal'].sections['06_local_proof'];
console.log('\n=== Dryer 06_local_proof ===');
console.log(dryerProof);

