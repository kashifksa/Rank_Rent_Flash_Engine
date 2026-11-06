global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

function parseComparisonFromContent(rawSec) {
  const defaultData = {
    heading: "The Quality Standard of Care: Comparison Benchmark",
    subhead: "Before hiring an air duct cleaning contractor in Rockford, examine how certified full-system decontamination compares against discount coupon companies and DIY attempts.",
    headers: ["Inspection & Cleaning Factor", "Rockford Air Duct Pros", "Budget Forty-Nine Dollar Coupon Vans", "DIY Shop-Vac Attempt"],
    rows: [
      {
        feature: "Vacuum Airflow Capacity",
        pro: "5,000 CFM Sealed Negative Air",
        other: "Portable 150 CFM Shop-Vac",
        diy: "Under 100 CFM Standard Vacuum"
      },
      {
        feature: "Mechanical Brush Agitation",
        pro: "360-Degree Rotary Motorized Scrubbing",
        other: "Compressed Air Wand Only",
        diy: "Manual Hand Brush Near Register Grille"
      },
      {
        feature: "Technician Accreditation",
        pro: "NADCA ASCS Certified Technicians",
        other: "Uncertified Subcontractors",
        diy: "Uncertified Homeowner"
      },
      {
        feature: "Live Video Verification",
        pro: "High-Definition Borescope Before & After",
        other: "Refuse to Show Duct Interior",
        diy: "Limited Flashlight View Only"
      },
      {
        feature: "Pricing Transparency",
        pro: "Upfront Flat-Rate Quotes with Zero Surcharges",
        other: "Low Bait-and-Switch Rate with High Upsells",
        diy: "Tool Rental Costs & Damaged Duct Vents"
      }
    ]
  };

  if (!rawSec) return defaultData;

  const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
  const lines = cleanMd.split(String.fromCharCode(10));
  let heading = "";
  let subhead = "";
  const tableLines = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    if (!heading && line.startsWith("## ")) {
      heading = line.replace(/^##[ \t]+/, "").trim();
      continue;
    }

    if (!subhead && !line.startsWith("#") && !line.startsWith("|")) {
      subhead = line;
      continue;
    }

    if (line.startsWith("|")) {
      tableLines.push(line);
    }
  }

  if (tableLines.length < 3) return defaultData;

  // Parse table headers
  const headerCells = tableLines[0].split("|").map(c => c.trim()).filter(Boolean);
  const rows = [];

  for (let i = 2; i < tableLines.length; i++) {
    const cells = tableLines[i].split("|").map(c => c.trim()).filter(Boolean);
    if (cells.length >= 2) {
      rows.push({
        feature: cells[0],
        pro: cells[1] || "",
        other: cells[2] || "",
        diy: cells[3] || ""
      });
    }
  }

  return {
    heading: heading || defaultData.heading,
    subhead: subhead || defaultData.subhead,
    headers: headerCells.length >= 3 ? headerCells : defaultData.headers,
    rows: rows.length > 0 ? rows : defaultData.rows
  };
}

console.log('=== HOMEPAGE COMPARISON PARSED ===');
const homeComp = window.BUILDER_PAGES_DATA.homepage.sections['comparison-table | BLOCK: CS-17'];
console.log(JSON.stringify(parseComparisonFromContent(homeComp), null, 2));

