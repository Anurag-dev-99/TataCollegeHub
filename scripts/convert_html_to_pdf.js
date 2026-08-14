/**
 * FAST PDF CONVERTER — Converts local HTML files to PDF
 * Uses a single browser instance with page.setContent() (no navigation)
 * Much faster than navigating to URLs: ~1-2 sec per PDF instead of 5 sec
 * 
 * Usage: node convert_html_to_pdf.js [BATCH_SIZE]
 *   BATCH_SIZE: Number of pages per browser context (default: all)
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const HTML_DIR = path.join(__dirname, '..', '2023', 'sem2', 'marksheet_html');
const PDF_DIR = path.join(__dirname, '..', '2023', 'sem2', 'marksheet_pdf');
if (!fs.existsSync(PDF_DIR)) fs.mkdirSync(PDF_DIR, { recursive: true });

// Get all HTML files, skip already-converted ones
const allHtml = fs.readdirSync(HTML_DIR).filter(f => f.endsWith('.html'));
const existingPdfs = new Set(
  fs.readdirSync(PDF_DIR).filter(f => f.endsWith('.pdf')).map(f => f.replace('.pdf', '.html'))
);
const remaining = allHtml.filter(f => !existingPdfs.has(f));

console.log(`Total HTML files: ${allHtml.length}`);
console.log(`Already converted: ${existingPdfs.size}`);
console.log(`Remaining: ${remaining.length}`);

if (remaining.length === 0) {
  console.log('All done!');
  process.exit(0);
}

let success = 0;
let errors = 0;
const startTime = Date.now();

function printProgress() {
  const elapsed = (Date.now() - startTime) / 1000;
  const total = success + errors;
  const rate = total > 0 ? total / elapsed : 0;
  const eta = rate > 0 ? ((remaining.length - total) / rate / 60).toFixed(1) : '?';
  process.stdout.write(
    `\r  [${total}/${remaining.length}] OK:${success} Err:${errors} | ` +
    `${rate.toFixed(1)}/s | ETA: ${eta} min   `
  );
}

(async () => {
  console.log(`\nLaunching browser...`);
  const browser = await chromium.launch({ headless: true });

  // Use setContent instead of goto — much faster, no network needed
  for (let i = 0; i < remaining.length; i++) {
    const file = remaining[i];
    try {
      const page = await browser.newPage();
      const htmlContent = fs.readFileSync(path.join(HTML_DIR, file), 'utf-8');
      
      // Set the base URL so CSS links resolve to KU's server
      await page.setContent(htmlContent, { 
        waitUntil: 'networkidle',
        timeout: 15000 
      });
      
      // Wait for external resources (logo, QR code, signature, CSS)
      await page.waitForTimeout(1500);
      
      const pdfName = file.replace('.html', '.pdf');
      await page.pdf({
        path: path.join(PDF_DIR, pdfName),
        format: 'A4',
        printBackground: true,
        margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
      });
      
      success++;
      await page.close();
    } catch (err) {
      errors++;
    }
    
    if ((i + 1) % 10 === 0) printProgress();
  }

  printProgress();
  const elapsed = ((Date.now() - startTime) / 1000 / 60).toFixed(1);
  console.log(`\n\nDone! ${success} PDFs | ${errors} errors | ${elapsed} min`);
  console.log(`Output: ${PDF_DIR}`);
  
  // Show size
  const pdfFiles = fs.readdirSync(PDF_DIR).filter(f => f.endsWith('.pdf'));
  const totalSize = pdfFiles.reduce((sum, f) => sum + fs.statSync(path.join(PDF_DIR, f)).size, 0);
  console.log(`Total: ${pdfFiles.length} PDFs | ${(totalSize / 1024 / 1024).toFixed(0)} MB`);
  
  await browser.close();
})();
