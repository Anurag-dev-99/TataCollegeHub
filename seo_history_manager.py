#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  KolhanHub — SEO History & Trend Manager
  Manages the historical SEO rankings database (JSON),
  imports past logs, accepts manual updates, and generates
  beautiful trend reports in Markdown.
============================================================
"""

import os
import re
import json
import glob
import argparse
from datetime import datetime

DATABASE_FILE = "seo_rankings_history.json"
REPORT_FILE = "seo_history_report.md"


def get_current_timestamp():
    """Get ISO 8601 formatted timestamp with local offset if possible."""
    # Using simple ISO format
    return datetime.now().isoformat()


def load_database():
    """Load the JSON database or return a fresh structure if not exists."""
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARNING] Error reading database: {e}. Starting fresh.")
    
    return {
        "last_updated": None,
        "history": []
    }


def save_database(db):
    """Save the database to JSON file."""
    db["last_updated"] = get_current_timestamp()
    # Sort history by timestamp to keep it chronological
    db["history"] = sorted(db["history"], key=lambda x: x["timestamp"])
    
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Database saved to {DATABASE_FILE}")


def parse_txt_log_content(content):
    """
    Parse the content of a standard seo_results_*.txt file.
    Returns a dictionary of keyword: rank (int or None).
    """
    rankings = {}
    lines = content.strip().split("\n")
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        
        # Skip headers and lines that aren't data
        if (line_str.startswith("KolhanHub") or 
            line_str.startswith("Domain:") or 
            line_str.startswith("Target:") or 
            line_str.startswith("===") or 
            line_str.startswith("---") or 
            line_str.startswith("Keyword") or
            line_str.startswith("Total:") or
            "RANKING SUMMARY" in line_str.upper()):
            continue
            
        # Parse standard lines:
        # e.g., "kolhanhub                                    #2       p.1"
        # e.g., "kolhan hub                                   Not found -"
        if "Not found" in line_str or "Error" in line_str:
            parts = re.split(r'\s{2,}', line_str)
            if parts:
                kw = parts[0].strip().lower()
                rankings[kw] = None
        elif "#" in line_str:
            # Look for rank number
            match = re.search(r'#(\d+)', line_str)
            if match:
                rank = int(match.group(1))
                # Keyword is before the #
                parts = line_str.split("#")
                kw = parts[0].strip().lower()
                rankings[kw] = rank
    return rankings


def parse_manual_ranking_data(text_data):
    """
    Parse raw manual copy-paste rankings from user.
    Supports formats like:
      kolhan hub 01
      kolhanhub 01
      kolhan result not in top 3 page
    Returns a dictionary of keyword: rank (int or None).
    """
    rankings = {}
    lines = text_data.strip().split("\n")
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
            
        line_lower = line_str.lower()
        
        # Check for 'not in top' or 'not found' or 'no rank'
        if any(phrase in line_lower for phrase in ["not in top", "not found", "no rank", "dropped"]):
            # Keyword is everything before the negative phrase
            for phrase in ["not in top", "not found", "no rank", "dropped"]:
                if phrase in line_lower:
                    idx = line_lower.find(phrase)
                    kw = line_str[:idx].strip().lower()
                    rankings[kw] = None
                    break
        else:
            # Try to split and parse last token as number
            words = line_str.split()
            if words:
                last_word = words[-1]
                # Check if last word is a number
                if last_word.isdigit():
                    rank = int(last_word)
                    kw = " ".join(words[:-1]).strip().lower()
                    rankings[kw] = rank
                else:
                    # Fallback: whole line as keyword, no rank
                    rankings[line_lower] = None
    return rankings


def add_run_to_database(db, timestamp, method, rankings):
    """
    Add a ranking run to the database. Avoids duplicates based on timestamp.
    """
    # Check if run with same timestamp already exists
    for run in db["history"]:
        if run["timestamp"] == timestamp:
            run["method"] = method
            run["rankings"] = rankings
            print(f"[INFO] Updated existing run for timestamp: {timestamp}")
            return
            
    db["history"].append({
        "timestamp": timestamp,
        "method": method,
        "rankings": rankings
    })
    print(f"[INFO] Added new run for timestamp: {timestamp} via {method}")


def import_existing_txt_logs(db):
    """Find and import all seo_results_*.txt files in current directory."""
    files = glob.glob("seo_results_*.txt")
    if not files:
        print("[INFO] No existing seo_results_*.txt files found to import.")
        return
        
    print(f"[INFO] Found {len(files)} log files. Importing...")
    for file_path in files:
        # Extract timestamp from filename
        # Pattern: seo_results_YYYY-MM-DD_HH-MM.txt
        match = re.search(r'seo_results_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2})\.txt', file_path)
        if match:
            date_str, time_str = match.groups()
            timestamp = f"{date_str}T{time_str.replace('-', ':')}:00"
        else:
            # Fallback to file modified time
            mtime = os.path.getmtime(file_path)
            timestamp = datetime.fromtimestamp(mtime).isoformat()
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Determine method based on content
            method = "selenium"
            if "SerpAPI" in content:
                method = "serpapi"
                
            rankings = parse_txt_log_content(content)
            if rankings:
                add_run_to_database(db, timestamp, method, rankings)
        except Exception as e:
            print(f"[ERROR] Failed to import {file_path}: {e}")


def generate_markdown_report(db):
    """Generate seo_history_report.md summarizing history and highlighting trends."""
    if not db["history"]:
        print("[INFO] No history entries to generate report.")
        return
        
    # Sort runs chronologically
    sorted_history = sorted(db["history"], key=lambda x: x["timestamp"])
    latest_run = sorted_history[-1]
    
    # Previous run for trend calculation
    previous_run = sorted_history[-2] if len(sorted_history) > 1 else None
    
    # Format times for display
    latest_time_raw = latest_run["timestamp"]
    try:
        latest_time_parsed = datetime.fromisoformat(latest_time_raw.split("+")[0])
        latest_time_disp = latest_time_parsed.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        latest_time_disp = latest_time_raw
        
    prev_time_disp = "N/A"
    if previous_run:
        prev_time_raw = previous_run["timestamp"]
        try:
            prev_time_parsed = datetime.fromisoformat(prev_time_raw.split("+")[0])
            prev_time_disp = prev_time_parsed.strftime("%d %b %Y, %I:%M %p")
        except Exception:
            prev_time_disp = prev_time_raw
            
    # Gather all unique keywords tracked in latest run
    latest_rankings = latest_run["rankings"]
    prev_rankings = previous_run["rankings"] if previous_run else {}
    
    # We list keywords sorted by their latest rank (with Nulls/Not found at the end)
    def rank_sort_key(item):
        kw, rank = item
        if rank is None:
            return 999999
        return rank
        
    sorted_latest = sorted(latest_rankings.items(), key=rank_sort_key)
    
    # Calculate stats for latest run
    total_keywords = len(latest_rankings)
    top_3 = sum(1 for r in latest_rankings.values() if isinstance(r, int) and r <= 3)
    top_10 = sum(1 for r in latest_rankings.values() if isinstance(r, int) and r <= 10)
    top_30 = sum(1 for r in latest_rankings.values() if isinstance(r, int) and r <= 30)
    not_found = sum(1 for r in latest_rankings.values() if r is None)
    
    # Trends calculations
    improved_count = 0
    dropped_count = 0
    new_count = 0
    lost_count = 0
    no_change_count = 0
    
    table_rows = []
    
    for kw, rank_new in sorted_latest:
        rank_old = prev_rankings.get(kw, "NOT_PRESENT")
        
        status_str = ""
        trend_icon = "⚪"
        
        if rank_old == "NOT_PRESENT":
            if rank_new is not None:
                status_str = f"✨ #{rank_new} (New)"
                trend_icon = "✨"
                new_count += 1
            else:
                status_str = "Not found"
                trend_icon = "⚪"
                no_change_count += 1
        elif rank_new is None:
            if rank_old is None:
                status_str = "Not found"
                trend_icon = "⚪"
                no_change_count += 1
            else:
                status_str = f"❌ Dropped (was #{rank_old})"
                trend_icon = "❌"
                lost_count += 1
        else: # rank_new is an integer
            if rank_old is None:
                status_str = f"🟢 #{rank_new} (Gained Rank)"
                trend_icon = "🟢"
                improved_count += 1
            elif rank_old == "NOT_PRESENT":
                # Handled above but just in case
                status_str = f"✨ #{rank_new} (New)"
                trend_icon = "✨"
                new_count += 1
            else: # both are integers
                diff = rank_old - rank_new
                if diff > 0:
                    status_str = f"🟢 #{rank_new} (▲ {diff})"
                    trend_icon = "🟢"
                    improved_count += 1
                elif diff < 0:
                    status_str = f"🔴 #{rank_new} (▼ {abs(diff)})"
                    trend_icon = "🔴"
                    dropped_count += 1
                else:
                    status_str = f"#{rank_new}"
                    trend_icon = "⚪"
                    no_change_count += 1
                    
        disp_old_rank = f"#{rank_old}" if isinstance(rank_old, int) else ("Not found" if rank_old is None else "-")
        disp_new_rank = f"#{rank_new}" if isinstance(rank_new, int) else "Not found"
        
        table_rows.append(f"| {trend_icon} | `{kw}` | {disp_old_rank} | {disp_new_rank} | {status_str} |")

    # Generate timeline stats
    timeline_rows = []
    # Take up to the last 10 runs
    for run in reversed(sorted_history[-10:]):
        run_time_raw = run["timestamp"]
        try:
            run_time_parsed = datetime.fromisoformat(run_time_raw.split("+")[0])
            run_time_disp = run_time_parsed.strftime("%d %b %Y, %I:%M %p")
        except Exception:
            run_time_disp = run_time_raw
            
        r_list = run["rankings"]
        r_top3 = sum(1 for r in r_list.values() if isinstance(r, int) and r <= 3)
        r_top10 = sum(1 for r in r_list.values() if isinstance(r, int) and r <= 10)
        r_top30 = sum(1 for r in r_list.values() if isinstance(r, int) and r <= 30)
        r_total = len(r_list)
        
        timeline_rows.append(f"| {run_time_disp} | `{run['method']}` | {r_total} | {r_top3} | {r_top10} | {r_top30} |")

    # Build the report content
    report_content = f"""# 📈 KolhanHub SEO Ranking History Report

> Last Updated: **{latest_time_disp}** (Method: `{latest_run['method']}`)
> Previous Run: **{prev_time_disp}**

---

## 📊 Summary Statistics

| Metric | Latest Count | Breakdown |
|---|---|---|
| **Total Keywords Tracked** | **{total_keywords}** | - |
| **Top 3 Rankings 🏆** | **{top_3}** | Rank #1 to #3 |
| **Top 10 Rankings 🟢** | **{top_10}** | Page 1 |
| **Top 30 Rankings 🟡** | **{top_30}** | Pages 1-3 |
| **Not Found in Top Results ❌** | **{not_found}** | - |

### Run-to-Run Trends (Compared to {prev_time_disp})
- 🟢 **Rank Improved:** {improved_count} keywords
- 🔴 **Rank Declined:** {dropped_count} keywords
- ✨ **New Rankings:** {new_count} keywords
- ❌ **Dropped Out of Top:** {lost_count} keywords
- ⚪ **No Change:** {no_change_count} keywords

---

## 🔍 Keyword Rankings & Trends

| Trend | Keyword | Previous Rank | Latest Rank | Change Detail |
| :---: | :--- | :---: | :---: | :--- |
{chr(10).join(table_rows)}

---

## ⏳ Historical Runs Timeline (Last 10 Checks)

| Check Date & Time | Method | Keywords | Top 3 | Top 10 | Top 30 |
| :--- | :---: | :---: | :---: | :---: | :---: |
{chr(10).join(timeline_rows)}

---
*Note: This report is automatically generated. To run manually or update data, use `python seo_history_manager.py`.*
"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[SUCCESS] Generated ranking report: {REPORT_FILE}")


def log_run_externally(method, rankings_dict):
    """API function to be called from other python scripts to save rankings."""
    db = load_database()
    timestamp = get_current_timestamp()
    add_run_to_database(db, timestamp, method, rankings_dict)
    save_database(db)
    generate_markdown_report(db)


def main():
    parser = argparse.ArgumentParser(description="Manage KolhanHub SEO Historical Rankings Database")
    parser.add_argument("--import-logs", action="store_true", help="Scan and import all local seo_results_*.txt files")
    parser.add_argument("--add-manual", help="Add manual run rankings. Argument should be the date/time string (e.g. '2026-06-24' or ISO timestamp)")
    parser.add_argument("--data", help="Manual rankings data (keyword and rank per line). If not provided with --add-manual, reads from stdin.")
    parser.add_argument("--report", action="store_true", help="Generate the Markdown history report")
    
    args = parser.parse_args()
    
    db = load_database()
    
    if args.import_logs:
        import_existing_txt_logs(db)
        save_database(db)
        generate_markdown_report(db)
        return
        
    if args.add_manual:
        # Determine timestamp
        date_str = args.add_manual
        # If it's just YYYY-MM-DD, add default time or convert to ISO
        if len(date_str) == 10:
            timestamp = f"{date_str}T12:00:00+05:30"
        else:
            timestamp = date_str
            
        # Get data
        if args.data:
            data_text = args.data
        else:
            print("Enter/Paste your manual SEO rankings (Press Ctrl+D or Ctrl+Z then Enter to finish):")
            import sys
            data_text = sys.stdin.read()
            
        rankings = parse_manual_ranking_data(data_text)
        if rankings:
            print(f"[INFO] Parsed {len(rankings)} keywords from manual input.")
            add_run_to_database(db, timestamp, "manual", rankings)
            save_database(db)
            generate_markdown_report(db)
        else:
            print("[ERROR] No rankings parsed. Check your format.")
        return
        
    if args.report:
        generate_markdown_report(db)
        return

    # If no arguments, show database info
    print("KolhanHub SEO History Database Info:")
    print(f"  Database file: {DATABASE_FILE}")
    print(f"  Total runs saved: {len(db['history'])}")
    if db['history']:
        latest = db['history'][-1]
        print(f"  Latest run: {latest['timestamp']} ({latest['method']}) with {len(latest['rankings'])} keywords")
    print("\nUse --help to see all available actions.")


if __name__ == "__main__":
    main()
