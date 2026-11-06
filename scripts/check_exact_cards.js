const { execSync } = require('child_process');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStart = result.indexOf('id="page-render-target"');
const targetEnd = result.indexOf('</main>', targetStart);
const pageHtml = result.substring(targetStart, targetEnd);

console.log('--- EXACT CARDS INSIDE page-render-target ---');
const cards = pageHtml.match(/<div class="wcp-card">([\s\S]*?)<\/div>/g);
console.log('Cards count:', cards ? cards.length : 0);

const titles = pageHtml.match(/<h3 class="wcp-title"[^>]*>([\s\S]*?)<\/h3>/g);
titles.forEach(t => console.log('  *', t.replace(/<[^>]+>/g, '').trim()));

