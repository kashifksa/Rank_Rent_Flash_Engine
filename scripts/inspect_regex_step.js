const fs = require('fs');
global.window = global;
const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

const bStart = html.indexOf('window.BUILDER_PAGES_DATA = {');
const bEnd = html.indexOf('</script>', bStart);
eval(html.substring(bStart, bEnd));

const rawSec = window.BUILDER_PAGES_DATA['homepage'].sections['services-grid | BLOCK: CS-02'];
const cleanMd = rawSec.replace(/<!--[\s\S]*?-->/g, '').trim();

// What is h3Regex in studio_builder.html?
const pStart = html.indexOf('function parseServicesFromContent(');
const pEnd = html.indexOf('// Render Canvas with Pure Hostinger', pStart);
const fnCode = html.substring(pStart, pEnd);

// Find h3Regex line in fnCode
const regexLine = fnCode.split('\n').find(l => l.includes('h3Regex'));
console.log("h3Regex line in studio_builder.html:");
console.log(regexLine);

eval(fnCode);
console.log("h3Regex test on cleanMd:", h3Regex.test(cleanMd));

