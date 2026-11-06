const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_section5_extracted.html', 'utf-8');

const p1 = html.indexOf('How ProFlow Handles Your Sprinkler Repair in Denton');
const p2 = html.indexOf('Why Denton Sprinkler Systems Break More Often Than You Think');

console.log('p1:', p1, 'p2:', p2);
const sectionHtml = html.substring(p1 - 100, p2);
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/denton_section5_clean.html', sectionHtml, 'utf-8');
console.log('Saved clean section 5 HTML (length: ' + sectionHtml.length + ')');

