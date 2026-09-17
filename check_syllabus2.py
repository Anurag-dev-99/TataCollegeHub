import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\syllabus.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"syllabus.json has {len(data)} entries. Sample:")
for item in data[:3]:
    print(item)
