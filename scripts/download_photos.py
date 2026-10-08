"""
KU Student Photo Downloader — Tata College (2022 Batch, Semester 7)
Fast & Direct HTTP Downloader with Auto-Resume & Safe Rate Limiting.
"""
import sys
import re
import json
import os
import time
import urllib.request
import urllib.parse
import urllib.error

sys.stdout.reconfigure(encoding="utf-8")

# ==================== CONFIGURATION ====================
COLLEGE = "Tata College"
BATCH = "2022"
PRIMARY_SEM = "7"            # Primary semester admit card to check (Sem 7)
FALLBACK_SEMS = ["4", "1"]    # Fallback semesters if Sem 7 admit card is unavailable
DELAY = 0.5                  # 0.5s pause between requests (~9-10 min total runtime)

BASE_URL = "https://www.kuuniv.in"
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos_tata_2022")
LOCAL_DATA_SOURCE = r"C:\Users\Anurag\Documents\GitHub\2022_batch_sem5_result\sem6_all_raw.json"

os.makedirs(SAVE_DIR, exist_ok=True)
# =======================================================

HDRS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def load_students():
    """Load the complete list of Tata College 2022 batch students."""
    students = []
    
    # 1. Try loading from local master sem6 data (1,143 records with DOBs)
    if os.path.exists(LOCAL_DATA_SOURCE):
        try:
            with open(LOCAL_DATA_SOURCE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                for item in raw_data:
                    roll = str(item.get("rollno") or "").strip()
                    dob = str(item.get("dateofbirth") or item.get("dob") or "").strip()
                    name = str(item.get("sname") or "").strip()
                    fname = str(item.get("fname") or "").strip()
                    regno = str(item.get("regno") or "").strip()
                    college = str(item.get("college_name") or COLLEGE).strip()
                    
                    if roll:
                        students.append({
                            "rollno": roll,
                            "dob": dob,
                            "name": name,
                            "fname": fname,
                            "regno": regno,
                            "college": college
                        })
            print(f"Loaded {len(students)} students from local database: {LOCAL_DATA_SOURCE}")
            return students
        except Exception as e:
            print(f"Warning: Could not read local file {LOCAL_DATA_SOURCE}: {e}")

    # 2. Check if students.json already exists in SAVE_DIR
    saved_students_path = os.path.join(SAVE_DIR, "students.json")
    if os.path.exists(saved_students_path):
        try:
            with open(saved_students_path, "r", encoding="utf-8") as f:
                students = json.load(f)
                print(f"Loaded {len(students)} students from existing {saved_students_path}")
                return students
        except Exception as e:
            print(f"Warning: Could not read {saved_students_path}: {e}")

    return students


def get_dob_from_api(rollno):
    """Fetch DOB from KU Result API if not present locally."""
    for sem in ["VI", "V", "IV", "III", "II", "I"]:
        url = f"{BASE_URL}/result/fetch/result/allcourse?course=FYUGP&semester={sem}&stream=nep&rollno={rollno}"
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
                if data.get("result") and len(data["result"]) > 0:
                    r = data["result"][0]
                    return r.get("dob") or r.get("dateofbirth")
        except Exception:
            pass
        time.sleep(0.3)
    return None


def fetch_admit_card_photo(rollno, dob):
    """
    Query the admit card endpoint via direct HTTP POST to extract photo URL.
    Checks primary semester (Sem 7) first, then fallback semesters.
    """
    if not dob:
        return None, "No DOB available"

    semesters_to_check = [PRIMARY_SEM] + [s for s in FALLBACK_SEMS if s != PRIMARY_SEM]
    post_url = f"{BASE_URL}/student/admitcardUgsem2/serch"

    for sem in semesters_to_check:
        post_data = urllib.parse.urlencode({
            "sem": sem,
            "dob": dob,
            "rollno": rollno
        }).encode("utf-8")

        req = urllib.request.Request(post_url, data=post_data, headers={
            **HDRS,
            "Referer": f"{BASE_URL}/login",
            "Content-Type": "application/x-www-form-urlencoded"
        })

        for retry in range(2):
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")

                    if "admit card not available" in html.lower():
                        break

                    # Match profile image URLs like /ftpwebapps/ku/resources/studentdata/users/profileimage/20444553_IMAGE.jpeg
                    photo_match = re.search(r'(/ftpwebapps/ku/resources/studentdata/users/profileimage/[^\s"\'<>]+\.(?:jpg|jpeg|png)|profileimage/[^\s"\'<>]+\.(?:jpg|jpeg|png)|profileimage/[^\s"\'<>]+_IMAGE[^\s"\'<>]*)', html, re.I)
                    if photo_match:
                        raw_src = photo_match.group(0)
                        if not raw_src.startswith("http"):
                            if raw_src.startswith("/"):
                                full_url = f"{BASE_URL}{raw_src}"
                            else:
                                full_url = f"{BASE_URL}/ftpwebapps/ku/resources/studentdata/users/{raw_src}"
                        else:
                            full_url = raw_src
                        return full_url, f"Found in Sem {sem}"
                    
                    break
            except Exception as e:
                time.sleep(1.0)

    return None, "No admit card / photo found"


def download_image(url, filepath):
    """Download JPEG photo and save to disk."""
    req = urllib.request.Request(url, headers={
        **HDRS,
        "Referer": f"{BASE_URL}/student/admitcardUgsem2/serch"
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                if len(data) > 500:  # Valid image (>500 bytes)
                    with open(filepath, "wb") as f:
                        f.write(data)
                    return len(data)
        except Exception as e:
            time.sleep(1.0)
    return None


def main():
    print("=" * 65)
    print(f"  KU Student Photo Downloader — {COLLEGE} ({BATCH} Batch, Sem {PRIMARY_SEM})")
    print(f"  Pause per request: {DELAY}s | Output: {SAVE_DIR}")
    print("=" * 65)

    students = load_students()
    if not students:
        print("❌ Error: No students found. Check data sources.")
        return

    total = len(students)
    print(f"Ready to process {total} students.\n")

    # Save full student master list
    students_path = os.path.join(SAVE_DIR, "students.json")
    with open(students_path, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)

    results = []
    success_count = 0
    skipped_count = 0
    failed_count = 0
    start_time = time.time()

    for idx, st in enumerate(students, 1):
        roll = st["rollno"]
        name = st.get("name", "STUDENT")
        dob = st.get("dob")
        safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name).strip("_")
        filename = f"{safe_name}_{roll}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)

        pct = (idx / total) * 100
        elapsed = time.time() - start_time
        avg_per_item = elapsed / idx
        est_remaining_sec = avg_per_item * (total - idx)
        est_rem_min = est_remaining_sec / 60

        prefix = f"[{idx:4d}/{total}] ({pct:5.1f}%) [ETA: {est_rem_min:4.1f}m] {name[:20]:20s} | {roll}"

        # Resume support: skip if photo already downloaded
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            size_kb = os.path.getsize(filepath) // 1024
            print(f"{prefix} | ⏩ Already downloaded ({size_kb} KB)")
            results.append({**st, "status": "already_downloaded", "filename": filename, "size_kb": size_kb})
            skipped_count += 1
            continue

        # Get DOB if missing
        if not dob:
            dob = get_dob_from_api(roll)
            st["dob"] = dob

        # Fetch Admit Card Photo URL
        photo_url, status_msg = fetch_admit_card_photo(roll, dob)

        if photo_url:
            img_size = download_image(photo_url, filepath)
            if img_size:
                size_kb = img_size // 1024
                print(f"{prefix} | ✅ Photo saved ({size_kb} KB) - {status_msg}")
                results.append({**st, "status": "success", "photo_url": photo_url, "filename": filename, "size_kb": size_kb})
                success_count += 1
            else:
                print(f"{prefix} | ⚠️ Photo URL found but download failed")
                results.append({**st, "status": "download_failed", "photo_url": photo_url})
                failed_count += 1
        else:
            print(f"{prefix} | ❌ {status_msg}")
            results.append({**st, "status": "no_photo", "error": status_msg})
            failed_count += 1

        time.sleep(DELAY)

    # Summary
    total_time_min = (time.time() - start_time) / 60
    print("\n" + "=" * 65)
    print("DOWNLOAD TASK COMPLETE!")
    print(f"Total time elapsed : {total_time_min:.2f} minutes")
    print(f"New Photos Downloaded: {success_count}")
    print(f"Previously Downloaded : {skipped_count}")
    print(f"Total Available Photos: {success_count + skipped_count} / {total}")
    print(f"No Photo / Unavailable: {failed_count}")
    print(f"Saved Directory       : {SAVE_DIR}")
    print("=" * 65)

    # Save detailed JSON summary
    results_path = os.path.join(SAVE_DIR, "photo_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Detailed log saved to: {results_path}")


if __name__ == "__main__":
    main()
