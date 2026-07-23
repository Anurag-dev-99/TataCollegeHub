import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

output = []
for item in data:
    if item.get("category") == "AEC" and "Hindi" in item.get("subject", ""):
        output.append(f"ID: {item['id']} | Title: {item['title']} | Year: {item.get('year')} | URL: {item.get('downloadUrl')}")

with open("hindi_aec.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
