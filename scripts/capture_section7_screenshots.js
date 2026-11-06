const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const outDir = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae";

// 1. Homepage Desktop View with Section 7 (1600x6000)
const outHp = `${outDir}\\denton_section7_desktop.png`;
console.log("Capturing Homepage Desktop with Section 7...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,6000 --virtual-time-budget=3000 --screenshot="${outHp}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 2. Mobile View with Section 7 (420x7200)
const outMob = `${outDir}\\denton_section7_mobile.png`;
console.log("Capturing Homepage Mobile with Section 7...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=420,7200 --virtual-time-budget=3000 --screenshot="${outMob}" "file:///D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 3. Eco Pure Archetype Live Token Test
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');
const ecoHtml = originalHtml.replace('setArchetype("industrial");', 'setArchetype("eco");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_eco_section7.html', ecoHtml, 'utf-8');

const outEco = `${outDir}\\denton_section7_eco_pure.png`;
console.log("Capturing Eco Pure Archetype Live Token Test...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,6000 --virtual-time-budget=3000 --screenshot="${outEco}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_eco_section7.html"`);

console.log("\n--- SECTION 7 CAPTURE RESULTS ---");
console.log("Homepage Desktop:", fs.statSync(outHp).size, "bytes");
console.log("Homepage Mobile:", fs.statSync(outMob).size, "bytes");
console.log("Eco Pure Archetype:", fs.statSync(outEco).size, "bytes");
console.log("All Section 7 captures completed successfully!");

