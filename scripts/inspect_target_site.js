const { execSync } = require('child_process');
const fs = require('fs');

const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const targetUrl = "https://pink-sardine-824660.hostingersite.com/";
const outDesktop = "D:\\Projects\\Rank_Rent_Flash_Engine\\target_site_desktop.png";
const outMobile = "D:\\Projects\\Rank_Rent_Flash_Engine\\target_site_mobile.png";
const outHtml = "D:\\Projects\\Rank_Rent_Flash_Engine\\target_site_dump.html";

console.log("Fetching target site screenshot and DOM...");

try {
  // 1. Desktop screenshot
  execSync(`"${chromePath}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=6000 --window-size=1440,2400 --screenshot="${outDesktop}" "${targetUrl}"`, { stdio: 'inherit' });
  console.log("Desktop screenshot captured:", outDesktop);

  // 2. Mobile screenshot
  execSync(`"${chromePath}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=6000 --window-size=390,1800 --screenshot="${outMobile}" "${targetUrl}"`, { stdio: 'inherit' });
  console.log("Mobile screenshot captured:", outMobile);

  // 3. Dump DOM
  execSync(`"${chromePath}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=6000 --dump-dom "${targetUrl}" > "${outHtml}"`, { stdio: 'inherit' });
  console.log("DOM dumped to:", outHtml);
} catch (err) {
  console.error("Error fetching target site:", err.message);
}

