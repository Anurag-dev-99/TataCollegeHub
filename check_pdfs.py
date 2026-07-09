import sys
import subprocess
import glob
import os

try:
    import pypdf
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pypdf'])
    import pypdf

pdf_dir = r"C:\Users\Anurag\Documents\GitHub\Merit_list"
for pdf_file in glob.glob(os.path.join(pdf_dir, "*.pdf")):
    try:
        reader = pypdf.PdfReader(pdf_file)
        if len(reader.pages) > 0:
            text = reader.pages[0].extract_text()
            print(f"\n--- {os.path.basename(pdf_file)} ---")
            print(f"Text length: {len(text)}")
            if len(text) > 0:
                print(text[:200].replace("\n", " "))
            else:
                print("[No text found - Likely a Scanned Image]")
    except Exception as e:
        print(f"Error reading {os.path.basename(pdf_file)}: {e}")
