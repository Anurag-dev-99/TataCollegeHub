import sys

# 1. Update index.astro
file1 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file1, "r", encoding="utf-8") as f:
    c1 = f.read()

# Update preview badge
c1 = c1.replace(
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #d97706); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">A</span>\n          Ayushi &amp; 13 others',
    '<span style="width: 20px; height: 20px; border-radius: 50%; background: linear-gradient(135deg, #ec4899, #be185d); display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; font-weight: 800; color: white;">I</span>\n          Isha &amp; 13 others'
)

# Extract blocks
ayushi_start = c1.find('<!-- Ayushi -->')
isha_start = c1.find('<!-- Isha -->')
dheeraj_start = c1.find('<!-- Dheeraj -->')

if ayushi_start != -1 and isha_start != -1 and dheeraj_start != -1:
    ayushi_block = c1[ayushi_start:isha_start]
    isha_block = c1[isha_start:dheeraj_start]

    # Update Isha's text
    isha_block = isha_block.replace('History MDC PYQ · Sem 1', 'History MDC, Chem Minor · Sem 1')

    # Swap them
    c1 = c1[:ayushi_start] + isha_block + ayushi_block + c1[dheeraj_start:]

with open(file1, "w", encoding="utf-8") as f:
    f.write(c1)
print("Updated index.astro")


# 2. Update pyqs/index.astro
file2 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\pyqs\\index.astro"
with open(file2, "r", encoding="utf-8") as f:
    c2 = f.read()

old_str = "{[{i:'A',c:'#f59e0b,#d97706',n:'Ayushi Kumari',f:'Geo Major, PolSci Minor Sem 1'},{i:'I',c:'#ec4899,#be185d',n:'Isha Kumari',f:'History MDC Sem 1'}"
new_str = "{[{i:'I',c:'#ec4899,#be185d',n:'Isha Kumari',f:'History MDC, Chem Minor Sem 1'},{i:'A',c:'#f59e0b,#d97706',n:'Ayushi Kumari',f:'Geo Major, PolSci Minor Sem 1'}"
c2 = c2.replace(old_str, new_str)

with open(file2, "w", encoding="utf-8") as f:
    f.write(c2)
print("Updated pyqs/index.astro")
