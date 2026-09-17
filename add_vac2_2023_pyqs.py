import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

subject_name = "Global Citizenship Education for Sustainable Development"

new_entries = [
    {
        "id": "pyq-vac-global-citizenship-sem4-2023-set1",
        "title": "Global Citizenship 2023 (Set 1)",
        "year": "2023-2027",
        "set": "Set 1",
        "semester": 4,
        "category": "VAC",
        "subject": subject_name,
        "downloadUrl": "https://drive.google.com/file/d/1ehxw2zqX6kYTGwkUKdN289TEPyrkzN4b/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-vac-global-citizenship-sem4-2023-set2",
        "title": "Global Citizenship 2023 (Set 2)",
        "year": "2023-2027",
        "set": "Set 2",
        "semester": 4,
        "category": "VAC",
        "subject": subject_name,
        "downloadUrl": "https://drive.google.com/file/d/1Oa4WY5WI4y3Q9o8Y3FVrIyz1tjfIANTV/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    }
]

data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_entries)} new entries. Total entries now: {len(data)}")
