import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entry = {
    "id": "pyq-iks-kolhan-sem1-2025-set3",
    "category": "IKS",
    "semester": 1,
    "subject": "Indian Knowledge System",
    "title": "IKS Sem 1 PYQ 2025 Set 3 (Kolhan University)",
    "year": "2025-2029",
    "set": "Set 3",
    "university": "Kolhan University",
    "matchRating": "100%",
    "matchNote": "Official Kolhan University Question Paper",
    "downloadUrl": "https://drive.google.com/file/d/19P7tCblBLpJSM8IbAZNUYeOFyxa8frAm/view?usp=drive_link",
    "fileSize": "PDF File",
    "downloadCount": 0
}

data.append(new_entry)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_entry['id']} to pyqs.json")
