const { execSync } = require('child_process');

try {
  execSync('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=2000 --window-size=500,12000 --screenshot="D:\\Projects\\Rank_Rent_Flash_Engine\\full_mobile_all.png" "file:///D:/Projects/Rank_Rent_Flash_Engine/master_template_sample.html"');
  console.log('Mobile screenshot saved successfully');
} catch (err) {
  console.error('Error taking mobile screenshot:', err);
}
