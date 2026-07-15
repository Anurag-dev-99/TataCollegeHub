import re

index_path = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\src\pages\index.astro"
pyqs_path = r"C:\Users\Anurag\Documents\GitHub\TataCollegeHub\src\pages\pyqs\index.astro"

with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

with open(pyqs_path, 'r', encoding='utf-8') as f:
    pyqs_content = f.read()

# 1. Update pyqs/index.astro array
new_array_str = "[{e:'📊',t:'Economics Major PYQ',s:'Sem 1'},{e:'⚛️',t:'Physics Minor PYQ',s:'Sem 1'},{e:'🐍',t:'Zoology Minor PYQ',s:'Sem 1'},{e:'📜',t:'MDC History PYQ',s:'Sem 1'},{e:'🌿',t:'Botany Minor PYQ',s:'Sem 1'},{e:'🏛️',t:'Political Science Major PYQ',s:'Sem 1'},{e:'📖',t:'English Major PYQ',s:'Sem 1'},{e:'📜',t:'History Major PYQ',s:'Sem 1'},{e:'📊',t:'Economics Major PYQ',s:'Sem 1'},{e:'⚛️',t:'Physics Major PYQ',s:'Sem 1'},{e:'🏛️',t:'Political Science Minor PYQ',s:'Sem 1'},{e:'🐍',t:'Zoology Major PYQ',s:'Sem 1'},{e:'🐍',t:'Zoology Minor PYQ',s:'Sem 1'},{e:'🌿',t:'Botany Major PYQ',s:'Sem 1'},{e:'🏠',t:'MDC Home Science PYQ',s:'Sem 1 & 3'},{e:'🏛️',t:'Political Science Minor PYQ',s:'Sem 1'},{e:'📐',t:'Maths Minor PYQ',s:'Sem 1'},{e:'🐍',t:'Zoology Minor PYQ',s:'Sem 1'},{e:'🌿',t:'Botany Major PYQ',s:'Sem 1'},{e:'🏠',t:'MDC Home Science PYQ',s:'Sem 1 & 3'},{e:'🧪',t:'Chemistry Minor PYQ',s:'Sem 1'},{e:'📜',t:'History Major PYQ',s:'Sem 1'},{e:'⚛️',t:'Physics Major PYQ',s:'Sem 1 · 2024 Batch'},{e:'📐',t:'Maths Major PYQ',s:'Sem 1 · All Batches'},{e:'⚛️',t:'Physics Major PYQ',s:'Sem 1–6'},{e:'🧪',t:'Chemistry Major PYQ',s:'Sem 1–3'},{e:'📊',t:'Economics Major PYQ',s:'Sem 1'},{e:'📖',t:'English Major PYQ',s:'Sem 1–4'},{e:'🧠',t:'MDC Psychology PYQ',s:'Sem 1–3'},{e:'📊',t:'MDC Statistics PYQ',s:'Sem 1'}]"

pyqs_content = re.sub(r'\{\[\{.*?\}\]\.map\(r => \(', f'{{{new_array_str}.map(r => (', pyqs_content)
pyqs_content = re.sub(r'<span[^>]*?>\d+</span>(\s*</div>\s*<ChevronRight id="pyq-req-chevron")', r'<span style="font-size: 0.6rem; font-weight: 700; background: rgba(16,185,129,0.12); color: var(--accent-success); border: 1px solid rgba(16,185,129,0.25); border-radius: 20px; padding: 1px 5px;">30</span>\1', pyqs_content)

with open(pyqs_path, 'w', encoding='utf-8') as f:
    f.write(pyqs_content)


# 2. Update index.astro HTML list
new_requests = [
    ("📊", "Economics Major PYQ", "Sem 1", "15 Jul", "15 Jul"),
    ("⚛️", "Physics Minor PYQ", "Sem 1", "15 Jul", "15 Jul"),
    ("🐍", "Zoology Minor PYQ", "Sem 1", "15 Jul", "15 Jul"),
    ("📜", "MDC History PYQ", "Sem 1", "15 Jul", "15 Jul"),
    ("🌿", "Botany Minor PYQ", "Sem 1", "15 Jul", "15 Jul"),
    ("🏛️", "Political Science Major PYQ", "Sem 1", "15 Jul", "15 Jul"),
    ("📖", "English Major PYQ", "Sem 1", "14 Jul", "15 Jul"),
    ("📜", "History Major PYQ", "Sem 1", "13 Jul", "15 Jul"),
    ("📊", "Economics Major PYQ", "Sem 1", "13 Jul", "15 Jul"),
    ("⚛️", "Physics Major PYQ", "Sem 1", "13 Jul", "15 Jul"),
    ("🏛️", "Political Science Minor PYQ", "Sem 1", "13 Jul", "15 Jul"),
    ("🐍", "Zoology Major PYQ", "Sem 1", "11 Jul", "15 Jul"),
    ("🐍", "Zoology Minor PYQ", "Sem 1", "11 Jul", "15 Jul"),
    ("🌿", "Botany Major PYQ", "Sem 1", "11 Jul", "15 Jul"),
    ("🏠", "MDC Home Science PYQ", "Sem 1 & 3", "10 Jul", "15 Jul")
]

html_blocks = []
for emoji, title, sem, req_date, up_date in new_requests:
    block = f"""        <!-- {title} -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <span style="font-size: 0.75rem; flex-shrink: 0;">{emoji}</span>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">{title}</span>
              <span style="font-size: 0.72rem; color: var(--text-tertiary); margin-left: 0.4rem;">{sem}</span>
            </div>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; text-align: right;">{req_date} &rarr; <strong style="color: var(--accent-success);">{up_date}</strong></span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>
"""
    html_blocks.append(block)

html_blocks_str = "\n".join(html_blocks)

index_content = re.sub(r'<span[^>]*?>\d+ Tasks Resolved</span>', r'<span style="font-size: 0.65rem; font-weight: 700; background: rgba(16, 185, 129, 0.12); color: var(--accent-success); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 20px; padding: 1px 7px; letter-spacing: 0.3px;">33 Tasks Resolved</span>', index_content)

header_marker = r"""        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; padding: 0.4rem 0.6rem; margin-bottom: 0.25rem;">
          <span style="font-size: 0.65rem; font-weight: 700; color: var(--text-tertiary); letter-spacing: 0.07em; text-transform: uppercase;">What was requested</span>
          <span style="font-size: 0.65rem; font-weight: 700; color: var(--text-tertiary); letter-spacing: 0.07em; text-transform: uppercase; text-align: right;">Requested → Uploaded</span>
        </div>"""

if header_marker in index_content:
    index_content = index_content.replace(header_marker, header_marker + "\n\n" + html_blocks_str)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

print("Updated index.astro and pyqs/index.astro")
