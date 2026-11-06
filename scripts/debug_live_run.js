const { execSync } = require('child_process');
const fs = require('fs');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
let html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// Inject error logger at the very top of head
const errLogger = `
  <script>
    window.builderLogs = [];
    window.onerror = function(msg, url, line, col, err) {
      window.builderLogs.push('ERROR: ' + msg + ' at line ' + line);
      document.title = 'ERROR: ' + msg + ' at line ' + line;
    };
    console.log = function(...args) { window.builderLogs.push('LOG: ' + args.join(' ')); };
    console.error = function(...args) { window.builderLogs.push('ERR: ' + args.join(' ')); };
  </script>
`;

html = html.replace('<head>', '<head>' + errLogger);

// Also after loadSelectedPage, set document.title to result
html = html.replace('loadSelectedPage("homepage");', `
  try {
    loadSelectedPage("homepage");
    const target = document.getElementById('page-render-target');
    document.title = 'RENDERED: ' + (target ? target.children.length : 'NO_TARGET') + ' children | wcp: ' + (target ? target.innerHTML.includes('wcp-section') : false);
  } catch(e) {
    document.title = 'EXCEPTION: ' + e.message;
  }
`);

fs.writeFileSync('D:/Projects/Rank_Rent_Flash_Engine/test_debug_builder.html', html, 'utf-8');

const cmd = `"${chrome}" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=4000 --dump-dom "file:///D:/Projects/Rank_Rent_Flash_Engine/test_debug_builder.html"`;
const result = execSync(cmd, { maxBuffer: 10 * 1024 * 1024 }).toString();

const titleMatch = result.match(/<title>([\s\S]*?)<\/title>/);
console.log('Document title after run:', titleMatch ? titleMatch[1] : 'No title');

const targetPos = result.indexOf('id="page-render-target"');
if (targetPos !== -1) {
  const content = result.substring(targetPos, targetPos + 1000);
  console.log('Target content:', content.substring(0, 300));
}

