const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_process_readable.html', 'utf-8');

const h2 = html.match(/<h2[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', h2 ? h2[1].trim() : 'None');

// Check steps
const steps = html.match(/<strong>\d+\.[^<]*<\/strong>/g);
console.log('Steps found:', steps);

// Look for images or background styles
const imgMatches = html.match(/<img[^>]*>/g);
console.log('Images in process section:', imgMatches);

// Check column layout
const colMatches = html.match(/kadence-column[0-9a-f_-]*/g);
console.log('Kadence columns:', colMatches);
