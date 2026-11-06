const { execSync } = require('child_process');
const fs = require('fs');

const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const studioUrl = "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html";
const outStudio = "D:\\Projects\\Rank_Rent_Flash_Engine\\studio_builder_hostinger_view.png";

console.log("Capturing high-resolution Studio Builder screenshot...");
execSync(`"${chromePath}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=3000 --window-size=1440,1100 --screenshot="${outStudio}" "${studioUrl}"`, { stdio: 'inherit' });

if (fs.existsSync(outStudio)) {
  console.log(`Studio screenshot created: ${outStudio} (${(fs.statSync(outStudio).size / 1024).toFixed(1)} KB)`);
}

// Copy to brain artifacts
const artifactPath = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\e26b9a46-bbd1-46f0-883b-32cef80bb7bd\\studio_builder_hostinger_view.png";
fs.copyFileSync(outStudio, artifactPath);
console.log(`Copied screenshot to artifacts: ${artifactPath}`);

