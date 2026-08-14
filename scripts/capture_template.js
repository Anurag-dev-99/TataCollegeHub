/**
 * Download 1 student's marksheet HTML from KU for template analysis.
 * Run from: C:\Users\Anurag\Documents\GitHub\result_main_folder\demo_pdfs\
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROLL = '241305716223';
const SEMESTER = 'II';
const OUTPUT_DIR = path.join(__dirname, 'template_analysis');
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR);

(async () => {
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('Navigating to KU result page...');
  await page.goto('https://www.kuuniv.in/result/login', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(2000);

  console.log(`Entering roll number: ${ROLL}`);

  // Select Course = FYUGP
  await page.locator('select').first().selectOption('FYUGP').catch(() => {});
  await page.waitForTimeout(500);

  // Select Semester
  await page.locator('select').nth(1).selectOption(SEMESTER).catch(() =>
    page.locator('select').nth(1).selectOption({ label: SEMESTER })
  );
  await page.waitForTimeout(500);

  // Select Stream = nep
  await page.locator('select').nth(2).selectOption('nep').catch(async () => {
    await page.locator('select').nth(2).selectOption({ label: 'NEP' }).catch(() => {});
  });
  await page.waitForTimeout(500);

  // Enter roll number
  const rollInput = page.locator('input[type="text"], input[type="number"], input[placeholder*="roll" i], input[ng-model*="roll" i]').first();
  await rollInput.fill(ROLL);
  await page.waitForTimeout(300);

  // Click submit
  console.log('Submitting...');
  const submitBtn = page.locator('button[type="submit"], input[type="submit"], button:has-text("Submit"), button:has-text("Search"), button:has-text("Get Result")').first();
  await submitBtn.click();

  // Wait for result to render
  await page.waitForTimeout(4000);
  await page.waitForSelector('.content-wrapper, .box-body, table', { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(1000);

  // 1. Save the FULL page HTML (complete with all scripts, styles, everything)
  const fullHtml = await page.content();
  const fullPath = path.join(OUTPUT_DIR, `${ROLL}_full_page.html`);
  fs.writeFileSync(fullPath, fullHtml, 'utf-8');
  console.log(`Saved full page HTML: ${fullPath} (${Math.round(fullHtml.length/1024)} KB)`);

  // 2. Save just the marksheet section
  const marksheetData = await page.evaluate(() => {
    const printArea = document.querySelector('.content-wrapper') ||
                     document.querySelector('#printArea') ||
                     document.querySelector('.box-body') ||
                     document.querySelector('.container-fluid');

    if (!printArea) return null;

    // Collect all CSS
    let styles = '';
    const links = [];
    for (const sheet of document.styleSheets) {
      try {
        for (const rule of sheet.cssRules) {
          styles += rule.cssText + '\n';
        }
      } catch(e) {
        if (sheet.href) links.push(sheet.href);
      }
    }

    return {
      content: printArea.outerHTML,
      styles,
      links,
      title: document.title
    };
  });

  if (marksheetData) {
    const linkTags = marksheetData.links.map(l => `<link rel="stylesheet" href="${l}">`).join('\n');
    const cleanHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>${marksheetData.title}</title>
<style>
${marksheetData.styles}
</style>
${linkTags}
</head>
<body>
${marksheetData.content}
</body>
</html>`;

    const cleanPath = path.join(OUTPUT_DIR, `${ROLL}_marksheet.html`);
    fs.writeFileSync(cleanPath, cleanHtml, 'utf-8');
    console.log(`Saved marksheet HTML: ${cleanPath} (${Math.round(cleanHtml.length/1024)} KB)`);
  }

  // 3. Take a screenshot for visual reference
  const screenshotPath = path.join(OUTPUT_DIR, `${ROLL}_screenshot.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`Saved screenshot: ${screenshotPath}`);

  // 4. Also save as PDF for comparison
  const pdfPath = path.join(OUTPUT_DIR, `${ROLL}_direct.pdf`);
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: { top: '5mm', bottom: '5mm', left: '5mm', right: '5mm' }
  });
  console.log(`Saved direct PDF: ${pdfPath} (${Math.round(fs.statSync(pdfPath).size/1024)} KB)`);

  await browser.close();
  console.log('\nDone! Files saved to:', OUTPUT_DIR);
  console.log('\nNext: Analyze the HTML template structure for data injection.');
})();
