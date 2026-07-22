import sys

# 1. Update index.astro
file1 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file1, "r", encoding="utf-8") as f:
    c1 = f.read()

# Update preview badge
c1 = c1.replace(
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #06b6d4, #0e7490); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">I</span>\n          ISHA &amp; 16 others',
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #d97706); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">A</span>\n          Ayushi &amp; 16 others'
)

# Find Ayushi block and remove it from current position
ayushi_start = c1.find('<!-- Ayushi -->')
gouranga_start = c1.find('<!-- Gouranga (GG) -->')

if ayushi_start != -1 and gouranga_start != -1:
    ayushi_block = c1[ayushi_start:gouranga_start]
    # Remove old ayushi block from current spot
    c1 = c1[:ayushi_start] + c1[gouranga_start:]

# Update Ayushi block text
new_ayushi_block = """<!-- Ayushi -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <div style="width: 24px; height: 24px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #d97706); display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 800; color: white; flex-shrink: 0;">A</div>
            <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Ayushi Kumari</span>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); text-align: right;">Geo Major, PolSci Minor, Phil MDC, Digital Edu · Sem 1</span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        """

# Insert new Ayushi block at the very top (before ISHA KUMARI)
top_contributor_start = c1.find('<!-- ISHA KUMARI (Eco) -->')
if top_contributor_start != -1:
    c1 = c1[:top_contributor_start] + new_ayushi_block + c1[top_contributor_start:]

with open(file1, "w", encoding="utf-8") as f:
    f.write(c1)
print("Updated index.astro")


# 2. Update pyqs/index.astro
file2 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\pyqs\\index.astro"
with open(file2, "r", encoding="utf-8") as f:
    c2 = f.read()

# Remove old Ayushi item from array
c2 = c2.replace(",{i:'A',c:'#f59e0b,#d97706',n:'Ayushi Kumari',f:'Geo Major, PolSci Minor Sem 1'}", "")

# Prepend Ayushi to beginning of array
old_array_start = "{[{i:'I',c:'#06b6d4,#0e7490',n:'ISHA KUMARI',f:'Economics Minor Sem 1'}"
new_array_start = "{[{i:'A',c:'#f59e0b,#d97706',n:'Ayushi Kumari',f:'Geo Major, PolSci Minor, Phil MDC, Digital Edu Sem 1'},{i:'I',c:'#06b6d4,#0e7490',n:'ISHA KUMARI',f:'Economics Minor Sem 1'}"
c2 = c2.replace(old_array_start, new_array_start)

with open(file2, "w", encoding="utf-8") as f:
    f.write(c2)
print("Updated pyqs/index.astro")
