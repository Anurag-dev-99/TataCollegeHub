import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

updated_count = 0

for item in data:
    if item.get("category") == "Major" and item.get("subject") == "Zoology" and item.get("semester") == 1:
        year_str = item.get("year", "")
        # Extract the start year from formats like "2022-2026", "2023-2027" or just "2023"
        start_year = year_str.split("-")[0] if "-" in year_str else year_str
        
        new_title = f"Zoology Major Sem 1 PYQ (MJ-01) {start_year} Batch"
        
        if item.get("title") != new_title:
            item["title"] = new_title
            updated_count += 1
            print(f"Updated title to: {new_title}")

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Updated {updated_count} entries.")
