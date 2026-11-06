const { execSync } = require('child_process');
const fs = require('fs');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmdHp = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const resultHp = execSync(cmdHp, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStartHp = resultHp.indexOf('id="page-render-target"');
const targetEndHp = resultHp.indexOf('</main>', targetStartHp);
const pageHtmlHp = resultHp.substring(targetStartHp, targetEndHp);

console.log('=== HOMEPAGE SECTION 7 (COMPARISON TABLE) ===');
console.log('comp-section in page:', pageHtmlHp.includes('comp-section'));
const headingHp = pageHtmlHp.match(/<h2 class="comp-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', headingHp ? headingHp[1].trim() : 'None');
const rowsHp = pageHtmlHp.match(/<tr>[\s\S]*?<\/tr>/g);
console.log('Table rows count:', rowsHp ? rowsHp.length : 0);

const features = pageHtmlHp.match(/<td class="cell-feature"[^>]*>([\s\S]*?)<\/td>/g);
if (features) {
  features.forEach((f, i) => console.log(`  Row ${i+1}: Feature = ${f.replace(/<[^>]+>/g, '').trim()}`));
}

