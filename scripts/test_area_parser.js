global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

function parseServiceAreaFromContent(rawSec) {
  const defaultData = {
    heading: "Greater Rockford Service Area and Dispatch Coverage",
    subhead: "Our fleet of specialized negative-air decontamination vehicles is staged daily across Winnebago and Boone counties for prompt same-day and next-day dispatch.",
    primaryCity: {
      name: "Rockford",
      tag: "Winnebago County • Primary Service Hub",
      desc: "Central, East Side, North End, and Midtown. Rapid same-day decontamination with zero travel surcharges.",
      postal: "61101, 61102, 61103, 61104, 61107, 61108, 61109, 61114"
    },
    cities: [
      {
        name: "Loves Park",
        tag: "Winnebago County • Active Service Zone",
        desc: "Forest Hills, Riverside Corridor, and Windsor Road. Under 35-minute mobile dispatch.",
        slug: "air-duct-cleaning-loves-park-il",
        color: "color-green"
      },
      {
        name: "Machesney Park",
        tag: "Winnebago County • Expansion Zone",
        desc: "Harlem Corridor, 173 Commercial Strip, and residential sub-divisions. Fast same-day service.",
        slug: null,
        color: "color-yellow"
      },
      {
        name: "Belvidere",
        tag: "Boone County • Regional Coverage",
        desc: "State Street Corridor, Chrysler plant vicinity, and outlying Boone County homes.",
        slug: null,
        color: "color-purple"
      },
      {
        name: "Cherry Valley",
        tag: "Winnebago County • Rapid Dispatch",
        desc: "Harrison Ave, Perryville Corridor, and Valley Woods residential communities.",
        slug: null,
        color: "color-teal"
      }
    ],
    nap: {
      name: "Rockford Air Duct Pros",
      address: "1111 S Alpine Rd, Rockford, IL 61108",
      phone: "(815) 555-0142",
      hours: "Monday – Saturday: 7:00 AM – 7:00 PM"
    }
  };

  if (!rawSec) return defaultData;

  const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
  const lines = cleanMd.split(String.fromCharCode(10));
  let heading = "";
  let subhead = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    if (!heading && line.startsWith("## ")) {
      heading = line.replace(/^##[ \t]+/, "").trim();
      continue;
    }

    if (!subhead && !line.startsWith("#") && !line.startsWith("*") && !line.startsWith("-")) {
      subhead = line;
      break;
    }
  }

  return {
    heading: heading || defaultData.heading,
    subhead: subhead || defaultData.subhead,
    primaryCity: defaultData.primaryCity,
    cities: defaultData.cities,
    nap: defaultData.nap
  };
}

console.log('=== HOMEPAGE SERVICE AREA PARSED ===');
const homeAreaSec = window.BUILDER_PAGES_DATA.homepage.sections['service-area | BLOCK: CS-11'];
console.log(JSON.stringify(parseServiceAreaFromContent(homeAreaSec), null, 2));

