import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for p in data:
    if p.get("subject") == "Digital India":
        print(f"  Renaming: {p.get('id')} -> Digital Education")
        p["subject"] = "Digital Education"
        count += 1

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nRenamed {count} entries from 'Digital India' to 'Digital Education'")
