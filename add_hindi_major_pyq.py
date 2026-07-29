import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entry = {
    "id": "pyq-major-hindi-sem1-2023",
    "title": "2023 Paper",
    "year": "2023-2027",
    "semester": 1,
    "category": "Major",
    "subject": "Hindi",
    "downloadUrl": "https://drive.google.com/file/d/1CzT3m7o9RJLn7zZ_9H-jj64SHAyzAEsy/view?usp=drive_link",
    "downloadCount": 0,
    "fileSize": "PDF File"
}

data.append(new_entry)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_entry['id']} to pyqs.json")
