const fs = require('fs');
const md = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/page_content_commercial-hvac-duct-cleaning.md', 'utf-8');

const matches = md.split('\n').filter(l => l.startsWith('## ') && (l.toLowerCase().includes('say') || l.toLowerCase().includes('review') || l.toLowerCase().includes('client')));
console.log('Commercial reviews headings:', matches);

