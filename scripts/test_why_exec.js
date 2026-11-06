const fs = require('fs');
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// Extract the script
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/i);
if (!scriptMatch) {
  console.log('No script found');
  process.exit(1);
}

// Set up fake DOM environment
const jsdom = require('jsdom');
// If jsdom is not installed, let's check or do mock window
console.log('Script length:', scriptMatch[1].length);

