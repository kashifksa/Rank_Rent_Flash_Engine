const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// 1. Commercial Service Page Test
const serviceHtml = originalHtml.replace('loadSelectedPage("homepage");', 'loadSelectedPage("commercial-hvac-duct-cleaning");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_service.html', serviceHtml, 'utf-8');

const serviceOut = "C:\\Users\\Kashif\\.gemini\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\builder_service_hero_verified.png";
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1500,1100 --virtual-time-budget=2500 --screenshot="${serviceOut}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_service.html"`);
console.log("Service page screenshot captured:", fs.existsSync(serviceOut));

// 2. Blog Post Test
const blogHtml = originalHtml.replace('loadSelectedPage("homepage");', 'loadSelectedPage("how-to-spot-air-duct-cleaning-scams");');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_blog.html', blogHtml, 'utf-8');

const blogOut = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\builder_blog_editorial_verified.png";
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1500,1100 --virtual-time-budget=2500 --screenshot="${blogOut}" "file:///D:/Projects/Rank_Rent_Flash_Engine/test_blog.html"`);
console.log("Blog page screenshot captured:", fs.existsSync(blogOut));

// Cleanup temp files
if (fs.existsSync('D:/Projects/Rank_Rent_Flash_Engine/test_service.html')) fs.unlinkSync('D:/Projects/Rank_Rent_Flash_Engine/test_service.html');
if (fs.existsSync('D:/Projects/Rank_Rent_Flash_Engine/test_blog.html')) fs.unlinkSync('D:/Projects/Rank_Rent_Flash_Engine/test_blog.html');

