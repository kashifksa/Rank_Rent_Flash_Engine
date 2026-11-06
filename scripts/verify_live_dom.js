const { execSync } = require('child_process');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetPos = result.indexOf('id="page-render-target"');
console.log('page-render-target found:', targetPos !== -1);
if (targetPos !== -1) {
  const content = result.substring(targetPos, targetPos + 10000);
  console.log('wcp-section in page-render-target:', content.includes('wcp-section'));
  console.log('wcp-card count in page-render-target:', (content.match(/wcp-card/g) || []).length);
  const titles = content.match(/<h3 class="wcp-title"[^>]*>([\s\S]*?)<\/h3>/g);
  console.log('Titles in page-render-target:', titles);
}

