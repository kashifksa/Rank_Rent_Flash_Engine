const fs = require('fs');

const html = fs.readFileSync('D:/Projects/Rank_Rent_Flash_Engine/studio_builder.html', 'utf-8');

// Check that our new functions and attributes are present in the HTML
console.log('Checking HTML for interactive feature elements...');

const checks = [
  { name: 'feat-radar checkbox with handleFeatureRowClick', pattern: /id="feat-radar"[^>]*onchange="toggleFeature\('radar'/ },
  { name: 'feat-winner checkbox with handleFeatureRowClick', pattern: /id="feat-winner"[^>]*onchange="toggleFeature\('winner'/ },
  { name: 'feat-pulse checkbox with handleFeatureRowClick', pattern: /id="feat-pulse"[^>]*onchange="toggleFeature\('pulse'/ },
  { name: 'feat-mobile checkbox with handleFeatureRowClick', pattern: /id="feat-mobile"[^>]*onchange="toggleFeature\('mobileBar'/ },
  { name: 'handleFeatureRowClick function defined', pattern: /function handleFeatureRowClick\(/ },
  { name: 'toggleFeature with auto-scroll dispatch', pattern: /if\s*\(feature === 'radar'\)\s*\{\s*scrollToSection\('radar'\);/ },
  { name: 'scrollToSection supports radar', pattern: /k === 'radar' \|\| k\.includes\('radar'\)/ },
  { name: 'scrollToSection supports winner', pattern: /k === 'winner' \|\| k\.includes\('winner'\)/ },
  { name: 'scrollToSection supports pulse', pattern: /k === 'pulse' \|\| k\.includes\('pulse'\)/ },
  { name: 'scrollToSection supports mobilebar', pattern: /k === 'mobilebar' \|\| k === 'mobile'/ },
  { name: 'feature-radar-beacon ID in generator', pattern: /id="feature-radar-beacon"/ },
  { name: 'comp-winner-ribbon ID in comparison table', pattern: /id="comp-winner-ribbon"/ },
  { name: 'mobile-call-bar ID in mobile bar', pattern: /id="mobile-call-bar"/ },
  { name: 'pulseClass applied to c-cta-btn-primary', pattern: /class="c-cta-btn-primary \$\{pulseClass\}"/ }
];

let allPassed = true;
checks.forEach((c, idx) => {
  const passed = c.pattern.test(html);
  console.log(`[${passed ? 'PASS' : 'FAIL'}] Check ${idx + 1}: ${c.name}`);
  if (!passed) allPassed = false;
});

if (allPassed) {
  console.log('\n>>> ALL 14 HTML CHECKS PASSED PERFECTLY! <<<');
} else {
  console.error('\n>>> SOME CHECKS FAILED! <<<');
  process.exit(1);
}

