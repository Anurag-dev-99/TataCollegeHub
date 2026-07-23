file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    content = f.read()

# Check which are actually 2025 batch vs 2024 batch
# Let's find all entries with "2024-2028" and see their titles
import json
data = json.loads(content)
for item in data:
    if item.get("year") == "2024-2028":
        print(f"  ID: {item['id']} | Title: {item['title']} | Year: {item['year']}")
