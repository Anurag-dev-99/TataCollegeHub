"""
PRODUCTION: Generate 1,930 Tata College Sem 2 Marksheet PDFs
- Parallel QR downloads (20 at a time)
- Embedded resources (CSS, images as base64)  
- Reads raw JSON for null vs "-" fix, credit1
- Correct subject order (p6 before p5)
"""
import json, os, sys, time, base64, io, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\cleaned\kolhan_sem2_2023_clean.json"
RAW_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\fetched_data"
HTML_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\marksheet_html"
PDF_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\2023\sem2\marksheet_pdf"
CACHE_DIR = r"C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs\resource_cache"
QR_CACHE = os.path.join(CACHE_DIR, "qr_codes")
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(QR_CACHE, exist_ok=True)

# ========== STEP 0: Load resources ==========
print("=" * 60)
print("Loading cached resources...")
cached = {}
for name in ["bootstrap.css", "adminlte.css", "logo.png", "signature.jpg"]:
    with open(os.path.join(CACHE_DIR, name), 'rb') as f:
        cached[name] = f.read()

logo_b64 = base64.b64encode(cached['logo.png']).decode('ascii')
sig_b64 = base64.b64encode(cached['signature.jpg']).decode('ascii')
bootstrap_css = cached['bootstrap.css'].decode('utf-8', errors='ignore')
adminlte_css = cached['adminlte.css'].decode('utf-8', errors='ignore')
print("  Resources loaded ✓")

# ========== STEP 1: Load students ==========
data = json.load(open(DATA_FILE, 'r', encoding='utf-8'))
tata = [r for r in data if 'Tata' in r.get('college_name', '')]
print(f"  Tata College students: {len(tata)}")

# ========== STEP 2: Download QR codes (parallel) ==========
print(f"\n{'=' * 60}")
print(f"STEP 1: Downloading QR codes (20 parallel)...")

def download_qr(student):
    rollno = student['rollno']
    cache_path = os.path.join(QR_CACHE, f"{rollno}.png")
    if os.path.exists(cache_path):
        return rollno, True
    qr_data = f"Student Name:{student['sname']},Roll No:{student['rollno']},Registration No.:{student['regno']},Grand Total:{student['grand_total']},Result:{student['result']}"
    encoded = urllib.parse.quote(qr_data)
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=70x70&data={encoded}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=15).read()
        with open(cache_path, 'wb') as f:
            f.write(data)
        return rollno, True
    except:
        return rollno, False

start = time.time()
done = 0
cached_count = len([f for f in os.listdir(QR_CACHE) if f.endswith('.png')])
print(f"  Already cached: {cached_count}")

with ThreadPoolExecutor(max_workers=20) as pool:
    futures = {pool.submit(download_qr, s): s for s in tata}
    for f in as_completed(futures):
        done += 1
        if done % 100 == 0:
            elapsed = time.time() - start
            print(f"  [{done}/{len(tata)}] {elapsed:.0f}s")

elapsed = time.time() - start
print(f"  QR download complete: {elapsed:.1f}s")

# ========== STEP 3: Generate HTML ==========
print(f"\n{'=' * 60}")
print(f"STEP 2: Generating {len(tata)} embedded HTML files...")

def load_raw(rollno):
    p = os.path.join(RAW_DIR, f"{rollno}.json")
    if os.path.exists(p):
        return json.load(open(p, 'r', encoding='utf-8'))
    return {}

def build_subjects(raw):
    subjects = []
    for i in range(1, 10):
        name = raw.get(f'cores2p{i}')
        if not name: continue
        subjects.append({
            'name': name,
            'theory': raw.get(f'mcores2th{i}') or '',
            'internal': raw.get(f'mcores2ia{i}') or '',
            'practical': raw.get(f'mcores2pr{i}') if raw.get(f'mcores2pr{i}') is not None else '',
            'total': raw.get(f'tot{i}') or '',
        })
    if len(subjects) >= 6:
        subjects = subjects[:4] + [subjects[5], subjects[4]]
    return subjects

def gen_html(student):
    raw = load_raw(student['rollno'])
    subjects = build_subjects(raw) if raw else []
    credit = (raw.get('credit1') or raw.get('credit') or '20') if raw else '20'
    sem_status = raw.get('semester_status', '') if raw else ''
    
    # QR from cache
    qr_path = os.path.join(QR_CACHE, f"{student['rollno']}.png")
    if os.path.exists(qr_path):
        qr_b64 = base64.b64encode(open(qr_path, 'rb').read()).decode('ascii')
    else:
        qr_b64 = ''

    rows = ""
    for s in subjects:
        rows += f'<tr align="center"><td style="text-align:left;padding-left:10px;"><span style="margin-left:2px;">{s["name"]}</span></td><td>{s["theory"]}</td><td>{s["internal"]}</td><td>{s["practical"]}</td><td>{s["total"]}</td></tr>\n'

    fullm = student.get('fullm','500'); thfm = student.get('thfm','75/60/50')
    intfm = student.get('intfm','25/15'); prfm = student.get('prfm','25')
    totfm = student.get('totfm','100/75/50'); prpm = student.get('prpm','10'); totpm = student.get('totpm','40/20/30')
    
    sem_row = f'<tr><td colspan="4" style="padding-left:25px;font-weight:bold;font-size:17px;padding-top:10px;">Semester Promotion : <span>{sem_status}</span></td></tr>' if sem_status else ''

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>KU::Result</title>
<style>{bootstrap_css}\n{adminlte_css}
.table>tbody>tr>td,.table>tbody>tr>th,.table>tfoot>tr>td,.table>tfoot>tr>th,.table>thead>tr>td,.table>thead>tr>th{{padding:5px;}}
div.container1{{height:1100px;width:1000px;border:1px solid black;margin:20px auto 10px;font-family:Arial,Helvetica,sans-serif;}}
div.container2{{width:985px;margin:20px auto 10px;font-family:Arial,Helvetica,sans-serif;}}
div.headerresult{{color:black;background-color:white;text-align:center;margin-bottom:30px;font-family:Arial,Helvetica,sans-serif;}}
div.table1{{padding-bottom:3px;font-family:Arial,Helvetica,sans-serif;}}
.table2{{font-weight:bold;font-size:14px;font-family:Arial,Helvetica,sans-serif;line-height:2.18234;width:96%!important;text-align:center;}}
</style></head><body>
<div class="container1" style="background:#fff;"><div class="container2">
<div class="headerresult">
<div style="float:left;"><img src="data:image/png;base64,{logo_b64}" style="height:100px;width:104px;"></div>
<div style="text-align:center;font-size:21px;text-decoration:underline;font-weight:bold">KOLHAN UNIVERSITY, CHAIBASA</div>
<div style="text-align:center;font-size:14px;text-decoration:underline;font-weight:bold"> {student.get('coursename','FYUGP Under NEP')}  Semester - {student.get('semester','II')}  Examination - {student.get('year_of_exam','2024')}</div>
<div style="text-align:center;text-decoration:underline;font-weight:bold;font-size:15px;"> Provisional Marks Card </div>
</div>
<div style="float:right;margin-right:47px;"><img src="data:image/png;base64,{qr_b64}" style="width:135px;height:135px;"></div>
<table class="table" style="width:80%;margin-left:11px;"><tbody>
<tr><th style="border-top:0px" nowrap="">REGISTRATION NO / YEAR</th><th style="border-top:0px;">{student['regno']} / {student['regyear']}</th></tr>
<tr><th style="border-top:0px;">COLLEGE NAME</th><th style="border-top:0px;">{student['college_name']}</th></tr>
<tr><th style="border-top:0px;" nowrap="">NAME OF THE STUDENT</th><th style="border-top:0px;">{student['sname']}</th></tr>
<tr><th style="border-top:0px;">FATHER'S NAME</th><th style="border-top:0px;">{student['fname']}</th></tr>
<tr><th style="border-top:0px;">ROLL NO.</th><th style="border-top:0px;">{student['rollno']}</th></tr>
<tr><th style="border-top:0px;"></th></tr><tr></tr>
</tbody></table>
<div style="width:980px;text-align:center;">
<table align="center" class="table2" border="1px solid black"><tbody>
<tr><th style="padding-left:170px;">Subject</th><th style="text-align:center;">Theory</th><th style="text-align:center;">Internal</th><th style="text-align:center;">Practical / Project</th><th style="text-align:center;">Total</th></tr>
<tr><th style="padding-left:10px;">Full Marks<label style="padding-left:100px;"> {fullm}</label></th><th style="text-align:center!important;">{thfm}</th><th style="text-align:center!important;">{intfm}</th><th style="text-align:center!important;">{prfm}</th><th style="text-align:center!important;">{totfm}</th></tr>
<tr><th style="padding-left:10px;">Pass Marks</th><th style="text-align:center!important;"></th><th style="text-align:center!important;"></th><th style="text-align:center!important;">{prpm}</th><th style="text-align:center!important;">{totpm}</th></tr>
<tr><th style="padding-left:147px;" colspan="2">Marks Obtained</th><th></th><th></th><th></th></tr>
{rows}</tbody></table></div><br>
<div class="table1"><table><tbody>
<tr><td width="25%" style="padding-left:25px;font-weight:bold;font-size:17px;">Result : {student['result']}</td>
<td width="20%" style="font-weight:bold;font-size:17px;">Credit : {credit}</td>
<td width="25%"></td>
<td width="30%" style="font-weight:bold;font-size:17px;text-align:right;padding-right:78px;">Grand Total : {student['grand_total']}</td></tr>
{sem_row}</tbody></table><br></div>
<div style="float:right;font-weight:bold;font-size:20px;margin-top:40px;margin-right:5%;">
<img src="data:image/jpeg;base64,{sig_b64}" style="height:40px;width:120px;margin-left:30%;"><br>Controller of Examination</div>
</div></div></body></html>"""

start2 = time.time()
generated = 0
for s in tata:
    path = os.path.join(HTML_DIR, f"{s['rollno']}_sem2.html")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(gen_html(s))
    generated += 1
    if generated % 200 == 0:
        print(f"  [{generated}/{len(tata)}] {time.time()-start2:.0f}s")

print(f"  HTML done: {generated} files in {time.time()-start2:.1f}s")
print(f"\n{'=' * 60}")
print(f"STEP 2 COMPLETE. Now run PDF conversion:")
print(f"  cd C:\\Users\\Anurag\\Documents\\GitHub\\result_main_folder\\demo_pdfs")
print(f"  node convert_embedded_pdf.js")
