const { execSync } = require('child_process');

const chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const result = execSync(`"${chrome}" --headless=new --no-sandbox --disable-gpu --dump-dom "D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html"`, { maxBuffer: 10 * 1024 * 1024 }).toString();

const cardMatches = result.match(/class="svc-card"/g);
console.log("Total svc-card occurrences in entire page:", cardMatches ? cardMatches.length : 0);

// Print the titles of all rendered cards
const titles = result.match(/class="svc-card__title"[^>]*>([^<]+)<\/h3>/g);
console.log("Card titles found:", titles);

