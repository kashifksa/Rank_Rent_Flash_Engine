const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const url = "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html";
const out = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\e26b9a46-bbd1-46f0-883b-32cef80bb7bd\\builder_live_verified.png";

console.log("Taking screenshot...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1440,1100 --virtual-time-budget=2000 --screenshot="${out}" "${url}"`);

if (fs.existsSync(out)) {
  console.log(`Screenshot saved successfully: ${out} (${(fs.statSync(out).size / 1024).toFixed(1)} KB)`);
} else {
  console.error("Failed to capture screenshot.");
}
