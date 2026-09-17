import json

file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\syllabus.json"
with open(file_json, "r", encoding="utf-8") as f:
    data = json.load(f)

new_entry = {
    "id": "syl-aec4-regional-ref",
    "title": "AEC-4 Regional Languages (Ranchi University Reference)",
    "department": "AEC",
    "semester": "Semester 4",
    "effectiveFrom": "2022 onwards",
    "fileSize": "Various PDFs",
    "description": "⚠️ Note: These are Ranchi University syllabi provided for reference purposes only, as the official Kolhan University syllabi for these subjects are currently unavailable. Please verify with your department.",
    "modules": ["Syllabus for AEC-4 regional languages covering grammar, literature, and history of respective languages."],
    "downloadUrls": [
        "https://drive.google.com/file/d/1qUegoIsTOXhdZzPJrVuPDz7sc1EDAhmf/view?usp=drive_link",
        "https://drive.google.com/file/d/1tWgBS0rh05r8tHNwtQPNgbWlUDZyfJnh/view?usp=drive_link",
        "https://drive.google.com/file/d/1ENTyW0phbtLgyO5BdQg6ecTwthAi4JVl/view?usp=drive_link",
        "https://drive.google.com/file/d/1NCmk9oyhfk5u2axCdvzR28ThxAz0FzTV/view?usp=drive_link",
        "https://drive.google.com/file/d/11v3QU6h1nOCVlk4EijHDFBXXxjAdQtcF/view?usp=drive_link",
        "https://drive.google.com/file/d/1yp4YkYo6ay62u4VI-EpCGy0HRMhcHkF0/view?usp=drive_link",
        "https://drive.google.com/file/d/1naws1t-aLEKEmK8AIjHvoV9XofzMMbag/view?usp=drive_link",
        "https://drive.google.com/file/d/1-Z2h687fTV6JiGARyP3CZOXuu9023n8q/view?usp=drive_link",
        "https://drive.google.com/file/d/1y0ZufgUQwQa1C63dlDxlO36rK3-2x38c/view?usp=drive_link",
        "https://drive.google.com/file/d/102DiXwrkYmJTejeYZK0vNHta5HGVVOxE/view?usp=drive_link"
    ],
    "downloadLabels": [
        "Download Bengali",
        "Download Ho",
        "Download Kharia",
        "Download Khortha",
        "Download Kurmali",
        "Download Kurukh",
        "Download Mundari",
        "Download Nagpuri",
        "Download Santali",
        "Download Urdu"
    ]
}

data.append(new_entry)

with open(file_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {new_entry['id']} to syllabus.json")
