import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find all unique categories
categories = set(item.get("category") for item in data)
output = "Categories: " + str(categories) + "\n\n"

# Check if any IKS entries exist
iks_entries = [item for item in data if "iks" in item.get("id","").lower() or "indian knowledge" in item.get("subject","").lower() or "iks" in item.get("subject","").lower()]
output += f"IKS entries found: {len(iks_entries)}\n"
for i in iks_entries:
    output += f"  {i['id']} | {i['title']}\n"

with open("iks_check.txt", "w", encoding="utf-8") as f:
    f.write(output)
