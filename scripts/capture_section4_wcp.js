const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const outDir = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae";

// 1. Homepage Desktop View with Section 4 (1600x3800 to capture Sections 1-4)
const outHp = `${outDir}\\denton_section4_desktop.png`;
console.log("Capturing Homepage Desktop with Section 4...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,3800 --virtual-time-budget=3000 --screenshot="${outHp}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 2. Mobile View with Section 4 (420x4500)
const outMob = `${outDir}\\denton_section4_mobile.png`;
console.log("Capturing Homepage Mobile with Section 4...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=420,4500 --virtual-time-budget=3000 --screenshot="${outMob}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 3. Commercial HVAC Page with Section 4 Dynamic Pillars
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const commHtml = originalHtml.replace('loadSelectedPage("homepage");', 'loadSelectedPage("commercial-hvac-duct-cleaning");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section4.html', commHtml, 'utf-8');

const outComm = `${outDir}\\denton_section4_commercial.png`;
console.log("Capturing Commercial HVAC with Section 4...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,3800 --virtual-time-budget=3000 --screenshot="${outComm}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section4.html"`);

console.log("Desktop screenshot size:", fs.statSync(outHp).size);
console.log("Mobile screenshot size:", fs.statSync(outMob).size);
console.log("Commercial screenshot size:", fs.statSync(outComm).size);
console.log("All Section 4 screenshots captured successfully!");
