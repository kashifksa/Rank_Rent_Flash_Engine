const fs = require('fs');
const md = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/page_content_homepage.md', 'utf-8');

const pos = md.indexOf('## The Quality Standard of Care: Comparison Benchmark');
console.log(md.substring(pos, pos + 1400));

