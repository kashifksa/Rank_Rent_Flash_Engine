const { execSync } = require('child_process');
const fs = require('fs');

const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const localUrl = "file:///D:/Projects/Rank_Rent_Flash_Engine/build/homepage_industrial_hostinger.html";
const outImg = "D:\\Projects\\Rank_Rent_Flash_Engine\\exported_hostinger_mobile_screenshot.png";
const artifactPath = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\e26b9a46-bbd1-46f0-883b-32cef80bb7bd\\exported_hostinger_mobile_screenshot.png";

console.log("Capturing mobile rendered page screenshot...");
execSync(`"${chromePath}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --window-size=390,1800 --screenshot="${outImg}" "${localUrl}"`, { stdio: 'inherit' });

if (fs.existsSync(outImg)) {
  fs.copyFileSync(outImg, artifactPath);
  console.log(`[PASS] Saved mobile screenshot: ${artifactPath} (${(fs.statSync(outImg).size / 1024).toFixed(1)} KB)`);
} else {
  console.error("[FAIL] Mobile screenshot failed");
}

