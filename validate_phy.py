import json, re, os, unicodedata

PHY_JSON = r"C:\Users\Anurag\Documents\GitHub\Sem6_2022_all\Phy_sem6_2022\merged_physics_students.json"
PDF_DIR  = r"C:\Users\Anurag\Documents\GitHub\Sem6_2022_all\Phy_sem6_2022\pdfs"

with open(PHY_JSON, "r", encoding="utf-8") as f:
    phy = json.load(f)

print(f"Total PHY records: {len(phy)}")

# 1. Roll number format check
bad_rolls = [s for s in phy if not str(s["roll_number"]).strip().isdigit()]
print(f"\n[1] Bad roll numbers: {len(bad_rolls)}")
for s in bad_rolls:
    print(f"    {s['roll_number']} - {s['student_name']}")

# 2. Non-Latin characters in names
bad_names = []
for s in phy:
    for ch in s["student_name"]:
        if unicodedata.category(ch)[0] not in ("L","Z","P","N"):
            bad_names.append(s)
            break
print(f"\n[2] Names with non-Latin chars: {len(bad_names)}")
for s in bad_names:
    print(f"    {repr(s['student_name'])} (roll {s['roll_number']})")

# 3. Grand total vs sum check
mismatch = []
for s in phy:
    totals = [s.get(f"major_{k}_total") for k in ["xii","xiii","xiv","xv"]]
    totals.append(s.get("minor_iic_total"))
    calc = sum(t for t in totals if t is not None)
    if int(calc) != int(s["grand_total"]):
        mismatch.append((s["student_name"], s["roll_number"], calc, s["grand_total"]))
print(f"\n[3] Grand total mismatches: {len(mismatch)}")
for name, roll, calc, stated in mismatch:
    print(f"    {name} ({roll}): calculated={calc}, stated={stated}")

# 4. PDF cross-check
pdf_rolls  = {os.path.splitext(f)[0] for f in os.listdir(PDF_DIR) if f.endswith(".pdf")}
json_rolls = {str(s["roll_number"]).strip() for s in phy}
no_pdf     = sorted(json_rolls - pdf_rolls)
no_json    = sorted(pdf_rolls - json_rolls)
print(f"\n[4] PDFs in folder:    {len(pdf_rolls)}")
print(f"    Students in JSON:   {len(json_rolls)}")
print(f"    In JSON, no PDF:    {len(no_pdf)} -> {no_pdf}")
print(f"    Has PDF, not JSON:  {len(no_json)} -> {no_json}")

# 5. Result values
valid = {"Pass","Promoted","Fail"}
bad_res = [s for s in phy if s.get("result") not in valid]
print(f"\n[5] Invalid result values: {len(bad_res)}")
for s in bad_res:
    print(f"    {s['student_name']} -> '{s['result']}'")

# 6. Duplicate roll numbers
rolls_list = [str(s["roll_number"]).strip() for s in phy]
from collections import Counter
dupes = {r:c for r,c in Counter(rolls_list).items() if c > 1}
print(f"\n[6] Duplicate roll numbers: {len(dupes)}")
for r,c in dupes.items():
    print(f"    {r} appears {c} times")

print("\n=== VALIDATION COMPLETE ===")
if not any([bad_rolls, bad_names, mismatch, no_pdf, bad_res, dupes]):
    print("ALL CHECKS PASSED - Safe to integrate!")
else:
    print("Some issues found above - review before integrating.")
