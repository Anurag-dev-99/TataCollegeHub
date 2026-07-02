/**
 * Google Sheets Apps Script — Tata College Hub
 *
 * Handles 3 actions:
 *   1. POST { type: "request",  ... }  → appends to "Requests" sheet tab
 *   2. POST { type: "download", ... }  → appends to "Downloads" sheet tab
 *   3. GET  ?action=stats              → returns JSON with live download totals
 *
 * Downloads sheet columns (Row 1 = headers you already created):
 *   A: Timestamp  B: Type  C: Subject  D: Category  E: Semester  F: Department
 */

// ─── POST Handler ─────────────────────────────────────────────────────────────
function doPost(e) {
  try {
    var ss   = SpreadsheetApp.getActiveSpreadsheet();
    var data = JSON.parse(e.postData.contents);

    if (data.type === 'download') {
      // ── Log a download event ──────────────────────────────────────────────
      var dlSheet = ss.getSheetByName('Downloads');
      if (!dlSheet) dlSheet = ss.insertSheet('Downloads');

      dlSheet.appendRow([
        new Date(),                         // A: Timestamp
        data.fileType    || 'pyq',          // B: Type ("pyq" or "syllabus")
        data.subject     || 'Unknown',      // C: Subject
        data.category    || 'Unknown',      // D: Category
        data.semester    || 'Unknown',      // E: Semester
        data.department  || ''              // F: Department (syllabus only)
      ]);

    } else {
      // ── Log a paper request ───────────────────────────────────────────────
      var reqSheet = ss.getSheetByName('Requests');
      if (!reqSheet) reqSheet = ss.getActiveSheet();

      reqSheet.appendRow([
        new Date(),
        data.name,
        (data.type === 'syllabus' ? 'Syllabus'
          : data.type === 'both'  ? 'PYQ + Syllabus'
          : 'PYQ Paper'),
        'Semester ' + data.semester,
        data.category,
        data.subject,
        data.year,
        data.session,
        data.contact || 'Not provided'
      ]);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ─── GET Handler — returns live download stats ────────────────────────────────
function doGet(e) {
  try {
    var ss      = SpreadsheetApp.getActiveSpreadsheet();
    var dlSheet = ss.getSheetByName('Downloads');

    var pyqCount      = 0;
    var syllabusCount = 0;

    if (dlSheet && dlSheet.getLastRow() > 1) {
      // Column B (col index 2) = Type; skip row 1 (header)
      var typeValues = dlSheet.getRange(2, 2, dlSheet.getLastRow() - 1, 1).getValues();
      typeValues.forEach(function(row) {
        var t = (row[0] || '').toString().toLowerCase().trim();
        if (t === 'syllabus') { syllabusCount++; }
        else                  { pyqCount++;       }
      });
    }

    return ContentService
      .createTextOutput(JSON.stringify({
        status:           'ok',
        pyqDownloads:     pyqCount,
        syllabusDownloads: syllabusCount,
        total:            pyqCount + syllabusCount,
        updatedAt:        new Date().toISOString()
      }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
