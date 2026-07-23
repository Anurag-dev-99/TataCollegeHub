import sys

# 1. Update pyqs.json
file_json = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\public\\data\\pyqs.json"
with open(file_json, "r", encoding="utf-8") as f:
    c_json = f.read()

new_json_entries = """    },
    {
        "id": "pyq-mdc-psych-sem1-2025",
        "category": "MDC",
        "semester": 1,
        "subject": "Psychology",
        "title": "Psychology MDC Sem 1 PYQ 2025 Batch",
        "year": "2024-2028",
        "downloadUrl": "https://drive.google.com/file/d/1c2NO_NoKAMP6SBDpzNhabs2Yu_iE5rV-/view?usp=drive_link",
        "fileSize": "PDF File",
        "downloadCount": 0
    }
]"""

c_json = c_json.replace("    }\n]", new_json_entries).replace("    }\r\n]", new_json_entries)

with open(file_json, "w", encoding="utf-8") as f:
    f.write(c_json)
print("Updated pyqs.json")

# 2. Update pyqs/index.astro
file_pyqs = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\pyqs\\index.astro"
with open(file_pyqs, "r", encoding="utf-8") as f:
    c_pyqs = f.read()

c_pyqs = c_pyqs.replace('padding: 1px 5px;">44<', 'padding: 1px 5px;">45<')
old_end = "s:'Sem 1 (2025)'}].map"
new_end = "s:'Sem 1 (2025)'},{e:'🧠',t:'MDC Psychology PYQ',s:'Sem 1 (2025)'}].map"
c_pyqs = c_pyqs.replace(old_end, new_end)

with open(file_pyqs, "w", encoding="utf-8") as f:
    f.write(c_pyqs)
print("Updated pyqs/index.astro")

# 3. Update index.astro
file_idx = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file_idx, "r", encoding="utf-8") as f:
    c_idx = f.read()

c_idx = c_idx.replace("47 Tasks Resolved", "48 Tasks Resolved")

insertion = "<!-- Digital India SEC PYQ -->"
new_rows = """<!-- Psychology MDC PYQ 2025 -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <span style="font-size: 0.75rem; flex-shrink: 0;">🧠</span>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Psychology MDC PYQ (2025)</span>
              <span style="font-size: 0.72rem; color: var(--text-tertiary); margin-left: 0.4rem;">Sem 1</span>
            </div>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; text-align: right;">23 Jul &rarr; <strong style="color: var(--accent-success);">23 Jul</strong></span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        """
c_idx = c_idx.replace(insertion, new_rows + insertion)

with open(file_idx, "w", encoding="utf-8") as f:
    f.write(c_idx)
print("Updated index.astro")
