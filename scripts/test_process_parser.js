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

    if (!subhead && !currentStep && !line.startsWith("#") && !line.startsWith("-") && !line.startsWith("*") && !line.match(/^\d+\./)) {
      subhead = line;
      continue;
    }

    // Match H3: ### 1. Title or ### Title
    const h3Match = line.match(/^###[ \t]+(?:\d+\.?\s*)?(.*)$/);
    if (h3Match) {
      if (currentStep) steps.push(currentStep);
      currentStep = {
        title: h3Match[1].replace(/^\d+\.\s*/, "").trim(),
        desc: ""
      };
      continue;
    }

    // Match numbered list: 1. **Title:** desc or 1. Title
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

  return { heading: heading || "Our 4-Step Process", subhead, steps };
}

console.log('--- HOMEPAGE PROCESS ---');
const homeProc = window.BUILDER_PAGES_DATA.homepage.sections['process | BLOCK: CS-04'];
console.log(parseProcessFromContent(homeProc));

console.log('\n--- COMMERCIAL HVAC PROCESS ---');
const commProc = window.BUILDER_PAGES_DATA['commercial-hvac-duct-cleaning'].sections['05_process'];
console.log(parseProcessFromContent(commProc));

console.log('\n--- DRYER VENT PROCESS ---');
const dryerProc = window.BUILDER_PAGES_DATA['dryer-vent-cleaning-and-lint-removal'].sections['05_process'];
console.log(parseProcessFromContent(dryerProc));

