const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const out = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section2_verified.png";

console.log("Capturing Section 2 verification screenshot...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,2200 --screenshot="${out}" "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

if (fs.existsSync(out)) {
  console.log(`Success! Screenshot captured: ${fs.statSync(out).size} bytes`);
} else {
  console.error("Screenshot file was not created.");
}

