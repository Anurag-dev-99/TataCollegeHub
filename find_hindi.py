import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    if item.get("category") == "AEC" and "Hindi" in item.get("subject", ""):
        print(f"ID: {item['id']} | Title: {item['title']} | Year: {item.get('year')} | URL: {item.get('downloadUrl')}")
