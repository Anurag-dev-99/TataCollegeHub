"""
EMBEDDED PDF GENERATOR — Demo (5 students)
Downloads all external resources ONCE, embeds everything in HTML.
No internet needed during PDF conversion = 6x faster.
"""
import json, os, sys, time, base64, io, random
import urllib.request
import qrcode

sys.stdout.reconfigure(encoding='utf-8')

# === Configuration ===
DATA_FILE = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\cleaned\kolhan_sem2_2023_clean.json"
RAW_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\fetched_data"
OUTPUT_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs\embedded_test"
CACHE_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs\resource_cache"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# ============================================================
# STEP 1: Download external resources ONCE
# ============================================================
print("=" * 60)
print("STEP 1: Downloading external resources (one-time)...")
print("=" * 60)

resources = {
    "bootstrap.css": "https://www.kuuniv.in/result/resources/registration/bootstrap/css/bootstrap.min.css",
    "adminlte.css": "https://www.kuuniv.in/result/resources/registration/dist/css/AdminLTE.min.css",
    "logo.png": "https://www.kuuniv.in/result/resources/images/buildinter.png",
    "signature.jpg": "https://www.kuuniv.in/result/resources/images/controller_sign_rd.jpg",
}

cached = {}
for name, url in resources.items():
    cache_path = os.path.join(CACHE_DIR, name)
    if os.path.exists(cache_path):
        print(f"  {name}: cached ✓")
        with open(cache_path, 'rb') as f:
            cached[name] = f.read()
    else:
        print(f"  {name}: downloading from {url[:50]}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=15).read()
            with open(cache_path, 'wb') as f:
                f.write(data)
            cached[name] = data
            print(f"    saved ({len(data)//1024} KB)")
        except Exception as e:
            print(f"    ERROR: {e}")
            cached[name] = b''

# Convert images to base64 data URIs
logo_b64 = base64.b64encode(cached['logo.png']).decode('ascii')
sig_b64 = base64.b64encode(cached['signature.jpg']).decode('ascii')
bootstrap_css = cached['bootstrap.css'].decode('utf-8', errors='ignore')
adminlte_css = cached['adminlte.css'].decode('utf-8', errors='ignore')

print(f"\n  Resources ready:")
print(f"    CSS: {len(bootstrap_css)//1024} KB + {len(adminlte_css)//1024} KB")
print(f"    Logo: {len(logo_b64)//1024} KB (base64)")
print(f"    Signature: {len(sig_b64)//1024} KB (base64)")

# ============================================================
# STEP 2: QR codes from api.qrserver.com (SAME API as KU uses)
# ============================================================
def generate_qr_base64(text):
    """Download QR code from api.qrserver.com — identical to official KU QR codes."""
    import urllib.parse
    encoded = urllib.parse.quote(text)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=70x70&data={encoded}"
    try:
        req = urllib.request.Request(qr_url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=15).read()
        return base64.b64encode(data).decode('ascii')
    except Exception as e:
        print(f"    QR download failed: {e}, using local fallback")
        # Fallback to local generation
        qr = qrcode.QRCode(version=1, box_size=4, border=1)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode('ascii')

# ============================================================
# STEP 3: Pick 5 test students
# ============================================================
print(f"\n{'=' * 60}")
print("STEP 2: Loading data & picking test students...")
print("=" * 60)

data = json.load(open(DATA_FILE, 'r', encoding='utf-8'))
tata = [r for r in data if 'Tata' in r.get('college_name', '')]
random.seed(99)
samples = random.sample(tata, 5)

for s in samples:
    print(f"  {s['rollno']} | {s['sname']} | {s['result']}")

# ============================================================
# Helpers
# ============================================================
def get_credit(rollno):
    raw_path = os.path.join(RAW_DIR, f"{rollno}.json")
    if os.path.exists(raw_path):
        raw = json.load(open(raw_path, 'r', encoding='utf-8'))
        return raw.get('credit1') or raw.get('credit') or '20'
    return '20'

def get_semester_status(rollno):
    raw_path = os.path.join(RAW_DIR, f"{rollno}.json")
    if os.path.exists(raw_path):
        raw = json.load(open(raw_path, 'r', encoding='utf-8'))
        return raw.get('semester_status', '')
    return ''

def fix_subject_order(subjects):
    if len(subjects) >= 6:
        return subjects[:4] + [subjects[5], subjects[4]]
    return subjects

# ============================================================
# STEP 4: Generate self-contained HTML (EVERYTHING embedded)
# ============================================================
def generate_embedded_html(student):
    subjects = fix_subject_order(student.get('subjects', []))
    credit_val = get_credit(student['rollno'])
    sem_status = get_semester_status(student['rollno'])

    # Generate QR code locally
    qr_data = f"Student Name:{student['sname']},Roll No:{student['rollno']},Registration No.:{student['regno']},Grand Total:{student['grand_total']},Result:{student['result']}"
    qr_b64 = generate_qr_base64(qr_data)

    subject_rows = ""
    for subj in subjects:
        subject_rows += f"""
  <tr align="center">
    <td style="text-align:left;padding-left:10px;"><span style="margin-left:2px;">{subj.get('name','')}</span></td>
    <td>{subj.get('theory','-')}</td><td>{subj.get('internal','-')}</td><td>{subj.get('practical','-')}</td><td>{subj.get('total','-')}</td>
  </tr>"""

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

    # ALL resources embedded — no external URLs!
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>KU::Result</title>
<style>
{bootstrap_css}
{adminlte_css}
.table>tbody>tr>td,.table>tbody>tr>th,.table>tfoot>tr>td,.table>tfoot>tr>th,.table>thead>tr>td,.table>thead>tr>th {{ padding:5px; }}
div.container1 {{ height:1100px;width:1000px;border:1px solid black;margin:20px auto 10px;font-family:Arial,Helvetica,sans-serif; }}
div.container2 {{ width:985px;margin:20px auto 10px;font-family:Arial,Helvetica,sans-serif; }}
div.headerresult {{ color:black;background-color:white;text-align:center;margin-bottom:30px;font-family:Arial,Helvetica,sans-serif; }}
div.table1 {{ padding-bottom:3px;font-family:Arial,Helvetica,sans-serif; }}
.table2 {{ font-weight:bold;font-size:14px;font-family:Arial,Helvetica,sans-serif;line-height:2.18234;width:96%!important;text-align:center; }}
</style>
</head>
<body>
<div class="container1" style="background:#fff;">
<div class="container2">
<div class="headerresult">
    <div style="float:left;"><img src="data:image/png;base64,{logo_b64}" style="height:100px;width:104px;"></div>
    <div style="text-align:center;font-size:21px;text-decoration:underline;font-weight:bold">KOLHAN UNIVERSITY, CHAIBASA</div>
    <div style="text-align:center;font-size:14px;text-decoration:underline;font-weight:bold">
 {student.get('coursename','FYUGP Under NEP')}  Semester - {student.get('semester','II')}  Examination - {student.get('year_of_exam','2024')}</div>
    <div style="text-align:center;text-decoration:underline;font-weight:bold;font-size:15px;"> Provisional Marks Card </div>
</div>
<div style="float:right;margin-right:47px;"><img src="data:image/png;base64,{qr_b64}" style="width:135px;height:135px;"></div>
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
  <img src="data:image/jpeg;base64,{sig_b64}" style="height:40px;width:120px;margin-left:30%;"><br>
  Controller of Examination
  </div>
</div>
</div>
</body>
</html>"""


# ============================================================
# STEP 5: Generate HTML + convert to PDF
# ============================================================
print(f"\n{'=' * 60}")
print("STEP 3: Generating embedded HTML files...")
print("=" * 60)

html_start = time.time()
html_files = []
for s in samples:
    html = generate_embedded_html(s)
    html_path = os.path.join(OUTPUT_DIR, f"{s['rollno']}_sem2_embedded.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    size = len(html) // 1024
    html_files.append(html_path)
    print(f"  {s['rollno']}_sem2_embedded.html ({size} KB) — fully self-contained ✓")

html_elapsed = time.time() - html_start
print(f"\n  HTML generation: {html_elapsed:.2f} seconds")

# Create the conversion script
convert_js = os.path.join(OUTPUT_DIR, '_convert_embedded.js')
with open(convert_js, 'w', encoding='utf-8') as f:
    f.write("""
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const INPUT_DIR = __dirname;
const htmlFiles = fs.readdirSync(INPUT_DIR).filter(f => f.endsWith('_embedded.html'));

(async () => {
  console.log('Converting ' + htmlFiles.length + ' embedded HTML files to PDF...');
  console.log('(No internet needed — everything is embedded)\\n');
  
  const browser = await chromium.launch({ headless: true });
  const startTime = Date.now();
  
  for (const file of htmlFiles) {
    const perStart = Date.now();
    const page = await browser.newPage();
    const htmlContent = fs.readFileSync(path.join(INPUT_DIR, file), 'utf-8');
    
    // No network needed! Everything is base64 embedded
    await page.setContent(htmlContent, { waitUntil: 'load', timeout: 10000 });
    await page.waitForTimeout(200); // Just a tiny wait for rendering
    
    const pdfName = file.replace('_embedded.html', '_embedded.pdf');
    const pdfPath = path.join(INPUT_DIR, pdfName);
    
    await page.pdf({
      path: pdfPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
    });
    
    const perElapsed = ((Date.now() - perStart) / 1000).toFixed(2);
    const size = Math.round(fs.statSync(pdfPath).size / 1024);
    console.log('  ' + pdfName + ' (' + size + ' KB) — ' + perElapsed + 's');
    await page.close();
  }
  
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log('\\nDone! ' + htmlFiles.length + ' PDFs in ' + elapsed + 's');
  console.log('Average: ' + (parseFloat(elapsed) / htmlFiles.length).toFixed(2) + 's per PDF');
  
  await browser.close();
})();
""")

print(f"\n{'=' * 60}")
print("STEP 4: Converting embedded HTML → PDF (no internet)...")
print("=" * 60)

import subprocess
os.chdir(r"C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs")
result = subprocess.run(['node', convert_js], capture_output=True, text=True, timeout=60)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:300])

print(f"\nOutput: {OUTPUT_DIR}")
print("Compare these with the old method PDFs and KU originals!")
