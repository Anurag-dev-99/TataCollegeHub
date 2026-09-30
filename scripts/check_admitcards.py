"""
ADMIT CARD DATA FETCHER — Check which students have admit cards
================================================================
For each roll number:
1. Get DOB from Result API
2. POST to /student/admitcardUgsem2/serch with sem=4, dob, rollno (as IDR!)
3. Parse HTML response for subject/paper details
4. Report which students have MJ-06 paper in their admit card
"""
import os, sys, json, base64, time
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.request

BASE_URL = "https://www.kuuniv.in"
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 2022 batch students who scored < 40 in MJ-06 Maths
ROLLS_2022 = [
    "231305779897",  # HIMANSHU MAHTO
    "231305779970",  # SANGITA DAS
    "231305779922",  # ABHAY GOPE
    "231305779903",  # SAMIR KUMAR
    "231305779921",  # VISHAL BARDA
    "231305779987",  # CHANDO LEYANGI
    "231305779958",  # JAMDAR SIRKA
    "231305779969",  # MUKESH MAHATO
    "231305779967",  # SARODA NAYAK
    "231305779961",  # PURUSHOTAM JAMUDA
    "231305779944",  # GURBA MURMU
    "231305779948",  # RAM KRISHNA GAGRAI
    "231305779916",  # KAMAL MAHATO
    "231305779983",  # MANJU PURTY
    "231305779989",  # MANISHA GAGRAI
    "231305779956",  # MUSKAN BASKEY
]

def fetch_dob(roll):
    """Get DOB from result API"""
    for sem in ["IV", "III", "II", "I"]:
        url = f"{BASE_URL}/result/fetch/result/allcourse?course=FYUGP&semester={sem}&stream=nep&rollno={roll}"
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            if data.get("result") and len(data["result"]) > 0:
                s = data["result"][0]
                return {
                    "rollno": roll,
                    "name": s.get("sname", ""),
                    "fname": s.get("fname", ""),
                    "dob": s.get("dob", ""),
                    "regno": s.get("regno", ""),
                    "mobile": s.get("mobile_no", ""),
                }
        except:
            pass
    return None

def parse_admit_card_html(driver):
    """Extract admit card data from the loaded page"""
    body = driver.find_element(By.TAG_NAME, "body").text
    
    if "Admit Card Not Available" in body:
        return {"available": False, "reason": "Not Available"}
    
    if len(body) < 100:
        return {"available": False, "reason": f"Empty page ({len(body)} chars)"}
    
    result = {"available": True, "subjects": [], "raw_text": body[:1000]}
    
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr, .table tr")
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td, th")
            row_text = [c.text.strip() for c in cells if c.text.strip()]
            if row_text:
                joined = " | ".join(row_text)
                if any(x in joined for x in ["MJ", "MN", "Major", "Minor", "VAC", "AEC", "SEC"]):
                    result["subjects"].append(joined)
                elif "Registration" in joined and "No" in joined:
                    result["reg_no"] = row_text[-1] if len(row_text) > 1 else ""
                elif "Name" in joined and "Student" in joined:
                    result["student_name"] = row_text[-1] if len(row_text) > 1 else ""
                elif "Center" in joined:
                    result["center"] = row_text[-1] if len(row_text) > 1 else ""
                elif "Roll Number" in joined or "IDR" in joined:
                    result["idr"] = row_text[-1] if len(row_text) > 1 else ""
                elif "Commencement" in joined:
                    result["exam_date"] = row_text[-1] if len(row_text) > 1 else ""
    except Exception as e:
        result["parse_error"] = str(e)[:100]
    
    return result

# ============================================================
print("=" * 80)
print("KOLHAN UNIVERSITY — ADMIT CARD DATA CHECKER (MJ-06 Paper)")
print("Semester: IV | Exam: FYUGP Under NEP 4th Semester 2025")
print("=" * 80)

# Step 1: Get DOB
print("\n📋 STEP 1: Fetching DOB from Result API...")
students = []
for roll in ROLLS_2022:
    info = fetch_dob(roll)
    if info and info["dob"]:
        students.append(info)
        print(f"  ✓ {roll} | {info['name']:25s} | DOB: {info['dob']}")
    else:
        print(f"  ✗ {roll} — No DOB found")
print(f"\n  Total: {len(students)}/{len(ROLLS_2022)}")

# Step 2: Check admit cards via Selenium
print(f"\n📄 STEP 2: Checking admit cards...")
print("-" * 80)

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")
opts.add_argument("--window-size=1050,1400")

driver = webdriver.Chrome(options=opts)
results = []

try:
    for i, student in enumerate(students):
        roll = student["rollno"]
        dob = student["dob"]
        name = student["name"]
        
        print(f"\n  [{i+1}/{len(students)}] {roll} | {name} | DOB: {dob}")
        
        driver.get(BASE_URL + "/login")
        time.sleep(3)
        
        # KEY FIX: Use ROLL NUMBER as IDR, semester=4
        js_fill = f"""
        (function() {{
            var form = document.getElementById('formUgsem2');
            if (!form) return 'ERROR: no form';
            
            var semSelect = form.querySelector('select[name="sem"]');
            if (semSelect) semSelect.value = '4';
            
            // Trigger change to show hidden fields
            semSelect.dispatchEvent(new Event('change', {{bubbles: true}}));
            
            // Force show hidden divs
            var dobDiv = form.querySelector('.ugdob');
            var rollDiv = form.querySelector('.ugrollno');
            if (dobDiv) dobDiv.style.display = 'block';
            if (rollDiv) rollDiv.style.display = 'block';
            
            // Fill DOB
            var dobInput = form.querySelector('input[name="dob"]');
            if (dobInput) {{
                dobInput.removeAttribute('readonly');
                dobInput.value = '{dob}';
            }}
            
            // Fill ROLL NUMBER as IDR (this is the key!)
            var rollInput = form.querySelector('input[name="rollno"]');
            if (rollInput) rollInput.value = '{roll}';
            
            form.submit();
            return 'OK: sem=4, dob={dob}, idr={roll}';
        }})();
        """
        
        fill_result = driver.execute_script(js_fill)
        print(f"    Form: {fill_result}")
        time.sleep(4)
        
        # Parse response
        admit_data = parse_admit_card_html(driver)
        
        if admit_data["available"]:
            subjects = admit_data.get("subjects", [])
            center = admit_data.get("center", "N/A")
            exam_date = admit_data.get("exam_date", "N/A")
            has_mj06 = any("MJ - 06" in s or "MJ-06" in s for s in subjects)
            
            print(f"    ✓ ADMIT CARD AVAILABLE!")
            print(f"    Center: {center}")
            for s in subjects:
                marker = " ← MJ-06!" if ("MJ - 06" in s or "MJ-06" in s) else ""
                exempted = " [EXEMPTED]" if "Exempted" in s else ""
                print(f"      • {s}{marker}{exempted}")
            
            results.append({
                "rollno": roll, "name": name, "dob": dob,
                "mobile": student.get("mobile", ""),
                "available": True, "has_mj06": has_mj06,
                "subjects": subjects, "center": center,
                "exam_date": exam_date,
            })
        else:
            reason = admit_data.get("reason", "Unknown")
            print(f"    ✗ {reason}")
            results.append({
                "rollno": roll, "name": name, "dob": dob,
                "available": False, "reason": reason,
            })

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    driver.quit()

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("SUMMARY — MJ-06 ADMIT CARD STATUS")
print("=" * 80)

available = [r for r in results if r["available"]]
not_available = [r for r in results if not r["available"]]
with_mj06 = [r for r in results if r.get("has_mj06")]

print(f"\n  Total checked: {len(results)}")
print(f"  ✓ Admit cards available: {len(available)}")
print(f"  ✗ Not available: {len(not_available)}")
print(f"  📝 With MJ-06 paper: {len(with_mj06)}")

if available:
    print(f"\n  {'#':3s} {'Roll':15s} {'Name':25s} {'MJ-06':6s} {'Center':35s} {'Papers':6s}")
    print(f"  {'-'*3} {'-'*15} {'-'*25} {'-'*6} {'-'*35} {'-'*6}")
    for idx, r in enumerate(available, 1):
        mj06 = "YES" if r.get("has_mj06") else "NO"
        papers = len(r.get("subjects", []))
        center = r.get("center", "N/A")[:35]
        print(f"  {idx:3d} {r['rollno']:15s} {r['name']:25s} {mj06:6s} {center:35s} {papers:6d}")

if not_available:
    print(f"\n  Students WITHOUT admit cards:")
    for r in not_available:
        print(f"  {r['rollno']} | {r['name']}")

# Save JSON
OUTPUT_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\admit_cards"
os.makedirs(OUTPUT_DIR, exist_ok=True)
json_path = os.path.join(OUTPUT_DIR, "mj06_admitcard_results.json")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n  JSON saved: {json_path}")
print("=" * 80)
