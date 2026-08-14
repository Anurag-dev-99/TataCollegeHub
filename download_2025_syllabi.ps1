
# Download all 2025 batch syllabus PDFs from kolhanuniversity.ac.in
# Saves to: ./downloaded_syllabi_2025/

$baseDir = "downloaded_syllabi_2025"

# Create directories
$categories = @("Major", "MDC", "AEC", "VAC", "SEC", "Other")
foreach ($cat in $categories) {
    New-Item -ItemType Directory -Force -Path "$baseDir/$cat" | Out-Null
}

Write-Host "=== Downloading 2025 Batch Syllabus PDFs ===" -ForegroundColor Cyan
Write-Host "Source: kolhanuniversity.ac.in/undergraduate-syllabus" -ForegroundColor Gray
Write-Host ""

$downloads = @(
    # === MAJOR SUBJECTS ===
    @{ Name = "Botany.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767179115_Botany.pdf"; Cat = "Major" },
    @{ Name = "Hindi.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767179206_Hindi.pdf"; Cat = "Major" },
    @{ Name = "BSc_IT.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767179305_IT.pdf"; Cat = "Major" },
    @{ Name = "Mathematics.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767180285_Mathematics_compressed.pdf"; Cat = "Major" },
    @{ Name = "Physics_New.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767180564_Physics_New.pdf"; Cat = "Major" },
    @{ Name = "Physics.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767180666_Physics.pdf"; Cat = "Major" },
    @{ Name = "Zoology.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767180981_Zoology.pdf"; Cat = "Major" },
    @{ Name = "BBA.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767184841_BBA.pdf"; Cat = "Major" },
    @{ Name = "Statistics.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767184986_Statistics.pdf"; Cat = "Major" },
    @{ Name = "Santhali.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767185061_Santhali.pdf"; Cat = "Major" },
    @{ Name = "Bangla.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767335679_Bangla_compressed.pdf"; Cat = "Major" },
    @{ Name = "Chemistry.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767336321_Chemistry_compressed.pdf"; Cat = "Major" },
    @{ Name = "Commerce.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767336502_Commerce_compressed.pdf"; Cat = "Major" },
    @{ Name = "Economics.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767336619_Economics_compressed.pdf"; Cat = "Major" },
    @{ Name = "English.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767337085_English_compressed.pdf"; Cat = "Major" },
    @{ Name = "Ho.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767337973_Ho_compressed.pdf"; Cat = "Major" },
    @{ Name = "Odia.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767338843_Odia_compressed.pdf"; Cat = "Major" },
    @{ Name = "Philosophy_Major.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767339059_Philosophy_Major_compressed.pdf"; Cat = "Major" },
    @{ Name = "Philosophy_Minor.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767339141_Philosophy_Minor_compressed.pdf"; Cat = "Major" },
    @{ Name = "Psychology.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767339331_Psychology_compressed.pdf"; Cat = "Major" },
    @{ Name = "Sanskrit.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767339899_Sanskrit_compressed.pdf"; Cat = "Major" },
    @{ Name = "Kudmali.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852238_Kudmali_compressed.pdf"; Cat = "Major" },
    @{ Name = "Kudmali_MJ1.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852123_Kudmali_MJ%201_compressed.pdf"; Cat = "Major" },
    @{ Name = "Kudmali_MN1A.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852179_Kudmali_MN-1A_compressed.pdf"; Cat = "Major" },
    @{ Name = "Kudmali_MJ2_MJ3.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852840_Kudmali_MJ-2%20%26%20MJ-3_compressed.pdf"; Cat = "Major" },
    @{ Name = "Kudmali_MN2A.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852923_Kudmali_MN-2A_compressed.pdf"; Cat = "Major" },
    @{ Name = "Geology_2025.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1768908529_2025_Onwards_FYUGP_UG%20Geology%20Syllabus_Kolhan%20University_compressed.pdf"; Cat = "Major" },
    @{ Name = "Geology_2022.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1768908562_2022_Onwards_FYUGP_UG%20Geology%20Syllabus_Kolhan%20University_compressed.pdf"; Cat = "Major" },
    @{ Name = "Home_Science.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1773639004_1370d5209eecbb73_NewUGSyllabus2024.pdf"; Cat = "Major" },
    @{ Name = "BCA.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767178918_BCA.pdf"; Cat = "Major" },
    @{ Name = "Mass_Comm_Video.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767179456_Mass%20Communication-%20Video%20Production.pdf"; Cat = "Major" },

    # === MDC SUBJECTS ===
    @{ Name = "BCA_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767178819_BCA_MDC.pdf"; Cat = "MDC" },
    @{ Name = "IT_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767179377_IT_MDC.pdf"; Cat = "MDC" },
    @{ Name = "Mathematics_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767179577_Mathematics_MDC.pdf"; Cat = "MDC" },
    @{ Name = "Mathematics_MDC_II.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767179684_Mathematics-MDC.pdf"; Cat = "MDC" },
    @{ Name = "Botany_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767180380_MDC_Botany.pdf"; Cat = "MDC" },
    @{ Name = "Philosophy_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767180473_Philosophy_MDC.pdf"; Cat = "MDC" },
    @{ Name = "Zoology_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767184923_Zoology_MDC.pdf"; Cat = "MDC" },
    @{ Name = "Santhali_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767185125_Santhali_MDC.pdf"; Cat = "MDC" },
    @{ Name = "Hindi_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767815364_Hindi_MDC.pdf"; Cat = "MDC" },
    @{ Name = "Anthropology_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767847691_Anthropology_MDC%20%282%29_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Bangla_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767847858_Bangla_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "BBA_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767335921_BBA_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Business_Admin_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848006_Business%20Administration_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Chemistry_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848108_Chemistry_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Commerce_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848260_Commerce_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Computer_App_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848324_Computer%20Application_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Economics_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848392_Economics_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "English_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848484_English_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "EnvScience_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848556_Environmental%20Science%20_%20Water%20Management_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Geography_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848621_Geography_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "History_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848882_History_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Ho_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767848975_Ho_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Home_Science_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849146_Home%20Science_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Info_Tech_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849311_Information%20Technology_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Kudmali_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849385_Kudmali_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Mass_Comm_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849436_Mass%20Communication_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Odia_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849512_Odia_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Physics_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849668_Physics_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "PolSci_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849750_Political%20Science_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Psychology_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849810_Psychology_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "PubAdmin_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849909_Public%20Administration_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Sanskrit_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767849971_Sanskrit_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Sociology_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767850030_Sociology_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Statistics_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767850100_Statistics_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Urdu_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767850191_Urdu_MDC_compressed.pdf"; Cat = "MDC" },
    @{ Name = "Geology_MDC.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767886303_MDC_Geology_2025-2029_compressed.pdf"; Cat = "MDC" },

    # === AEC SUBJECTS ===
    @{ Name = "Hindi_AEC1_Sem1.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767815175_Hindi_AEC-1.pdf"; Cat = "AEC" },
    @{ Name = "Santhali_AEC3.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767185228_Santhali_AEC-3.pdf"; Cat = "AEC" },
    @{ Name = "English_AEC2_Sem2.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767853279_AEC-2_English_compressed.pdf"; Cat = "AEC" },
    @{ Name = "English_AEC3_Sem3.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767853317_AEC-3_English_Sem-III_compressed.pdf"; Cat = "AEC" },
    @{ Name = "English_AEC4_Sem4.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767853368_AEC-4_English_Sem-IV_compressed.pdf"; Cat = "AEC" },
    @{ Name = "Hindi_AEC4_Sem4.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767853432_AEC-4_Hindi_Sem-IV_compressed.pdf"; Cat = "AEC" },

    # === VAC SUBJECTS ===
    @{ Name = "VAC1_EnvStudies_Sem1.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852376_VAC-1_Environmental%20Studies_compressed.pdf"; Cat = "VAC" },
    @{ Name = "VAC1_Health_Wellness_Sem1.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852456_VAC-1_Health%20_%20Wellness_compressed.pdf"; Cat = "VAC" },
    @{ Name = "VAC1_Understanding_India_Sem1.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852554_VAC-1_Understanding%20India_compressed.pdf"; Cat = "VAC" },
    @{ Name = "VAC1_Yoga_Sem1.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767852616_VAC-1_Yoga_compressed.pdf"; Cat = "VAC" },
    @{ Name = "VAC2_Global_Citizenship_Sem4.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767853034_VAC-2_Global%20Citizenship%20Education%20for%20Sustainable%20Development_Sem-IV_compressed.pdf"; Cat = "VAC" },

    # === SEC SUBJECTS ===
    @{ Name = "SEC3_Math_Computational.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767338362_Mathematical%20%26%20Computational%20Thinking%20and%20Analysis_SEC-3_compressed.pdf"; Cat = "SEC" },

    # === OTHER ===
    @{ Name = "Env_Water_Management.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767337292_Environment%20%26%20Water%20Mangement_compressed.pdf"; Cat = "Other" },
    @{ Name = "EnvSci_Water_Management.pdf"; Url = "https://www.kolhanuniversity.ac.in/storage/curriculum-pdfs/1767337628_Environmental%20Science%20%26%20Water%20Mangement_compressed.pdf"; Cat = "Other" }
)

$success = 0
$failed = 0
$total = $downloads.Count

foreach ($dl in $downloads) {
    $outPath = "$baseDir/$($dl.Cat)/$($dl.Name)"
    Write-Host "[$($success + $failed + 1)/$total] Downloading $($dl.Name)..." -NoNewline
    try {
        Invoke-WebRequest -Uri $dl.Url -OutFile $outPath -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop
        $fileSize = (Get-Item $outPath).Length / 1KB
        Write-Host " OK ($([math]::Round($fileSize))KB)" -ForegroundColor Green
        $success++
    } catch {
        Write-Host " FAILED: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

Write-Host ""
Write-Host "=== Download Complete ===" -ForegroundColor Cyan
Write-Host "Success: $success / $total" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "Failed: $failed / $total" -ForegroundColor Red
}

# Show folder sizes
Write-Host ""
Write-Host "=== Folder Summary ===" -ForegroundColor Cyan
foreach ($cat in $categories) {
    $catPath = "$baseDir/$cat"
    $files = Get-ChildItem -Path $catPath -File -ErrorAction SilentlyContinue
    if ($files) {
        $totalSize = ($files | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "  $cat : $($files.Count) files, $([math]::Round($totalSize, 1))MB" -ForegroundColor White
    }
}
