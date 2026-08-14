"""
TEMPLATE INJECTION PDF GENERATOR v2 - FIXED
Fixes:
  1. Credit value now read from raw API data (credit1 field)
  2. Subject order matches KU template (swaps last two: SEC before AEC)
"""
import json, os, random, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

# === Configuration ===
DATA_FILE = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\cleaned\kolhan_sem2_2023_clean.json"
RAW_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\fetched_data"
OUTPUT_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs\template_test_v2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Step 1: Pick same 5 students ===
print("Loading data...")
data = json.load(open(DATA_FILE, 'r', encoding='utf-8'))
tata_students = [r for r in data if 'Tata' in r.get('college_name', '')]
random.seed(99)
samples = random.sample(tata_students, 5)

print(f"Selected 5 students for testing:")
for s in samples:
    print(f"  {s['rollno']} | {s['sname']} | {s['result']} | Total: {s['grand_total']}")

# === Step 2: Get credit1 from raw data ===
def get_credit(rollno):
    """Read credit1 from raw API JSON file."""
    raw_path = os.path.join(RAW_DIR, f"{rollno}.json")
    if os.path.exists(raw_path):
        raw = json.load(open(raw_path, 'r', encoding='utf-8'))
        # credit1 is the correct field (credit is always null)
        return raw.get('credit1') or raw.get('credit') or '20'
    return '20'

# === Step 3: Fix subject order to match KU template ===
def fix_subject_order(subjects):
    """
    KU template renders subjects as: p1, p2, p3, p4, p6, p5
    (Skill Enhancement before Ability Enhancement)
    Our cleaned data stores them as: p1, p2, p3, p4, p5, p6
    So we swap the last two.
    """
    if len(subjects) >= 6:
        fixed = subjects[:4] + [subjects[5], subjects[4]]  # swap index 4 and 5
        return fixed
    return subjects

def generate_marksheet_html(student, credit_val):
    """Generate a KU-authentic marksheet HTML for one student."""
    
    # Fix subject order (swap last two to match KU template)
    subjects = fix_subject_order(student.get('subjects', []))
    
    # Build subject rows
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
    <td>{theory}</td> 
    <td>{internal}</td>
    <td>{practical}</td> 
    <td>{total}</td>     
  </tr>"""

    # QR code URL (same format as KU uses)
    qr_data = f"Student Name:{student['sname']},Roll No:{student['rollno']},Registration No.:{student['regno']},Grand Total:{student['grand_total']},Result:{student['result']}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=70x70&data={qr_data}"
    
    # Full marks info
    fullm = student.get('fullm', '500')
    thfm = student.get('thfm', '75/60/50')
    intfm = student.get('intfm', '25/15')
    prfm = student.get('prfm', '25')
    totfm = student.get('totfm', '100/75/50')
    prpm = student.get('prpm', '10')
    totpm = student.get('totpm', '40/20/30')
    
    # Semester promotion (from raw data if available)
    sem_promotion = ""
    raw_path = os.path.join(RAW_DIR, f"{student['rollno']}.json")
    sem_status = None
    if os.path.exists(raw_path):
        raw = json.load(open(raw_path, 'r', encoding='utf-8'))
        sem_status = raw.get('semester_status')
    
    if sem_status:
        sem_promotion = f'<tr><td colspan="4" style="padding-left: 25px; font-weight: bold; font-size: 17px; padding-top: 10px;">Semester Promotion : <span>{sem_status}</span></td></tr>'
    
    html = f"""<!DOCTYPE html>
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
  footer {{ display:none; }}
  .noprint {{ display:none; }}
  .header {{ display:none; }}
  .footer {{ display:none; }}
}}
@media print {{
  .chead {{ -webkit-print-color-adjust: exact; }}
  .shead {{ -webkit-print-color-adjust: exact; }}
}}
.table>tbody>tr>td, .table>tbody>tr>th, .table>tfoot>tr>td, .table>tfoot>tr>th, .table>thead>tr>td, .table>thead>tr>th {{
  padding: 5px;
}}
.main-footer {{ margin-left: 0px; }}
div.container1 {{
  height:1100px; width: 1000px; border: 1px solid black;
  margin-left:auto; margin-right:auto; margin-bottom:10px; margin-top: 20px;
  font-family: Arial, Helvetica, sans-serif;
}}
div.container2 {{
  width:985px; margin-left:auto; margin-right:auto;
  margin-bottom:10px; margin-top: 20px;
  font-family: Arial, Helvetica, sans-serif;
}}
div.headerresult {{
  color: black; background-color:white; text-align: center;
  margin-bottom:30px; font-family: Arial, Helvetica, sans-serif;
}}
div.table {{ margin-top:20px; padding-bottom:1px; font-weight: bold; font-size: 14px;
  align:center; font-family: Arial, Helvetica, sans-serif; line-height: 2.18234; }}
div.table1 {{ padding-bottom:3px; align:center; font-family: Arial, Helvetica, sans-serif; }}
.table2 {{
  font-weight: bold; font-size: 14px; font-family: Arial, Helvetica, sans-serif;
  line-height: 2.18234; width:96% !important; text-align:center;
}}
</style>
</head>
<body>
<div class="container1" style="background:#fff;">
<div class="container2">
<div class="headerresult">
    <div style="float:left;"><img src="https://www.kuuniv.in/result/resources/images/buildinter.png" style="height:100px;width:104px;"></div>
    <div style="text-align:center;font-size:21px;text-decoration: underline; font-weight:bold">KOLHAN UNIVERSITY, CHAIBASA</div>
    <div style="text-align:center;font-size: 14px;text-decoration: underline;font-weight:bold">
 {student.get('coursename', 'FYUGP Under NEP')}  Semester - {student.get('semester', 'II')}  Examination - {student.get('year_of_exam', '2024')}</div>
    <div style="text-align:center;text-decoration: underline;font-weight: bold;font-size:15px;"> Provisional Marks Card </div>
</div>
<div style="float:right;margin-right:47px;"><img src="{qr_url}" style="width:135px;height:135px;"></div>
<table class="table" style="width: 80%;margin-left: 11px;">
<tbody>
  <tr>
    <th style="border-top:0px" nowrap="">REGISTRATION NO / YEAR</th>
    <th style="border-top:0px;">{student['regno']} / {student['regyear']}</th>
  </tr>
  <tr>
    <th style="border-top:0px;">COLLEGE NAME</th>
    <th style="border-top:0px;">{student['college_name']}</th>
  </tr>
  <tr>
    <th style="border-top:0px;" nowrap="">NAME OF THE STUDENT</th>
    <th style="border-top:0px;">{student['sname']}</th>
  </tr>
  <tr>
    <th style="border-top:0px;">FATHER'S NAME</th>
    <th style="border-top:0px;">{student['fname']}</th>
  </tr>
  <tr>
    <th style="border-top:0px;">ROLL NO.</th>
    <th style="border-top:0px;">{student['rollno']}</th>
  </tr>
  <tr>
    <th style="border-top:0px;"></th>
  </tr>
  <tr></tr>
</tbody>
</table>
<div style="width:980px; text-align:center;">
<table align="center" class="table2" border="1px solid black">
<tbody>
  <tr>
    <th style="padding-left:170px;">Subject</th>
    <th style="text-align: center;">Theory</th>
    <th style="text-align: center;">Internal</th>
    <th style="text-align: center;">Practical / Project</th>
    <th style="text-align: center;">Total</th>
  </tr>
  <tr>
    <th style="padding-left:10px;">Full Marks<label style="padding-left:100px;"> {fullm}</label></th>
    <th style="text-align: center!important;">{thfm}</th>
    <th style="text-align: center!important;">{intfm}</th>
    <th style="text-align: center!important;">{prfm}</th>
    <th style="text-align: center!important;">{totfm}</th>
  </tr>
  <tr>
    <th style="padding-left:10px;">Pass Marks</th>
    <th style="text-align: center!important;"></th>
    <th style="text-align: center!important;"></th>
    <th style="text-align: center!important;">{prpm}</th>
    <th style="text-align: center!important;">{totpm}</th>
  </tr>
  <tr>
    <th style="padding-left:147px;" colspan="2">Marks Obtained</th>
    <th></th>
    <th></th>
    <th></th>
  </tr>
  {subject_rows}
</tbody>
</table>
</div>
<br>
<div class="table1">
<table>
<tbody>
<tr>
    <td width="25%" style="padding-left:25px;font-weight:bold;font-size:17px;">
        Result : {student['result']}
    </td>
    <td width="20%" style="font-weight:bold;font-size:17px;">
        Credit : {credit_val}
    </td>
    <td width="25%"></td>
    <td width="30%" style="font-weight:bold;font-size:17px;text-align:right;padding-right:78px;">
        Grand Total : {student['grand_total']}
    </td>
</tr>
{sem_promotion}
</tbody>
</table>
<br>
</div>

  <div style="float:right;font-weight:bold;font-size:20px;margin-top:40px;margin-right:5%;">
  <img src="https://www.kuuniv.in/result/resources/images/controller_sign_rd.jpg" style="height:40px;width:120px;margin-left:30%;">
  <br>
  Controller of Examination
  </div>

</div>
</div>
</body>
</html>"""
    return html


# === Step 4: Generate HTML files ===
print(f"\nGenerating HTML files (v2 - fixed)...")
html_files = []
for s in samples:
    credit_val = get_credit(s['rollno'])
    html = generate_marksheet_html(s, credit_val)
    html_path = os.path.join(OUTPUT_DIR, f"{s['rollno']}_sem2.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    html_files.append(html_path)
    print(f"  Created: {s['rollno']}_sem2.html | Credit: {credit_val}")

# === Step 5: Convert HTML → PDF ===
convert_script = os.path.join(OUTPUT_DIR, '_convert_test.js')
with open(convert_script, 'w', encoding='utf-8') as f:
    f.write("""
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const INPUT_DIR = __dirname;
const htmlFiles = fs.readdirSync(INPUT_DIR).filter(f => f.endsWith('_sem2.html'));

(async () => {
  console.log('Converting ' + htmlFiles.length + ' HTML files to PDF...');
  const browser = await chromium.launch({ headless: true });
  
  for (const file of htmlFiles) {
    const page = await browser.newPage();
    const htmlPath = 'file:///' + path.join(INPUT_DIR, file).replace(/\\\\/g, '/');
    
    await page.goto(htmlPath, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    const pdfName = file.replace('.html', '.pdf');
    const pdfPath = path.join(INPUT_DIR, pdfName);
    
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
    });
    
    const size = Math.round(fs.statSync(pdfPath).size / 1024);
    console.log('  ' + pdfName + ' (' + size + ' KB)');
    await page.close();
  }
  
  await browser.close();
  console.log('\\nDone!');
})();
""")

print(f"\nConverting to PDF...")
os.chdir(r"C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs")
result = subprocess.run(['node', convert_script], capture_output=True, text=True, timeout=120)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])

print(f"\nv2 PDFs saved to: {OUTPUT_DIR}")
print("\nFIXES APPLIED:")
print("  1. Credit value now from raw API data (credit1 field)")
print("  2. Subject order: Skill Enhancement before Ability Enhancement (matches KU)")
print("\nCompare with official marksheets:")
for s in samples:
    print(f"  {s['rollno']} | {s['sname']}")
