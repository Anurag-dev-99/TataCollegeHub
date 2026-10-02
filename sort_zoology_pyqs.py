import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find all Zoology Major Sem 1 papers
zoology_papers = []
zoology_indices = []

for i, item in enumerate(data):
    if item.get("category") == "Major" and item.get("subject") == "Zoology" and item.get("semester") == 1:
        zoology_papers.append(item)
        zoology_indices.append(i)

if zoology_papers:
    # Sort them ascending by year (e.g., "2022-2026", "2023-2027")
    zoology_papers.sort(key=lambda x: x.get("year", ""))
    
    # Place them back in the array at the exact same indices
    for i, idx in enumerate(zoology_indices):
        data[idx] = zoology_papers[i]

    with open(file_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Sorted {len(zoology_papers)} Zoology Major Sem 1 papers.")
    for p in zoology_papers:
        print(f"- {p['title']}")
else:
    print("No Zoology papers found to sort.")
