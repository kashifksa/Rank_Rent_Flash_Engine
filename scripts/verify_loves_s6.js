const { execSync } = require('child_process');
const fs = require('fs');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const lpHtml = originalHtml.replace('loadSelectedPage("homepage");', 'loadSelectedPage("air-duct-cleaning-loves-park-il");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_loves_section6.html', lpHtml, 'utf-8');

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/test_loves_section6.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStart = result.indexOf('id="page-render-target"');
const targetEnd = result.indexOf('</main>', targetStart);
const pageHtml = result.substring(targetStart, targetEnd);

console.log('=== LOVES PARK SECTION 6 (REVIEWS) ===');
console.log('test-section in page:', pageHtml.includes('test-section'));
const heading = pageHtml.match(/<h2 class="test-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', heading ? heading[1].trim() : 'None');
const cards = pageHtml.match(/<article class="test-card">([\s\S]*?)<\/article>/g);
console.log('Reviews count:', cards ? cards.length : 0);
const authors = pageHtml.match(/<span class="test-author-name"[^>]*>([\s\S]*?)<\/span>/g);
if (authors) {
  authors.forEach((a, i) => console.log(`  Review ${i+1}: Author = ${a.replace(/<[^>]+>/g, '').trim()}`));
}

