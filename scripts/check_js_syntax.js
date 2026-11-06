const fs = require('fs');

const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// Extract the main script
const scriptStart = html.lastIndexOf('<script>');
const scriptEnd = html.lastIndexOf('</script>');
const scriptCode = html.substring(scriptStart + 8, scriptEnd);

console.log("Script length:", scriptCode.length);

try {
  // Try evaluating the syntax with new Function
  new Function(scriptCode);
  console.log("Syntax is valid!");
} catch (e) {
  console.error("Syntax Error found!");
  console.error(e.message);
  console.error(e.stack);
}

