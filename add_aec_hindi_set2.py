import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entry = {
    "id": "pyq-aec-hindi-sem1-2025-set2",
    "title": "AEC-1 Hindi 2025 (Set 2)",
    "year": "2025-2029",
    "set": "Set 2",
    "semester": 1,
    "category": "AEC",
    "subject": "Hindi",
    "downloadUrl": "https://drive.google.com/file/d/1FYXrMbV0ia6C9wN9-QXukO9a8NGvBmm5/view?usp=drive_link",
    "downloadCount": 0,
    "fileSize": "PDF File"
}

data.append(new_entry)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_entry['id']} to pyqs.json")
