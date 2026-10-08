# KU Student Photo Downloader — Complete Guide
## Download student photos for Tata College, 2022 batch (All 1,143 Students)

---

## How It Works

```
Roll Number + DOB (from local master data) → Admit Card POST (Sem 7 / 4 / 1) → Extract Photo URL → Direct HTTP Download JPEG
```

### Key Facts:
- **No Selenium / Chrome needed:** Uses direct, high-speed HTTP requests.
- **Fast speed:** **0.5 seconds** pause per student.
- **Total Students:** **1,143 students** (covers Arts, Science, and Commerce).
- **Total Runtime:** **~9 to 10 minutes** total.
- **Resume support:** If stopped, re-running skips already downloaded photos automatically.
- **Photo Quality:** High-resolution JPEG (~30–50 KB each).

### Endpoints Used:
```
1. Admit Card POST: https://www.kuuniv.in/student/admitcardUgsem2/serch  (body: sem=7&dob={DOB}&rollno={ROLL})
2. Photo URL:       https://www.kuuniv.in/ftpwebapps/ku/resources/studentdata/users/profileimage/{PHOTO_ID}_IMAGE.jpg
```

---

## How to Run

Open your terminal or PowerShell and run:

```bash
python -u "C:\Users\Anurag\Documents\GitHub\TataCollegeHub\scripts\download_photos.py"
```

### Output:
- **Photos directory:** `scripts/photos_tata_2022/{Student_Name}_{RollNo}.jpg`
- **Master student list:** `scripts/photos_tata_2022/students.json`
- **Detailed results log:** `scripts/photos_tata_2022/photo_results.json`
