import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []
removed_count = 0
renamed_count = 0

for item in data:
    title = item.get("title", "")
    
    # Task 1: Fix History Major Sem 4 MJ-09 -> MJ-08
    if item.get("category") == "Major" and item.get("subject") == "History" and item.get("semester") == 4:
        if "MJ-09" in title and "2022" in title:
            item["title"] = title.replace("MJ-09", "MJ-08")
            renamed_count += 1
            print(f"Renamed: {title} -> {item['title']}")
            
    # Tasks 2, 3, 4: Remove the specific 'Coming Soon' placeholder boxes
    # "2024 Paper - Introductory Physics"
    # "2024 Paper - Indian Culture & Heritage MDC" 
    # "2024 Paper - Introduction to Constitution MDC"
    
    if title == "2024 Paper - Introductory Physics" and item.get("subject") == "Physics":
        print(f"Removed: {title}")
        removed_count += 1
        continue
        
    if title == "2024 Paper - Indian Culture & Heritage MDC" and item.get("subject") == "History":
        print(f"Removed: {title}")
        removed_count += 1
        continue
        
    if "Introduction to Constitution MDC" in title and item.get("subject") == "Political Science":
        print(f"Removed: {title}")
        removed_count += 1
        continue
        
    new_data.append(item)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)

print(f"\nSummary: {renamed_count} renamed, {removed_count} removed.")
