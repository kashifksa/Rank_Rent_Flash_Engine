const { execSync } = require('child_process');
const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const targetPos = result.indexOf('id="page-render-target"');
if (targetPos !== -1) {
  const content = result.substring(targetPos, targetPos + 25000);
  const sectionIds = content.match(/<section[^>]*id="([^"]*)"/g);
  console.log('All section IDs in page-render-target:');
  console.log(sectionIds);
}

