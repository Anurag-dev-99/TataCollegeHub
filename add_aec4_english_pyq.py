import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entry = {
    "id": "pyq-aec-4-english-sem4-2022",
    "title": "AEC-4 English 2022 Paper",
    "year": "2022-2026",
    "semester": 4,
    "category": "AEC",
    "subject": "English",
    "downloadUrl": "https://drive.google.com/file/d/1xSCuprUiIQxIs1diDthM0Ubnv4B-f6Jt/view?usp=drive_link",
    "downloadCount": 0,
    "fileSize": "PDF File"
}

data.append(new_entry)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_entry['id']} to pyqs.json")
