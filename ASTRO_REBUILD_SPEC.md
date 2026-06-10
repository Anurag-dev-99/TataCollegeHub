# Tata College Student Hub — Astro Rebuild Specifications

This document defines the requirements, visual design choices, routing structure, and implementation logic for rebuilding the **Tata College Student Hub** using **Astro**. Use this file as the primary source of truth for the rebuild.

---

## 1. Project Goals & Architecture

* **Core Goal**: Transition the legacy Single Page Application (SPA) into a high-performance, SEO-friendly, mobile-first **Astro Static Site (SSG)**.
* **Routing**: Move away from URL hashes (`index.html#pyqs`) to static, crawlabale paths (e.g., `/pyqs/major/mathematics/1/`).
* **Deployment**: Deploy automatically to GitHub Pages using GitHub Actions on pushes to the `main` branch of the `TataCollegeHub` repository.
* **Host URL**: `https://anurag-dev-99.github.io/TataCollegeHub/`

---

## 2. Technical Stack

* **Framework**: Astro (Static mode)
* **Styling**: Vanilla CSS (based on the original `styles.css` system with modern visual improvements)
* **Icons**: Lucide Icons (imported directly in Astro components)
* **Charts**: Chart.js (loaded on the client side for result graphs)
* **Data Layer**: Local static JSON files under `public/data/` (copied from the old project)
* **PDFs**: Stored in `public/pdf/` (syllabuses) or hosted externally on Google Drive (PYQs)

---

## 3. Visual Design System (Modern Neo-Minimalism)

The website should look extremely premium, clean, and run at lightning speed. 

### Palette
* **Theme**: Native Light/Dark Mode (persisted in `localStorage` and toggled via `<html>` attribute).
* **Backgrounds**:
  * Dark Mode: Deep Charcoal (`#0d0e12`) and slate card backgrounds (`#15171e`).
  * Light Mode: Cool Soft Grey (`#f8fafc`) and white card backgrounds (`#ffffff`).
* **Accents**: 
  * Primary: Electric Indigo (`#6366f1` / `#4f46e5`).
  * Secondary/Success: Forest Emerald (`#10b981`).
  * Danger/Deadlines: Warm Amber (`#f59e0b`) or Crimson (`#ef4444`).

### Layout & Micro-interactions
* **Grid**: Clean CSS Grid structure with responsive flex columns.
* **UI Elements**: Soft borders, modern typography (Plus Jakarta Sans or Outfit), and subtle glassmorphic blurs (`backdrop-filter`) for headers/modals.
* **Transitions**: Smooth page loads and hover effects (e.g., scale button on hover, fade-in for notices).
* **Mobile Shell**: Responsive sidebar for desktop and a thumb-friendly sticky header/bottom nav for mobile screens.

---

## 4. Routing & Page Directory Structure

Compile your Astro pages to the following routes:

```
src/pages/
├── index.astro                             # Home Dashboard (notices, quick links, event calendar, recent activity)
├── notices.astro                           # Notice Board (filter by general, exam, admissions; pinned cards at top)
├── results.astro                           # Results Analytics (semester pass rates, toppers chart, CGPA/SGPA comparator)
├── syllabus/
│   ├── index.astro                         # Department selection (Mathematics, Physics, Chemistry, etc.)
│   └── [department].astro                 # Dynamic route: Displays Syllabus details & semesters 1-8 tabs
└── pyqs/
    ├── index.astro                         # Search page: subject selectors and course category filters
    └── [category]/[subject]/[semester].astro # Dynamic route: Shows downloadable papers matching the query
```

---

## 5. Major Features & Logic to Build

### A. The "No Dead Ends" PDF Download System
* **Context**: In the legacy project, clicking on missing PDFs downloaded a blank `.txt` file or failed silently.
* **Requirement**:
  * Check the database (`data/syllabus.json` or `data/pyqs.json`).
  * If a file does not have a real URL or local path, **do not show a download button**. 
  * Replace it with a greyed-out **"Coming Soon"** state and a prominent **"Request Paper"** or **"Submit Paper"** action button.
  * This button should open a modal with a simple Google Form link to allow students to submit papers they have or report missing ones.

### B. Notice Board & Visual Exam Deadlines
* **Requirement**:
  * Parse descriptions inside `data/notices.json`.
  * If a notice description contains keywords like `"last date"`, `"deadline"`, or `"exam form"`, automatically extract the date.
  * Render a bright **Warning Banner** at the top of the Home Dashboard (e.g., `⚠️ Exam Form Deadline: 15-June-2026`) so students never miss form fill dates.

### C. Client-Side Results Charts
* **Requirement**:
  * The `/results` page needs to import `Chart.js`.
  * Since Astro pre-renders HTML, wrap the canvas and chart initialization inside a `<script>` tag that executes only in the client browser.
  * Render:
    1. A Bar Chart showing pass percentages per semester.
    2. A Line Chart tracking overall yearly performance.
    3. An interactive CGPA comparator.

---

## 6. Original Data Schemas (Strict Compliance)

Keep JSON file schemas exactly as follows to prevent data parsing errors:

### `public/data/pyqs.json`
```json
{
  "id": "pyq-mj-math-sem1-mj01-2022",
  "title": "maths_mj_01_sem1_pyq_2022-2026.pdf",
  "year": "2022-2026",
  "semester": 1,
  "category": "Major",
  "subject": "Mathematics",
  "downloadCount": 46,
  "fileSize": "PDF File",
  "downloadUrl": "https://drive.google.com/file/d/FILE_ID/view?usp=sharing"
}
```

### `public/data/syllabus.json`
```json
{
  "id": "syl-math-ug",
  "title": "B.Sc Mathematics Honours Syllabus (FYUGP NEP-2020)",
  "department": "Mathematics",
  "semester": "All Semesters (1-8)",
  "effectiveFrom": "2022 onwards",
  "fileSize": "2.4 MB",
  "description": "Mathematics FYUGP syllabus details.",
  "modules": [
    "Sem 1: MJ-1 (Calculus & Analytical Geometry)",
    "Sem 2: MJ-2 (Real Analysis - I)",
    "Sem 3: MJ-4 & MJ-5",
    "Sem 4: MJ-6, MJ-7 & MJ-8"
  ]
}
```

---

## 7. Immediate Next Steps for the Developer/AI

1. **Copy assets**: Move the `data/` folder and `pdf/` files from the legacy project backup into `public/data/` and `public/pdf/`.
2. **Setup Global Styles**: Move the old CSS tokens and variables into `src/styles/global.css`.
3. **Build layout**: Create `src/layouts/Layout.astro` containing the HTML structure, light/dark theme switch, search suggestions header, and footer.
4. **Implement dynamic routing**: Start with `src/pages/syllabus/[department].astro` and generate paths using `getStaticPaths()`.
