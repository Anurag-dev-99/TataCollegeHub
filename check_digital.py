import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

digital_papers = [p for p in data if "DIGITAL" in p.get("subject", "").upper()]

print(f"Found {len(digital_papers)} existing Digital papers.")
for p in digital_papers:
    print(p.get("subject"), "-", p.get("category"))
