import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\kolhan_syllabi.json"
try:
    with open(file_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"kolhan_syllabi.json has {len(data)} entries. Sample:")
    for item in data[:2]:
        print(item)
except FileNotFoundError:
    pass

file_json2 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\syllabus.json"
try:
    with open(file_json2, "r", encoding="utf-8") as f:
        data2 = json.load(f)
    print(f"\nsyllabus.json has {len(data2)} entries. Sample:")
    for item in data2[:2]:
        print(item)
except FileNotFoundError:
    pass
