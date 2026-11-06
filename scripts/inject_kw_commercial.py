path = r"D:\Projects\Rank_Rent_Flash_Engine\page_content_commercial-hvac-duct-cleaning.md"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_str = "Facility managers throughout Winnebago County rely on our specialized commercial ventilation services to resolve indoor air quality challenges and maintain regulatory compliance."
new_str = "When contracting for commercial hvac duct cleaning rockford il facility managers rely on our specialized commercial ventilation services to resolve indoor air quality challenges and maintain regulatory compliance."

if old_str in text:
    text = text.replace(old_str, new_str)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Injected second occurrence successfully")
else:
    print("Target string not found")

