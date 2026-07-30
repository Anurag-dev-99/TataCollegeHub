import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# find any subject with BBA in it
bba_papers = [p for p in data if "BBA" in p.get("subject", "").upper() or "BUSINESS ADMINISTRATION" in p.get("subject", "").upper()]

print(f"Found {len(bba_papers)} existing BBA papers.")
for p in bba_papers:
    print(p.get("subject"))
