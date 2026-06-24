#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
# Force UTF-8 output so Unicode chars work on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

"""
========================================================
  KolhanHub SEO Rank Checker
  Automatically checks Google rankings for kolhanhub.in
  across all target keywords.
  
  SETUP (run once):
    pip install selenium webdriver-manager colorama
  
  RUN:
    python seo_rank_checker.py
========================================================
"""

import time
import random
import sys
import datetime

# ── Try importing dependencies ─────────────────────────────────────────────────
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import NoSuchElementException, WebDriverException
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("\n[ERROR] Missing dependencies. Please run:")
    print("  pip install selenium webdriver-manager\n")
    sys.exit(1)

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    class Fore:
        GREEN = YELLOW = RED = CYAN = WHITE = MAGENTA = BLUE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

# ══════════════════════════════════════════════════════════════════════════════
#   CONFIGURATION — Edit these as needed
# ══════════════════════════════════════════════════════════════════════════════

TARGET_DOMAIN = "kolhanhub.in"

# All keywords you want to track
KEYWORDS = [
    # Primary brand keywords
    "kolhan hub",
    "kolhanhub",
    
    # PYQ keywords (currently ~#58)
    "kolhan pyq",
    "kolhan university pyq",
    "kolhan university previous year papers",
    "kolhan university question papers",
    "kolhan university question papers download",
    
    # Syllabus keywords (currently ~#32)
    "kolhan syllabus",
    "kolhan university syllabus",
    "kolhan university nep 2020 syllabus",
    "kolhan university fyugp syllabus",
    
    # Result keywords (currently 50+)
    "kolhan result",
    "kolhan university result",
    "kolhan university exam result 2024",
    
    # Tata College keywords (already ranking well)
    "tata college pyq",
    "tata college syllabus",
    "tata college result",
    "tata college chaibasa",
    "tata college chaibasa result",
    "tata college chaibasa pyq",
]

MAX_RESULTS_TO_CHECK = 50   # Check top 50 Google results (5 pages)
SEARCH_DELAY_MIN = 3         # Min seconds between searches (avoid bot detection)
SEARCH_DELAY_MAX = 6         # Max seconds between searches
HEADLESS = False             # Set True to run Chrome in background (no window)

# ══════════════════════════════════════════════════════════════════════════════
#   RANK CHECKER ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def create_driver(headless=False):
    """Initialize Chrome WebDriver"""
    options = Options()
    
    # Standard options
    options.add_argument("--lang=en-IN")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Realistic user agent
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
    
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Remove webdriver flag
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    if not headless:
        driver.maximize_window()
    
    return driver


def find_rank(driver, keyword, max_results=50):
    """
    Search Google and find position of TARGET_DOMAIN.
    Returns (rank_number, page_number) or (None, None) if not found.
    """
    try:
        # Build Google search URL (force Indian results, English interface)
        query = keyword.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}&hl=en&gl=in&num=10"
        driver.get(url)
        time.sleep(random.uniform(2, 3.5))
        
        # Check if we hit CAPTCHA
        page_source = driver.page_source.lower()
        if "unusual traffic" in page_source or "captcha" in page_source:
            print(f"  {Fore.RED}[CAPTCHA] Google is asking for verification. Pausing 30s...")
            time.sleep(30)
            driver.get(url)
            time.sleep(3)
        
        global_position = 0
        pages_to_check = max_results // 10
        
        for page_num in range(1, pages_to_check + 1):
            # Grab all search result anchor tags
            result_anchors = driver.find_elements(
                By.CSS_SELECTOR, 
                "div.g a[href^='http'], div[data-hveid] a[href^='http']"
            )
            
            seen_urls = set()
            for anchor in result_anchors:
                href = anchor.get_attribute("href") or ""
                
                # Skip Google-internal links and duplicates
                if not href or "google." in href or href in seen_urls:
                    continue
                if not href.startswith("http"):
                    continue
                
                seen_urls.add(href)
                global_position += 1
                
                # Check if this is our domain!
                if TARGET_DOMAIN in href:
                    return global_position, page_num
            
            # Move to next page
            if page_num < pages_to_check:
                try:
                    next_btn = driver.find_element(By.ID, "pnnext")
                    next_btn.click()
                    time.sleep(random.uniform(2, 3))
                except NoSuchElementException:
                    break  # No more pages
        
        return None, None  # Not found in top N results
    
    except WebDriverException as e:
        return "ERROR", str(e)[:50]


def status_icon(rank):
    """Return colored status based on rank"""
    if rank is None:
        return f"{Fore.RED}[X] Not in top 50"
    if rank == "ERROR":
        return f"{Fore.MAGENTA}[!] Error"
    if rank <= 3:
        return f"{Fore.GREEN}{Style.BRIGHT}[TOP] #{rank} (Top 3!)"
    if rank <= 10:
        return f"{Fore.GREEN}[OK]  #{rank} (Page 1)"
    if rank <= 20:
        return f"{Fore.YELLOW}[~]   #{rank} (Page 2)"
    if rank <= 30:
        return f"{Fore.YELLOW}[!]   #{rank} (Page 3)"
    return f"{Fore.RED}[v]   #{rank} (Deep)"


def print_header():
    width = 62
    now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    sep = "=" * width
    print(f"\n{Fore.CYAN}{sep}")
    print(f"{Fore.CYAN}  {Style.BRIGHT}KolhanHub SEO Rank Checker")
    print(f"{Fore.CYAN}  Target: {Fore.WHITE}{Style.BRIGHT}{TARGET_DOMAIN}")
    print(f"{Fore.CYAN}  Checking {len(KEYWORDS)} keywords  |  Date: {now}")
    print(f"{Fore.CYAN}{sep}{Style.RESET_ALL}\n")


def print_summary(results):
    width = 62
    sep  = "=" * width
    dash = "-" * width
    print(f"\n{Fore.CYAN}{sep}")
    print(f"{Fore.CYAN}  {Style.BRIGHT}RANKING SUMMARY -- {TARGET_DOMAIN}")
    print(f"{Fore.CYAN}{sep}{Style.RESET_ALL}")
    
    # Separate found and not found
    found     = [(kw, r, p) for kw, r, p in results if isinstance(r, int) and r <= 50]
    not_found = [(kw, r, p) for kw, r, p in results if r is None or r == "ERROR"]
    
    if found:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}  [RANKING KEYWORDS]{Style.RESET_ALL}")
        print(f"  {'Keyword':<42} {'Rank':<8} {'Page'}")
        print(f"  {'-'*56}")
        for kw, rank, page in sorted(found, key=lambda x: x[1]):
            icon  = "[TOP]" if rank <= 3 else "[OK] " if rank <= 10 else "[~]  "
            color = Fore.GREEN if rank <= 10 else Fore.YELLOW
            print(f"  {color}{icon} {kw:<40} #{str(rank):<7} p.{page}{Style.RESET_ALL}")
    
    if not_found:
        print(f"\n{Fore.RED}{Style.BRIGHT}  [NOT YET RANKING — 50+]{Style.RESET_ALL}")
        print(f"  {'-'*56}")
        for kw, rank, page in not_found:
            print(f"  {Fore.RED}[X] {kw}{Style.RESET_ALL}")
    
    # Stats
    total = len(results)
    top10 = sum(1 for _, r, _ in results if isinstance(r, int) and r <= 10)
    top30 = sum(1 for _, r, _ in results if isinstance(r, int) and r <= 30)
    print(f"\n{Fore.CYAN}{dash}")
    print(f"  Total keywords: {total}  |  In Top 10: {Fore.GREEN}{top10}{Fore.CYAN}  |  In Top 30: {Fore.YELLOW}{top30}{Fore.CYAN}")
    print(f"{sep}{Style.RESET_ALL}\n")
    
    # Save to file
    save_results(results)


def save_results(results):
    """Save results to a timestamped text file and append to JSON database"""
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"seo_results_{now}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"KolhanHub SEO Rank Check — {now}\n")
        f.write(f"Target: {TARGET_DOMAIN}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"{'Keyword':<42} {'Rank':<8} {'Page'}\n")
        f.write("-" * 60 + "\n")
        for kw, rank, page in sorted(results, key=lambda x: x[1] if isinstance(x[1], int) else 999):
            rank_str = f"#{rank}" if isinstance(rank, int) else "Not found"
            page_str = f"p.{page}" if isinstance(page, int) else "-"
            f.write(f"{kw:<42} {rank_str:<8} {page_str}\n")
    
    print(f"  {Fore.CYAN}[SAVED] Results saved to: {Style.BRIGHT}{filename}{Style.RESET_ALL}")

    # Log to JSON Database
    try:
        import seo_history_manager
        rankings_dict = {}
        for kw, rank, page in results:
            if isinstance(rank, int):
                rankings_dict[kw.strip().lower()] = rank
            else:
                rankings_dict[kw.strip().lower()] = None
        seo_history_manager.log_run_externally("selenium", rankings_dict)
        print(f"  {Fore.GREEN}[DATABASE] Successfully appended run to JSON database and updated report.{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"  {Fore.RED}[DATABASE ERROR] Could not save to database: {e}{Style.RESET_ALL}\n")


# ══════════════════════════════════════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print_header()
    
    print(f"{Fore.WHITE}  Starting Chrome...{Style.RESET_ALL}")
    driver = create_driver(headless=HEADLESS)
    
    results = []
    
    try:
        for i, keyword in enumerate(KEYWORDS, 1):
            progress = f"[{i}/{len(KEYWORDS)}]"
            print(f"\n  {Fore.CYAN}{progress}{Fore.WHITE} Checking: {Style.BRIGHT}\"{keyword}\"{Style.RESET_ALL}")
            
            rank, page = find_rank(driver, keyword, MAX_RESULTS_TO_CHECK)
            results.append((keyword, rank, page))
            
            # Print immediate result
            print(f"  -> {status_icon(rank)}{Style.RESET_ALL}")
            
            # Random delay between searches (avoid bot detection)
            if i < len(KEYWORDS):
                delay = random.uniform(SEARCH_DELAY_MIN, SEARCH_DELAY_MAX)
                print(f"  {Style.DIM}(waiting {delay:.1f}s...){Style.RESET_ALL}", end="", flush=True)
                time.sleep(delay)
                print()
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}  [!] Interrupted by user. Showing partial results...{Style.RESET_ALL}")
    
    finally:
        driver.quit()
    
    if results:
        print_summary(results)


if __name__ == "__main__":
    main()
