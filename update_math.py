import sys

# 1. Update pyqs/index.astro
file1 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\pyqs\\index.astro"
with open(file1, "r", encoding="utf-8") as f:
    c1 = f.read()

c1 = c1.replace('padding: 1px 5px;">36<', 'padding: 1px 5px;">37<')
old_end = "s:'Sem 1'}].map"
new_end = "s:'Sem 1'},{e:'📐',t:'Mathematics Minor PYQ',s:'Sem 1'}].map"
c1 = c1.replace(old_end, new_end)

with open(file1, "w", encoding="utf-8") as f:
    f.write(c1)
print("Updated pyqs/index.astro")

# 2. Update index.astro
file2 = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file2, "r", encoding="utf-8") as f:
    c2 = f.read()

c2 = c2.replace("39 Tasks Resolved", "40 Tasks Resolved")

insertion = "<!-- Psychology Major PYQ -->"
new_row = """<!-- Mathematics Minor PYQ -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <span style="font-size: 0.75rem; flex-shrink: 0;">📐</span>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Mathematics Minor PYQ</span>
              <span style="font-size: 0.72rem; color: var(--text-tertiary); margin-left: 0.4rem;">Sem 1</span>
            </div>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; text-align: right;">20 Jul &rarr; <strong style="color: var(--accent-success);">20 Jul</strong></span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        """
c2 = c2.replace(insertion, new_row + insertion)

with open(file2, "w", encoding="utf-8") as f:
    f.write(c2)
print("Updated index.astro")
