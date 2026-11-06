const { execSync } = require('child_process');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section4.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStart = result.indexOf('id="page-render-target"');
const targetEnd = result.indexOf('</main>', targetStart);
const pageHtml = result.substring(targetStart, targetEnd);

console.log('--- COMMERCIAL HVAC EXACT CARDS ---');
const heading = pageHtml.match(/<h2 class="wcp-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', heading ? heading[1].trim() : 'None');

const titles = pageHtml.match(/<h3 class="wcp-title"[^>]*>([\s\S]*?)<\/h3>/g);
console.log('Cards count:', titles ? titles.length : 0);
if (titles) {
  titles.forEach(t => console.log('  *', t.replace(/<[^>]+>/g, '').trim()));
}

