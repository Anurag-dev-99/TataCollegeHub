import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entries = [
    {
        "id": "pyq-iks-kolhan-sem1-2025-set1",
        "category": "IKS",
        "semester": 1,
        "subject": "Indian Knowledge System",
        "title": "IKS Sem 1 PYQ 2025 Set 1 (Kolhan University)",
        "year": "2025-2029",
        "set": "Set 1",
        "university": "Kolhan University",
        "matchRating": "100%",
        "matchNote": "Official Kolhan University Question Paper",
        "downloadUrl": "https://drive.google.com/file/d/114zR1UbF6Nn5ofCx-0nK0wfECl20ry-E/view?usp=drive_link",
        "fileSize": "PDF File",
        "downloadCount": 0
    },
    {
        "id": "pyq-iks-kolhan-sem1-2025-set2",
        "category": "IKS",
        "semester": 1,
        "subject": "Indian Knowledge System",
        "title": "IKS Sem 1 PYQ 2025 Set 2 (Kolhan University)",
        "year": "2025-2029",
        "set": "Set 2",
        "university": "Kolhan University",
        "matchRating": "100%",
        "matchNote": "Official Kolhan University Question Paper",
        "downloadUrl": "https://drive.google.com/file/d/1-t_hvYnuD59X658tGSBEy3DLEg5X_i-k/view?usp=drive_link",
        "fileSize": "PDF File",
        "downloadCount": 0
    },
    {
        "id": "pyq-aec-hindi-sem1-2025-set1",
        "title": "AEC-1 Hindi PYQ 2025 (Set 1)",
        "year": "2025-2029",
        "set": "Set 1",
        "semester": 1,
        "category": "AEC",
        "subject": "Hindi",
        "downloadUrl": "https://drive.google.com/file/d/15-GBpSC84lkO1wKBL9vMo4PxL9fIKN78/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF"
    },
    {
        "id": "pyq-vac-understanding-india-sem1-2025-set1",
        "title": "Understanding India PYQ 2025 (Set 1)",
        "year": "2025-2029",
        "set": "Set 1",
        "semester": 1,
        "category": "VAC",
        "subject": "Understanding India",
        "downloadUrl": "https://drive.google.com/file/d/1BaTir8o3o6X_9i1pQcZOawKHzhCvnxIw/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF"
    }
]

data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_entries)} entries to pyqs.json")
