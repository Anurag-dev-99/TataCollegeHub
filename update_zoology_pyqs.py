import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Data to update/add
updates = [
    {
        "year": "2022-2026",
        "url": "https://drive.google.com/file/d/10EC7Iqgur-SO_xNr_LcrU9MxqI-KWJFU/view?usp=drive_link",
        "id_suffix": "2022"
    },
    {
        "year": "2023-2027",
        "url": "https://drive.google.com/file/d/1a0-8EzPCkG-JGQ1-gpXw7IQwWWQknIFS/view?usp=drive_link",
        "id_suffix": "2023"
    },
    {
        "year": "2024-2028",
        "url": "https://drive.google.com/file/d/1GQpaf_VF6I5pFdZ0vrvTMnE-fuwDAdKG/view?usp=drive_link",
        "id_suffix": "2024"
    },
    {
        "year": "2025-2029",
        "url": "https://drive.google.com/file/d/15x04oTL2wC3Xk2RzNv5JvMKyS_fhkUEk/view?usp=drive_link",
        "id_suffix": "2025"
    }
]

added_count = 0
updated_count = 0

for update in updates:
    found = False
    for item in data:
        if item.get("category") == "Major" and item.get("subject") == "Zoology" and item.get("semester") == 1 and item.get("year") == update["year"]:
            item["downloadUrl"] = update["url"]
            found = True
            updated_count += 1
            print(f"Updated existing entry for {update['year']}")
            break
            
    if not found:
        new_entry = {
            "id": f"pyq-mj-zoology-sem1-{update['id_suffix']}",
            "title": f"MJ-01 Zoology Sem 1 ({update['year']} Batch)",
            "year": update["year"],
            "semester": 1,
            "category": "Major",
            "subject": "Zoology",
            "downloadUrl": update["url"],
            "downloadCount": 0,
            "fileSize": "PDF File"
        }
        data.append(new_entry)
        added_count += 1
        print(f"Added new entry for {update['year']}")

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nSummary: {added_count} added, {updated_count} updated.")
