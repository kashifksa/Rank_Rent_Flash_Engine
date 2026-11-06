const fs = require('fs');
global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

const hp = window.BUILDER_PAGES_DATA.homepage;
console.log('Homepage section keys:');
Object.keys(hp.sections).forEach(k => {
  console.log('  -', k);
  if (k.includes('why-us') || k.includes('why_us') || k.includes('why-choose') || k.includes('why_choose')) {
    console.log('    --> MATCHES Section 4 why branch!');
  }
});

