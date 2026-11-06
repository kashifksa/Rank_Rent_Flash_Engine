const fs = require('fs');
const md = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/page_content_dryer-vent-cleaning-and-lint-removal.md', 'utf-8');

const matches = md.split('\n').filter(l => l.startsWith('## ') && (l.toLowerCase().includes('say') || l.toLowerCase().includes('review') || l.toLowerCase().includes('client') || l.toLowerCase().includes('customer')));
console.log('Dryer reviews headings:', matches);

