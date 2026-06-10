# Tata College Student Hub — Astro Rebuild Specifications (Implementation Completed)

This document serves as the primary specification and documentation of the **implemented** Astro migration for the **Tata College Student Hub**. It details the architecture, routing, visual style constraints, completed features, and commands to build/maintain the project.

---

## 1. Project Architecture & Live URLs

* **Framework**: Astro 6+ Static Site Generation (SSG).
* **Repository**: `TataCollegeHub`
* **Base Path**: The site is compiled with a base path configured in `astro.config.mjs` as `base: '/TataCollegeHub'`. All links must prepend this base URL dynamically using `${baseUrl}` in templates.
* **Production Host**: Hosted on GitHub Pages at `https://anurag-dev-99.github.io/TataCollegeHub/`.
* **Deployment Pipeline**: Deployed automatically via GitHub Actions `.github/workflows/deploy.yml` on every push to the `main` branch.

---

## 2. Implemented Features & Routing

The project uses static, indexable, and crawler-friendly routes compiled into HTML/CSS files:

* **`/index.html` (Home Dashboard)**:
  * Renders recent notices, shortcut cards, and upcoming calendar schedules.
  * **Automated Deadline Banner**: Scans notice descriptions for keywords like `last date`, `deadline`, or `admission form` and dynamically displays a prominent red warning banner at the top of the dashboard.
* **`/notices/index.html` (Notice Board)**:
  * Lists and categorizes all college notices from `notices.json`.
  * Features category tab switching (All, Exams, Admissions, Academic, Results).
  * Includes a `[View Archived Notices]` button that reveals older notices.
* **`/results/index.html` (Results Portal & CGPA Calculator)**:
  * Shows overall metrics and features an **Interactive CGPA / SGPA Calculator** for students to input marks and project scores.
* **`/syllabus/` (Syllabus Directory & Detail dynamic pages)**:
  * `/syllabus/index.html` selects departments.
  * Dynamic `/syllabus/[department]/index.html` details courses and displays tabbed modules (Sem 1 to 8).
  * **"No Dead Ends" Filtering**: Astro compiles **only** pages and tab elements that have actual files in `public/pdf` or external links, dropping compile paths from 34 to 12. If a specific tab has no PDF, it shows a greyed-out "Coming Soon" label alongside a button to request the file.
* **`/pyqs/` (PYQs Directory & dynamic pages)**:
  * `/pyqs/index.html` features categories (*Major, Minor, MDC, SEC, VAC, AEC*) with expandible accordions containing active subjects.
  * Dynamic routes `/pyqs/[category]/[subject]/[semester]/index.html` list matching download assets. If empty, it triggers the Request modal.

---

## 3. Simplified Contributions & Privacy Request flows

The submission and request flows are wired globally in `src/layouts/Layout.astro` and customize how students share or request papers:

### A. Simplified Submission (Premium Cards)
* Clicking any **"Submit Paper"** button bypasses text input forms completely.
* Instantly triggers `#submit-modal` containing a premium 2-column card layout:
  * **Google Form Card**: Directs to the official upload form (Recommended, 100% anonymous & private).
  * **WhatsApp Card**: Opens a direct chat link to the admin.
* Utilizes a `.submit-grid` responsive layout in `global.css` that displays a 1-column layout on mobile viewports and transitions to 2 columns on desktop.

### B. Dedicated Request Modal with Privacy Choices
* Clicking any **"Request Paper"** button opens `#request-modal` which gathers targeted details:
  * Student's Name
  * Semester (Dropdown 1 to 8)
  * Course Category (Major, Minor, SEC, MDC, AEC, VAC)
  * Subject/Paper Name
  * Exam Year (Dropdown)
  * Session/Batch (Dropdown)
  * Contact Number (Optional)
* **Dual-Action Success Delivery**: Upon form submission, the modal prompts the user to select how they want to submit the request:
  1. **Send via WhatsApp (Fastest)**: Launches a prefilled text template containing all form options to send directly to the admin (discloses the student's phone number).
  2. **Submit Anonymously (Google Form)**: Redirects to the official Google Form (100% private, no phone number revealed).

---

## 4. Visual Theme & CSS Variables

The styles are configured in [global.css](file:///c:/Users/Anurag/Documents/GitHub/TataCollegeHub/src/styles/global.css) conforming to the original design assets:
* **Palette**: Dark theme by default to prevent flashes of light on mobile devices.
  * Midnight Blue background: `#090d16`
  * Slate cards container backgrounds: `#111625`
  * Primary Accent (Indigo highlight): `#6366f1` / `#4f46e5`
  * Secondary Accent (Forest Emerald success): `#10b981`
* **Fonts**: `Plus Jakarta Sans` for body text and `Outfit` for display headings (loaded from Google Fonts).
* **Responsive Mobile Shell**: Left-aligned sidebar on desktop and a native thumb-friendly bottom nav bar (6 tabs matching the legacy layout: Home, PYQs, Syllabus, Notices, Results, and CGPA) on mobile.

---

## 5. Development & Deployment Commands

Since script execution policy might be restricted on the Windows host, execute all npm/astro actions by invoking cmd directly:

### Local Development Server
To start the live development server:
```powershell
cmd.exe /c npm run dev
```

### Build & Compilation
To compile the static pages under the `/dist/` folder:
```powershell
cmd.exe /c npm run build
```

### Local Network Preview (For Mobile/Android Testing)
To preview the compiled production build from local network devices (e.g. Android devices on the same Wi-Fi) on port `4321` (or next free port):
```powershell
cmd.exe /c npm run preview -- --host
```
* **Local url**: `http://localhost:4321/TataCollegeHub`
* **Network url**: `http://192.168.29.208:4321/TataCollegeHub` (adjust based on host IP)

---

## 6. Configured External Integration Links

* **Admin WhatsApp Contact**: `+918002059887`
* **Official Google Form Link**: `https://docs.google.com/forms/d/e/1FAIpQLSdBj3G1eQnF6zIrHjc5VtudcCzknOV1wsUXT2dE4xE11P9Qgg/viewform?usp=sharing&ouid=101804319546278458995`
