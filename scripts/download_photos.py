"""
KU Student Photo Downloader
Downloads student photos for Tata College, 2022 batch
Prerequisites: pip install selenium
"""
import sys, re, json, urllib.request, os, time

sys.stdout.reconfigure(encoding="utf-8")

# ============ CONFIGURATION ============
COLLEGE = "Tata College"
BATCH = "2022"
SEMESTER_FOR_ADMIT = "7"   # Which semester's admit card to check
SEMESTER_FOR_API = "VI"    # Which semester to query Result API (use one that has data)
ROLL_START = 231305779800  # Start of roll number range to scan
ROLL_END = 231305780200    # End of roll number range to scan
DELAY = 1.5                # Seconds between requests (to avoid rate limiting)

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos_tata_2022")
os.makedirs(SAVE_DIR, exist_ok=True)
# ========================================

BASE = "https://www.kuuniv.in"
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def get_student_info(rollno):
    """Get student info from Result API"""
    for sem in [SEMESTER_FOR_API, "V", "IV", "VI", "I", "II", "III"]:
        url = f"{BASE}/result/fetch/result/allcourse?course=FYUGP&semester={sem}&stream=nep&rollno={rollno}"
        try:
            req = urllib.request.Request(url, headers=HDRS)
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read().decode())
            if data.get("result") and len(data["result"]) > 0:
                r = data["result"][0]
                return {
                    "name": r.get("sname", "UNKNOWN"),
                    "dob": r.get("dob"),
                    "rollno": str(rollno),
                    "regno": r.get("regno"),
                    "college": r.get("college_name", ""),
                    "fname": r.get("fname", ""),
                }
        except:
            pass
        time.sleep(0.3)
    return None


def main():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    # Phase 1: Find all valid students
    print("=" * 60)
    print(f"PHASE 1: Finding students (roll range {ROLL_START}-{ROLL_END})")
    print("=" * 60)

    students = []
    for roll in range(ROLL_START, ROLL_END + 1):
        info = get_student_info(str(roll))
        if info and COLLEGE.lower() in info["college"].lower():
            students.append(info)
            print(f"  [{len(students):3d}] {info['name'][:25]:25s} | {roll} | DOB: {info['dob']}")
        time.sleep(DELAY)

        # Progress
        if (roll - ROLL_START) % 50 == 0:
            pct = (roll - ROLL_START) / (ROLL_END - ROLL_START) * 100
            print(f"  ... {pct:.0f}% scanned, {len(students)} found so far")

    print(f"\nTotal students found: {len(students)}")

    # Save student list
    students_path = os.path.join(SAVE_DIR, "students.json")
    with open(students_path, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
    print(f"Student list saved: {students_path}")

    # Phase 2: Get photos via admit card
    print(f"\n{'=' * 60}")
    print(f"PHASE 2: Downloading photos via admit card (sem {SEMESTER_FOR_ADMIT})")
    print(f"{'=' * 60}")

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)
    results = []
    success = 0
    failed = 0

    try:
        for i, student in enumerate(students):
            print(f"\n[{i+1}/{len(students)}] {student['name']}...")

            photo_found = False
            for sem in [SEMESTER_FOR_ADMIT, "4", "1"]:
                driver.get(f"{BASE}/login")
                time.sleep(1)

                js_code = f"""
                var form = document.createElement('form');
                form.method = 'POST';
                form.action = '/student/admitcardUgsem2/serch';
                var f1 = document.createElement('input'); f1.name='sem'; f1.value='{sem}'; form.appendChild(f1);
                var f2 = document.createElement('input'); f2.name='dob'; f2.value='{student["dob"]}'; form.appendChild(f2);
                var f3 = document.createElement('input'); f3.name='rollno'; f3.value='{student["rollno"]}'; form.appendChild(f3);
                document.body.appendChild(form);
                form.submit();
                """
                driver.execute_script(js_code)
                time.sleep(3)

                body = driver.find_element(By.TAG_NAME, "body").text

                if "admit card not available" in body.lower():
                    continue

                if student["name"].split()[0].upper() in body.upper():
                    imgs = driver.find_elements(By.TAG_NAME, "img")
                    for img in imgs:
                        src = img.get_attribute("src") or ""
                        if "profileimage" in src and "_IMAGE" in src:
                            photo_id = re.search(r'/profileimage/(\d+)_IMAGE', src)
                            if photo_id:
                                pid = photo_id.group(1)
                                try:
                                    req = urllib.request.Request(src, headers=HDRS)
                                    resp = urllib.request.urlopen(req, timeout=10)
                                    img_data = resp.read()

                                    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', student["name"])
                                    filename = f"{safe_name}_{student['rollno']}.jpg"
                                    filepath = os.path.join(SAVE_DIR, filename)
                                    with open(filepath, "wb") as f:
                                        f.write(img_data)

                                    results.append({**student, "photo_id": pid, "filename": filename, "size_kb": len(img_data) // 1024})
                                    success += 1
                                    print(f"  ✅ Photo ID {pid} | {len(img_data)//1024} KB")
                                    photo_found = True
                                except Exception as e:
                                    print(f"  Download error: {str(e)[:40]}")
                                break
                if photo_found:
                    break

            if not photo_found:
                failed += 1
                results.append({**student, "photo_id": None, "error": "No admit card"})
                print(f"  ❌ No admit card")

            time.sleep(DELAY)

    finally:
        driver.quit()

    # Summary
    print(f"\n{'=' * 60}")
    print(f"COMPLETE! {success} photos downloaded, {failed} failed")
    print(f"{'=' * 60}")

    # Save results
    results_path = os.path.join(SAVE_DIR, "photo_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved: {results_path}")
    print(f"Photos saved in: {SAVE_DIR}")


if __name__ == "__main__":
    main()
