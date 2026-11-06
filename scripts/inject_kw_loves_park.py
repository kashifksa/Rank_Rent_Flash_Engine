path = r"D:\Projects\Rank_Rent_Flash_Engine\page_content_air-duct-cleaning-loves-park-il.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace in snippet zone
old1 = "Professional air duct cleaning in Loves Park, IL delivers certified ventilation remediation for residential homeowners across Winnebago County."
new1 = "When searching for professional air duct cleaning loves park il homeowners turn to [Rockford Air Duct Pros](/) for certified ventilation remediation across Winnebago County."

# Replace in section 3 intro
old2 = "Loves Park homeowners rely on our comprehensive suite of residential air quality solutions, engineered to eliminate airborne contaminants from central heating and cooling networks."
new2 = "Providing premier air duct cleaning loves park il residents trust, our technicians eliminate stubborn contaminants from central heating and cooling networks with commercial-grade equipment."

if old1 in text and old2 in text:
    text = text.replace(old1, new1).replace(old2, new2)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Injected exact keyword occurrences successfully")
else:
    print("Target strings not found")

