#!/usr/bin/env python3
"""
============================================================
  KolhanHub — SEO Rank Checker via SerpAPI
  Uses the official SerpAPI to get REAL Google rankings
  with zero captcha / bot detection issues.
  
  FREE TIER: 100 searches/month at serpapi.com
  
  SETUP:
  1. Go to https://serpapi.com/  (sign up free)
  2. Copy your API key from the dashboard
  3. Paste it below as SERPAPI_KEY = "your_key_here"
  4. pip install requests
  5. python seo_rank_checker_api.py
============================================================
"""

import requests
import datetime
import time

# ── PUT YOUR SERPAPI KEY HERE ─────────────────────────────
SERPAPI_KEY   = "8b69fbfb2f25217cb08a6c98cda5912f1011a675244ff418fcb3b376ce7e340d"
TARGET_DOMAIN = "kolhanhub.in"
GITHUB_DOMAIN = "anurag-dev-99.github.io"  # GitHub Pages also counts as your site

# ── Keywords to track ─────────────────────────────────────
KEYWORDS = [
    "kolhan hub",
    "kolhanhub",
    "kolhan pyq",
    "kolhan university pyq",
    "kolhan university previous year papers",
    "kolhan university question papers download",
    "kolhan syllabus",
    "kolhan university syllabus",
    "kolhan university nep 2020 syllabus",
    "kolhan result",
    "kolhan university result",
    "tata college pyq",
    "tata college syllabus",
    "tata college result",
    "tata college chaibasa",
    "tata college chaibasa result",
    "tata college chaibasa pyq",
]

# ── SerpAPI Search ────────────────────────────────────────
def get_google_rank(keyword, api_key, domain, pages=3):
    """
    Use SerpAPI to get Google results and find our domain rank.
    Uses Indian Google (google.co.in) for accurate local results.
    Checks up to `pages` pages (10 results each).
    3 pages = 30 results = ~51 API credits for all 17 keywords/run.
    """
    for page in range(pages):
        params = {
            "engine":        "google",
            "q":             keyword,
            "api_key":       api_key,
            "google_domain": "google.co.in",   # Indian Google domain
            "gl":            "in",              # Country: India
            "hl":            "en",              # Language: English
            "location":      "Jharkhand, India", # Location near Chaibasa
            "num":           "10",              # 10 results per page
            "start":         page * 10,         # Pagination offset
        }

        try:
            response = requests.get(
                "https://serpapi.com/search",
                params=params,
                timeout=20
            )
            data = response.json()

            # Handle API errors
            if "error" in data:
                return None, None, f"API Error: {data['error']}"

            # Check organic results
            organic = data.get("organic_results", [])
            
            # No more results — stop searching
            if not organic:
                break

            for i, result in enumerate(organic):
                link      = result.get("link", "")
                displayed = result.get("displayed_link", "")
                # Match both custom domain AND GitHub Pages link
                is_match = (
                    domain        in link or domain        in displayed or
                    GITHUB_DOMAIN in link or GITHUB_DOMAIN in displayed
                )
                if is_match:
                    global_rank = (page * 10) + i + 1
                    return global_rank, page + 1, None

        except requests.exceptions.RequestException as e:
            return None, None, f"Network error: {str(e)[:60]}"

    return None, None, None  # Not found in top N results



# ── Display Helpers ───────────────────────────────────────
def rank_label(rank):
    if rank is None:
        return "[X] Not in top 50"
    if rank <= 3:
        return f"[TOP] #{rank} - Top 3! Great!"
    if rank <= 10:
        return f"[OK]  #{rank} - Page 1"
    if rank <= 20:
        return f"[~]   #{rank} - Page 2"
    if rank <= 30:
        return f"[!]   #{rank} - Page 3"
    return f"[v]   #{rank} - Deep"


def save_results(results):
    now      = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"seo_results_{now}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"KolhanHub SEO Rank Check (SerpAPI) - {now}\n")
        f.write(f"Domain: {TARGET_DOMAIN}\n")
        f.write("=" * 62 + "\n\n")
        f.write(f"{'Keyword':<44} {'Rank':<8} {'Page'}\n")
        f.write("-" * 62 + "\n")
        for kw, rank, page, err in sorted(results, key=lambda x: x[1] if isinstance(x[1], int) else 999):
            rank_str = f"#{rank}" if isinstance(rank, int) else ("Error" if err else "Not found")
            page_str = f"p.{page}" if isinstance(page, int) else "-"
            f.write(f"{kw:<44} {rank_str:<8} {page_str}\n")
    print(f"\n  [SAVED] Results saved to: {filename}")

    # Log to JSON Database
    try:
        import seo_history_manager
        rankings_dict = {}
        for kw, rank, page, err in results:
            if isinstance(rank, int):
                rankings_dict[kw.strip().lower()] = rank
            else:
                rankings_dict[kw.strip().lower()] = None
        seo_history_manager.log_run_externally("serpapi", rankings_dict)
        print(f"  [DATABASE] Successfully appended run to JSON database and updated report.\n")
    except Exception as e:
        print(f"  [DATABASE ERROR] Could not save to database: {e}\n")

    return filename



# ── Main ──────────────────────────────────────────────────
def main():
    # Check API key
    if SERPAPI_KEY == "YOUR_SERPAPI_KEY_HERE":
        print("\n[ERROR] You need to set your SerpAPI key!")
        print("  1. Sign up free at: https://serpapi.com/")
        print("  2. Copy your API key from the dashboard")
        print("  3. Open this file and replace YOUR_SERPAPI_KEY_HERE")
        print("\n  Free tier: 100 searches/month = enough for weekly tracking\n")
        return

    now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    print("\n" + "=" * 62)
    print("  KolhanHub SEO Rank Checker (via SerpAPI)")
    print(f"  Domain: {TARGET_DOMAIN}  |  Date: {now}")
    print(f"  Checking {len(KEYWORDS)} keywords...")
    print("=" * 62 + "\n")

    results = []

    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"  [{i:02d}/{len(KEYWORDS)}] \"{keyword}\"...", end=" ", flush=True)

        rank, page, err = get_google_rank(keyword, SERPAPI_KEY, TARGET_DOMAIN)
        results.append((keyword, rank, page, err))

        if err:
            print(f"[ERROR] {err}")
        else:
            print(rank_label(rank))

        # Small delay to be nice to the API
        time.sleep(0.5)

    # ── Summary ───────────────────────────────────────────
    print("\n" + "=" * 62)
    print(f"  RANKING SUMMARY -- {TARGET_DOMAIN}")
    print("=" * 62)

    found     = [(kw, r, p, e) for kw, r, p, e in results if isinstance(r, int)]
    not_found = [(kw, r, p, e) for kw, r, p, e in results if not isinstance(r, int)]

    if found:
        print(f"\n  RANKING KEYWORDS ({len(found)})")
        print(f"  {'Keyword':<44} {'Rank':<8} {'Page'}")
        print(f"  {'-'*56}")
        for kw, rank, page, _ in sorted(found, key=lambda x: x[1]):
            label = "[TOP]" if rank <= 3 else "[OK] " if rank <= 10 else "[~]  "
            print(f"  {label} {kw:<42} #{str(rank):<7} p.{page}")

    if not_found:
        print(f"\n  NOT YET RANKING / 50+ ({len(not_found)})")
        print(f"  {'-'*56}")
        for kw, _, _, err in not_found:
            suffix = f" [{err}]" if err else ""
            print(f"  [X]  {kw}{suffix}")

    # Stats
    top10 = sum(1 for _, r, _, _ in results if isinstance(r, int) and r <= 10)
    top30 = sum(1 for _, r, _, _ in results if isinstance(r, int) and r <= 30)
    print(f"\n  Total: {len(results)} | Top 10: {top10} | Top 30: {top30}")
    print("=" * 62)

    save_results(results)


if __name__ == "__main__":
    main()
