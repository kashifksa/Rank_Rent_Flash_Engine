global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

for (const p of Object.keys(window.BUILDER_PAGES_DATA)) {
  const pKeys = Object.keys(window.BUILDER_PAGES_DATA[p].sections);
  const procKey = pKeys.find(k => k.includes('process') || k.includes('step'));
  console.log(`Page: ${p.padEnd(42)} -> Process Key: ${procKey}`);
}

