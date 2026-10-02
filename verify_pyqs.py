import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Checking a few other subjects to ensure they are untouched:")
for item in data[:5]:
    print(f"- {item.get('subject', 'Unknown')} ({item.get('category', 'Unknown')}): {item.get('title', 'Unknown')}")
