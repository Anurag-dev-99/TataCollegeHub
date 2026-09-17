import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\aec.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entries = [
    {"id": "aec-4-bengali", "name": "AEC-4 Bengali", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1qUegoIsTOXhdZzPJrVuPDz7sc1EDAhmf/view?usp=drive_link"},
    {"id": "aec-4-ho", "name": "AEC-4 Ho", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1tWgBS0rh05r8tHNwtQPNgbWlUDZyfJnh/view?usp=drive_link"},
    {"id": "aec-4-kharia", "name": "AEC-4 Kharia", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1ENTyW0phbtLgyO5BdQg6ecTwthAi4JVl/view?usp=drive_link"},
    {"id": "aec-4-khortha", "name": "AEC-4 Khortha", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1NCmk9oyhfk5u2axCdvzR28ThxAz0FzTV/view?usp=drive_link"},
    {"id": "aec-4-kurmali", "name": "AEC-4 Kurmali", "semester": "Semester 4", "link": "https://drive.google.com/file/d/11v3QU6h1nOCVlk4EijHDFBXXxjAdQtcF/view?usp=drive_link"},
    {"id": "aec-4-kurukh", "name": "AEC-4 Kurukh", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1yp4YkYo6ay62u4VI-EpCGy0HRMhcHkF0/view?usp=drive_link"},
    {"id": "aec-4-mundari", "name": "AEC-4 Mundari", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1naws1t-aLEKEmK8AIjHvoV9XofzMMbag/view?usp=drive_link"},
    {"id": "aec-4-nagpuri", "name": "AEC-4 Nagpuri", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1-Z2h687fTV6JiGARyP3CZOXuu9023n8q/view?usp=drive_link"},
    {"id": "aec-4-santali", "name": "AEC-4 Santali", "semester": "Semester 4", "link": "https://drive.google.com/file/d/1y0ZufgUQwQa1C63dlDxlO36rK3-2x38c/view?usp=drive_link"},
    {"id": "aec-4-urdu", "name": "AEC-4 Urdu", "semester": "Semester 4", "link": "https://drive.google.com/file/d/102DiXwrkYmJTejeYZK0vNHta5HGVVOxE/view?usp=drive_link"}
]

data.extend(new_entries)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_entries)} new entries to aec.json")
