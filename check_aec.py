import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\aec.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data[:3]:
    print(item)
