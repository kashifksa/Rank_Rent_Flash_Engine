path = r"D:\Projects\Rank_Rent_Flash_Engine\scripts\generate_studio_builder_v2.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_render = """    function renderCurrentPage() {
      const pageData = window.BUILDER_PAGES_DATA[currentActivePage];
      if (!pageData) return;"""

new_render = """    function renderCurrentPage() {
      if (!currentActivePage || !window.BUILDER_PAGES_DATA || !window.BUILDER_PAGES_DATA[currentActivePage] || !pageSectionOrder[currentActivePage]) return;
      const pageData = window.BUILDER_PAGES_DATA[currentActivePage];"""

old_dom = """    window.addEventListener('DOMContentLoaded', () => {
      setArchetype('industrial');
      loadSelectedPage('homepage');"""

new_dom = """    window.addEventListener('DOMContentLoaded', () => {
      loadSelectedPage('homepage');
      setArchetype('industrial');"""

if old_render in text and old_dom in text:
    text = text.replace(old_render, new_render).replace(old_dom, new_dom)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully patched generate_studio_builder_v2.py")
else:
    print("Patterns not matched")

