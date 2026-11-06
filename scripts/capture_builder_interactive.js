const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const url = "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html";
const out = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\builder_interactive_features_updated.png";

console.log("Capturing Studio Builder with updated interactive feature controls...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1440,900 --virtual-time-budget=2500 --screenshot="${out}" "${url}"`);

if (fs.existsSync(out)) {
  console.log(`Success: Captured screenshot: ${out} (${(fs.statSync(out).size / 1024).toFixed(1)} KB)`);
} else {
  console.error("Failed to capture screenshot.");
}

