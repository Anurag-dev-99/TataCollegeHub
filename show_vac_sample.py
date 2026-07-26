import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Show a sample VAC entry
for item in data:
    if item.get("category") == "VAC":
        import json as j
        with open("sample_vac.txt", "w", encoding="utf-8") as f:
            f.write(j.dumps(item, indent=4, ensure_ascii=False))
        break
