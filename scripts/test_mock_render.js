global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

let currentActivePage = 'homepage';
let sectionVariants = {
  hero: "denton",
  intro: "denton",
  services: "cornerstone",
  why: "cornerstone",
  reviews: "cards"
};

// Test parseWhyUsFromContent
function parseWhyUsFromContent(rawSec, pageKey) {
  const defaultPillars = [
    {
      title: "Genuinely Local – Not a Call Center",
      desc: "Dispatched directly from Winnebago County. You speak directly with our local certified technicians—never an out-of-state call center."
    },
    {
      title: "NADCA Certified Source Removal",
      desc: "We adhere strictly to ACR-2021 source removal standards using 5,000 CFM negative air pressure and mechanical brush scouring."
    },
    {
      title: "No Surprise Bills – Ever",
      desc: "All estimates are approved in writing before work begins. Strictly zero hidden disposal fees, hookup charges, or bait-and-switch upsells."
    },
    {
      title: "We Treat Your Home Like Our Own",
      desc: "Protective drop cloths, clean indoor booties, and register magnetic seals protect your living space with zero interior blowback."
    }
  ];

  if (!rawSec) return { heading: "Why Rockford Property Owners Choose Us", items: defaultPillars };

  const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
  const lines = cleanMd.split(String.fromCharCode(10));
  let heading = "";
  const parsedItems = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!heading && line.startsWith("## ")) {
      heading = line.replace(/^##[ \t]+/, "").trim();
    }
    const bMatch = line.match(/^[-*][ \t]+\*\*([^*]+)\*\*[: \t]*(.*)$/);
    if (bMatch) {
      parsedItems.push({
        title: bMatch[1].replace(/:$/, "").trim(),
        desc: bMatch[2].trim()
      });
    }
  }

  if (parsedItems.length < 3) {
    return {
      heading: (heading && !heading.toLowerCase().includes("technical")) ? heading : "Why Rockford Property Owners Choose Us",
      items: defaultPillars
    };
  }

  return {
    heading: heading || "Why Rockford Property Owners Choose Us",
    items: parsedItems
  };
}

const pageData = window.BUILDER_PAGES_DATA[currentActivePage];
console.log('Testing all section keys for homepage:');
Object.keys(pageData.sections).forEach(key => {
  const rawSec = pageData.sections[key];
  if (key.includes('why-us') || key.includes('why_us') || key.includes('why-choose') || key.includes('why_choose')) {
    console.log('\n--- Section matched why-us: key =', key);
    const whyData = parseWhyUsFromContent(rawSec, currentActivePage);
    console.log('Heading:', whyData.heading);
    console.log('Items count:', whyData.items.length);
    whyData.items.forEach((it, idx) => {
      console.log(`  [${idx+1}] ${it.title}: ${it.desc.substring(0, 50)}...`);
    });
  }
});

