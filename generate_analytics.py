"""
Reads all semester results from public/data/results_semX_master.json,
calculates pass percentages, extracts toppers, and updates results.json.
"""
import json, os, glob

DATA_DIR = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data"
RESULTS_JSON = os.path.join(DATA_DIR, "results.json")
KU_SEM2_STATS = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\cleaned\college_summary.json"

print("Loading results.json...")
results_db = json.load(open(RESULTS_JSON, 'r', encoding='utf-8'))

# --- Calculate Semester Pass Rates ---
print("\nCalculating Semester Pass Rates...")
pass_by_semester = []

# Mapping files to nice display names
sem_files = [
    ("Semester 1", "results_sem1_master.json"),
    ("Semester 2", "results_sem2_master.json"),
    ("Semester 3", "results_sem3_master.json"),
    ("Semester 4", "results_sem4_master.json"),
    ("Semester 6", "results_sem6_master.json")
]

overall_students = 0
overall_passed = 0

all_departments = {}

for sem_name, file_name in sem_files:
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        data = json.load(open(file_path, 'r', encoding='utf-8'))
        total = len(data)
        if total == 0: continue
        
        passed = sum(1 for s in data if str(s.get("result", "")).lower() == "pass")
        pass_rate = round((passed / total) * 100, 1)
        
        overall_students += total
        overall_passed += passed
        
        pass_by_semester.append({
            "semester": sem_name,
            "passPercentage": pass_rate,
            "totalStudents": total
        })
        print(f"  {sem_name}: {pass_rate}% ({total} students)")
        
        # Aggregate department stats
        for s in data:
            # Need to figure out major/department
            dept = "Unknown"
            if "subjects" in s:
                for k, v in s["subjects"].items():
                    if k.startswith("major"):
                        # Extract department name from subject title
                        name = v.get("subject", "")
                        parts = name.split("-")
                        dept = parts[-1].strip() if len(parts) >= 2 else name
                        break
            
            # Clean up dept name if it's messy
            if "Mathematics" in dept or "Math" in dept: dept = "Mathematics"
            elif "Physics" in dept: dept = "Physics"
            elif "Chemistry" in dept: dept = "Chemistry"
            elif "Zoology" in dept: dept = "Zoology"
            elif "Botany" in dept: dept = "Botany"
            elif "Psychology" in dept: dept = "Psychology"
            elif "History" in dept: dept = "History"
            elif "Political Science" in dept: dept = "Political Science"
            elif "Geography" in dept: dept = "Geography"
            elif "Economics" in dept: dept = "Economics"
            elif "Hindi" in dept: dept = "Hindi"
            elif "English" in dept: dept = "English"
            elif "Ho" in dept: dept = "Ho"
            elif "Computer Application" in dept or "CA" == dept: dept = "Computer Application"
            
            if dept != "Unknown" and len(dept) < 30:
                if dept not in all_departments:
                    all_departments[dept] = {"total": 0, "passed": 0, "top_score": 0, "topper": ""}
                
                all_departments[dept]["total"] += 1
                if str(s.get("result", "")).lower() == "pass":
                    all_departments[dept]["passed"] += 1
                
                try:
                    gt = int(s.get("grand_total", 0))
                    if gt > all_departments[dept]["top_score"]:
                        all_departments[dept]["top_score"] = gt
                        all_departments[dept]["topper"] = s.get("student_name", "Unknown")
                except: pass

# --- Get University Average (Sem 2) ---
ku_average = 0
if os.path.exists(KU_SEM2_STATS):
    try:
        ku_data = json.load(open(KU_SEM2_STATS, 'r', encoding='utf-8'))
        ku_average = ku_data.get("overall_pass_rate", 50.9)
    except: pass

# --- Calculate Department Pass Rates ---
print("\nCalculating Department Pass Rates...")
pass_by_dept = []
for dept, stats in sorted(all_departments.items(), key=lambda x: -x[1]["total"]):
    if stats["total"] >= 20: # Only show departments with enough students
        pass_rate = round((stats["passed"] / stats["total"]) * 100, 1)
        pass_by_dept.append({
            "department": dept,
            "passPercentage": pass_rate,
            "toppers": [f"{stats['topper']} ({stats['top_score']} marks)"]
        })
        print(f"  {dept}: {pass_rate}% ({stats['total']} students)")

# Only keep top 6 departments for the UI
pass_by_dept = sorted(pass_by_dept, key=lambda x: -x["passPercentage"])[:6]

# Update the results DB
results_db["passPercentageBySemester"] = pass_by_semester
results_db["passPercentageByDepartment"] = pass_by_dept

# We can replace yearlyTrends with university comparison data
results_db["universityComparison"] = {
    "tataCollege": pass_by_semester[0]["passPercentage"] if pass_by_semester else 40.9,
    "kolhanUniversity": ku_average
}

print("\nUpdating results.json...")
with open(RESULTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(results_db, f, indent=2, ensure_ascii=False)
print("DONE!")
