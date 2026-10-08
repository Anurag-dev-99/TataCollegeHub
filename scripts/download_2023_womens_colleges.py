"""
Ultra-Fast Multi-Threaded Photo Downloader — All Women's Colleges (Kolhan University, 2023 Batch)
Downloads photos for all 4 dedicated Women's / Mahila Colleges using 10 concurrent workers.
Saves to categorized folders under: C:\\Users\\Anurag\\Documents\\GitHub\\Photos\\2023_batch\\
"""
import sys
import os
import re
import json
import time
import urllib.request
import urllib.parse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

# ==================== CONFIGURATION ====================
BATCH = "2023"
SEMESTER = "4"               # Sem 4 admit cards are currently active for 2023 batch
FALLBACK_SEMS = ["1", "7"]
MAX_WORKERS = 10             # 10 parallel workers for ~15-18 min completion
BASE_URL = "https://www.kuuniv.in"

PHOTOS_ROOT = r"C:\Users\Anurag\Documents\GitHub\Photos"
BATCH_DIR = os.path.join(PHOTOS_ROOT, "2023_batch")
METADATA_DIR = os.path.join(PHOTOS_ROOT, "2023_batch")

# Target 4 Women's Colleges
WOMENS_COLLEGES = {
    "05A": {
        "name": "The Graduate School College for Women, Jamshedpur",
        "folder": "The_Graduate_School_College_for_Women",
    },
    "11A": {
        "name": "Mahila College, Chaibasa",
        "folder": "Mahila_College_Chaibasa",
    },
    "14A": {
        "name": "B.D.S.L. Mahila College, Ghatshila",
        "folder": "BDSL_Mahila_College_Ghatshila",
    },
    "64A": {
        "name": "Mahila Mahavidyalaya, Seraikella-Kharsawan",
        "folder": "Mahila_Mahavidyalaya_Seraikella",
    },
}

for col_info in WOMENS_COLLEGES.values():
    os.makedirs(os.path.join(BATCH_DIR, col_info["folder"]), exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)
# =======================================================

HDRS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

lock = threading.Lock()
stats = {
    "processed": 0,
    "photos_downloaded": 0,
    "already_existing": 0,
    "no_admit_card": 0,
    "no_dob": 0,
}
college_stats = {code: {"downloaded": 0, "total": 0} for code in WOMENS_COLLEGES}
results_log = []


def load_womens_colleges_students():
    """Load all 2023 batch students from the 4 Women's Colleges."""
    p_master = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\kolhan_sem2_2023_master.json"
    students = []
    
    if os.path.exists(p_master):
        with open(p_master, "r", encoding="utf-8") as f:
            d = json.load(f)
            for x in d:
                code = str(x.get("college_code", "")).upper()
                if code in WOMENS_COLLEGES:
                    roll = str(x.get("rollno", "")).strip()
                    dob = x.get("dob") or x.get("dateofbirth")
                    name = x.get("sname", "STUDENT")
                    regyear = str(x.get("regyear", ""))
                    if roll:
                        students.append({
                            "rollno": roll,
                            "dob": dob,
                            "name": name,
                            "regyear": regyear,
                            "college_code": code,
                            "folder": WOMENS_COLLEGES[code]["folder"],
                            "college_name": WOMENS_COLLEGES[code]["name"]
                        })
                        college_stats[code]["total"] += 1
    return students


def get_dob_from_api(rollno):
    """Fetch student name & DOB from Result API if missing."""
    for sem in ["III", "II", "I"]:
        url = f"{BASE_URL}/result/fetch/result/allcourse?course=FYUGP&semester={sem}&stream=nep&rollno={rollno}"
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
                if data.get("result") and len(data["result"]) > 0:
                    r = data["result"][0]
                    return r.get("sname", "STUDENT"), r.get("dob") or r.get("dateofbirth")
        except Exception:
            pass
        time.sleep(0.2)
    return "UNKNOWN", None


def fetch_admit_card(rollno, dob):
    """Fetch admit card HTML and extract Photo URL."""
    semesters = [SEMESTER] + FALLBACK_SEMS
    post_url = f"{BASE_URL}/student/admitcardUgsem2/serch"

    for sem in semesters:
        post_data = urllib.parse.urlencode({"sem": sem, "dob": dob, "rollno": rollno}).encode("utf-8")
        req = urllib.request.Request(post_url, data=post_data, headers={
            **HDRS,
            "Referer": f"{BASE_URL}/login",
            "Content-Type": "application/x-www-form-urlencoded"
        })
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                if "admit card not available" in html.lower():
                    continue

                photo_match = re.search(r"(/ftpwebapps/ku/resources/studentdata/users/profileimage/[^\s\"\'<>]+\.(?:jpg|jpeg|png)|profileimage/[^\s\"\'<>]+\.(?:jpg|jpeg|png)|profileimage/[^\s\"\'<>]+_IMAGE[^\s\"\'<>]*)", html, re.I)
                photo_url = None
                if photo_match:
                    raw_src = photo_match.group(0)
                    if not raw_src.startswith("http"):
                        if raw_src.startswith("/"):
                            photo_url = f"{BASE_URL}{raw_src}"
                        else:
                            photo_url = f"{BASE_URL}/ftpwebapps/ku/resources/studentdata/users/{raw_src}"
                    else:
                        photo_url = raw_src

                return photo_url, f"Sem {sem}"
        except Exception:
            time.sleep(0.5)

    return None, "No Admit Card"


def download_photo(photo_url, filepath):
    """Download JPEG photo file."""
    req = urllib.request.Request(photo_url, headers={
        **HDRS,
        "Referer": f"{BASE_URL}/student/admitcardUgsem2/serch"
    })
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) > 500:
                    with open(filepath, "wb") as f:
                        f.write(data)
                    return len(data)
        except Exception:
            time.sleep(0.5)
    return None


def process_single_student(st, total_students, start_time):
    """Worker task for a single student."""
    rollno = st["rollno"]
    name = st.get("name", "STUDENT")
    dob = st.get("dob")
    code = st["college_code"]
    folder = st["folder"]
    save_folder = os.path.join(BATCH_DIR, folder)

    if not dob:
        name_api, dob = get_dob_from_api(rollno)
        if name_api and name == "STUDENT":
            name = name_api

    if not dob:
        with lock:
            stats["processed"] += 1
            stats["no_dob"] += 1
            p = stats["processed"]
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | [{code}] {rollno} | ⚠️ No DOB")
        return {"rollno": rollno, "name": name, "status": "no_dob", "college_code": code}

    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name).strip("_")
    filename = f"{safe_name}_{rollno}.jpg"
    filepath = os.path.join(save_folder, filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        with lock:
            stats["processed"] += 1
            stats["already_existing"] += 1
            p = stats["processed"]
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | [{code}] {name[:18]:18s} | ⏩ Already exists")
        return {"rollno": rollno, "name": name, "status": "already_exists", "filename": filename, "college_code": code}

    photo_url, sem_info = fetch_admit_card(rollno, dob)

    if not photo_url:
        with lock:
            stats["processed"] += 1
            stats["no_admit_card"] += 1
            p = stats["processed"]
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | [{code}] {name[:18]:18s} | ❌ No admit card")
        return {"rollno": rollno, "name": name, "status": "no_admit_card", "college_code": code}

    img_size = download_photo(photo_url, filepath)
    with lock:
        stats["processed"] += 1
        p = stats["processed"]
        elapsed = time.time() - start_time
        rate = p / elapsed if elapsed > 0 else 1
        eta_min = (total_students - p) / rate / 60 if rate > 0 else 0

        if img_size:
            stats["photos_downloaded"] += 1
            college_stats[code]["downloaded"] += 1
            size_kb = img_size // 1024
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) [ETA: {eta_min:4.1f}m] | [{code}] {name[:18]:18s} | ✅ SAVED ({size_kb} KB)")
            res = {"rollno": rollno, "name": name, "dob": dob, "status": "downloaded", "filename": filename, "size_kb": size_kb, "college_code": code, "college_name": st["college_name"]}
        else:
            stats["no_admit_card"] += 1
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | [{code}] {name[:18]:18s} | ⚠️ Download failed")
            res = {"rollno": rollno, "name": name, "dob": dob, "status": "failed", "college_code": code}

        results_log.append(res)
        return res


def main():
    print("=" * 75)
    print("  🚀 KU MULTI-THREADED PHOTO DOWNLOADER — ALL WOMEN'S COLLEGES (2023 BATCH)")
    print(f"  Target: 4 WOMEN'S COLLEGES (100% FEMALE) | Workers: {MAX_WORKERS} Concurrent Threads")
    print(f"  Output Directory: {BATCH_DIR}")
    print("=" * 75)

    students = load_womens_colleges_students()
    total = len(students)
    print(f"\nTotal Students Loaded: {total}")
    for code, data in WOMENS_COLLEGES.items():
        print(f"  [{code}] {data['name'][:42]:42s} : {college_stats[code]['total']:5d} students")
    print("-" * 75 + "\n")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_student, st, total, start_time): st["rollno"] for st in students}
        for f in as_completed(futures):
            try:
                f.result()
            except Exception:
                pass

    total_time_min = (time.time() - start_time) / 60
    print("\n" + "=" * 75)
    print("🎉 ALL WOMEN'S COLLEGES PHOTO DOWNLOAD COMPLETE!")
    print(f"Total Time Taken              : {total_time_min:.2f} minutes")
    print(f"Total Students Processed      : {stats['processed']} / {total}")
    print(f"New Photos Downloaded         : {stats['photos_downloaded']}")
    print(f"Previously Existing           : {stats['already_existing']}")
    print(f"Total Photos on Disk          : {stats['photos_downloaded'] + stats['already_existing']}")
    print(f"No Admit Card / Unavailable   : {stats['no_admit_card'] + stats['no_dob']}")
    print("\nBreakdown by College:")
    for code, data in WOMENS_COLLEGES.items():
        print(f"  [{code}] {data['name'][:42]:42s} : {college_stats[code]['downloaded']} photos saved")
    print(f"\nSaved Folder                  : {BATCH_DIR}")
    print("=" * 75)

    results_path = os.path.join(METADATA_DIR, "womens_colleges_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results_log, f, indent=2, ensure_ascii=False)
    print(f"Results log saved: {results_path}")


if __name__ == "__main__":
    main()
