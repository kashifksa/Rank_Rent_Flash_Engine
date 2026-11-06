const { execSync } = require('child_process');

try {
  execSync('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=2000 --window-size=1200,9000 --screenshot="D:\\Projects\\Rank_Rent_Flash_Engine\\full_desktop_all.png" "file:///D:/Projects/Rank_Rent_Flash_Engine/master_template_sample.html"');
  console.log('Desktop screenshot saved successfully');
} catch (err) {
  console.error('Error taking desktop screenshot:', err);
}
