# KU Admit Card Data Fetcher — Complete Guide
## How to check which students have admit cards and what papers they're sitting for

---

## What This Does
Given a list of **roll numbers** (e.g., students who scored < 40 in a paper):
1. **Fetches DOB** from KU's Result API (no need to know DOB beforehand!)
2. **Checks admit card** by submitting the form at `kuuniv.in/login`
3. **Parses HTML** to extract which papers the student is sitting for
4. **Saves results** as JSON

## Prerequisites
```bash
pip install selenium
```
- Python 3.x
- Chrome browser installed
- ChromeDriver matching your Chrome version

---

## How KU's Admit Card System Works

### Step 1: Get DOB from Result API
```
GET https://www.kuuniv.in/result/fetch/result/allcourse?course=FYUGP&semester=IV&stream=nep&rollno={ROLL_NUMBER}
```
Returns JSON with `dob` field (e.g., `"01/01/2005"`), plus `regno`, `mobile_no`, `sname`, etc.

### Step 2: Submit Admit Card Form
The form at `kuuniv.in/login` under "Click Here For Admit Card Of FYUGP Under NEP" posts to:
```
POST https://www.kuuniv.in/student/admitcardUgsem2/serch
```
With fields:
- `sem` — Semester number (1, 4, 7, etc.)
- `dob` — Date of birth in DD/MM/YYYY format
- `rollno` — **The ROLL NUMBER (IDR Number)**, NOT the KU registration number!

> **CRITICAL:** The IDR Number field takes the ROLL NUMBER (e.g., 231305779897), 
> NOT the registration number (e.g., KU2022002848). This was the key discovery.

### Step 3: Parse Response
- If admit card exists -> Full HTML page with student details and subject table
- If not -> "Admit Card Not Available"

---

## Available Semester Options (as of Sep 2026)
The FYUGP admit card form currently has these semesters enabled:
- `1` — 1st Semester
- `4` — 4th Semester (FYUGP Under NEP Semester IV Examination 2025)
- `7` — 7th Semester (FYUGP Under NEP Semester VII Examination 2026)

---

## The Working Script

**Location:** `C:\Users\Anurag\Documents\GitHub\result_main_folder\admit_cards\scripts\check_admitcards.py`

### How to Modify for Different Batches/Papers

1. **Change the roll numbers** — Edit the `ROLLS_2022` list at the top of the script

2. **Change the semester** — In the JavaScript form fill, change `'4'` to desired semester:
```python
semSelect.value = '4';  # Change to '1', '4', or '7'
```

3. **Change what paper to check** — Modify the detection string:
```python
has_mj06 = any("MJ - 06" in s or "MJ-06" in s for s in subjects)
# Change to whatever paper code you want
```

### How to Run
```bash
python -u "C:\Users\Anurag\Documents\GitHub\result_main_folder\admit_cards\scripts\check_admitcards.py"
```

### Output
- Console: Real-time progress for each student
- JSON: `result_main_folder\admit_cards\mj06_admitcard_results.json`

---

## API Reference

### Result API (to get DOB, mobile, etc.)
```
GET https://www.kuuniv.in/result/fetch/result/allcourse
    ?course=FYUGP
    &semester=IV
    &stream=nep
    &rollno={ROLL_NUMBER}
```

Key fields: `dob`, `sname`, `fname`, `regno`, `mobile_no`, `rollno`, `result`, `grand_total`

### Admit Card Form POST
```
POST https://www.kuuniv.in/student/admitcardUgsem2/serch

sem=4&dob=01/01/2005&rollno=231305779897
```

### Other Admit Card Endpoints
```
POST /student/admitcardbedsem3/serch/    -> B.Ed (fields: course, semester, ansidrno, dob)
AJAX /student/admitcard/part1/check/{btoa(reg)}/{btoa(dob)}
AJAX /student/admitcard/part3/check/{btoa(reg)}/{btoa(dob)}
AJAX /student/admitcard/pgall/check/{btoa(reg)}/{btoa(dob)}
```

---

## Roll Number Format
| Batch | Format | Example |
|-------|--------|---------|
| 2022 batch | 2313XXXXXXX | 231305779897 |
| 2023 batch | 2413XXXXXXX | 241305XXXXXX |
| 2024 batch | 2513XXXXXXX | 251305147716 |

---

## Quick Prompt for New Chat

Copy-paste this to continue in a new chat:

```
I need to check KU admit card availability for a list of roll numbers.

The working script is at:
C:\Users\Anurag\Documents\GitHub\result_main_folder\admit_cards\scripts\check_admitcards.py

Full instructions at:
C:\Users\Anurag\Documents\GitHub\result_main_folder\admit_cards\scripts\ADMIT_CARD_GUIDE.md

The approach:
1. Roll Number -> Result API -> Get DOB (dob field in response)
2. POST to /student/admitcardUgsem2/serch with sem={semester}, dob={dob}, rollno={roll_number}
3. Parse HTML response for subject/paper details

KEY: Use the ROLL NUMBER as IDR (not KU registration number).
Result API: GET https://www.kuuniv.in/result/fetch/result/allcourse?course=FYUGP&semester=IV&stream=nep&rollno={ROLL}

Here are the roll numbers I need to check: [paste roll numbers]
They are from [batch year] batch, semester [X].
```
