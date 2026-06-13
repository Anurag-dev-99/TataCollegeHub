import os
import json
import shutil

def transform_student(student):
    subjects = {}
    
    # Major XII
    if student.get("major_xii_subject"):
        subjects["major_xii"] = {
            "subject": f"MAJOR-XII-{student['major_xii_subject']}",
            "theory": student.get("major_xii_theory"),
            "internal": student.get("major_xii_internal"),
            "practical": student.get("major_xii_practical"),
            "total": student.get("major_xii_total")
        }
        
    # Major XIII
    if student.get("major_xiii_subject"):
        subjects["major_xiii"] = {
            "subject": f"MAJOR-XIII-{student['major_xiii_subject']}",
            "theory": student.get("major_xiii_theory"),
            "internal": student.get("major_xiii_internal"),
            "practical": student.get("major_xiii_practical"),
            "total": student.get("major_xiii_total")
        }
        
    # Major XIV
    if student.get("major_xiv_subject"):
        subjects["major_xiv"] = {
            "subject": f"MAJOR-XIV-{student['major_xiv_subject']}",
            "theory": student.get("major_xiv_theory"),
            "internal": student.get("major_xiv_internal"),
            "practical": student.get("major_xiv_practical"),
            "total": student.get("major_xiv_total")
        }
        
    # Major XV
    if student.get("major_xv_subject"):
        subjects["major_xv"] = {
            "subject": f"MAJOR-XV-{student['major_xv_subject']}",
            "theory": student.get("major_xv_theory"),
            "internal": student.get("major_xv_internal"),
            "practical": student.get("major_xv_practical"),
            "total": student.get("major_xv_total")
        }
        
    # Minor IIC
    if student.get("minor_iic_subject"):
        subjects["minor_iic"] = {
            "subject": f"Minor-IIC-{student['minor_iic_subject']}",
            "theory": student.get("minor_iic_theory"),
            "internal": student.get("minor_iic_internal"),
            "practical": student.get("minor_iic_practical"),
            "total": student.get("minor_iic_total")
        }
        
    return {
        "student_name": student["student_name"].strip(),
        "roll_number": student["roll_number"].strip(),
        "result": student["result"].strip(),
        "grand_total": int(student["grand_total"]),
        "subjects": subjects
    }

def main():
    source_dir = r"C:\Users\Anurag\Documents\GitHub\sem_6_2022_batch_result"
    files = {
        "maths": "sem6_2022_maths_Merged.json"
    }
    
    # Destination for the master JSON results file
    output_path = r"c:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results_sem6_master.json"
    
    # Destination directory for copying student result PDFs
    pdf_source_dir = os.path.join(source_dir, "Maths_sem6_2022", "pdfs")
    pdf_dest_dir = r"c:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\pdfs\results\sem6_2022"
    
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
            
            if roll in seen_rolls:
                print(f"Warning: Duplicate student with roll {roll} found. Skipping.")
                continue
                
            transformed = transform_student(item)
            merged_results.append(transformed)
            seen_rolls.add(roll)
            transformed_count += 1
            
        print(f"Transformed {transformed_count} students from {filename}.")
        
    # Ensure master JSON output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the master JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_results, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully merged {len(merged_results)} students into {output_path}")

    # Copy PDF marksheets if source directory exists
    if os.path.exists(pdf_source_dir):
        print(f"Copying PDF files from {pdf_source_dir} to {pdf_dest_dir}...")
        os.makedirs(pdf_dest_dir, exist_ok=True)
        copied_count = 0
        
        for roll in seen_rolls:
            pdf_filename = f"{roll}.pdf"
            src_pdf = os.path.join(pdf_source_dir, pdf_filename)
            
            if os.path.exists(src_pdf):
                dest_pdf = os.path.join(pdf_dest_dir, pdf_filename)
                shutil.copy2(src_pdf, dest_pdf)
                copied_count += 1
            else:
                print(f"Warning: PDF marksheet not found for roll {roll} at {src_pdf}")
                
        print(f"Successfully copied {copied_count} PDFs to website data assets.")
    else:
        print(f"Warning: PDF source directory {pdf_source_dir} not found. No PDFs copied.")

if __name__ == "__main__":
    main()
