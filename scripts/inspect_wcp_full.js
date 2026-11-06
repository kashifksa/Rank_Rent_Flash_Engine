const { execSync } = require('child_process');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetPos = result.indexOf('id="page-render-target"');
const content = result.substring(targetPos);

console.log('wcp-section inside rendered page:', content.includes('wcp-section'));
console.log('wcp-card count:', (content.match(/class="wcp-card"/g) || []).length);
const titles = content.match(/<h3 class="wcp-title"[^>]*>([\s\S]*?)<\/h3>/g);
console.log('\nwcp-titles rendered:');
if (titles) {
  titles.forEach(t => console.log('  -', t.replace(/<[^>]+>/g, '').trim()));
}

const headingMatch = content.match(/<h2 class="wcp-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('\nwcp-heading:', headingMatch ? headingMatch[1].trim() : 'Not found');

