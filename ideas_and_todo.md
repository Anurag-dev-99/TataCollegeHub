# 🎯 KolhanHub — Daily To-Do & Future Ideas

Welcome back! This file is your dashboard for immediate tasks, content creation, and experimental ideas. Keep this open as your go-to guide.

---

## 📅 Today's Must-Do List (June 20, 2026)

- [ ] **Create and Post Your First YouTube Short!** (See guide below — this is your #1 priority today 🚀)
- [ ] **Share the #1 Google Rank with Friends:** Ask 2-3 classmates to search "kolhan pyq" in Incognito and send you screenshots.
- [ ] **Push the latest `seo_open_tabs.py` update to GitHub** so your local changes are backed up.
  ```powershell
  git add seo_open_tabs.py
  git commit -m "tool: update open tabs script to support Chrome Incognito & pws=0"
  git push
  ```

---

## 🎥 YouTube Shorts: No-Face, High-Impact Plan

Creating content can feel lazy/difficult when you think you need to show your face, record voiceovers, or do heavy editing. **You don't need to do any of that.** 

Because your website is now **#1 on Google for "kolhan pyq"**, your first Short will write itself.

### 📝 30-Second Shorts Script (No Face Needed)
* **Hook (0-5s):** Show a laptop or phone screen. Type on screen: *"Still asking seniors for Kolhan University PYQs?"*
* **Body (5-15s):** Screen record yourself opening Google Chrome, typing `kolhan pyq`, and showing your website `kolhanhub.in` sitting proud at **#1**.
* **Value (15-25s):** Click the link, show how fast the page loads, click on a semester, and download a paper in 1 tap.
* **Call to Action (25-30s):** Text on screen: *"Stop wasting time. Search 'kolhan pyq' on Google or go to kolhanhub.in. Link in bio/comments."*

### ⚡ Why you should do this TODAY:
1. **0 Subscribers is fine:** YouTube's Shorts algorithm pushes videos to random users' feeds based on interests, meaning you can easily get 500–2,000 views on your very first upload.
2. **Backlink & Traffic Power:** If 50 students search "kolhan pyq" after seeing your video, it tells Google's algorithm that your site is highly clicked, locking in your #1 rank forever.
3. **Takes 10 Minutes:** Use your phone to record your screen, add a trending audio track directly in the YouTube app, add some text, and hit post. **Do it today!**

---

## 💡 Future Ideas & Experimental Features

### 🌐 1. Interactive 360° Campus & Department Tours
Anurag's idea to help new and old students locate departments (Exam Department, Science block, specific teachers) using 360° photos and drone shots.

#### ❓ Is it possible to host 360° photos on our site?
**Yes, absolutely.** You don't need to be a giant company like Google to do this. We can implement this directly in Astro.

#### ❓ Will it make our website slow?
If we do it wrong, yes. 360° images are massive (often 5MB to 15MB) because they need high resolution. If loaded on page load, they will ruin performance.
**How we keep it super-fast:**
1. **Lazy Loading:** We only load the 3D viewer library and the heavy image *after* a student clicks a "Launch 360° View" button.
2. **Lightweight Library:** We will use **Pannellum** — a tiny, open-source 360° viewer library that requires no dependencies and is only ~20KB.
3. **Google Maps Embed (Alternative):** We can embed existing Google Street View panoramas via iframes, which puts 0 load on our servers.

#### ❓ How does it help SEO?
Google tracks **Dwell Time** (how long a user stays on your website). If a new student spends 2 minutes rotating a 360° photo of the chemistry department to find where a room is, Google views your site as highly valuable. This drastically improves your ranking authority.

#### 🛠️ How 360° Photos Work:
1. **The Equirectangular Image:** You take a flat 2D panorama image that has a `2:1` aspect ratio (covers 360 degrees horizontal and 180 degrees vertical). You can take these on your phone using standard panoramic apps or the Google Street View app.
2. **The 3D Sphere projection:** The Javascript library (Pannellum) takes this flat image, maps it inside a virtual 3D sphere, and places the user's camera in the center. When the user drags, the camera rotates.

#### 📍 Roadmap for implementation:
* [ ] **Capture:** Go to the Tata College campus and take 3-4 clean 360° panoramas (e.g., Main Entrance, Exam block, Library, Science block).
* [ ] **Develop a Sandbox:** We will build a small `/campus-tour` page using the Pannellum library.
* [ ] **Overlay Hotspots:** Add clickable pins inside the 360° image (e.g., clicking on a door shows "Go to Chemistry Lab").

---

### 🚁 2. Drone Shot Campus Map
* Use a high-quality top-down drone photograph of the Tata College campus.
* Create an interactive **SVG Map Overlay** where clicking different buildings opens information cards or links to their respective 360° interior tours.

---

### 📚 3. Official Syllabus & PYQ Verification (Tata College Visit)
* **Objective:** Ensure only 100% verified, up-to-date syllabi and PYQs are hosted to prevent student confusion.
* **Why:** Many links from the old Kolhan University website redirect to a generic downloads index page (`https://old.kolhanuniversity.ac.in/index.php/students/downloads.html`) due to missing files on their server. Checking and fixing 280+ links manually is highly time-consuming and can lead to obsolete files.
* **Plan:**
  * Postpone automated link correcting/scraping for now.
  * Anurag will visit Tata College Chaibasa in person.
  * Ask teachers and department heads directly for guidance, official syllabus files, and PYQs.
  * Manually upload only verified, correct files directly to our hosting, bypassing unstable external links.
