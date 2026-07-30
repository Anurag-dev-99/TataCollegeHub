import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entry = {
    "id": "pyq-major-bba-sem1-2025",
    "title": "BBA Major 2025 Paper",
    "year": "2025-2029",
    "semester": 1,
    "category": "Major",
    "subject": "BBA",
    "downloadUrl": "https://drive.google.com/file/d/1MKYAc19a8dVVehmCzQM18ksEagQ4Q5D2/view?usp=drive_link",
    "downloadCount": 0,
    "fileSize": "PDF File"
}

data.append(new_entry)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_entry['id']} to pyqs.json")
