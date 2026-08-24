"""
Convert 2024 Batch Semester 2 Tata College clean data
from scraper format to TataCollegeHub results format.

Source: result_main_folder/2024/sem2_tata/tata_sem2_2024_clean.json
Output: public/data/results_sem2_2024_master.json
"""
import json
import re

SOURCE = r'C:\Users\Anurag\Documents\GitHub\result_main_folder\2024\sem2_tata\tata_sem2_2024_clean.json'
OUTPUT = r'C:\Users\Anurag\Documents\GitHub\TataCollegeHub\public\data\results_sem2_2024_master.json'


def parse_mark(val):
    """Convert a mark string to an integer, handling absent/missing values."""
    if val is None:
        return None
    val = str(val).strip()
    if val in ('', '-', 'ab', 'AB', 'Ab'):
        return None
    try:
        return int(val)
    except ValueError:
        return None


def classify_subject_key(name):
    """Map a subject name to a structured key like major_ii, minor_iia, etc."""
    name_lower = name.lower().strip()
    
    if name_lower.startswith('major -ii -') or name_lower.startswith('major -ii-') or name_lower == 'major -ii':
        return 'major_ii'
    if name_lower.startswith('major -iii -') or name_lower.startswith('major -iii-') or name_lower == 'major -iii':
        return 'major_iii'
    if name_lower.startswith('minor - iia') or name_lower.startswith('minor -iia'):
        return 'minor_iia'
    if 'multi disciplinary course-ii' in name_lower or 'multi disciplinary course -ii' in name_lower:
        return 'mdc_ii'
    if 'ability enhancement course' in name_lower:
        return 'aec_ii'
    if 'skill enhancement course' in name_lower:
        return 'sec_ii'
    
    # Fallback: use a sanitized version of the name
    sanitized = re.sub(r'[^a-z0-9]+', '_', name_lower).strip('_')
    return sanitized[:30]


def compute_grade(percentage):
    """Compute letter grade from percentage."""
    if percentage >= 90:
        return 'O'
    elif percentage >= 80:
        return 'A+'
    elif percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B+'
    elif percentage >= 50:
        return 'B'
    elif percentage >= 40:
        return 'C'
    elif percentage >= 33:
        return 'D'
    else:
        return 'F'


def convert_record(rec):
    """Convert a single student record from scraper format to site format."""
    # Parse grand_total
    grand_total = parse_mark(rec.get('grand_total')) or 0
    
    # Compute percentage and grade (full marks = 500 for sem 2)
    full_marks = 500
    percentage = round((grand_total / full_marks) * 100, 1) if full_marks > 0 else 0
    grade = compute_grade(percentage)
    
    # Convert subjects array to object with named keys
    subjects_obj = {}
    for sub in rec.get('subjects', []):
        name = sub.get('name', '')
        key = classify_subject_key(name)
        
        entry = {'subject': name}
        
        theory = parse_mark(sub.get('theory'))
        internal = parse_mark(sub.get('internal'))
        practical = parse_mark(sub.get('practical'))
        total = parse_mark(sub.get('total'))
        
        if theory is not None:
            entry['theory'] = theory
        if internal is not None:
            entry['internal'] = internal
        if practical is not None:
            entry['practical'] = practical
        if total is not None:
            entry['total'] = total
        else:
            # Calculate total from components if missing
            calc = sum(x for x in [theory, internal, practical] if x is not None)
            entry['total'] = calc if calc > 0 else 0
        
        subjects_obj[key] = entry
    
    return {
        'student_name': rec.get('sname', ''),
        'father_name': rec.get('fname', ''),
        'roll_number': rec.get('rollno', ''),
        'reg_no': rec.get('regno', ''),
        'reg_year': rec.get('regyear', ''),
        'college_name': rec.get('college_name', 'Tata College, Chaibasa'),
        'coursename': rec.get('coursename', 'FYUGP Under NEP'),
        'semester': rec.get('semester', 'II'),
        'year_of_exam': rec.get('year_of_exam', '2025'),
        'result': rec.get('result', ''),
        'grand_total': grand_total,
        'full_marks': full_marks,
        'percentage': percentage,
        'grade': grade,
        'subjects': subjects_obj,
        'batch': rec.get('batch', '2024'),
        'sem': rec.get('sem', '2'),
    }


def main():
    # Read source data
    print(f'Reading source data from:\n  {SOURCE}')
    with open(SOURCE, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f'  → {len(raw_data)} records loaded')
    
    # Convert all records
    converted = [convert_record(r) for r in raw_data]
    
    # Sort by grand_total descending, then alphabetically by name for ties
    converted.sort(key=lambda s: (-s['grand_total'], s['student_name']))
    
    # Print some stats
    total = len(converted)
    pass_count = sum(1 for s in converted if s['result'].lower() == 'pass')
    promoted_count = sum(1 for s in converted if s['result'].lower() == 'promoted')
    pass_pct = round((pass_count / total) * 100, 1) if total else 0
    
    print(f'\n  Stats:')
    print(f'    Total: {total}')
    print(f'    Pass: {pass_count} ({pass_pct}%)')
    print(f'    Promoted: {promoted_count}')
    
    if converted:
        print(f'\n  Top 5 students:')
        for i, s in enumerate(converted[:5]):
            print(f'    {i+1}. {s["student_name"]} — {s["grand_total"]} marks ({s["percentage"]}%, {s["grade"]})')
    
    # Verify subject keys
    print(f'\n  Subject key check (first record):')
    if converted:
        for key, sub in converted[0]['subjects'].items():
            print(f'    {key}: {sub["subject"][:50]}... → total={sub.get("total", "?")}')
    
    # Compute department distribution
    dept_counts = {}
    for s in converted:
        major_sub = s['subjects'].get('major_ii', {})
        dept = major_sub.get('subject', 'Unknown')
        # Extract department name
        dept = dept.replace('MAJOR -II - ', '').replace('MAJOR -II- ', '').strip()
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    
    print(f'\n  Department distribution:')
    for dept, count in sorted(dept_counts.items(), key=lambda x: -x[1]):
        print(f'    {dept}: {count}')
    
    # Write output
    print(f'\nWriting output to:\n  {OUTPUT}')
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(converted, f, ensure_ascii=False, separators=(',', ':'))
    
    import os
    size_mb = os.path.getsize(OUTPUT) / (1024 * 1024)
    print(f'  → Done! File size: {size_mb:.2f} MB')
    print(f'\n✅ Successfully converted {total} records to TataCollegeHub format.')


if __name__ == '__main__':
    main()
