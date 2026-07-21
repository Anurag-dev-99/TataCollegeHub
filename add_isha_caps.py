import sys

# 1. Update index.astro
file1 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file1, "r", encoding="utf-8") as f:
    c1 = f.read()

# Update preview badge
c1 = c1.replace(
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #ec4899, #be185d); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">I</span>\n          Isha &amp; 15 others',
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #06b6d4, #0e7490); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">I</span>\n          ISHA &amp; 16 others'
)

isha1_start = c1.find('<!-- Isha -->')

if isha1_start != -1:
    new_isha_row = """<!-- ISHA KUMARI (Eco) -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <div style="width: 24px; height: 24px; border-radius: 50%; background: linear-gradient(135deg, #06b6d4, #0e7490); display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 800; color: white; flex-shrink: 0;">I</div>
            <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">ISHA KUMARI</span>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); text-align: right;">Economics Minor · Sem 1</span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        """
    c1 = c1[:isha1_start] + new_isha_row + c1[isha1_start:]

with open(file1, "w", encoding="utf-8") as f:
    f.write(c1)
print("Updated index.astro")


# 2. Update pyqs/index.astro
file2 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\pyqs\\index.astro"
with open(file2, "r", encoding="utf-8") as f:
    c2 = f.read()

old_str = "{[{i:'I',c:'#ec4899,#be185d',n:'Isha Kumari',f:'History MDC, Chem Minor Sem 1'}"
new_str = "{[{i:'I',c:'#06b6d4,#0e7490',n:'ISHA KUMARI',f:'Economics Minor Sem 1'},{i:'I',c:'#ec4899,#be185d',n:'Isha Kumari',f:'History MDC, Chem Minor Sem 1'}"
c2 = c2.replace(old_str, new_str)

with open(file2, "w", encoding="utf-8") as f:
    f.write(c2)
print("Updated pyqs/index.astro")
