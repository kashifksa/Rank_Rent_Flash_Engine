const { execSync } = require('child_process');
const fs = require('fs');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

// 1. Check Homepage
const cmdHp = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const resultHp = execSync(cmdHp, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStartHp = resultHp.indexOf('id="page-render-target"');
const targetEndHp = resultHp.indexOf('</main>', targetStartHp);
const pageHtmlHp = resultHp.substring(targetStartHp, targetEndHp);

console.log('=== HOMEPAGE SECTION 5 (PROCESS) ===');
console.log('proc-section in page:', pageHtmlHp.includes('proc-section'));
const headingHp = pageHtmlHp.match(/<h2 class="proc-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', headingHp ? headingHp[1].trim() : 'None');
const stepsHp = pageHtmlHp.match(/<h3 class="proc-title"[^>]*>([\s\S]*?)<\/h3>/g);
console.log('Steps count:', stepsHp ? stepsHp.length : 0);
if (stepsHp) {
  stepsHp.forEach((s, i) => console.log(`  Step 0${i+1}: ${s.replace(/<[^>]+>/g, '').trim()}`));
}

// 2. Check Commercial HVAC
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const commHtml = originalHtml.replace('loadSelectedPage("homepage");', 'loadSelectedPage("commercial-hvac-duct-cleaning");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section5.html', commHtml, 'utf-8');

const cmdComm = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section5.html"`;
const resultComm = execSync(cmdComm, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetStartComm = resultComm.indexOf('id="page-render-target"');
const targetEndComm = resultComm.indexOf('</main>', targetStartComm);
const pageHtmlComm = resultComm.substring(targetStartComm, targetEndComm);

console.log('\n=== COMMERCIAL HVAC SECTION 5 (PROCESS) ===');
console.log('proc-section in page:', pageHtmlComm.includes('proc-section'));
const headingComm = pageHtmlComm.match(/<h2 class="proc-heading"[^>]*>([\s\S]*?)<\/h2>/);
console.log('Heading:', headingComm ? headingComm[1].trim() : 'None');
const stepsComm = pageHtmlComm.match(/<h3 class="proc-title"[^>]*>([\s\S]*?)<\/h3>/g);
console.log('Steps count:', stepsComm ? stepsComm.length : 0);
if (stepsComm) {
  stepsComm.forEach((s, i) => console.log(`  Phase 0${i+1}: ${s.replace(/<[^>]+>/g, '').trim()}`));
}

