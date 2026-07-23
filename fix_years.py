import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for item in data:
    if item["id"].endswith("-2025") or item["id"].endswith("-2025-set1"):
        if item["year"] == "2024-2028":
            item["year"] = "2025-2029"
            count += 1
            print(f"  Fixed: {item['id']} -> 2025-2029")

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nTotal fixed: {count} papers")
