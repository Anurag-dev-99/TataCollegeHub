import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entries = [
    {
        "id": "pyq-iks-bbmku-sem1-2026",
        "category": "IKS",
        "semester": 1,
        "subject": "Indian Knowledge System",
        "title": "BBMKU IKS Sem 1 PYQ 2026 (95% Match with Kolhan Syllabus)",
        "year": "2026",
        "university": "BBMKU (Binod Bihari Mahto Koylanchal University)",
        "matchRating": "95%",
        "matchNote": "100% exam pattern match (50 MCQs / OMR). Best study material for Kolhan IKS exam.",
        "downloadUrl": "https://drive.google.com/file/d/1NkPH-aQ8stbHvDqJzy_jEtlvqi9aUQ1e/view?usp=drive_link",
        "fileSize": "PDF File",
        "downloadCount": 0
    },
    {
        "id": "pyq-iks-vbu-sem1-2026-set1",
        "category": "IKS",
        "semester": 1,
        "subject": "Indian Knowledge System",
        "title": "VBU IKS Sem 1 PYQ 2026 Set 1 (65-70% Match with Kolhan Syllabus)",
        "year": "2026",
        "set": "Set 1",
        "university": "Vinoba Bhave University (VBU)",
        "matchRating": "65-70%",
        "matchNote": "Good for core concepts & factual revision. Subjective pattern.",
        "downloadUrl": "https://drive.google.com/file/d/1U2LtU4343Par_ifG0j1BOWhHSEDBpSGW/view?usp=drive_link",
        "fileSize": "PDF File",
        "downloadCount": 0
    },
    {
        "id": "pyq-iks-vbu-sem1-2026-set2",
        "category": "IKS",
        "semester": 1,
        "subject": "Indian Knowledge System",
        "title": "VBU IKS Sem 1 PYQ 2026 Set 2 (65-70% Match with Kolhan Syllabus)",
        "year": "2026",
        "set": "Set 2",
        "university": "Vinoba Bhave University (VBU)",
        "matchRating": "65-70%",
        "matchNote": "Good for core concepts & factual revision. Subjective pattern.",
        "downloadUrl": "https://drive.google.com/file/d/1zqX3jmo_uOMAa4B5L4ETi73kUujL6Dmu/view?usp=drive_link",
        "fileSize": "PDF File",
        "downloadCount": 0
    },
    {
        "id": "notes-iks-sem1-2025",
        "category": "IKS",
        "semester": 1,
        "subject": "Indian Knowledge System",
        "title": "IKS Sem 1 Notes (2025 Batch - Kolhan University)",
        "year": "2025-2029",
        "type": "notes",
        "downloadUrl": "https://drive.google.com/file/d/1iljyaJBGVq006bYH9KgrWqgX6DoZugZB/view?usp=drive_link",
        "fileSize": "PDF File",
        "downloadCount": 0
    }
]

data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_entries)} IKS entries to pyqs.json")
for e in new_entries:
    print(f"  {e['id']}")
