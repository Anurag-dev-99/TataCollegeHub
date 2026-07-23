import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

url_map = {
    "pyq-aec-1-hindi-2022-set1": "https://drive.google.com/file/d/1HlU2qIFRJyhzaA2YFV_HooLoEpvzRbxN/view?usp=drive_link",
    "pyq-aec-1-hindi-2022-set2": "https://drive.google.com/file/d/1IGB9IK81rnU_boAO2Tp6PaLiEozUh0au/view?usp=drive_link",
    "pyq-aec-1-hindi-2023-set1": "https://drive.google.com/file/d/1A4qK9Ws1dCcNKvOcDrgHiVu21gIFz9x9/view?usp=drive_link",
    "pyq-aec-1-hindi-2023-set2": "https://drive.google.com/file/d/1DhbaMC_qBti3f4PfHg4CCD5qF572-fQC/view?usp=drive_link",
    "pyq-aec-1-hindi-2024-set1": "https://drive.google.com/file/d/13ECHMfpR_8iiuac3sitmZONd1jmZ3YLx/view?usp=drive_link",
    "pyq-aec-1-hindi-2024-set3": "https://drive.google.com/file/d/1fn--l91bZ5HrsNrosgri8FQgtU2IWKPZ/view?usp=drive_link"
}

count = 0
for item in data:
    if item['id'] in url_map:
        item['downloadUrl'] = url_map[item['id']]
        count += 1
        print(f"Updated URL for {item['id']}")

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nTotal updated: {count} papers")
