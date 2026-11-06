const { execSync } = require('child_process');
const fs = require('fs');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmdHp = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const resultHp = execSync(cmdHp, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStartHp = resultHp.indexOf('id="page-render-target"');
const targetEndHp = resultHp.indexOf('</main>', targetStartHp);
const pageHtmlHp = resultHp.substring(targetStartHp, targetEndHp);

console.log('=== HOMEPAGE SECTION 8 (SERVICE AREA & MAP) ===');
console.log('aws-section in page:', pageHtmlHp.includes('aws-section'));
const headingHp = pageHtmlHp.match(/<h2 class="aws-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', headingHp ? headingHp[1].trim() : 'None');
console.log('Has map iframe:', pageHtmlHp.includes('<iframe'));
const cardsHp = pageHtmlHp.match(/<div class="aws-card[\s\S]*?<\/div>/g);
console.log('Location cards count:', cardsHp ? cardsHp.length : 0);

const citiesHp = pageHtmlHp.match(/<h3 class="aws-card__city"[^>]*>([\s\S]*?)<\/h3>/g);
if (citiesHp) {
  citiesHp.forEach((c, i) => console.log(`  City ${i+1}: ${c.replace(/<[^>]+>/g, '').trim()}`));
}

