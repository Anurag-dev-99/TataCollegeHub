/**
 * KU MARKSHEET HTML BULK DOWNLOADER
 * Downloads HTML marksheets for ALL students using multiple parallel browser instances.
 * Supports resume (skips already-downloaded files).
 * 
 * Usage: node download_html_bulk.js [NUM_BROWSERS] [START_INDEX]
 *   NUM_BROWSERS: Number of parallel browsers (default: 5)
 *   START_INDEX: Start from this index in the roll list (default: 0)
 * 
 * IMPORTANT: Copy this file to C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs\
 *            before running, so it has access to Playwright and the roll number files.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// === Configuration ===
const ROLL_FILE = path.join(__dirname, '..', '2023', 'sem2', 'all_roll_numbers.json');
const OUTPUT_DIR = path.join(__dirname, '..', '2023', 'sem2', 'marksheet_html');
const SEMESTER = 'II';  // Roman numeral for Sem 2
const NUM_BROWSERS = parseInt(process.argv[2]) || 5;
const START_INDEX = parseInt(process.argv[3]) || 0;

if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true });

// === Load roll numbers ===
const allRolls = JSON.parse(fs.readFileSync(ROLL_FILE, 'utf-8'));
console.log(`Total roll numbers: ${allRolls.length}`);

// === Check already downloaded ===
const existing = new Set(
  fs.readdirSync(OUTPUT_DIR)
    .filter(f => f.endsWith('.html'))
    .map(f => f.replace('_sem2.html', '').replace('_sem2_full.html', ''))
);
console.log(`Already downloaded: ${existing.size}`);

const remaining = allRolls.filter((r, i) => i >= START_INDEX && !existing.has(r));
console.log(`Remaining to download: ${remaining.length}`);
console.log(`Using ${NUM_BROWSERS} parallel browsers\n`);

if (remaining.length === 0) {
  console.log('All done! Nothing to download.');
  process.exit(0);
}

// === Stats tracking ===
let success = 0;
let errors = 0;
let startTime = Date.now();

function printProgress() {
  const elapsed = (Date.now() - startTime) / 1000;
  const total = success + errors;
  const rate = total > 0 ? total / elapsed : 0;
  const eta = rate > 0 ? ((remaining.length - total) / rate / 60).toFixed(0) : '?';
  process.stdout.write(
    `\r  [${total}/${remaining.length}] OK:${success} Err:${errors} | ` +
    `${rate.toFixed(1)}/s | ETA: ${eta} min   `
  );
}

// === Worker function: one browser instance processing a chunk of rolls ===
async function workerFn(workerId, rolls) {
  let browser = await chromium.launch({ headless: true });
  let context = await browser.newContext();
  let page = await context.newPage();

  // Navigate to KU result page once
  await page.goto('https://www.kuuniv.in/result/login', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(1500);

  for (let ri = 0; ri < rolls.length; ri++) {
    const roll = rolls[ri];

    try {
      // Select Course = FYUGP
      const courseSelect = page.locator('select').first();
      await courseSelect.selectOption('FYUGP').catch(() =>
        courseSelect.selectOption({ label: 'FYUGP' })
      );
      await page.waitForTimeout(300);

      // Select Semester
      const semSelect = page.locator('select').nth(1);
      await semSelect.selectOption(SEMESTER).catch(() =>
        semSelect.selectOption({ label: SEMESTER })
      );
      await page.waitForTimeout(300);

      // Select Stream = nep
      const streamSelect = page.locator('select').nth(2);
      await streamSelect.selectOption('nep').catch(async () => {
        try { await streamSelect.selectOption({ label: 'nep' }); } catch(e) {
          await streamSelect.selectOption({ label: 'NEP' }).catch(() => {});
        }
      });
      await page.waitForTimeout(300);

      // Enter roll number
      const rollInput = page.locator('input[type="text"], input[type="number"], input[placeholder*="roll" i], input[ng-model*="roll" i]').first();
      await rollInput.fill('');
      await rollInput.fill(roll);
      await page.waitForTimeout(200);

      // Click submit
      const submitBtn = page.locator('button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Search"), button:has-text("Get Result")').first();
      await submitBtn.click();

      // Wait for marksheet to render
      await page.waitForTimeout(2500);
      await page.waitForSelector('.content-wrapper, .box-body, table', { timeout: 8000 }).catch(() => {});
      await page.waitForTimeout(500);

      // Extract marksheet HTML
      const marksheetData = await page.evaluate(() => {
        const printArea = document.querySelector('.content-wrapper') ||
                         document.querySelector('#printArea') ||
                         document.querySelector('.box-body') ||
                         document.querySelector('.container-fluid');

        if (printArea) {
          let styles = '';
          for (const sheet of document.styleSheets) {
            try {
              for (const rule of sheet.cssRules) {
                styles += rule.cssText + '\n';
              }
            } catch(e) {
              if (sheet.href) styles += `/* External: ${sheet.href} */\n`;
            }
          }
          return {
            content: printArea.outerHTML,
            styles: styles,
            title: document.title
          };
        }
        return null;
      });

      if (marksheetData) {
        const cleanHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>${marksheetData.title}</title>
<style>
${marksheetData.styles}
</style>
<link rel="stylesheet" href="https://www.kuuniv.in/result/resources/css/bootstrap.min.css">
<link rel="stylesheet" href="https://www.kuuniv.in/result/resources/css/AdminLTE.min.css">
</head>
<body>
${marksheetData.content}
</body>
</html>`;

        const outPath = path.join(OUTPUT_DIR, `${roll}_sem2.html`);
        fs.writeFileSync(outPath, cleanHtml, 'utf-8');
        success++;
      } else {
        // Save full page as fallback
        const fullHtml = await page.content();
        const outPath = path.join(OUTPUT_DIR, `${roll}_sem2_full.html`);
        fs.writeFileSync(outPath, fullHtml, 'utf-8');
        success++;
      }

      // Go back for next student
      await page.goto('https://www.kuuniv.in/result/login', { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(800);

    } catch (err) {
      errors++;
      // Try to recover
      try {
        await page.goto('https://www.kuuniv.in/result/login', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1000);
      } catch(e) {
        // If recovery fails, restart browser entirely
        try { await browser.close(); } catch(x) {}
        browser = await chromium.launch({ headless: true });
        context = await browser.newContext();
        page = await context.newPage();
        await page.goto('https://www.kuuniv.in/result/login', { waitUntil: 'networkidle', timeout: 30000 });
        await page.waitForTimeout(1500);
      }
    }

    printProgress();
  }

  await browser.close();
}

// === Main: split rolls across workers and run in parallel ===
(async () => {
  console.log('='.repeat(70));
  console.log(`DOWNLOADING ${remaining.length} HTML MARKSHEETS | ${NUM_BROWSERS} browsers`);
  console.log('='.repeat(70));
  console.log(`Output: ${OUTPUT_DIR}\n`);

  // Split rolls into chunks for each worker
  const chunkSize = Math.ceil(remaining.length / NUM_BROWSERS);
  const chunks = [];
  for (let i = 0; i < remaining.length; i += chunkSize) {
    chunks.push(remaining.slice(i, i + chunkSize));
  }

  console.log(`Split into ${chunks.length} chunks of ~${chunkSize} rolls each\n`);

  // Launch all workers in parallel
  const workers = chunks.map((chunk, i) => workerFn(i, chunk));
  await Promise.all(workers);

  const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
  console.log(`\n\n${'='.repeat(70)}`);
  console.log(`COMPLETE | OK: ${success} | Errors: ${errors} | Time: ${elapsed} min`);
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log('='.repeat(70));
})();
