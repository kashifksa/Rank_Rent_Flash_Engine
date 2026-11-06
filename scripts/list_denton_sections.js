const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html', 'utf-8');

const regex = /<section[^>]*class="([^"]*)"[^>]*>/g;
let match;
while ((match = regex.exec(html)) !== null) {
  const snippet = html.substring(match.index, match.index + 300);
  const hMatch = snippet.match(/<h[2-3][^>]*>([\s\S]*?)<\/h[2-3]>/);
  console.log(`Class: ${match[1].padEnd(20)} | Heading: ${hMatch ? hMatch[1].replace(/<[^>]+>/g, '').trim() : 'None'}`);
}

