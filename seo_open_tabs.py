#!/usr/bin/env python3
"""
============================================================
  KolhanHub — SEO Quick Browser Opener
  Opens all target keywords in Chrome tabs so you can
  manually check your Google ranking quickly.
  
  NO pip install needed. Uses only built-in Python modules.
  
  RUN:
    python seo_open_tabs.py
============================================================
"""

import webbrowser
import time
import urllib.parse

# ── Target keywords to check ─────────────────────────────
KEYWORDS = [
    # Brand (should be #1-4)
    "kolhan hub",
    "kolhanhub",

    # PYQ (target: Top 10)
    "kolhan pyq",
    "kolhan university pyq",
    "kolhan university previous year papers",
    "kolhan university question papers download",

    # Syllabus (target: Top 10)
    "kolhan syllabus",
    "kolhan university syllabus",
    "kolhan university nep 2020 syllabus",

    # Result (target: Top 10)
    "kolhan result",
    "kolhan university result",

    # Tata College (should be Page 1 already)
    "tata college pyq",
    "tata college syllabus",
    "tata college result",
    "tata college chaibasa",
]

# ── Config ────────────────────────────────────────────────
DELAY_BETWEEN_TABS = 0.8   # seconds between opening each tab
TARGET_DOMAIN      = "kolhanhub.in"


def build_google_url(keyword):
    """Build a Google search URL for the keyword"""
    query = urllib.parse.quote_plus(keyword)
    # hl=en : English interface
    # gl=in : Results from India (most relevant for you)
    # pws=0 : Disable personalization (no personalization bias)
    return f"https://www.google.co.in/search?q={query}&hl=en&gl=in&pws=0"


def open_in_chrome_incognito(url):
    """Attempt to open the URL in Chrome Incognito mode on Windows, falling back if needed."""
    import subprocess
    import shutil
    import os

    # 1. Search common Windows installation paths for Chrome
    chrome_paths = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    
    chrome_bin = None
    for p in chrome_paths:
        if os.path.exists(p):
            chrome_bin = p
            break
            
    if not chrome_bin:
        chrome_bin = shutil.which("chrome")
        
    # 2. Open via direct executable path if found
    if chrome_bin:
        try:
            subprocess.Popen([chrome_bin, "--incognito", url])
            return True
        except Exception:
            pass
            
    # 3. Fallback: try Windows 'start' shell command for Chrome
    try:
        subprocess.Popen(f'start chrome --incognito "{url}"', shell=True)
        return True
    except Exception:
        pass
        
    # 4. Final Fallback: use default browser (regular mode)
    webbrowser.open(url)
    return False


def main():
    print("=" * 60)
    print("  KolhanHub SEO Browser Opener (Incognito & Unbiased)")
    print(f"  Opening {len(KEYWORDS)} keyword searches in Chrome Incognito...")
    print("=" * 60)
    print()
    print("  TIP: Use Ctrl+F in each tab and search for")
    print(f"       '{TARGET_DOMAIN}' to quickly find your position.")
    print()
    print("  Note: Search URLs contain '&pws=0' to turn off Google personalization.")
    print()

    for i, keyword in enumerate(KEYWORDS, 1):
        url = build_google_url(keyword)
        print(f"  [{i:02d}/{len(KEYWORDS)}] Opening: \"{keyword}\"")
        open_in_chrome_incognito(url)
        time.sleep(DELAY_BETWEEN_TABS)

    print()
    print("=" * 60)
    print(f"  Done! {len(KEYWORDS)} tabs opened.")
    print()
    print("  How to check your rank in each tab:")
    print("  1. Press Ctrl+F")
    print(f"  2. Type: {TARGET_DOMAIN}")
    print("  3. If not found -> scroll to next page & repeat")
    print("  4. Count the results above you = your rank")
    print("=" * 60)


if __name__ == "__main__":
    main()
