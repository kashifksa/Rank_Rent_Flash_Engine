const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const outDesktop = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section3_desktop.png";
const outMobile = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section3_mobile.png";

console.log("Capturing Section 3 Desktop screenshot (1600x3200)...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,3200 --screenshot="${outDesktop}" "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

console.log("Capturing Section 3 Mobile screenshot (420x2400)...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=420,2400 --screenshot="${outMobile}" "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

console.log("Desktop size:", fs.statSync(outDesktop).size);
console.log("Mobile size:", fs.statSync(outMobile).size);
console.log("Both Section 3 captures completed successfully!");

