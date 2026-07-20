import sys

file_path = "C:\\Users\\Anurag\\Documents\\GitHub\\TataCollegeHub\\src\\pages\\index.astro"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Locate Philosophy MDC PYQ block
start_idx = content.find('<!-- Philosophy MDC PYQ -->')
end_idx = content.find('<!-- Botany Minor PYQ -->', start_idx)

if start_idx != -1 and end_idx != -1:
    block = content[start_idx:end_idx]
    new_block = block.replace('20 Jul &rarr; <strong style="color: var(--accent-success);">20 Jul</strong>', '19 Jul &rarr; <strong style="color: var(--accent-success);">20 Jul</strong>')
    content = content[:start_idx] + new_block + content[end_idx:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated index.astro requested date for Philosophy MDC")
