const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// 1. Homepage Dynamic Services (Exact 3 Cards)
const outHp = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section3_synced_3cards.png";
console.log("Capturing Homepage 3-Card Services Grid screenshot...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,2800 --screenshot="${outHp}" "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 2. Location Page Dynamic Services (Exact 4 Cards)
const target = 'loadSelectedPage("homepage");';
const replacement = 'loadSelectedPage("air-duct-cleaning-loves-park-il");';
const locHtml = originalHtml.replace(target, replacement);
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_loves_park_synced.html', locHtml, 'utf-8');

const outLoc = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section3_synced_location_4cards.png";
console.log("Capturing Loves Park 4-Card Services Grid screenshot...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,3000 --screenshot="${outLoc}" "D:/Projects/Rank_Rent_Flash_Engine/test_loves_park_synced.html"`);

console.log("Homepage 3-Card size:", fs.statSync(outHp).size);
console.log("Location 4-Card size:", fs.statSync(outLoc).size);
console.log("Both screenshots captured successfully!");

