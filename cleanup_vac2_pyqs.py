import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# The old entries have year "2022"
filtered_data = []
removed_count = 0

for item in data:
    if item.get("category") == "VAC" and item.get("subject") == "Global Citizenship Education for Sustainable Development":
        if item.get("year") == "2022":
            removed_count += 1
            print(f"Removing old entry: {item.get('title')}")
            continue
    
    filtered_data.append(item)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=4, ensure_ascii=False)

print(f"Removed {removed_count} old entries. Total remaining: {len(filtered_data)}")
