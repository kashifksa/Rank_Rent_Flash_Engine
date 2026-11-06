const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const url = "file:///D:/Projects/Rank_Rent_Flash_Engine/denton_site_dump.html";
const out = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section2_live.png";

// Capture taller screenshot or scroll to section 2
console.log("Capturing Section 2 of Denton site...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1440,2400 --virtual-time-budget=3000 --screenshot="${out}" "${url}"`);

if (fs.existsSync(out)) {
  console.log(`Success: Captured full height screenshot (${(fs.statSync(out).size / 1024).toFixed(1)} KB)`);
}

