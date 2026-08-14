# 📦 Result Data Registry

> **Last Updated:** 2026-08-13
> This file keeps track of all scraped Kolhan University result data — what we have, where it's stored, and how many records.

---

## 🌐 Website-Ready Data (Cleaned, Live on TataCollegeHub)

**Location:** `C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\`

| # | File | Semester | Batch | Scope | Students | Size | Status |
|---|------|----------|-------|-------|----------|------|--------|
| 1 | `results_sem1_master.json` | Semester 1 | 2024-2028 | Tata College Only | 2,081 | 1.91 MB | ✅ Live |
| 2 | `results_sem2_master.json` | Semester 2 | 2023-2027 | Tata College Only | 1,930 | 2.44 MB | ✅ Live |
| 3 | `results_sem3_master.json` | Semester 3 | 2023-2027 | Tata College Only | 1,402 | 3.25 MB | ✅ Live |
| 4 | `results_sem4_master.json` | Semester 4 | 2022-2026 | Tata College Only | 1,232 | 1.06 MB | ✅ Live |
| 5 | `results_sem6_master.json` | Semester 6 | 2022-2026 | Tata College Only | 1,143 | 1.48 MB | ✅ Live |

**Website Total: 7,788 student records | 10.14 MB**

Registry file: `results.json` — links semesters with pass rates, toppers, department analytics.

---

## 🗄️ Raw Scraped Data (from KU API)

### 1. Semester 2 — 2023 Batch — FULL KOLHAN UNIVERSITY (All Colleges)

**Location:** `C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\`

| File / Folder | Records | Size | Description |
|---------------|---------|------|-------------|
| `Part1.txt` to `Part13.json` | — | — | Raw roll number lists (13 parts from gazette PDF) |
| `kolhan_sem2_2023_master.json` | 18,661 | 65.47 MB | Combined raw API responses |
| `fetched_data\` | 18,661 files | 65.43 MB | Individual per-student JSON files |
| `cleaned\kolhan_sem2_2023_clean.json` | 18,661 | 24.17 MB | Cleaned & sanitized |
| `cleaned\college_summary.json` | — | — | Per-college breakdown |
| `cleaned\by_college\` | — | — | Data split by individual college |

**Scripts:** `fetch_all.py`, `clean_all.py`, `convert_for_website.py`

> Also has an older copy at: `C:\Users\Anurag\Documents\GitHub\Kolhan_university_2023_sem2_all\`

---

### 2. Semester 1 — 2024 Batch — Tata College Only

**Location:** `C:\Users\Anurag\Documents\GitHub\result_main_folder\2024\sem1\tata_college\`

| File / Folder | Records | Size | Description |
|---------------|---------|------|-------------|
| `2024_batch_tata_college.json` | — | — | Roll number list |
| `fetched\` | 2,081 files | 3.95 MB | Individual per-student raw API JSON |

**Script:** `fetch_and_convert.py` (fetches + cleans + outputs website-ready JSON in one step)

---

### 3. Semester 4 — 2022 Batch — Tata College Only

**Location:** `C:\Users\Anurag\Documents\GitHub\result\sem4_2022_batch\`

| File / Folder | Records | Size | Description |
|---------------|---------|------|-------------|
| `Science.json` | — | — | Roll numbers: Science departments |
| `art1.json` | — | — | Roll numbers: Arts batch 1 |
| `history_hindi.json` | — | — | Roll numbers: History + Hindi |
| `geo_eng_eco_bengalig_anthro.json` | — | — | Roll numbers: Geography, English, Economics, Bengali, Anthropology |
| `raw_data\` | 1,288 files | 3.96 MB | Individual per-student raw API JSON |
| `cleaned_data\` | — | — | Cleaned output |

**Scripts:** `fetch_science_sem4.py`, `fetch_art1_sem4.py`, `fetch_history_hindi_sem4.py`, `fetch_final_sem4.py`

---

### 4. Semester 6 — 2022 Batch — Tata College Only

**Location:** `C:\Users\Anurag\Documents\GitHub\2022_batch_sem5_result\`

| File / Folder | Records | Size | Description |
|---------------|---------|------|-------------|
| `sem5_2022_batch_tata_college.txt` | 1,121 | — | Roll number source (from Sem 5 gazette) |
| `tata_college_sem5_2022.json` | 992 | — | Alternate roll number list |
| `fetched\` | 1,143 files | 4.25 MB | Individual per-student raw API JSON |
| `sem6_all_raw.json` | 1,143 | 5.26 MB | Combined raw API responses |

**Scripts:** `fetch_sem6_all.py`, `fetch_sem6_demo.py`, `clean_and_convert_sem6.py`

---

## 📄 PDF Marksheet Data

### Demo PDFs & Scripts
**Location:** `C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs\`

| File | Description |
|------|-------------|
| `download_html.js` | Playwright — downloads KU's exact rendered HTML (Method 3A) |
| `convert_to_pdf.js` | Converts downloaded HTML → pixel-perfect PDFs (Method 3B) |
| `generate_perfect.py` | Offline Python template-based PDF generation (Method 2) |
| `downloaded_html\` | Saved HTML marksheets |
| `final_pdfs\` | Generated PDF marksheets |
| 5 sample `.html` + `.pdf` pairs | Demo marksheets |
| `ku_logo.png`, `controller_sign.jpg` | KU branding assets |

### Headless Browser Capture
**Location:** `C:\Users\Anurag\Documents\GitHub\result\sem2_2023_marksheets\`

| File | Description |
|------|-------------|
| `capture_official_marksheet.py` | Headless browser capture — Method 1 (slow, authentic) |
| `generate_marksheets.py` | Offline template generation |
| `html\`, `pdfs\`, `raw_data\` | Output folders |

---

## 📊 Grand Totals

| Category | Records | Storage |
|----------|---------|---------|
| Website-ready (Tata College, 5 semesters) | **7,788** | ~10 MB |
| Raw Kolhan-wide Sem 2 (all colleges) | **18,661** | ~90 MB |
| Individual fetched files (all semesters) | **23,173** | ~77 MB |
| **Total unique records scraped** | **~25,000+** | **~170+ MB** |

---

## ❌ Data We DON'T Have Yet

| Semester | Batch | What's Missing |
|----------|-------|----------------|
| Semester 1 | 2024 | Full Kolhan University (we only have Tata College) |
| Semester 3 | 2023 | Full Kolhan University (we only have Tata College) |
| Semester 4 | 2022 | Full Kolhan University (we only have Tata College) |
| Semester 5 | 2022 | Roll numbers available, results NOT scraped |
| Semester 6 | 2022 | Full Kolhan University (we only have Tata College) |

---

## 🔗 API Reference

**Endpoint:** `https://www.kuuniv.in/result/fetch/result/allcourse`

**Parameters:**
- `course=FYUGP`
- `semester=I` / `II` / `III` / `IV` / `V` / `VI` (Roman numerals)
- `stream=nep`
- `rollno={roll_number}`

**Example:** `https://www.kuuniv.in/result/fetch/result/allcourse?course=FYUGP&semester=VI&stream=nep&rollno=231305178350`
