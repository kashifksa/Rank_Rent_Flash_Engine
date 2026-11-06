const { execSync } = require('child_process');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const result = execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --dump-dom "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`, { maxBuffer: 10 * 1024 * 1024 }).toString();

const svcSecIdx = result.indexOf('class="svc-section"');
if (svcSecIdx !== -1) {
  const endSecIdx = result.indexOf('</section>', svcSecIdx);
  console.log("svc-section found! Content:");
  console.log(result.substring(svcSecIdx, endSecIdx + 10));
} else {
  console.log("svc-section not found in rendered DOM!");
}

