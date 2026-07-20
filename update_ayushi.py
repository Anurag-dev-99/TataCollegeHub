import sys

# 1. Update index.astro
file1 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file1, "r", encoding="utf-8") as f:
    c1 = f.read()

# Update preview
c1 = c1.replace(
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #ec4899, #be185d); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">I</span>\n          Isha &amp; 12 others',
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #d97706); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">A</span>\n          Ayushi &amp; 13 others'
)

insertion = "<!-- Isha -->"
new_row = """<!-- Ayushi -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <div style="width: 24px; height: 24px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #d97706); display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 800; color: white; flex-shrink: 0;">A</div>
            <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Ayushi Kumari</span>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); text-align: right;">Geo Major, PolSci Minor · Sem 1</span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        """
c1 = c1.replace(insertion, new_row + insertion)

with open(file1, "w", encoding="utf-8") as f:
    f.write(c1)
print("Updated index.astro")


# 2. Update pyqs/index.astro
file2 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\pyqs\\index.astro"
with open(file2, "r", encoding="utf-8") as f:
    c2 = f.read()

# Update the array
old_array = "{[{i:'I',c:'#ec4899,#be185d',n:'Isha Kumari',f:'History MDC Sem 1'}"
new_array = "{[{i:'A',c:'#f59e0b,#d97706',n:'Ayushi Kumari',f:'Geo Major, PolSci Minor Sem 1'},{i:'I',c:'#ec4899,#be185d',n:'Isha Kumari',f:'History MDC Sem 1'}"
c2 = c2.replace(old_array, new_array)

with open(file2, "w", encoding="utf-8") as f:
    f.write(c2)
print("Updated pyqs/index.astro")
