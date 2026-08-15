/**
 * FAST EMBEDDED PDF CONVERTER
 * Converts self-contained HTML files to PDF (no internet needed).
 * Skips already-converted files for resume support.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const HTML_DIR = 'C:\\Users\\Anurag\\Documents\\GitHub\\result_main_folder\\2023\\sem2\\marksheet_html';
const PDF_DIR = 'C:\\Users\\Anurag\\Documents\\GitHub\\result_main_folder\\2023\\sem2\\marksheet_pdf';
if (!fs.existsSync(PDF_DIR)) fs.mkdirSync(PDF_DIR, { recursive: true });

const allHtml = fs.readdirSync(HTML_DIR).filter(f => f.endsWith('.html'));
const existing = new Set(
  fs.readdirSync(PDF_DIR).filter(f => f.endsWith('.pdf')).map(f => f.replace('.pdf', '.html'))
);
const remaining = allHtml.filter(f => !existing.has(f));

console.log(`Total: ${allHtml.length} | Done: ${existing.size} | Remaining: ${remaining.length}`);
if (!remaining.length) { console.log('All done!'); process.exit(0); }

let ok = 0, err = 0;
const t0 = Date.now();

(async () => {
  const browser = await chromium.launch({ headless: true });
  console.log('Browser launched. Converting...\n');

  for (let i = 0; i < remaining.length; i++) {
    try {
      const page = await browser.newPage();
      const html = fs.readFileSync(path.join(HTML_DIR, remaining[i]), 'utf-8');
      await page.setContent(html, { waitUntil: 'load', timeout: 10000 });
      await page.waitForTimeout(200);
      await page.pdf({
        path: path.join(PDF_DIR, remaining[i].replace('.html', '.pdf')),
        format: 'A4', printBackground: true,
        margin: { top: '10mm', bottom: '10mm', left: '10mm', right: '10mm' }
      });
      ok++;
      await page.close();
    } catch (e) { err++; }

    if ((i + 1) % 50 === 0) {
      const elapsed = (Date.now() - t0) / 1000;
      const rate = (ok + err) / elapsed;
      const eta = ((remaining.length - ok - err) / rate / 60).toFixed(1);
      process.stdout.write(`\r  [${ok+err}/${remaining.length}] OK:${ok} Err:${err} | ${rate.toFixed(1)}/s | ETA: ${eta} min`);
    }
  }

  const mins = ((Date.now() - t0) / 60000).toFixed(1);
  console.log(`\n\nDone! ${ok} PDFs, ${err} errors, ${mins} min`);

  const pdfs = fs.readdirSync(PDF_DIR).filter(f => f.endsWith('.pdf'));
  const sz = pdfs.reduce((s, f) => s + fs.statSync(path.join(PDF_DIR, f)).size, 0);
  console.log(`Total: ${pdfs.length} PDFs | ${(sz/1024/1024).toFixed(0)} MB`);
  console.log(`Location: ${PDF_DIR}`);

  await browser.close();
})();
