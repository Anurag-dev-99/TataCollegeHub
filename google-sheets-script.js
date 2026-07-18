/**
 * Google Sheets Apps Script — Tata College Hub
 *
 * Handles 5 actions:
 *   1. POST { type: "request",  ... }  → appends to "Requests" sheet tab
 *   2. POST { type: "download", ... }  → appends to "Downloads" sheet tab
 *   3. POST { type: "download", fileType: "note", ... } → appends to "Notes" sheet tab
 *   4. GET  ?action=stats              → returns JSON with live download totals
 *   5. GET  ?action=top                → returns top 5 most-downloaded papers
 *   6. GET  ?action=papercounts        → returns per-paper download counts
 *
 * Downloads sheet columns (Row 1 = headers):
 *   A: Timestamp  B: Type  C: Subject  D: Category  E: Semester  F: Department
 *
 * Notes sheet columns (Row 1 = headers):
 *   A: Timestamp  B: Subject  C: Language  D: Category  E: Medium
 */

// ─── POST Handler ─────────────────────────────────────────────────────────────
function doPost(e) {
  try {
    var ss   = SpreadsheetApp.getActiveSpreadsheet();
    var data = JSON.parse(e.postData.contents);

    if (data.type === 'download') {

      if (data.fileType === 'note') {
        // ── Log a note open/download ───────────────────────────────────────
        var notesSheet = ss.getSheetByName('Notes');
        if (!notesSheet) {
          notesSheet = ss.insertSheet('Notes');
          notesSheet.appendRow(['Timestamp', 'Subject', 'Language', 'Category', 'Medium']);
        }

        notesSheet.appendRow([
          new Date(),                         // A: Timestamp
          data.subject  || 'Unknown',         // B: Subject (e.g. "Psychology")
          data.language || 'Unknown',         // C: Language (e.g. "Hindi")
          data.category || 'MDC',             // D: Category
          data.medium   || ''                 // E: Medium code (e.g. "HI" / "EN")
        ]);

      } else {
        // ── Log a PYQ / Syllabus download ────────────────────────────────────
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
      }

    } else if (data.type === 'report') {
      // ── Log a wrong paper / broken link report ─────────────────────────────
      var repSheet = ss.getSheetByName('Reports');
      if (!repSheet) {
        repSheet = ss.insertSheet('Reports');
        repSheet.appendRow(['Timestamp', 'Page URL', 'Issue Details']);
      }

      repSheet.appendRow([
        new Date(),
        data.url || 'Unknown page',
        data.message || ''
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

// ─── GET Handler ──────────────────────────────────────────────────────────────
function doGet(e) {
  try {
    var action  = (e.parameter.action || 'stats').toLowerCase();
    var ss      = SpreadsheetApp.getActiveSpreadsheet();
    var dlSheet = ss.getSheetByName('Downloads');

    // ── action=stats: total pyq vs syllabus counts ────────────────────────
    if (action === 'stats') {
      var pyqCount      = 0;
      var syllabusCount = 0;

      if (dlSheet && dlSheet.getLastRow() > 1) {
        var typeValues = dlSheet.getRange(2, 2, dlSheet.getLastRow() - 1, 1).getValues();
        typeValues.forEach(function(row) {
          var t = (row[0] || '').toString().toLowerCase().trim();
          if (t === 'syllabus') { syllabusCount++; }
          else                  { pyqCount++;       }
        });
      }

      return ContentService
        .createTextOutput(JSON.stringify({
          status:            'ok',
          pyqDownloads:      pyqCount,
          syllabusDownloads: syllabusCount,
          total:             pyqCount + syllabusCount,
          updatedAt:         new Date().toISOString()
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // ── action=top: top 5 most-downloaded papers ──────────────────────────
    if (action === 'top') {
      var counts = {};  // key = "subject||category||semester||fileType"

      if (dlSheet && dlSheet.getLastRow() > 1) {
        var rows = dlSheet.getRange(2, 1, dlSheet.getLastRow() - 1, 6).getValues();
        rows.forEach(function(row) {
          var fileType = (row[1] || 'pyq').toString().toLowerCase().trim();
          var subject  = (row[2] || 'Unknown').toString().trim();
          var category = (row[3] || 'Unknown').toString().trim();
          var semester = (row[4] || '').toString().trim();
          var key = subject + '||' + category + '||' + semester + '||' + fileType;
          counts[key] = (counts[key] || 0) + 1;
        });
      }

      // Sort descending by count, take top 5
      var top = Object.keys(counts)
        .map(function(k) {
          var parts = k.split('||');
          return { subject: parts[0], category: parts[1], semester: parts[2], fileType: parts[3], count: counts[k] };
        })
        .sort(function(a, b) { return b.count - a.count; })
        .slice(0, 5);

      return ContentService
        .createTextOutput(JSON.stringify({ status: 'ok', top: top, updatedAt: new Date().toISOString() }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // ── action=papercounts: counts for all papers ────────────────────────
    if (action === 'papercounts') {
      var counts = {};
      if (dlSheet && dlSheet.getLastRow() > 1) {
        var rows = dlSheet.getRange(2, 3, dlSheet.getLastRow() - 1, 1).getValues(); // Column C = Subject
        rows.forEach(function(row) {
          var subject = (row[0] || '').toString().trim();
          if (subject) {
            counts[subject] = (counts[subject] || 0) + 1;
          }
        });
      }
      return ContentService
        .createTextOutput(JSON.stringify({ status: 'ok', counts: counts }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: 'Unknown action' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
