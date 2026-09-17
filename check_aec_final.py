import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\aec.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total AEC entries: {len(data)}")
print("Last 12 entries:")
for item in data[-12:]:
    print(f" - {item['name']} (Sem: {item['semester']})")
