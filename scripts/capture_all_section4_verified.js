const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const outDir = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae";

// 1. Homepage Desktop View with Section 4
const outHp = `${outDir}\\denton_section4_desktop.png`;
console.log("Capturing Homepage Desktop with Section 4...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,3800 --virtual-time-budget=3000 --screenshot="${outHp}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 2. Mobile View with Section 4 (420x4500)
const outMob = `${outDir}\\denton_section4_mobile.png`;
console.log("Capturing Homepage Mobile with Section 4...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=420,4500 --virtual-time-budget=3000 --screenshot="${outMob}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 3. Commercial HVAC Page with Section 4 Dynamic 5 Pillars
const outComm = `${outDir}\\denton_section4_commercial.png`;
console.log("Capturing Commercial HVAC with Section 4...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,3800 --virtual-time-budget=3000 --screenshot="${outComm}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section4.html"`);

// 4. Eco Pure Archetype Live Token Test
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const ecoHtml = originalHtml.replace('setArchetype("industrial");', 'setArchetype("eco");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_eco_section4.html', ecoHtml, 'utf-8');

const outEco = `${outDir}\\denton_section4_eco_pure.png`;
console.log("Capturing Eco Pure Archetype Live Token Test...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,3800 --virtual-time-budget=3000 --screenshot="${outEco}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_eco_section4.html"`);

console.log("\n--- VERIFICATION SIZES ---");
console.log("Homepage Desktop:", fs.statSync(outHp).size, "bytes");
console.log("Homepage Mobile:", fs.statSync(outMob).size, "bytes");
console.log("Commercial HVAC:", fs.statSync(outComm).size, "bytes");
console.log("Eco Pure Archetype:", fs.statSync(outEco).size, "bytes");
console.log("All screenshots verified successfully!");

