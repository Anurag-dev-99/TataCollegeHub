# KolhanHub (TataCollegeHub) — Master Project Context

> **Read this file first in every new conversation / with every new AI model.**
> Keep it updated: add a line to the Changelog (section 11) after every meaningful change.
> Last updated: 2026-10-30

---

## 0. First-message prompt for a new AI conversation

Paste this as the first message, then add your task:

```
Read PROJECT_CONTEXT.md in the project root fully before doing anything.
Follow its rules strictly (especially section 2 "Hard rules" and section 6 "Homepage playbook").
Task: <describe what you want>
```

---

## 1. What this project is

- **KolhanHub** — free student resource hub for **Kolhan University** (Tata College, Chaibasa) students: PYQs, syllabus, notices, results, CGPA calculator, exam info.
- Live site: **https://kolhanhub.in** (custom domain, GitHub Pages, HTTPS enforced). Repo: `TataCollegeHub`.
- Audience: mostly mobile users, students of FYUGP (NEP) batches 2022–2028.
- Brand tone: student-first, friendly, no pressure. Social recognition (names/Instagram) rather than money for contributors.
- Claims used on site: 10,000+ downloads, #1 on Google for several "kolhan pyq" keywords. Don't invent new numbers.

## 2. Hard rules (never break)

1. **NEVER run `git commit` / `git push` / stage files.** The owner does all Git manually (see `.agents/AGENTS.md`).
2. **Always run `npm run build` after edits.** It must finish with 0 errors. (Last known: 143 pages.)
3. **Only touch what the task asks.** `src/pages/index.astro` is ~2,300 lines with many unrelated sections — never "tidy up" other sections.
4. When deleting a section, also delete its own `<script>` block and any now-unused data. Leave at most one blank line behind.
5. Use **inline styles** + the CSS variables already used in the file. Don't introduce new CSS frameworks/classes.
6. Don't change webhook / Google Apps Script URLs, GA ID, or `CNAME`.
7. Don't edit `dist/`, `.astro/`, `node_modules/` (generated).
8. Never expose private student data (roll numbers etc. only exist in result JSON that is already public by design — don't add more personal data like phone numbers).
9. Ask the owner if a request is ambiguous (e.g. which semester/batch) instead of guessing dates or fees.

## 3. Tech stack

| Thing | Value |
|---|---|
| Framework | **Astro 6** (static output, `.astro` files = HTML + TS frontmatter) |
| Language | TypeScript in frontmatter, plain JS in `<script>` blocks, inline-style HTML |
| Icons | `@lucide/astro` (e.g. `<Download size={12} />`) |
| Charts | `chart.js` (results page) |
| SEO | `@astrojs/sitemap` → `sitemap-index.xml` |
| Node | >= 22.12 |
| Hosting/CI | GitHub Pages via `.github/workflows` (deploys on push to `main`) |
| Analytics | GA4 `G-TV5YZQ3ELX` (in `Layout.astro`) |
| Backend | **Google Apps Script** web app (`google-sheets-script.js`) → Google Sheets: logs downloads, paper requests/submissions, serves live download stats |
| Helper scripts | Python (`*.py` in repo root) for editing/validating JSON data; PowerShell on Windows |

Commands: `npm run dev` (local), `npm run build` (verify), `npm run preview`.
Windows + PowerShell is the dev environment (use `;` not `&&`).

## 4. Folder map

```
TataCollegeHub/
├─ src/
│  ├─ layouts/Layout.astro      # global shell: header/nav, GA, search, request toast, SEO schema
│  ├─ styles/global.css         # CSS variables (--text-primary, --radius-sm, --font-display …)
│  └─ pages/
│     ├─ index.astro            # HOMEPAGE (most edits happen here)
│     ├─ notices.astro  results.astro  recheck.astro  cgpa.astro
│     ├─ exam-archive.astro  faq.astro  about.astro  contact.astro  privacy.astro
│     ├─ pyqs/ ([category]/…)   # PYQ browser pages
│     └─ syllabus/ (index, [department])
├─ public/
│  ├─ data/                     # ALL site content as JSON (see section 5)
│  ├─ pdf/ pdfs/ images/        # static assets; CNAME, robots.txt
├─ scripts/                     # result-scraping guides (ADMIT_CARD_GUIDE.md, KOLHAN_RESULT_KNOWLEDGE.md …)
├─ trackers/                    # PYQ coverage trackers
├─ google-sheets-script.js      # Apps Script source (deployed separately in Google)
├─ *.py                         # one-off data maintenance scripts (add_*, update_*, fix_*, check_*)
└─ md docs: Astro_Project_Handoff.md, DATA_REGISTRY.md, ideas_and_todo.md, ASTRO_REBUILD_SPEC.md, seo_history_report.md
```

Related but **separate** repo/folder: `kolhan-result` (Next.js results/leaderboard project). Don't mix the two.

## 5. Data files (`public/data/`)

| File | Purpose | Key shape |
|---|---|---|
| `pyqs.json` | Every PYQ (≈230). Powers PYQ pages, homepage stats, "What's New" | `{id, title, year:"2022-2026", semester, category, subject, downloadCount, fileSize, downloadUrl}` |
| `notices.json` | Notices page + homepage pinned notices | `{id, title, date, category, isPinned, isArchived, description, links[]}` |
| `syllabus.json`, `kolhan_syllabi.json` | Syllabus listings | — |
| `mdc.json`, `sec.json`, `vac.json`, `aec.json`, `iks.json` | Subject lists per course type | — |
| `exam-schedule.json`, `exam-archive.json` | Exam dates / past exams | `[{date, day, sittings:[{sitting,time_start,time_end,paper_type,details}]}]` |
| `calendar.json`, `holidays-2026.json` | Academic calendar & holidays | — |
| `results*.json`, `results_semN_master.json` | Result data (Tata College only) | see `DATA_REGISTRY.md` |
| `faq.json` | FAQ | — |

PYQ **categories**: Major, Minor, MDC, VAC, AEC, SEC, IKS. `category`/`subject` strings must match existing spelling or filters break (use the `check_*.py`/`verify_*.py` scripts).
Drive links must be `https://drive.google.com/file/d/<ID>/view?usp=drive_link` (or `usp=sharing`).

**Archiving a notice:** set `isPinned:false`, `isArchived:true` (never delete).

## 6. Homepage playbook (`src/pages/index.astro`)

Frontmatter imports `notices.json`, `calendar.json`, `pyqs.json`, `holidays-2026.json` and defines `baseUrl`.
Use `` {`${baseUrl}/path`} `` for internal links.

### Current section order (top → bottom; line numbers drift, search by the marker text)

1. Header welcome (`<!-- Header welcome -->`, hero text)
2. **Temporary banner zone** — directly after the hero, **before** the Thank You accordion. *Currently empty.* All time-limited items go here (exam clock, form fill-up notice, practical notes, etc.)
3. Thank You accordion — `THANK YOU - COLLAPSIBLE ACCORDION`, ids `thankyou-toggle` / `thankyou-content` (stats text only; **no contributors here**)
4. Contribute & Support — `CONTRIBUTE & SUPPORT - SIDE BY SIDE BOXES` ("Help Your Juniors" + "Support" boxes)
5. Requests Completed accordion — ids `completed-requests-trigger` / `completed-requests-content`
6. **File Contributors accordion** — `<!-- ===== FILE CONTRIBUTORS`, ids `contributors-trigger` / `contributors-content`, preview text `id="contributors-preview"` ("Ayushi & 17 others")
7. Quick Actions — `QUICK ACTIONS`
8. Can't find your paper (Request / Submit Paper) — `CAN'T FIND YOUR PAPER`
9. What's New + Activity Stats — `WHAT'S NEW + ACTIVITY STATS` (stats come from `pyqs.json` at build + live fetch from Apps Script)
10. Schedule & Calendar / Deadlines / Holidays modal + several `<script>` blocks (holidays logic appears **twice** — existing duplication, don't "fix" unless asked)
11. FAQ teaser, Notes Coming Soon, Buy Me a Chai donation + modal

### Design tokens (reuse, don't invent)

- Text: `var(--text-primary|secondary|tertiary)`, borders `var(--border-color)`, radius `var(--radius-sm|xs)`, headings `var(--font-display)`
- Accent colors (use as `rgba(...,0.2)` borders / `0.04–0.1` backgrounds): indigo `#818cf8`, green `#34d399`/`rgba(37,211,102,…)`, amber `#fbbf24`, red `#f87171`, purple `#a78bfa`
- Sizes: titles 0.82–0.95rem weight 800; body 0.68–0.85rem; pills `border-radius:20px; padding:2px 8px; font-size:.6rem`; buttons `border-radius:20px; padding:4px 12px`
- Mobile-first; flex rows with `flex-wrap: wrap`; emoji icons are fine.

### Banner template (compact, e.g. a PDF/notice link)

```html
<div style="margin-bottom: 1rem; border: 1px solid rgba(139,92,246,0.2); border-radius: var(--radius-sm); padding: 0.7rem 1rem; background: linear-gradient(135deg, rgba(139,92,246,0.04) 0%, rgba(0,0,0,0.12) 100%);">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:0.5rem; flex-wrap:wrap;">
    <div style="display:flex; align-items:center; gap:0.5rem; min-width:0;">
      <span style="font-size:1rem; flex-shrink:0;">🔬</span>
      <div>
        <div style="font-size:0.82rem; font-weight:800; color:#a78bfa; font-family:var(--font-display);">TITLE</div>
        <div style="font-size:0.68rem; color:var(--text-tertiary); margin-top:1px;">subtitle</div>
      </div>
    </div>
    <a href="LINK" target="_blank" rel="noopener" style="display:inline-flex; align-items:center; gap:0.3rem; font-size:0.68rem; font-weight:700; color:#a78bfa; text-decoration:none; background:rgba(139,92,246,0.1); border:1px solid rgba(139,92,246,0.25); border-radius:20px; padding:4px 12px; white-space:nowrap;">
      <Download size={12} /> Download PDF
    </a>
  </div>
</div>
```

Wrap every temporary banner in a clearly named comment, e.g. `<!-- SEM 5 EXAM FORM FILL-UP -->` … so it is easy to find and delete later.

### Exam-clock pattern (used for Sem 4 and Sem 7 earlier; now removed)
Container with title + "Notice PDF" / "Centre PDF" buttons → toggle row showing next exam + live countdown → expandable per-date cards → one `<script>` with a `schedule` array and a `setInterval(tick,1000)`. Ids used before: `s4-toggle-row`, `s4-cards-grid`, `s4-all-done`. To rebuild: take the dates JSON the owner supplies (format in section 5), keep **IST (+05:30)**, and remove the whole block (HTML + script) once all exams finish. Previous versions are in git history (commit "removed sem7 exam table and sem4 practical and sem 3 exam form fill date" removed the latest one — `git show` its parent to copy the code).

### File Contributors — row pattern

Each contributor = one `req-row` grid + a 1px divider. Initial avatar with a unique gradient, name (optional `(nickname)`), small "major · college" line, description on the right, optional Instagram icon link (`https://instagram.com/<user>`, no `@`).
When adding/removing: also update `contributors-preview` ("Ayushi & N others", N = total − 1). Max ~20 rows. Full HTML + color palette are in the artifact `contributor_system_plan.md` (conversation history); copy a neighbouring row if unsure.
Collection message to contributors (soft tone): *"Thank you for sharing! If you'd like, we can add your name (and Instagram) to our contributors list — totally optional."* Ask name + optional Instagram first; major/college only if names clash.

## 7. Common tasks — checklists

**A. Add a new notice / banner**
1. Add the item to `notices.json` (pinned if urgent) **and/or** a banner in the banner zone.
2. Use Drive links in the `…/view?usp=drive_link` form.
3. `npm run build`.

**B. Remove an expired section** — delete HTML + its `<script>`; archive related notice in `notices.json`; build.

**C. Add PYQs** — add entries to `pyqs.json` (unique `id`, correct `category`/`subject`/`semester`/`year`), run `python verify_pyqs.py` / relevant `check_*.py`, build. Log the request in `ideas_and_todo.md` "Request Completed Log".

**D. Add/Update a contributor** — see section 6.

**E. Exam schedule update** — update/replace the dates in the exam clock `schedule` array (if one is live) and notice PDF links; double check day-of-week for each date.

## 8. University rules the site explains (FYUGP / NEP)

- Course types: **MJ** (Major), **MN** (Minor), **MDC** (Multidisciplinary), **AEC** (Ability Enhancement), **SEC** (Skill Enhancement), **VAC** (Value Added), **IKS**.
- **MDC rule:** you can only pick an MDC subject that is *not* in your 10+2 marksheet, *not* chosen as MDC-1 (Sem 1) or MDC-2 (Sem 2); no repeating; Commerce students can't take Commerce as MDC-3.
- **AEC-3 (Sem 3) and AEC-4 (Sem 4) are the same language** — choose after reading both syllabi. **SEC-3** is considered high-scoring.
- **Sem 3 exam form fees (2025-session notice):** Arts/Commerce (non-practical) ₹410 · Arts (practical) ₹480 · Science ₹500 · Vocational (Business Admin, Computer Application, IT, Mass Comm, Env & Water Mgt) ₹750. Late fine: ₹200 / ₹500 / ₹1000 in successive 5-day windows.
- Official portal for forms: **https://www.kuuniv.in/login** (NOT `kuuniv.ac.in`, which does not work).

## 9. Backend / integrations

- `google-sheets-script.js` (Apps Script web app) — handles: download count logging, "Request a paper", "Submit a paper", and returns live stats to the homepage (`STATS_URL` in `index.astro`; webhook in `Layout.astro`). Changing the script requires **re-deploying in Google Apps Script** (owner does this).
- Google Search Console property: `https://kolhanhub.in/` (sitemap submitted). SEO rank tracking scripts: `seo_rank_checker*.py`, `seo_history_manager.py`.
- Performance: the request toast auto-popup is **intentionally disabled** (it hurt LCP). Don't re-enable.

## 10. Known loose ends / ideas

- `notices.json` still has the Sem 3 form fill-up notice (`notice-sem3-formfillup-2024batch`) pinned & unarchived although the deadline passed (15 Oct) — likely should be `isArchived:true` (ask owner first).
- Holidays script block duplicated in `index.astro`.
- Results for newer semesters (Sem 5/7) are not on the site (see `DATA_REGISTRY.md`).
- Contributor list could move to a data-driven `contributors.json` if it grows beyond ~20 people.
- Sem 4 Physics Minor practical notes PDF: `https://drive.google.com/file/d/1ss3mpfG872iAHBmVeSrPVldMszXPV70N/view?usp=drive_link` — suggested permanent homes: a "Notes" section/Syllabus page for Physics instead of a homepage banner.
- Other docs with more detail: `ideas_and_todo.md` (requests log + to-do), `DATA_REGISTRY.md` (result data), `Astro_Project_Handoff.md` (domain/SEO history), `scripts/*.md` (scraping guides).

## 11. Changelog (newest first — append here)

| Date | Change |
|---|---|
| 2026-10-30 | Created this `PROJECT_CONTEXT.md`. |
| 2026-10-23 | Removed expired homepage blocks: Sem 7 exam clock, Sem 3 form fill-up card, Physics Minor Sem 4 practical-notes banner. Build OK (143 pages). |
| 2026-10-02 | Moved "Top Contributors" out of Thank You; added contributor Afshan Ishaque (Zoology Major Sem 1); designed contributor system (nickname, major/college, Instagram link, PYQ count). |
| 2026-10 | Sem 7 (2022 batch) exam clock with **revised** dates (Oct 7–9, 12–13 …) + notice & centre PDFs. Added Physics Minor Sem 4 practical notes banner. |
| 2026-09 | Added Sem 3 form fill-up card (2024 batch + 2023 ex-regular), fees & tips dropdown; fixed form link to `https://www.kuuniv.in/login`; removed AEC exam clock and Sem 4 notices after exams ended. |
| 2026-08-13 | Result data registry updated (Sem 1/2/3/4/6 master JSONs live). |
| 2026-06-18 | Migrated to custom domain `kolhanhub.in`; GA4 + GSC updated; LCP fix (request toast auto-popup disabled). See `Astro_Project_Handoff.md`. |

