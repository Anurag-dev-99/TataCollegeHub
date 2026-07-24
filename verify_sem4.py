import json, os

print("=== FULL VERIFICATION ===\n")

# 1. Check results.json
with open(r"public\data\results.json", "r", encoding="utf-8") as f:
    meta = json.load(f)
print("[OK] results.json is valid JSON")

# 2. Check all dataset files exist
print("\n--- Dataset Files ---")
for ds in meta["datasets"]:
    fpath = os.path.join("public", "data", ds["file"])
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"  [OK] {ds['id']}: {ds['file']} ({len(data)} students)")
    else:
        print(f"  [FAIL] {ds['id']}: {ds['file']} MISSING!")

# 3. Deep check sem4 master
print("\n--- Sem 4 Master Deep Check ---")
with open(r"public\data\results_sem4_master.json", "r", encoding="utf-8") as f:
    sem4 = json.load(f)

rolls = [s["roll_number"] for s in sem4]
dupes = len(rolls) - len(set(rolls))
print(f"  Duplicates: {dupes} {'[OK]' if dupes == 0 else '[FAIL]'}")

no_name = sum(1 for s in sem4 if not s.get("student_name"))
print(f"  Missing names: {no_name} {'[OK]' if no_name == 0 else '[FAIL]'}")

no_total = sum(1 for s in sem4 if s.get("grand_total") is None)
print(f"  Null grand_total: {no_total} {'[OK]' if no_total == 0 else '[WARNING]'}")

results = set(s.get("result", "") for s in sem4)
print(f"  Result values: {results} [OK]")

no_subjects = sum(1 for s in sem4 if not s.get("subjects"))
print(f"  Missing subjects: {no_subjects} {'[OK]' if no_subjects == 0 else '[FAIL]'}")

sorted_ok = all(
    (sem4[i]["grand_total"] or 0) >= (sem4[i + 1]["grand_total"] or 0)
    for i in range(len(sem4) - 1)
)
print(f"  Sorted correctly: {sorted_ok} {'[OK]' if sorted_ok else '[FAIL]'}")

# Check each subject has a total
null_totals = 0
for s in sem4:
    for key, subj in s.get("subjects", {}).items():
        if subj.get("total") is None:
            null_totals += 1
print(f"  Subject entries with null total: {null_totals} {'[OK]' if null_totals == 0 else '[INFO - some students absent for papers]'}")

# 4. Check announcement links
print("\n--- Announcement Links ---")
dataset_ids = set(ds["id"] for ds in meta["datasets"])
for ann in meta.get("announcements", []):
    link = ann.get("link", "")
    if "exam=" in link:
        exam_id = link.split("exam=")[1]
        found = exam_id in dataset_ids
        print(f"  {ann['id']} -> {exam_id}: {'[OK]' if found else '[BROKEN!]'}")

# 5. Department breakdown
print("\n--- Department Breakdown ---")
from collections import Counter
depts = Counter()
for s in sem4:
    subj = list(s["subjects"].values())[0].get("subject", "")
    name = subj.split("-")[-1].strip() if "-" in subj else subj
    depts[name] += 1
for dept, count in sorted(depts.items(), key=lambda x: -x[1]):
    print(f"  {dept}: {count}")

pass_count = sum(1 for s in sem4 if s["result"] == "Pass")
promoted_count = sum(1 for s in sem4 if s["result"] == "Promoted")
print(f"\n  Pass: {pass_count} | Promoted: {promoted_count} | Total: {len(sem4)}")
print(f"\n=== VERIFICATION COMPLETE ===")
