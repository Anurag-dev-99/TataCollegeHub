import os
import re
import json
import shutil

# ── PATHS ────────────────────────────────────────────────────────────────────
PHY_JSON_PATH    = r"C:\Users\Anurag\Documents\GitHub\Sem6_2022_all\Phy_sem6_2022\Phy_sem6_merged.json"
PHY_PDF_SRC_DIR  = r"C:\Users\Anurag\Documents\GitHub\Sem6_2022_all\Phy_sem6_2022\pdfs"

MASTER_JSON_PATH  = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results_sem6_master.json"
PDF_DEST_DIR      = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\pdfs\results\sem6_2022"
RESULTS_JSON_PATH = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results.json"

# ── HELPER: Clean roll numbers like ="[231305779995]" → "231305779995" ────────
def clean_roll(raw):
    raw = str(raw).strip()
    # Remove Excel ="[...]" wrapper
    cleaned = re.sub(r'[="\[\]]+', '', raw)
    return cleaned.strip()

# ── TRANSFORM: flat PHY record → nested website schema ───────────────────────
def transform_phy_student(s):
    subjects = {}
    for key in ["major_xii", "major_xiii", "major_xiv", "major_xv"]:
        subj_name = s.get(f"{key}_subject")
        if subj_name:
            roman = key.split("_")[1].upper()
            subjects[key] = {
                "subject":   f"MAJOR-{roman}-{subj_name}",
                "theory":    s.get(f"{key}_theory"),
                "internal":  s.get(f"{key}_internal"),
                "practical": s.get(f"{key}_practical"),
                "total":     s.get(f"{key}_total"),
            }
    if s.get("minor_iic_subject"):
        subjects["minor_iic"] = {
            "subject":   f"Minor-IIC-{s['minor_iic_subject']}",
            "theory":    s.get("minor_iic_theory"),
            "internal":  s.get("minor_iic_internal"),
            "practical": s.get("minor_iic_practical"),
            "total":     s.get("minor_iic_total"),
        }
    roll = clean_roll(s["roll_number"])
    return {
        "student_name": s["student_name"].strip(),
        "roll_number":  roll,
        "result":       s["result"].strip(),
        "grand_total":  int(s["grand_total"]),
        "subjects":     subjects,
    }

# ── STEP 1: Load existing master JSON (Maths only, 68 students) ───────────────
print("Loading existing master JSON (Maths only)...")
with open(MASTER_JSON_PATH, "r", encoding="utf-8-sig") as f:
    master = json.load(f)
existing_rolls = {entry["roll_number"] for entry in master}
print(f"  Current students in master: {len(master)}")

# ── STEP 2: Load & transform PHY JSON ────────────────────────────────────────
print("\nLoading Physics JSON...")
with open(PHY_JSON_PATH, "r", encoding="utf-8") as f:
    phy_raw = json.load(f)
print(f"  PHY records found: {len(phy_raw)}")

# Show roll number cleaning in action
print(f"  Sample raw roll: {phy_raw[0]['roll_number']}")
print(f"  After cleaning:  {clean_roll(phy_raw[0]['roll_number'])}")

added = 0
skipped_dup = 0
for record in phy_raw:
    roll_raw = record.get("roll_number", "")
    roll = clean_roll(roll_raw)
    if not roll:
        print(f"  WARNING: Empty roll number after cleaning '{roll_raw}' - skipping.")
        continue
    if roll in existing_rolls:
        print(f"  INFO: Roll {roll} already in master - skipping duplicate.")
        skipped_dup += 1
        continue
    transformed = transform_phy_student(record)
    master.append(transformed)
    existing_rolls.add(roll)
    added += 1

print(f"\n  Added:   {added} Physics students")
if skipped_dup:
    print(f"  Skipped: {skipped_dup} duplicates")
print(f"  Total in master after merge: {len(master)}")

# ── STEP 3: Sort by grand_total descending ────────────────────────────────────
master.sort(key=lambda x: x["grand_total"], reverse=True)

# ── STEP 4: Write updated master JSON ────────────────────────────────────────
with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=4)
print(f"\nMaster JSON saved -> {MASTER_JSON_PATH}")

# ── STEP 5: Copy PHY PDFs to website ─────────────────────────────────────────
print("\nCopying Physics PDFs to website...")
os.makedirs(PDF_DEST_DIR, exist_ok=True)

# Get all PDFs from the source folder
pdf_files = [f for f in os.listdir(PHY_PDF_SRC_DIR) if f.lower().endswith(".pdf")]
copied = 0
already_exists = 0

for pdf_file in pdf_files:
    src = os.path.join(PHY_PDF_SRC_DIR, pdf_file)
    dst = os.path.join(PDF_DEST_DIR, pdf_file)
    if os.path.exists(dst):
        already_exists += 1
        continue
    shutil.copy2(src, dst)
    copied += 1

print(f"  Copied:         {copied} new Physics PDFs")
if already_exists:
    print(f"  Already existed: {already_exists} (skipped)")

# Cross-check: which students in JSON have no PDF?
phy_rolls_in_json = {clean_roll(r["roll_number"]) for r in phy_raw}
pdf_basenames = {os.path.splitext(f)[0] for f in pdf_files}
missing_pdfs = phy_rolls_in_json - pdf_basenames
if missing_pdfs:
    print(f"\n  WARNING: {len(missing_pdfs)} students have no PDF:")
    for r in sorted(missing_pdfs):
        name = next((s["student_name"] for s in phy_raw if clean_roll(s["roll_number"]) == r), "?")
        print(f"    {r} - {name}")
else:
    print("  All students in JSON have a matching PDF.")

# ── STEP 6: Update results.json ───────────────────────────────────────────────
print("\nUpdating results.json...")
with open(RESULTS_JSON_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

for dataset in config.get("datasets", []):
    if dataset.get("id") == "sem6_master_2022-2026":
        dataset["status"] = "Maths + Physics Live"
        dataset["title"]  = "Semester 6 \u2014 Science Streams (Maths + Physics Live)"
        dataset.setdefault("updates", []).append({
            "version": "2.0",
            "title":   "Physics Results Live",
            "desc":    f"Physics major results published ({added} students added). Chemistry results are pending."
        })
        break

for ann in config.get("announcements", []):
    if ann.get("id") == "res-ug-sem6-science":
        ann["title"] = "UG Semester 6 Science Streams (Session 2022-26) [Maths + Physics Live]"
        break

with open(RESULTS_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print("  results.json updated -> 'Maths + Physics Live'")

# ── FINAL SUMMARY ─────────────────────────────────────────────────────────────
print("\n" + "="*55)
print("[SUCCESS] Physics integration complete!")
print(f"  Maths students (existing):  68")
print(f"  Physics students added:     {added}")
print(f"  Total in master JSON:       {len(master)}")
print(f"  New PDFs copied to website: {copied}")
total_pdfs = len(list(os.listdir(PDF_DEST_DIR)))
print(f"  Total PDFs in website:      {total_pdfs}")
print("="*55)
