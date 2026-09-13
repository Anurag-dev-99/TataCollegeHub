import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter out old Set 1 and Set 3 for Global Citizenship...
# The exact subject name might be "Global Citizenship Education for Sustainable Development"
# Let's filter by category VAC, semester 4, and year 2022-2026.
# Or just by subject name if it's unique.
subject_name = "Global Citizenship Education for Sustainable Development"

filtered_data = [
    item for item in data 
    if not (item.get("category") == "VAC" and 
            item.get("semester") == 4 and 
            item.get("subject") == subject_name and
            item.get("year") == "2022-2026" and
            item.get("set") in ["Set 1", "Set 3"])
]

print(f"Original entries: {len(data)}, After removal: {len(filtered_data)}")

# Add new entries
new_entries = [
    {
        "id": "pyq-vac-global-citizenship-sem4-2022-set1",
        "title": "Global Citizenship 2022 (Set 1)",
        "year": "2022-2026",
        "set": "Set 1",
        "semester": 4,
        "category": "VAC",
        "subject": subject_name,
        "downloadUrl": "https://drive.google.com/file/d/1ZN5iBiBFPRHjeA5UYiVr4zdoW9ACqKiC/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-vac-global-citizenship-sem4-2022-set2",
        "title": "Global Citizenship 2022 (Set 2)",
        "year": "2022-2026",
        "set": "Set 2",
        "semester": 4,
        "category": "VAC",
        "subject": subject_name,
        "downloadUrl": "https://drive.google.com/file/d/1Z7J-axXv3BqZhThDa24IpRdkIvlLX7co/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-vac-global-citizenship-sem4-2022-set3",
        "title": "Global Citizenship 2022 (Set 3)",
        "year": "2022-2026",
        "set": "Set 3",
        "semester": 4,
        "category": "VAC",
        "subject": subject_name,
        "downloadUrl": "https://drive.google.com/file/d/1OmHjKcSJzfW18YM264lVazF9I_RpObGT/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    }
]

filtered_data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=4, ensure_ascii=False)

print(f"Added 3 new entries. Total entries now: {len(filtered_data)}")
