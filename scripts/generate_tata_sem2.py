"""
PRODUCTION PDF GENERATOR — Tata College Sem 2 (2023 Batch)
Generates 1,930 marksheet PDFs using template injection.

Step 1: Generate HTML files (fast, pure Python)
Step 2: Convert HTML → PDF (using available tool)
"""
import json, os, sys, time, concurrent.futures

sys.stdout.reconfigure(encoding='utf-8')

# === Configuration ===
DATA_FILE = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\cleaned\kolhan_sem2_2023_clean.json"
RAW_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\fetched_data"
HTML_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\marksheet_html"
PDF_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\marksheet_pdf"
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# === Load data ===
print("Loading cleaned data...")
data = json.load(open(DATA_FILE, 'r', encoding='utf-8'))
tata_students = [r for r in data if 'Tata' in r.get('college_name', '')]
print(f"Tata College Sem 2 students: {len(tata_students)}")

# === Helper: Get credit1 from raw data ===
def get_credit(rollno):
    raw_path = os.path.join(RAW_DIR, f"{rollno}.json")
    if os.path.exists(raw_path):
        raw = json.load(open(raw_path, 'r', encoding='utf-8'))
        return raw.get('credit1') or raw.get('credit') or '20'
    return '20'

# === Helper: Get semester_status from raw data ===
def get_semester_status(rollno):
    raw_path = os.path.join(RAW_DIR, f"{rollno}.json")
    if os.path.exists(raw_path):
        raw = json.load(open(raw_path, 'r', encoding='utf-8'))
        return raw.get('semester_status', '')
    return ''

# === Fix subject order (KU template renders p6 before p5) ===
def fix_subject_order(subjects):
    if len(subjects) >= 6:
        return subjects[:4] + [subjects[5], subjects[4]]
    return subjects

# === Generate HTML ===
def generate_html(student):
    subjects = fix_subject_order(student.get('subjects', []))
    credit_val = get_credit(student['rollno'])
    sem_status = get_semester_status(student['rollno'])
    
    subject_rows = ""
    for subj in subjects:
        name = subj.get('name', '')
        theory = subj.get('theory', '-')
        internal = subj.get('internal', '-')
        practical = subj.get('practical', '-')
        total = subj.get('total', '-')
        subject_rows += f"""
  <tr align="center">
    <td style="text-align:left;padding-left:10px;"><span style="margin-left:2px;">{name}</span></td>
    <td>{theory}</td><td>{internal}</td><td>{practical}</td><td>{total}</td>
  </tr>"""

    qr_data = f"Student Name:{student['sname']},Roll No:{student['rollno']},Registration No.:{student['regno']},Grand Total:{student['grand_total']},Result:{student['result']}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=70x70&data={qr_data}"

    fullm = student.get('fullm', '500')
    thfm = student.get('thfm', '75/60/50')
    intfm = student.get('intfm', '25/15')
    prfm = student.get('prfm', '25')
    totfm = student.get('totfm', '100/75/50')
    prpm = student.get('prpm', '10')
    totpm = student.get('totpm', '40/20/30')

    sem_promotion = ""
    if sem_status:
        sem_promotion = f'<tr><td colspan="4" style="padding-left:25px;font-weight:bold;font-size:17px;padding-top:10px;">Semester Promotion : <span>{sem_status}</span></td></tr>'

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>KU::Result</title>
<link rel="stylesheet" href="https://www.kuuniv.in/result/resources/registration/bootstrap/css/bootstrap.min.css">
<link rel="stylesheet" href="https://www.kuuniv.in/result/resources/registration/dist/css/AdminLTE.min.css">
<style>
@media print {{
  .container {{ width:950px; margin-top:2px; }}
  div.container1 {{ border: 1px solid black !important; }}
  div.container2 {{ border: 1px solid #fff !important; }}
  .text-center {{ margin-top:-71px; }}
  footer,.noprint,.header,.footer {{ display:none; }}
  .chead,.shead {{ -webkit-print-color-adjust: exact; }}
}}
.table>tbody>tr>td, .table>tbody>tr>th, .table>tfoot>tr>td, .table>tfoot>tr>th, .table>thead>tr>td, .table>thead>tr>th {{ padding: 5px; }}
.main-footer {{ margin-left: 0px; }}
div.container1 {{ height:1100px; width:1000px; border:1px solid black; margin:20px auto 10px; font-family:Arial,Helvetica,sans-serif; }}
div.container2 {{ width:985px; margin:20px auto 10px; font-family:Arial,Helvetica,sans-serif; }}
div.headerresult {{ color:black; background-color:white; text-align:center; margin-bottom:30px; font-family:Arial,Helvetica,sans-serif; }}
div.table1 {{ padding-bottom:3px; font-family:Arial,Helvetica,sans-serif; }}
.table2 {{ font-weight:bold; font-size:14px; font-family:Arial,Helvetica,sans-serif; line-height:2.18234; width:96%!important; text-align:center; }}
</style>
</head>
<body>
<div class="container1" style="background:#fff;">
<div class="container2">
<div class="headerresult">
    <div style="float:left;"><img src="https://www.kuuniv.in/result/resources/images/buildinter.png" style="height:100px;width:104px;"></div>
    <div style="text-align:center;font-size:21px;text-decoration:underline;font-weight:bold">KOLHAN UNIVERSITY, CHAIBASA</div>
    <div style="text-align:center;font-size:14px;text-decoration:underline;font-weight:bold">
 {student.get('coursename','FYUGP Under NEP')}  Semester - {student.get('semester','II')}  Examination - {student.get('year_of_exam','2024')}</div>
    <div style="text-align:center;text-decoration:underline;font-weight:bold;font-size:15px;"> Provisional Marks Card </div>
</div>
<div style="float:right;margin-right:47px;"><img src="{qr_url}" style="width:135px;height:135px;"></div>
<table class="table" style="width:80%;margin-left:11px;">
<tbody>
  <tr><th style="border-top:0px" nowrap="">REGISTRATION NO / YEAR</th><th style="border-top:0px;">{student['regno']} / {student['regyear']}</th></tr>
  <tr><th style="border-top:0px;">COLLEGE NAME</th><th style="border-top:0px;">{student['college_name']}</th></tr>
  <tr><th style="border-top:0px;" nowrap="">NAME OF THE STUDENT</th><th style="border-top:0px;">{student['sname']}</th></tr>
  <tr><th style="border-top:0px;">FATHER'S NAME</th><th style="border-top:0px;">{student['fname']}</th></tr>
  <tr><th style="border-top:0px;">ROLL NO.</th><th style="border-top:0px;">{student['rollno']}</th></tr>
  <tr><th style="border-top:0px;"></th></tr><tr></tr>
</tbody>
</table>
<div style="width:980px;text-align:center;">
<table align="center" class="table2" border="1px solid black">
<tbody>
  <tr><th style="padding-left:170px;">Subject</th><th style="text-align:center;">Theory</th><th style="text-align:center;">Internal</th><th style="text-align:center;">Practical / Project</th><th style="text-align:center;">Total</th></tr>
  <tr><th style="padding-left:10px;">Full Marks<label style="padding-left:100px;"> {fullm}</label></th><th style="text-align:center!important;">{thfm}</th><th style="text-align:center!important;">{intfm}</th><th style="text-align:center!important;">{prfm}</th><th style="text-align:center!important;">{totfm}</th></tr>
  <tr><th style="padding-left:10px;">Pass Marks</th><th style="text-align:center!important;"></th><th style="text-align:center!important;"></th><th style="text-align:center!important;">{prpm}</th><th style="text-align:center!important;">{totpm}</th></tr>
  <tr><th style="padding-left:147px;" colspan="2">Marks Obtained</th><th></th><th></th><th></th></tr>
  {subject_rows}
</tbody>
</table>
</div>
<br>
<div class="table1">
<table>
<tbody>
<tr>
    <td width="25%" style="padding-left:25px;font-weight:bold;font-size:17px;">Result : {student['result']}</td>
    <td width="20%" style="font-weight:bold;font-size:17px;">Credit : {credit_val}</td>
    <td width="25%"></td>
    <td width="30%" style="font-weight:bold;font-size:17px;text-align:right;padding-right:78px;">Grand Total : {student['grand_total']}</td>
</tr>
{sem_promotion}
</tbody>
</table>
<br>
</div>
  <div style="float:right;font-weight:bold;font-size:20px;margin-top:40px;margin-right:5%;">
  <img src="https://www.kuuniv.in/result/resources/images/controller_sign_rd.jpg" style="height:40px;width:120px;margin-left:30%;"><br>
  Controller of Examination
  </div>
</div>
</div>
</body>
</html>"""


# ============================================================
# STEP 1: Generate all HTML files
# ============================================================
print(f"\n{'='*60}")
print(f"STEP 1: Generating {len(tata_students)} HTML files...")
print(f"{'='*60}")

start = time.time()
generated = 0
skipped = 0

for student in tata_students:
    html_path = os.path.join(HTML_DIR, f"{student['rollno']}_sem2.html")
    if os.path.exists(html_path):
        skipped += 1
        continue
    html = generate_html(student)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    generated += 1
    if generated % 200 == 0:
        elapsed = time.time() - start
        rate = generated / elapsed
        print(f"  [{generated}/{len(tata_students)}] {rate:.0f} files/sec")

elapsed = time.time() - start
print(f"\n  HTML generation complete!")
print(f"  Generated: {generated} | Skipped (existing): {skipped}")
print(f"  Time: {elapsed:.1f} seconds")
print(f"  Output: {HTML_DIR}")

# Count total HTML files
html_count = len([f for f in os.listdir(HTML_DIR) if f.endswith('.html')])
total_size = sum(os.path.getsize(os.path.join(HTML_DIR, f)) for f in os.listdir(HTML_DIR) if f.endswith('.html'))
print(f"  Total HTML files: {html_count} | Size: {total_size/1024/1024:.1f} MB")

print(f"\n{'='*60}")
print(f"STEP 1 COMPLETE! HTML files ready.")
print(f"STEP 2: Run PDF conversion separately.")
print(f"{'='*60}")
