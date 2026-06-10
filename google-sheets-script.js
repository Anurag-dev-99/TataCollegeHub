/**
 * Google Sheets Apps Script Webhook for Tata College Student Hub Requests
 * 
 * INSTRUCTIONS FOR DEPLOYMENT:
 * ----------------------------
 * 1. Create a new Google Sheet in Google Drive.
 * 2. Add headers in the first row (Row 1):
 *    Column A: Timestamp
 *    Column B: Name
 *    Column C: Semester
 *    Column D: Category
 *    Column E: Subject
 *    Column F: Exam Year
 *    Column G: Session/Batch
 *    Column H: Contact Number (WhatsApp)
 * 3. Go to Extensions > Apps Script.
 * 4. Delete any default code in Code.gs and paste this script content.
 * 5. Click "Deploy" > "New Deployment".
 * 6. Select type "Web app".
 * 7. Configure:
 *    - Execute as: Me (your-email@gmail.com)
 *    - Who has access: Anyone (This is critical to let the website send requests anonymously)
 * 8. Click "Deploy". Authorize the script when prompted.
 * 9. Copy the generated Web App URL.
 * 10. Paste this URL into your `src/layouts/Layout.astro` file inside the `webhookUrl` variable (around line 500).
 */

function doPost(e) {
  try {
    // Open active sheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Parse incoming JSON data
    var data = JSON.parse(e.postData.contents);
    
    // Append a new row with details
    sheet.appendRow([
      new Date(),                         // Timestamp
      data.name,                          // Name
      "Semester " + data.semester,        // Semester
      data.category,                      // Category
      data.subject,                       // Subject Name
      data.year,                          // Exam Year
      data.session,                       // Session/Batch
      data.contact || "Not provided"      // Contact (WhatsApp)
    ]);
    
    // Return success response to bypass CORS restrictions
    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    // Return error message if parser or append fails
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
