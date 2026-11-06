global.window = global;
require('D:/Projects/Rank_Rent_Flash_Engine/scripts/builder_data.js');

function parseReviewsFromContent(rawSec) {
  const defaultReviews = [
    {
      author: "Marcus T.",
      loc: "Verified Homeowner • Loves Park (Forest Hills)",
      initials: "MT",
      quote: "After purchasing our 1970s ranch home in Loves Park, the dust blowing through registers was unbearable. They showed us endoscope video before and after. The difference was night and day, and our furnace runs noticeably quieter."
    },
    {
      author: "Sarah and David K.",
      loc: "Verified Homeowners • Rockford (Edgebrook)",
      initials: "SK",
      quote: "We got caught two years ago by a forty-nine dollar coupon company that blew dust into our master bedroom. These technicians brought real truck-mounted 5,000 CFM negative air equipment and sealed every register. Honest flat rate honored."
    },
    {
      author: "Elena R.",
      loc: "Verified Homeowner • Machesney Park",
      initials: "ER",
      quote: "Called early in the morning after noticing a musty odor whenever the air conditioner cycled on. They had a certified two-man crew at our home by early afternoon. The botanical spray smelled natural and clean."
    }
  ];

  if (!rawSec) return { heading: "What Winnebago County Homeowners Say", subhead: "Authentic reviews from verified local property owners.", reviews: defaultReviews };

  const cleanMd = rawSec.replace(/<!--[^]*?-->/g, "").trim();
  const lines = cleanMd.split(String.fromCharCode(10));
  let heading = "";
  let subhead = "";
  const parsedReviews = [];

  let curRev = null;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    if (!heading && line.startsWith("## ")) {
      heading = line.replace(/^##[ \t]+/, "").trim();
      continue;
    }

    if (!subhead && !curRev && !line.startsWith("#") && !line.startsWith(">") && !line.startsWith("-") && !line.startsWith("*")) {
      subhead = line;
      continue;
    }

    // A. Match Blockquote reviews: > "Quote text..." followed by > - Author, Location
    if (line.startsWith(">")) {
      const bqText = line.replace(/^>[ \t]*/, "").trim();
      if (bqText.includes("★")) continue; // Star rating line
      if (bqText.startsWith("-") || bqText.startsWith("—")) {
        // Author line
        if (curRev) {
          const authRaw = bqText.replace(/^[-—][ \t]*/, "").trim();
          const parts = authRaw.split(",");
          curRev.author = parts[0].trim();
          curRev.loc = parts.length > 1 ? parts.slice(1).join(",").trim() : "Verified Customer";
          const nameParts = curRev.author.split(/\s+/).filter(Boolean);
          if (nameParts.length >= 2) {
            curRev.initials = (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase();
          } else if (nameParts.length === 1) {
            curRev.initials = nameParts[0].substring(0, 2).toUpperCase();
          }
          parsedReviews.push(curRev);
          curRev = null;
        }
        continue;
      }
      // It is a quote
      if (!curRev) {
        curRev = {
          quote: bqText.replace(/^["“]|["”]$/g, "").trim(),
          author: "",
          loc: "",
          initials: ""
        };
      } else {
        curRev.quote += " " + bqText.replace(/^["“]|["”]$/g, "").trim();
      }
      continue;
    }

    // B. Match H3 reviews: ### Location or Author
    if (line.startsWith("### ")) {
      if (curRev && curRev.quote) parsedReviews.push(curRev);
      const locOrName = line.replace(/^###[ \t]+/, "").trim();
      curRev = {
        loc: locOrName,
        author: "",
        initials: "",
        quote: ""
      };
      continue;
    }

    if (line.toLowerCase().startsWith("rating:")) {
      continue;
    }

    if (line.toLowerCase().startsWith("reviewer:")) {
      if (curRev) {
        const fullReviewer = line.replace(/^reviewer:\s*/i, "").trim();
        const parts = fullReviewer.split(",");
        curRev.author = parts[0].trim();
        if (parts.length > 1) {
          curRev.loc = parts.slice(1).join(",").trim() + (curRev.loc ? " • " + curRev.loc : "");
        }
        const nameParts = curRev.author.split(/\s+/).filter(Boolean);
        if (nameParts.length >= 2) {
          curRev.initials = (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase();
        } else if (nameParts.length === 1) {
          curRev.initials = nameParts[0].substring(0, 2).toUpperCase();
        }
      }
      continue;
    }

    // Append to quote
    if (curRev) {
      if (!curRev.quote) {
        curRev.quote = line;
      } else {
        curRev.quote += " " + line;
      }
    }
  }

  if (curRev && curRev.quote) parsedReviews.push(curRev);

  parsedReviews.forEach(r => {
    if (!r.author) {
      r.author = r.loc || "Verified Customer";
      r.loc = "Verified Customer";
    }
    if (!r.initials) {
      const parts = r.author.split(/\s+/).filter(Boolean);
      r.initials = parts.length >= 2 ? (parts[0][0] + parts[1][0]).toUpperCase() : r.author.substring(0, 2).toUpperCase();
    }
  });

  return {
    heading: heading || "What Property Owners Say",
    subhead: subhead || "Authentic customer reviews from verified local service calls.",
    reviews: parsedReviews.length > 0 ? parsedReviews : defaultReviews
  };
}

console.log('=== COMMERCIAL REVIEWS PARSED ===');
const commProof = window.BUILDER_PAGES_DATA['commercial-hvac-duct-cleaning'].sections['06_local_proof'];
console.log(JSON.stringify(parseReviewsFromContent(commProof), null, 2));

console.log('\n=== DRYER REVIEWS PARSED ===');
const dryerProof = window.BUILDER_PAGES_DATA['dryer-vent-cleaning-and-lint-removal'].sections['06_local_proof'];
console.log(JSON.stringify(parseReviewsFromContent(dryerProof), null, 2));

console.log('\n=== LOVES PARK REVIEWS PARSED ===');
const lovesProof = window.BUILDER_PAGES_DATA['air-duct-cleaning-loves-park-il'].sections['04_local_proof'];
console.log(JSON.stringify(parseReviewsFromContent(lovesProof), null, 2));

