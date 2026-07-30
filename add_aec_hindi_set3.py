import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entry = {
    "id": "pyq-aec-hindi-sem1-2025-set3",
    "title": "AEC-1 Hindi 2025 (Set 3)",
    "year": "2025-2029",
    "set": "Set 3",
    "semester": 1,
    "category": "AEC",
    "subject": "Hindi",
    "downloadUrl": "https://drive.google.com/file/d/1SMCxspPqFqjR9yxAFFNQ75sOrD3daizB/view?usp=drive_link",
    "downloadCount": 0,
    "fileSize": "PDF File"
}

data.append(new_entry)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_entry['id']} to pyqs.json")
