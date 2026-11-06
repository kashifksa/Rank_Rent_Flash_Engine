const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const pStart = html.indexOf('id="process"');
console.log('pStart:', pStart);
const pEnd = html.indexOf('Why Denton Sprinkler Systems Break More Often Than You Think', pStart);
console.log('pEnd:', pEnd);

const raw = html.substring(pStart - 100, pEnd);

// Let's strip out messy attributes for readability
const clean = raw
  .replace(/data-kb-block="[^"]*"/g, '')
  .replace(/class="[^"]*wp-block-kadence-[^"]*"/g, '')
  .replace(/<div class="kt-inside-inner-col">/g, '<div>')
  .replace(/<div class="kt-row-column-wrap[^"]*">/g, '<div class="row">')
  .replace(/<div class="wp-block-kadence-column[^"]*">/g, '<div class="col">');

fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_process_readable.html', raw, 'utf-8');
console.log('Saved readable process block (length: ' + raw.length + ')');

