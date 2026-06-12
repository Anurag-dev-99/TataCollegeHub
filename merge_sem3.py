import os
import json

def transform_student(student):
    subjects = {}
    
    # Major IV
    if student.get("major_iv_subject"):
        subjects["major_iv"] = {
            "subject": f"MAJOR-IV-{student['major_iv_subject']}",
            "theory": student.get("major_iv_theory"),
            "internal": student.get("major_iv_internal"),
            "practical": student.get("major_iv_practical"),
            "total": student.get("major_iv_total")
        }
        
    # Major V
    if student.get("major_v_subject"):
        subjects["major_v"] = {
            "subject": f"MAJOR-V-{student['major_v_subject']}",
            "theory": student.get("major_v_theory"),
            "internal": student.get("major_v_internal"),
            "practical": student.get("major_v_practical"),
            "total": student.get("major_v_total")
        }
        
    # Minor IB
    if student.get("minor_ib_subject"):
        subjects["minor_ib"] = {
            "subject": f"Minor-IB-{student['minor_ib_subject']}",
            "theory": student.get("minor_ib_theory"),
            "internal": student.get("minor_ib_internal"),
            "practical": student.get("minor_ib_practical"),
            "total": student.get("minor_ib_total")
        }
        
    # MDC III
    if student.get("mdc_iii_subject"):
        subjects["mdc_iii"] = {
            "subject": f"Multi Disciplinary Course-III - {student['mdc_iii_subject']}",
            "total": student.get("mdc_iii_total")
        }
        
    # AEC III
    if student.get("aec_iii_subject"):
        subjects["aec_iii"] = {
            "subject": f"Ability Enhancement Courses-III - {student['aec_iii_subject']}",
            "total": student.get("aec_iii_total")
        }
        
    # SEC III
    if student.get("sec_iii_subject"):
        subjects["sec_iii"] = {
            "subject": f"Skill Enhancement Course-III - {student['sec_iii_subject']}",
            "total": student.get("sec_iii_total")
        }
        
    return {
        "student_name": student["student_name"].strip(),
        "roll_number": student["roll_number"].strip(),
        "result": student["result"].strip(),
        "grand_total": int(student["grand_total"]),
        "subjects": subjects
    }

def load_excluded_rolls(filepath=r"C:\Users\Anurag\Documents\GitHub\rollno.txt"):
    if not os.path.exists(filepath):
        print(f"Warning: Excluded roll numbers file not found at {filepath}")
        return set()
    try:
        with open(filepath, "r", encoding="utf-16") as f:
            rolls = set(line.strip() for line in f if line.strip())
            print(f"Loaded {len(rolls)} roll numbers to exclude from {filepath}")
            return rolls
    except Exception as e:
        print(f"Error reading {filepath} with UTF-16: {e}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                rolls = set(line.strip() for line in f if line.strip())
                print(f"Loaded {len(rolls)} roll numbers to exclude from {filepath} (using UTF-8)")
                return rolls
        except Exception as e2:
            print(f"Error reading {filepath} with UTF-8: {e2}")
            return set()

def main():
    source_dir = r"C:\Users\Anurag\Documents\GitHub\Sem_3_2023_batch_result"
    files = {
        "math": "math_Sem3_Merged.json",
        "physics": "phy_sem3_Merged.json",
        "chemistry": "che_sem3_Merged.json"
    }
    
    excluded_rolls = load_excluded_rolls()
    excluded_count = 0
    
    merged_results = []
    seen_rolls = set()
    
    for subject, filename in files.items():
        filepath = os.path.join(source_dir, filename)
        if not os.path.exists(filepath):
            print(f"Error: {filepath} does not exist.")
            continue
            
        print(f"Reading {filename}...")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        transformed_count = 0
        for item in data:
            roll = item.get("roll_number")
            if not roll:
                continue
            roll = roll.strip()
            
            if roll in excluded_rolls:
                excluded_count += 1
                continue
                
            # Warn/handle duplicates if any
            if roll in seen_rolls:
                print(f"Warning: Duplicate student with roll {roll} found in {filename}. Skipping.")
                continue
                
            transformed = transform_student(item)
            merged_results.append(transformed)
            seen_rolls.add(roll)
            transformed_count += 1
            
        print(f"Transformed {transformed_count} students from {filename}.")
        
    output_path = r"c:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results_sem3_master.json"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_results, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully merged {len(merged_results)} students into {output_path}")
    print(f"Excluded {excluded_count} students based on rollno.txt")

if __name__ == "__main__":
    main()
