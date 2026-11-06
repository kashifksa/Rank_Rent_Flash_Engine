const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// 1. Homepage Dynamic Services (Exact 3 Cards)
const outHp = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section3_dynamic_3cards.png";
console.log("Capturing Homepage Dynamic 3-Card Services Grid screenshot...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,2800 --screenshot="${outHp}" "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`);

// 2. Location Page Dynamic Services (Exact 4 Cards)
const locSnippet = `<script>
  window.addEventListener('DOMContentLoaded', () => {
    loadSelectedPage('air-duct-cleaning-loves-park-il');
  });
</script></body>`;
// Replace the LAST occurrence of </body>
const lastBodyIdx = originalHtml.lastIndexOf('</body>');
const locHtml = originalHtml.substring(0, lastBodyIdx) + locSnippet + originalHtml.substring(lastBodyIdx + 7);
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_loc_dynamic.html', locHtml, 'utf-8');

const outLoc = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\denton_section3_dynamic_location.png";
console.log("Capturing Location Page Dynamic Services Grid screenshot...");
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1600,2800 --screenshot="${outLoc}" "D:/Projects/Rank_Rent_Flash_Engine/test_loc_dynamic.html"`);

console.log("Homepage screenshot size:", fs.statSync(outHp).size);
console.log("Location screenshot size:", fs.statSync(outLoc).size);
console.log("Captures completed successfully!");

