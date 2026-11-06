import os

script_path = r'D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v4.py'

with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """    document.addEventListener("DOMContentLoaded", () => {
      if (window.BUILDER_PAGES_DATA) {
        for (const [pid, pdata] of Object.entries(window.BUILDER_PAGES_DATA)) {
          pageSectionOrder[pid] = Object.keys(pdata.sections);
          sectionVisibility[pid] = {};
          pageSectionOrder[pid].forEach(k => { sectionVisibility[pid][k] = true; });
        }
      }

      setArchetype("industrial");
      loadSelectedPage("homepage");
    });"""

replacement = """    function initBuilder() {
      if (window.BUILDER_PAGES_DATA) {
        for (const [pid, pdata] of Object.entries(window.BUILDER_PAGES_DATA)) {
          pageSectionOrder[pid] = Object.keys(pdata.sections);
          sectionVisibility[pid] = {};
          pageSectionOrder[pid].forEach(k => { sectionVisibility[pid][k] = true; });
        }
      }

      setArchetype("industrial");
      loadSelectedPage("homepage");
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", initBuilder);
    } else {
      initBuilder();
    }"""

if target in code:
    code = code.replace(target, replacement)
    print("Updated initBuilder pattern successfully!")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(code)
else:
    print("Target not found!")

