# Astro Project Rebuild & Handoff Guide

This file provides a summary of the work completed to rebuild the **Tata College Student Hub** in Astro, including the custom domain launch and performance optimization, and guides how to resume development in the next session.

---

## 1. Accomplished Work Summary

### A. Custom Domain Migration & Setup (`kolhanhub.in`)
1. **Domain Launch:** Connected the custom domain **`kolhanhub.in`** to replace the old GitHub Pages subpath `anurag-dev-99.github.io/TataCollegeHub`.
2. **DNS & KYC Configuration:** 
   * Completed NIXI registry Aadhaar KYC verification on GoDaddy to unlock DNS settings.
   * Pointed the domain’s DNS `A` records to GitHub's server IPs:
     * `185.199.108.153`
     * `185.199.109.153`
     * `185.199.110.153`
     * `185.199.111.153`
   * Configured the `CNAME` record for `www` to point to `anurag-dev-99.github.io`.
3. **Repository Pages Configuration:**
   * Set Custom Domain to `kolhanhub.in` and checked **Enforce HTTPS** (SSL certificate generated successfully).
   * Created a [CNAME](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/public/CNAME) file containing `kolhanhub.in` in the public directory to maintain custom domain routing across compiles.
4. **Site Paths & SEO Updates:**
   * Set `site: 'https://kolhanhub.in'` and base path `base: '/'` in [astro.config.mjs](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/astro.config.mjs), changing the site root from a subdirectory to the root.
   * Updated canonical tags, school schemas, and metadata paths in [Layout.astro](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/layouts/Layout.astro) to point to the new domain.
   * Replaced the hardcoded `/TataCollegeHub` base path in [results.astro](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/pages/results.astro) client-script fetch calls with Astro's dynamic `BASE_URL` logic.
   * Updated [robots.txt](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/public/robots.txt) to target sitemap indexing at `https://kolhanhub.in/sitemap-index.xml`.

### B. Speed & Core Web Vitals Optimization
* **LCP Layout Shift Resolved:** Disabled the automatic slide-in popup of the Floating Request Toast inside [Layout.astro](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/layouts/Layout.astro). This toast was popping up after a 3.5s delay, which Lighthouse flagged as a late Largest Contentful Paint (LCP) shift. Disabling the auto-popup restored a perfect **Grade A / 100% Performance (562ms LCP, 65ms TBT)** on GTmetrix. (The request paper buttons themselves still work 100% manually).

### C. Analytics & Search Integrations
1. **Google Analytics (GA4):** Updated the Web Data Stream URL inside the GA Admin Panel from the old GitHub subdirectory link to the new root domain `https://kolhanhub.in`. No code changes were needed because the Measurement ID `G-TV5YZQ3ELX` is already integrated in layout headers.
2. **Google Search Console (GSC):** Added the new prefix property `https://kolhanhub.in/` and submitted the new sitemap `https://kolhanhub.in/sitemap-index.xml` for indexing. Requested indexing for key URLs: Home (`/`), Results (`/results/`), Syllabus (`/syllabus/`), Notices (`/notices/`), and PYQs (`/pyqs/`).

---

## 2. File Architecture & Key Codebases

### A. Astro Web Application
* **Global Layout:** [Layout.astro](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/layouts/Layout.astro) (Handles headers, Google Analytics tags, search databases, request webhook, and mobile triggers).
* **Results Portal:** [results.astro](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/pages/results.astro) (Result announcement hubs, autocomplete roll search, student comparisons, Chart.js graphs, and browse lists).
* **Syllabus Directory:** [src/pages/syllabus/index.astro](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/pages/syllabus/index.astro) (Multi-disciplinary tabs and syllabus indexing).
* **CGPA Calculator:** [cgpa.astro](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/pages/cgpa.astro) (Standalone SGPA to CGPA converter widget).

### B. Python Data Utility Scripts
These utility scripts are located in the repository root and are used for processing, validation, and merging student academic results data:
* [merge_sem3.py](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/merge_sem3.py): Script for processing and merging Semester 3 academic records.
* [merge_sem6.py](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/merge_sem6.py): Script for processing and merging Semester 6 academic records.
* [merge_sem6_phy.py](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/merge_sem6_phy.py): Tailored merging script for Semester 6 Physics students.
* [validate_phy.py](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/validate_phy.py): Validation script checking constraints and data integrity for Physics students.

### C. Google Sheets Integration
* [google-sheets-script.js](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/google-sheets-script.js): Contains the Google Apps Script code deployed to the linked Google Sheets sheet. This manages paper request workflows, notices logging, or feedback submissions sent from the web app client.

---

## 3. How to Resume in the Next AI Session
Copy and paste this instruction when launching a new pairing session under your Google AI Pro / other model workspaces (which has full API quota):

```markdown
Resume pair-programming on the Tata College Hub portal (kolhanhub.in).
Read the Handoff Guide in `./Astro_Project_Handoff.md` to review the custom domain launch and codebase structure.

Key Instructions for the Agent:
1. Run `npm run dev` in the terminal to verify the local development environment works.
2. Check Google Search Console (https://search.google.com/search-console) for kolhanhub.in to verify sitemap status (the "Couldn't fetch" quirk resolves to green "Success" automatically over 24-48h) and track search keywords.
3. Help the user implement new features, upload notices (`notices.json`), connect new PYQ PDFs, or process academic results using the Python scripts in the root directory.
4. Continue using maximum visual quality (vanilla CSS, sleek dark modes, premium typography) and keep GTmetrix performance at Grade A (LCP < 1.0s, no auto-popup delay layout shifts).
```
