import sys

file_path = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update count
content = content.replace("35 Tasks Resolved", "39 Tasks Resolved")

insertion_point = "<!-- Psychology Major PYQ -->"
new_rows = """<!-- History MDC PYQ -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <span style="font-size: 0.75rem; flex-shrink: 0;">📜</span>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">History MDC PYQ</span>
              <span style="font-size: 0.72rem; color: var(--text-tertiary); margin-left: 0.4rem;">Sem 1</span>
            </div>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; text-align: right;">20 Jul &rarr; <strong style="color: var(--accent-success);">20 Jul</strong></span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        <!-- Geography Major PYQ -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <span style="font-size: 0.75rem; flex-shrink: 0;">🌍</span>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Geography Major PYQ</span>
              <span style="font-size: 0.72rem; color: var(--text-tertiary); margin-left: 0.4rem;">Sem 1</span>
            </div>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; text-align: right;">20 Jul &rarr; <strong style="color: var(--accent-success);">20 Jul</strong></span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        <!-- Political Science Minor PYQ -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <span style="font-size: 0.75rem; flex-shrink: 0;">🏛️</span>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Political Science Minor PYQ</span>
              <span style="font-size: 0.72rem; color: var(--text-tertiary); margin-left: 0.4rem;">Sem 1</span>
            </div>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; text-align: right;">20 Jul &rarr; <strong style="color: var(--accent-success);">20 Jul</strong></span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        <!-- Economics Minor PYQ -->
        <div style="display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.6rem 0.6rem; border-radius: var(--radius-xs); transition: background 0.15s;" class="req-row">
          <div style="display: flex; align-items: center; gap: 0.6rem; min-width: 0;">
            <span style="font-size: 0.75rem; flex-shrink: 0;">📊</span>
            <div>
              <span style="font-size: 0.85rem; font-weight: 700; color: var(--text-primary);">Economics Minor PYQ</span>
              <span style="font-size: 0.72rem; color: var(--text-tertiary); margin-left: 0.4rem;">Sem 1</span>
            </div>
          </div>
          <span style="font-size: 0.72rem; color: var(--text-secondary); white-space: nowrap; text-align: right;">20 Jul &rarr; <strong style="color: var(--accent-success);">20 Jul</strong></span>
        </div>

        <div style="height: 1px; background: var(--border-color); margin: 0 0.2rem; opacity: 0.5;"></div>

        """

content = content.replace(insertion_point, new_rows + insertion_point)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated index.astro successfully")
