import os
import json
import shutil

# ── PATHS ────────────────────────────────────────────────────────────────────
PHY_JSON_PATH    = r"C:\Users\Anurag\Documents\GitHub\Sem6_2022_all\Phy_sem6_2022\merged_physics_students.json"
PHY_PDF_SRC_DIR  = r"C:\Users\Anurag\Documents\GitHub\Sem6_2022_all\Phy_sem6_2022\pdfs"

MASTER_JSON_PATH  = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results_sem6_master.json"
PDF_DEST_DIR      = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\pdfs\results\sem6_2022"
RESULTS_JSON_PATH = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results.json"

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

    # Recalculate grand_total from subject totals (fixes website errors)
    all_totals = [s.get(f"major_{k}_total") for k in ["xii","xiii","xiv","xv"]]
    all_totals.append(s.get("minor_iic_total"))
    correct_total = int(sum(t for t in all_totals if t is not None))
    stated_total  = int(s["grand_total"])
    if correct_total != stated_total:
        print(f"  [FIX] {s['student_name']} ({s['roll_number']}): "
              f"grand_total {stated_total} -> {correct_total} (recalculated from subjects)")

    return {
        "student_name": s["student_name"].strip(),
        "roll_number":  str(s["roll_number"]).strip(),
        "result":       s["result"].strip(),
        "grand_total":  correct_total,
        "subjects":     subjects,
    }

# ── STEP 1: Load master JSON (Maths only, 68 students) ───────────────────────
print("Loading master JSON (Maths only)...")
with open(MASTER_JSON_PATH, "r", encoding="utf-8-sig") as f:
    master = json.load(f)
existing_rolls = {entry["roll_number"] for entry in master}
print(f"  Existing Maths students: {len(master)}")

# ── STEP 2: Load, fix & transform PHY JSON ───────────────────────────────────
print("\nLoading Physics JSON...")
with open(PHY_JSON_PATH, "r", encoding="utf-8") as f:
    phy_raw = json.load(f)
print(f"  PHY records: {len(phy_raw)}")

added = 0
skipped = 0
for record in phy_raw:
    roll = str(record.get("roll_number", "")).strip()
    if not roll:
        continue
    if roll in existing_rolls:
        print(f"  [SKIP] Roll {roll} already in master.")
        skipped += 1
        continue
    transformed = transform_phy_student(record)
    master.append(transformed)
    existing_rolls.add(roll)
    added += 1

print(f"\n  Added:   {added} Physics students")
if skipped:
    print(f"  Skipped: {skipped} duplicates")
print(f"  Total in master: {len(master)}")

# ── STEP 3: Sort by grand_total descending ────────────────────────────────────
master.sort(key=lambda x: x["grand_total"], reverse=True)

# ── STEP 4: Write master JSON ─────────────────────────────────────────────────
with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=4)
print(f"\nMaster JSON saved -> {MASTER_JSON_PATH}")

# ── STEP 5: Copy all 44 PHY PDFs to website ───────────────────────────────────
print("\nCopying Physics PDFs to website...")
os.makedirs(PDF_DEST_DIR, exist_ok=True)
pdf_files = [f for f in os.listdir(PHY_PDF_SRC_DIR) if f.lower().endswith(".pdf")]
copied = 0
for pdf_file in pdf_files:
    shutil.copy2(os.path.join(PHY_PDF_SRC_DIR, pdf_file),
                 os.path.join(PDF_DEST_DIR, pdf_file))
    copied += 1
print(f"  Copied: {copied} PDFs")
total_pdfs = len([f for f in os.listdir(PDF_DEST_DIR) if f.endswith(".pdf")])
print(f"  Total PDFs in website folder: {total_pdfs}")

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
            "desc":    f"Physics major results added ({added} students). Chemistry results are pending."
        })
        break

for ann in config.get("announcements", []):
    if ann.get("id") == "res-ug-sem6-science":
        ann["title"] = "UG Semester 6 Science Streams (Session 2022-26) [Maths + Physics Live]"
        break

with open(RESULTS_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
print("  results.json -> 'Maths + Physics Live'")

# ── SUMMARY ───────────────────────────────────────────────────────────────────
print("\n" + "="*55)
print("[SUCCESS] Physics integration complete!")
print(f"  Maths students:       68")
print(f"  Physics students:     {added}")
print(f"  Total master JSON:    {len(master)}")
print(f"  Total PDFs (website): {total_pdfs}")
print("="*55)
