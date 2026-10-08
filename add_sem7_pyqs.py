import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entries = [
    {
        "id": "pyq-mj-zoology-sem7-mj16-2022",
        "title": "Zoology Major Sem 7 PYQ (MJ-16) 2022 Batch",
        "year": "2022-2026",
        "semester": 7,
        "category": "Major",
        "subject": "Zoology",
        "downloadUrl": "https://drive.google.com/file/d/1x_mxT52KhTXUT4If93Ghcgt5092bGRZA/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-mj-zoology-sem7-mj17-2022",
        "title": "Zoology Major Sem 7 PYQ (MJ-17) 2022 Batch",
        "year": "2022-2026",
        "semester": 7,
        "category": "Major",
        "subject": "Zoology",
        "downloadUrl": "https://drive.google.com/file/d/1NoDPi9s7XOGo_pxIyhMOmbVBttDNaXxQ/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-mj-physics-sem7-mj16-2022",
        "title": "Physics Major Sem 7 PYQ (MJ-16) 2022 Batch",
        "year": "2022-2026",
        "semester": 7,
        "category": "Major",
        "subject": "Physics",
        "downloadUrl": "https://drive.google.com/file/d/1NDhEwPxvWOHj4wUCvWHDZ8wnQAL461-z/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-mj-physics-sem7-mj17-2022",
        "title": "Physics Major Sem 7 PYQ (MJ-17) 2022 Batch",
        "year": "2022-2026",
        "semester": 7,
        "category": "Major",
        "subject": "Physics",
        "downloadUrl": "https://drive.google.com/file/d/1TMhMXhRzbZTg_c4oV6HehLl4OrsxNHER/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-mj-chemistry-sem7-mj16-2022",
        "title": "Chemistry Major Sem 7 PYQ (MJ-16) 2022 Batch",
        "year": "2022-2026",
        "semester": 7,
        "category": "Major",
        "subject": "Chemistry",
        "downloadUrl": "https://drive.google.com/file/d/11pCfZVOqmGx5dWt4-Ncqx_Ns4B3BcUwi/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    },
    {
        "id": "pyq-mj-chemistry-sem7-mj17-2022",
        "title": "Chemistry Major Sem 7 PYQ (MJ-17) 2022 Batch",
        "year": "2022-2026",
        "semester": 7,
        "category": "Major",
        "subject": "Chemistry",
        "downloadUrl": "https://drive.google.com/file/d/1jAlOzwfosoWQl6PpDxC1fFU7RvUcdu5L/view?usp=drive_link",
        "downloadCount": 0,
        "fileSize": "PDF File"
    }
]

data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_entries)} entries to pyqs.json.")
