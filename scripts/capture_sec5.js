const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const originalHtml = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// Inject script to scroll to sec-process
const testScript = `
<script>
window.addEventListener('load', () => {
  setTimeout(() => {
    scrollToSection('process');
  }, 500);
});
</script>
`;

const modified = originalHtml.replace('</body>', testScript + '</body>');
fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/demo_sec5.html', modified, 'utf-8');

const out = "C:\\Users\\Kashif\\.gemini\\antigravity\\brain\\652a7bff-4272-4ea9-a998-2015a13c31ae\\section_5_process_view.png";
execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --window-size=1440,1050 --virtual-time-budget=2000 --screenshot="${out}" "file:///D:/Projects/Rank_Rent_Flash_Engine/demo_sec5.html"`);

fs.unlinkSync('D:/Projects/Rank_Rent_Flash_Engine/demo_sec5.html');
console.log("Section 5 screenshot captured!");

