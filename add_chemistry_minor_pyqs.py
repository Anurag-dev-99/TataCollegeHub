import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entries = [
    {
        "id": "pyq-minor-chemistry-sem2-2022-mn2a",
        "title": "2022 Paper (MN 2A)",
        "year": "2022-2026",
        "semester": 2,
        "category": "Minor",
        "subject": "Chemistry",
        "downloadUrl": "https://drive.google.com/file/d/1yK-7XqYKPrlR8l3I-iFI8r8uSQBZzQeQ/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-minor-chemistry-sem3-2022-mn1b",
        "title": "2022 Paper (MN 1B)",
        "year": "2022-2026",
        "semester": 3,
        "category": "Minor",
        "subject": "Chemistry",
        "downloadUrl": "https://drive.google.com/file/d/1jj5OnSV8rp9hGRxWJxuXLr4tAG58YQcT/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-minor-chemistry-sem2-2023-mn2a",
        "title": "2023 Paper (MN 2A)",
        "year": "2023-2027",
        "semester": 2,
        "category": "Minor",
        "subject": "Chemistry",
        "downloadUrl": "https://drive.google.com/file/d/1H9nJ5SDO3G0qXO7hGHu0-kZyLEIluxxR/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-minor-chemistry-sem2-2024-mn2a",
        "title": "2024 Paper (MN 2A)",
        "year": "2024-2028",
        "semester": 2,
        "category": "Minor",
        "subject": "Chemistry",
        "downloadUrl": "https://drive.google.com/file/d/1BBKG6wvAo9TBEf-6X2Z_k5Bj6sqNXcZ1/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    }
]

data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_entries)} entries to pyqs.json")
