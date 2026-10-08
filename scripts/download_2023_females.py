"""
Ultra-Fast Multi-Threaded Photo Downloader — Tata College (2023 Batch, Female Students)
Downloads ONLY female student photos using 8 concurrent workers.
Saves to: C:\\Users\\Anurag\\Documents\\GitHub\\Photos\\2023_batch\\female\\
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
COLLEGE = "Tata College"
BATCH = "2023"
SEMESTER = "4"               # Sem 4 admit cards are currently active for 2023 batch
FALLBACK_SEMS = ["1", "7"]
MAX_WORKERS = 8              # 8 parallel workers for ~15 min completion
BASE_URL = "https://www.kuuniv.in"

PHOTOS_ROOT = r"C:\Users\Anurag\Documents\GitHub\Photos"
SAVE_DIR = os.path.join(PHOTOS_ROOT, "2023_batch", "female")
METADATA_DIR = os.path.join(PHOTOS_ROOT, "2023_batch")

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)
# =======================================================

HDRS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

FEMALE_KEYWORDS = {
    "KUMARI", "DEVI", "RANI", "KHATOON", "PARVEEN", "BEGUM", "BAI", "PARBIN", "LATA", "BALA",
    "KHUSHBU", "SHIVANI", "URMILA", "GORATI", "KIRAN", "PURNIMA", "SITA", "LAXMI", "JAYANTI",
    "SHASHI", "YASHODA", "ANITA", "SUMITRA", "TANU", "BABITA", "DIYA", "PRIYANKA", "AMISHA",
    "ANISHA", "CHANDMUNI", "ANKITA", "FULO", "PRITI", "KAJAL", "NIKITA", "SUNITA", "REENA",
    "PUJA", "MANISHA", "MAHNAAZ", "JYOTI", "PRATIVHA", "PRATIBHA", "SARITA", "BINITA", "SUMI",
    "SALMI", "GURUBARI", "SUKMATI", "DULARI", "MUGALI", "SANJANA", "POOJA", "SIMRAN", "SWATI",
    "PAYAL", "RASHMI", "MAMTA", "GEETA", "SHIKHA", "SONI", "SONIA", "BABY", "PINKI", "PINKY",
    "SHITAL", "RUPALI", "SWEETY", "ARTI", "SHANTI", "TULSI", "SUSHILA", "SARASWATI", "MEENA",
    "CHAMPA", "SANJITA", "MALTI", "PRAMILA", "MADHU", "REKHA", "ANNA", "SALONI", "SNEHA",
    "KAVITA", "ARCHANA", "ASHA", "USHA", "SEEMA", "RITA", "REETA", "NEHA", "MONIKA", "NISHA",
    "SUGGI", "ANJALI", "GITANJALI", "BANDNA", "BANDANA", "DURGI", "SARSWATI", "SUKHMATI"
}

# Thread-safe counters and lock
lock = threading.Lock()
stats = {
    "processed": 0,
    "female_photos_downloaded": 0,
    "female_already_existing": 0,
    "males_skipped": 0,
    "no_admit_card": 0,
    "no_dob": 0,
}
results_log = []


def load_2023_rolls():
    """Aggregate all 2023 batch Tata College roll numbers from local data sources."""
    import glob
    rolls = set()

    # 1. sem3_2023_batch json files
    for f in glob.glob(r"C:\Users\Anurag\Documents\GitHub\sem3_2023_batch\*.json"):
        if "cleaned" in f: continue
        try:
            with open(f, "r", encoding="utf-8") as fp:
                d = json.load(fp)
                for dept, st_dict in d.get("results", {}).items():
                    if isinstance(st_dict, dict):
                        for lst in st_dict.values():
                            for r in lst:
                                if str(r).startswith("241305"):
                                    rolls.add(str(r))
        except Exception:
            pass

    # 2. roll_number_2023_batch_full txt files
    for f in glob.glob(r"C:\Users\Anurag\Documents\GitHub\roll_number_2023_batch_full\*.txt"):
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                for line in fp:
                    l = line.strip()
                    if l.startswith("241305"):
                        rolls.add(l)
        except Exception:
            pass

    sorted_rolls = sorted(list(rolls))
    return sorted_rolls


def get_dob_from_api(rollno):
    """Fetch student name & DOB from Result API."""
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
    """Fetch admit card HTML and extract Gender + Photo URL."""
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

                # Extract Gender
                g_match = re.search(r"id=[\"']gender[\"'][^>]*>([^<]+)<", html, re.I)
                gender = g_match.group(1).strip() if g_match else "Unknown"

                # Extract Photo
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

                return gender, photo_url, f"Sem {sem}"
        except Exception:
            time.sleep(0.5)

    return "Unknown", None, "No Admit Card"


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


def process_single_student(rollno, total_students, start_time):
    """Worker task for a single student."""
    name, dob = get_dob_from_api(rollno)

    if not dob:
        with lock:
            stats["processed"] += 1
            stats["no_dob"] += 1
            p = stats["processed"]
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | {rollno} | ⚠️ No DOB found")
        return {"rollno": rollno, "name": name, "status": "no_dob"}

    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name).strip("_")
    filename = f"{safe_name}_{rollno}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)

    # Check if already downloaded
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        with lock:
            stats["processed"] += 1
            stats["female_already_existing"] += 1
            p = stats["processed"]
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | {name[:18]:18s} | 🌸 FEMALE | ⏩ Already exists")
        return {"rollno": rollno, "name": name, "gender": "Female", "status": "already_exists", "filename": filename}

    gender, photo_url, sem_info = fetch_admit_card(rollno, dob)

    # Check if female
    is_female = (gender.lower() == "female") or any(k in set(re.findall(r"[A-Z]+", name.upper())) for k in FEMALE_KEYWORDS)

    if not is_female and gender.lower() == "male":
        with lock:
            stats["processed"] += 1
            stats["males_skipped"] += 1
            p = stats["processed"]
            # Print brief notice
            if p % 10 == 0 or stats["processed"] <= 20:
                print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | {name[:18]:18s} | 👦 MALE   | ⏭️ Skipped")
        return {"rollno": rollno, "name": name, "gender": "Male", "status": "male_skipped"}

    if not photo_url:
        with lock:
            stats["processed"] += 1
            stats["no_admit_card"] += 1
            p = stats["processed"]
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | {name[:18]:18s} | ❓ {gender:6s} | ❌ No admit card")
        return {"rollno": rollno, "name": name, "gender": gender, "status": "no_admit_card"}

    # Download female photo
    img_size = download_photo(photo_url, filepath)
    with lock:
        stats["processed"] += 1
        p = stats["processed"]
        elapsed = time.time() - start_time
        rate = p / elapsed if elapsed > 0 else 1
        eta_min = (total_students - p) / rate / 60 if rate > 0 else 0

        if img_size:
            stats["female_photos_downloaded"] += 1
            size_kb = img_size // 1024
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) [ETA: {eta_min:4.1f}m] | {name[:18]:18s} | 🌸 FEMALE | ✅ SAVED ({size_kb} KB)")
            res = {"rollno": rollno, "name": name, "dob": dob, "gender": "Female", "status": "downloaded", "filename": filename, "size_kb": size_kb}
        else:
            stats["no_admit_card"] += 1
            print(f"[{p:4d}/{total_students}] ({p/total_students*100:5.1f}%) | {name[:18]:18s} | 🌸 FEMALE | ⚠️ Download failed")
            res = {"rollno": rollno, "name": name, "dob": dob, "gender": "Female", "status": "failed"}

        results_log.append(res)
        return res


def main():
    print("=" * 70)
    print("  🚀 KU ULTRA-FAST PHOTO DOWNLOADER — TATA COLLEGE (2023 BATCH)")
    print(f"  Target: FEMALE STUDENTS ONLY | Workers: {MAX_WORKERS} Concurrent Threads")
    print(f"  Saving to: {SAVE_DIR}")
    print("=" * 70)

    rolls = load_2023_rolls()
    total = len(rolls)
    print(f"Total 2023 batch roll numbers to process: {total}\n")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_student, roll, total, start_time): roll for roll in rolls}
        for f in as_completed(futures):
            try:
                f.result()
            except Exception as e:
                pass

    total_time_min = (time.time() - start_time) / 60
    print("\n" + "=" * 70)
    print("🎉 2023 BATCH FEMALE PHOTO DOWNLOAD COMPLETE!")
    print(f"Total Time Taken              : {total_time_min:.2f} minutes")
    print(f"Total Students Processed      : {stats['processed']} / {total}")
    print(f"Female Photos Downloaded      : {stats['female_photos_downloaded']}")
    print(f"Female Photos Already Present : {stats['female_already_existing']}")
    print(f"Total Female Photos on Disk   : {stats['female_photos_downloaded'] + stats['female_already_existing']}")
    print(f"Male Students Skipped         : {stats['males_skipped']}")
    print(f"No Admit Card / Unavailable   : {stats['no_admit_card'] + stats['no_dob']}")
    print(f"Saved Folder                  : {SAVE_DIR}")
    print("=" * 70)

    # Save detailed metadata
    results_path = os.path.join(METADATA_DIR, "female_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results_log, f, indent=2, ensure_ascii=False)
    print(f"Results log saved: {results_path}")


if __name__ == "__main__":
    main()
