import sys

# 1. Update index.astro
file1 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file1, "r", encoding="utf-8") as f:
    c1 = f.read()

# Update preview count
c1 = c1.replace('Isha &amp; 14 others', 'Isha &amp; 15 others')

gouranga_start = c1.find('<!-- Gouranga (GG) -->')
dheeraj_start = c1.find('<!-- Dheeraj -->')

if gouranga_start != -1 and dheeraj_start != -1:
    pooja_row = """<!-- Pooja Rani Pradhan -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <div style="width: 24px; height: 24px; border-radius: 50%; background: linear-gradient(135deg, #a855f7, #7e22ce); display: flex; align-items: center; justify-content: center; font-size: 0.65rem; font-weight: 800; color: white; flex-shrink: 0;">P</div>
            <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Pooja Rani Pradhan</span>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); text-align: right;">Home Science MDC · Sem 1</span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        """
    c1 = c1[:dheeraj_start] + pooja_row + c1[dheeraj_start:]

with open(file1, "w", encoding="utf-8") as f:
    f.write(c1)
print("Updated index.astro")

# 2. Update pyqs/index.astro
file2 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\pyqs\\index.astro"
with open(file2, "r", encoding="utf-8") as f:
    c2 = f.read()

old_str = "{i:'G',c:'#3b82f6,#1d4ed8',n:'Gouranga (GG)',f:'Maths Minor, Geo MDC Sem 1'}"
new_str = "{i:'G',c:'#3b82f6,#1d4ed8',n:'Gouranga (GG)',f:'Maths Minor, Geo MDC Sem 1'},{i:'P',c:'#a855f7,#7e22ce',n:'Pooja Rani Pradhan',f:'Home Science MDC Sem 1'}"
c2 = c2.replace(old_str, new_str)

with open(file2, "w", encoding="utf-8") as f:
    f.write(c2)
print("Updated pyqs/index.astro")
