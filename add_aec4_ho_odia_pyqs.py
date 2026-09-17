import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entries = [
    {
        "id": "pyq-aec-4-ho-2022",
        "title": "AEC-4 Ho PYQ 2022",
        "year": "2022-2026",
        "semester": 4,
        "category": "AEC",
        "subject": "Ho",
        "downloadCount": 0,
        "fileSize": "PDF File",
        "downloadUrl": "https://drive.google.com/file/d/1jdtTyfEw85z9XvCTDEI9TelqHLasbKLM/view?usp=drive_link"
    },
    {
        "id": "pyq-aec-4-odia-2022",
        "title": "AEC-4 Odia PYQ 2022",
        "year": "2022-2026",
        "semester": 4,
        "category": "AEC",
        "subject": "Odia",
        "downloadCount": 0,
        "fileSize": "PDF File",
        "downloadUrl": "https://drive.google.com/file/d/1HcfbbHwffRRZCX1toB5by5O93jE8gEA6/view?usp=drive_link"
    }
]

data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_entries)} new entries to pyqs.json")
