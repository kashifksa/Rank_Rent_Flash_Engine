const { execSync } = require('child_process');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const result = execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --dump-dom "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`, { maxBuffer: 10 * 1024 * 1024 }).toString();

const svcIdx = result.indexOf('svc-');
console.log("svc- index:", svcIdx);
if (svcIdx !== -1) {
  console.log("Found svc- at:", svcIdx);
  console.log(result.substring(svcIdx - 100, svcIdx + 600));
}

const h2Matches = result.match(/<h2[^>]*>.*?<\/h2>/g);
console.log("\nAll H2s rendered in page:", h2Matches);

