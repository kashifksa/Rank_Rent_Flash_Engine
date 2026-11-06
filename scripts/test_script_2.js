const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

const s2Start = 173022 + 8;
const s2End = html.indexOf('</script>', s2Start);
const code = html.substring(s2Start, s2End);

console.log('Script 2 length:', code.length);

try {
  new Function(code);
  console.log('Script 2 syntax is VALID!');
} catch (e) {
  console.error('Script 2 SYNTAX ERROR:', e.message);
  console.error(e.stack);
}

