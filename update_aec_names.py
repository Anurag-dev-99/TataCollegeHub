import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\aec.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

regional_languages = ["bengali", "ho", "kharia", "khortha", "kurmali", "kurukh", "mundari", "nagpuri", "santali", "urdu"]

updated_count = 0
for item in data:
    if any(lang in item.get("id", "") for lang in regional_languages):
        if "(Ranchi Univ.)" not in item["name"]:
            item["name"] = f"{item['name']} (Ranchi Univ.)"
            updated_count += 1

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Updated {updated_count} entries in aec.json")
