const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const outDir = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae";

// 1. Homepage Desktop View with Section 5 (1600x4400)
const outHp = `${outDir}\\denton_section5_desktop.png`;
console.log("Capturing Homepage Desktop with Section 5...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,4400 --virtual-time-budget=3000 --screenshot="${outHp}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 2. Mobile View with Section 5 (420x5200)
const outMob = `${outDir}\\denton_section5_mobile.png`;
console.log("Capturing Homepage Mobile with Section 5...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=420,5200 --virtual-time-budget=3000 --screenshot="${outMob}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 3. Commercial HVAC with Section 5 (1600x4400)
const outComm = `${outDir}\\denton_section5_commercial.png`;
console.log("Capturing Commercial HVAC with Section 5...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,4400 --virtual-time-budget=3000 --screenshot="${outComm}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_commercial_section5.html"`);

// 4. Eco Pure Archetype Live Token Test
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const ecoHtml = originalHtml.replace('setArchetype("industrial");', 'setArchetype("eco");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_eco_section5.html', ecoHtml, 'utf-8');

const outEco = `${outDir}\\denton_section5_eco_pure.png`;
console.log("Capturing Eco Pure Archetype Live Token Test...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,4400 --virtual-time-budget=3000 --screenshot="${outEco}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_eco_section5.html"`);

console.log("\n--- SECTION 5 CAPTURE RESULTS ---");
console.log("Homepage Desktop:", fs.statSync(outHp).size, "bytes");
console.log("Homepage Mobile:", fs.statSync(outMob).size, "bytes");
console.log("Commercial HVAC:", fs.statSync(outComm).size, "bytes");
console.log("Eco Pure Archetype:", fs.statSync(outEco).size, "bytes");
console.log("All Section 5 captures completed successfully!");

