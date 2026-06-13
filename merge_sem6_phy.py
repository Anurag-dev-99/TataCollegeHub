import os
import json
import shutil

# ── PATHS ────────────────────────────────────────────────────────────────────
PHY_JSON_PATH     = r"C:\Users\Anurag\Documents\GitHub\semester6PHY\sem6_2022_phy_Merged.json"
PHY_PDF_SRC_DIR   = r"C:\Users\Anurag\Documents\GitHub\semester6PHY\Phy_sem6_2022\pdfs"

MASTER_JSON_PATH  = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results_sem6_master.json"
PDF_DEST_DIR      = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\pdfs\results\sem6_2022"
RESULTS_JSON_PATH = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results.json"

# ── TRANSFORM: flat PHY record → nested website schema ───────────────────────
def transform_phy_student(s):
    subjects = {}

    for key in ["major_xii", "major_xiii", "major_xiv", "major_xv"]:
        subj_name = s.get(f"{key}_subject")
        if subj_name:
            roman = key.split("_")[1].upper()   # XII, XIII, XIV, XV
            subjects[key] = {
                "subject":    f"MAJOR-{roman}-{subj_name}",
                "theory":     s.get(f"{key}_theory"),
                "internal":   s.get(f"{key}_internal"),
                "practical":  s.get(f"{key}_practical"),
                "total":      s.get(f"{key}_total"),
            }

    if s.get("minor_iic_subject"):
        subjects["minor_iic"] = {
            "subject":   f"Minor-IIC-{s['minor_iic_subject']}",
            "theory":    s.get("minor_iic_theory"),
            "internal":  s.get("minor_iic_internal"),
            "practical": s.get("minor_iic_practical"),
            "total":     s.get("minor_iic_total"),
        }

    return {
        "student_name": s["student_name"].strip(),
        "roll_number":  str(s["roll_number"]).strip(),
        "result":       s["result"].strip(),
        "grand_total":  int(s["grand_total"]),
        "subjects":     subjects,
    }

# ── STEP 1: Load existing master JSON ────────────────────────────────────────
print("Loading existing master JSON...")
with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
    master = json.load(f)

existing_rolls = {entry["roll_number"] for entry in master}
print(f"  Current students in master: {len(master)}")

# ── STEP 2: Load & transform PHY JSON ────────────────────────────────────────
print("\nLoading Physics JSON...")
with open(PHY_JSON_PATH, "r", encoding="utf-8") as f:
    phy_raw = json.load(f)

print(f"  PHY records found: {len(phy_raw)}")

added = 0
skipped = 0
for record in phy_raw:
    roll = str(record.get("roll_number", "")).strip()
    if not roll:
        print("  WARNING: Record with no roll number - skipping.")
        continue
    if roll in existing_rolls:
        print(f"  INFO: Roll {roll} already exists in master (same student in Maths) - skipping duplicate.")
        skipped += 1
        continue

    transformed = transform_phy_student(record)
    master.append(transformed)
    existing_rolls.add(roll)
    added += 1

print(f"\n  Added:   {added} Physics students")
print(f"  Skipped: {skipped} duplicates")
print(f"  Total in master after merge: {len(master)}")

# ── STEP 3: Sort master by grand_total descending (optional but nice) ─────────
master.sort(key=lambda x: x["grand_total"], reverse=True)

# ── STEP 4: Write updated master JSON ────────────────────────────────────────
with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=4)
print(f"\nMaster JSON updated -> {MASTER_JSON_PATH}")

# ── STEP 5: Copy PHY PDFs to website ─────────────────────────────────────────
print("\nCopying Physics PDFs to website...")
os.makedirs(PDF_DEST_DIR, exist_ok=True)

phy_rolls_added = {str(r["roll_number"]).strip() for r in phy_raw}
copied = 0
missing = 0

for roll in phy_rolls_added:
    src = os.path.join(PHY_PDF_SRC_DIR, f"{roll}.pdf")
    dst = os.path.join(PDF_DEST_DIR, f"{roll}.pdf")
    if os.path.exists(src):
        shutil.copy2(src, dst)
        copied += 1
    else:
        print(f"  WARNING: PDF not found for roll {roll}")
        missing += 1

print(f"  Copied: {copied} PDFs")
if missing:
    print(f"  Missing: {missing} PDFs (no PDF file found for those rolls)")

# ── STEP 6: Update results.json status ───────────────────────────────────────
print("\nUpdating results.json dataset status...")
with open(RESULTS_JSON_PATH, "r", encoding="utf-8") as f:
    results_config = json.load(f)

updated = False
for dataset in results_config.get("datasets", []):
    if dataset.get("id") == "sem6_master_2022-2026":
        dataset["status"] = "Maths + Physics Live"
        dataset["title"] = "Semester 6 - Science Streams (Maths + Physics Live)"

        # Add Physics update entry
        updates = dataset.setdefault("updates", [])
        updates.append({
            "version": "2.0",
            "title": "Physics Results Live",
            "desc": f"Physics major results published ({added} students). Chemistry results are pending."
        })
        updated = True
        break

# Also update the announcement title
for ann in results_config.get("announcements", []):
    if ann.get("id") == "res-ug-sem6-science":
        ann["title"] = "UG Semester 6 Science Streams (Session 2022-26) [Maths + Physics Live]"
        break

with open(RESULTS_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(results_config, f, ensure_ascii=False, indent=2)

if updated:
    print("  results.json status updated to 'Maths + Physics Live'")
else:
    print("  WARNING: sem6_master_2022-2026 dataset not found in results.json!")

print("\n[SUCCESS] Physics integration complete!")
print(f"  Master JSON: {len(master)} total students (Maths + Physics)")
print(f"  PDFs in website: {copied} new Physics PDFs copied")
print(f"  Website status: Maths + Physics Live")
