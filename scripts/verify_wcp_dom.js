const { execSync } = require('child_process');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const wcpIdx = result.indexOf('class="wcp-section"');
console.log('wcp-section in live rendered DOM:', wcpIdx !== -1);
if (wcpIdx !== -1) {
  console.log('\n--- Rendered HTML snippet ---');
  console.log(result.substring(wcpIdx, wcpIdx + 600));
}

const wcpCards = result.match(/class="wcp-card"/g);
console.log('\nwcp-cards rendered count:', wcpCards ? wcpCards.length : 0);

const titles = result.match(/<h3 class="wcp-title"[^>]*>([\s\S]*?)<\/h3>/g);
console.log('\nwcp-titles rendered:', titles);

