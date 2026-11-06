const { execSync } = require('child_process');
const fs = require('fs');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

// 1. Check Homepage
const cmdHp = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const resultHp = execSync(cmdHp, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStartHp = resultHp.indexOf('id="page-render-target"');
const targetEndHp = resultHp.indexOf('</main>', targetStartHp);
const pageHtmlHp = resultHp.substring(targetStartHp, targetEndHp);

console.log('=== HOMEPAGE SECTION 6 (REVIEWS) ===');
console.log('test-section in page:', pageHtmlHp.includes('test-section'));
const headingHp = pageHtmlHp.match(/<h2 class="test-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', headingHp ? headingHp[1].trim() : 'None');
const cardsHp = pageHtmlHp.match(/<article class="test-card">([\s\S]*?)<\/article>/g);
console.log('Reviews count:', cardsHp ? cardsHp.length : 0);

const authorsHp = pageHtmlHp.match(/<span class="test-author-name"[^>]*>([\s\S]*?)<\/span>/g);
if (authorsHp) {
  authorsHp.forEach((a, i) => console.log(`  Review ${i+1}: Author = ${a.replace(/<[^>]+>/g, '').trim()}`));
}

// 2. Check Commercial HVAC
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const commHtml = originalHtml.replace('loadSelectedPage("homepage");', 'loadSelectedPage("commercial-hvac-duct-cleaning");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section6.html', commHtml, 'utf-8');

const cmdComm = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section6.html"`;
const resultComm = execSync(cmdComm, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStartComm = resultComm.indexOf('id="page-render-target"');
const targetEndComm = resultComm.indexOf('</main>', targetStartComm);
const pageHtmlComm = resultComm.substring(targetStartComm, targetEndComm);

console.log('\n=== COMMERCIAL HVAC SECTION 6 (REVIEWS) ===');
console.log('test-section in page:', pageHtmlComm.includes('test-section'));
const headingComm = pageHtmlComm.match(/<h2 class="test-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', headingComm ? headingComm[1].trim() : 'None');
const cardsComm = pageHtmlComm.match(/<article class="test-card">([\s\S]*?)<\/article>/g);
console.log('Reviews count:', cardsComm ? cardsComm.length : 0);
const authorsComm = pageHtmlComm.match(/<span class="test-author-name"[^>]*>([\s\S]*?)<\/span>/g);
if (authorsComm) {
  authorsComm.forEach((a, i) => console.log(`  Review ${i+1}: Author = ${a.replace(/<[^>]+>/g, '').trim()}`));
}

