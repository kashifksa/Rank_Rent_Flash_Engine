global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

function parseProcessFromContent(rawSec) {
  if (!rawSec) return { heading: "Our 4-Step Cleaning Protocol", subhead: "", steps: [] };

  const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
  const lines = cleanMd.split(String.fromCharCode(10));
  let heading = "";
  let subhead = "";
  const steps = [];

  let currentStep = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    if (!heading && line.startsWith("## ")) {
      heading = line.replace(/^##[ \t]+/, "").trim();
      continue;
    }

    if (!subhead && !currentStep && !line.startsWith("#") && !line.startsWith("|") && !line.startsWith("-") && !line.startsWith("*") && !line.match(/^\d+\./)) {
      subhead = line;
      continue;
    }

    // A. Match table row: | **Phase X: Title** | Description | ...
    if (line.startsWith("|") && !line.includes("---")) {
      const cells = line.split("|").map(c => c.trim()).filter(Boolean);
      // Skip header row if it contains 'Phase' or 'Stage' in generic sense
      if (cells.length >= 2 && cells[0].toLowerCase().includes("phase") && !cells[0].includes("**") && !cells[0].match(/\d+/)) {
        continue; // table header
      }
      if (cells.length >= 2) {
        const titleRaw = cells[0].replace(/\*\*/g, "").trim();
        // Remove 'Phase 1: ' or similar prefix
        const cleanTitle = titleRaw.replace(/^(?:Phase|Stage|Step)\s*\d+:\s*/i, "").trim();
        steps.push({
          title: cleanTitle || titleRaw,
          desc: cells[1].trim(),
          window: cells[2] ? cells[2].trim() : ""
        });
        continue;
      }
    }

    // B. Match H3: ### 1. Title or ### Title
    const h3Match = line.match(/^###[ \t]+(?:\d+\.?\s*)?(.*)$/);
    if (h3Match) {
      if (currentStep) steps.push(currentStep);
      currentStep = {
        title: h3Match[1].replace(/^\d+\.\s*/, "").trim(),
        desc: ""
      };
      continue;
    }

    // C. Match numbered list: 1. **Title:** desc or 1. Title
    const numMatch = line.match(/^(\d+)\.\s+(?:\*\*([^*:]+):?\*\*)?\s*(.*)$/);
    if (numMatch && !line.startsWith("#")) {
      if (currentStep) steps.push(currentStep);
      currentStep = {
        title: numMatch[2] ? numMatch[2].trim() : `Step ${numMatch[1]}`,
        desc: numMatch[3] ? numMatch[3].trim() : ""
      };
      continue;
    }

    // Append to current step description
    if (currentStep) {
      if (!currentStep.desc) {
        currentStep.desc = line;
      } else {
        currentStep.desc += " " + line;
      }
    }
  }

  if (currentStep) steps.push(currentStep);

  return { heading: heading || "Our Step-by-Step Protocol", subhead, steps };
}

console.log('--- HOMEPAGE ---');
console.log(parseProcessFromContent(window.BUILDER_PAGES_DATA.homepage.sections['process | BLOCK: CS-04']));

console.log('\n--- COMMERCIAL ---');
console.log(parseProcessFromContent(window.BUILDER_PAGES_DATA['commercial-hvac-duct-cleaning'].sections['05_process']));

console.log('\n--- DRYER VENT ---');
console.log(parseProcessFromContent(window.BUILDER_PAGES_DATA['dryer-vent-cleaning-and-lint-removal'].sections['05_process']));

