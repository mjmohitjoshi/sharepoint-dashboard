import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find all script blocks
scripts = re.findall(r'<script>(.*?)</script>', html, flags=re.DOTALL)
with open('extracted_script.js', 'w', encoding='utf-8') as f:
    for i, s in enumerate(scripts):
        f.write(f"\n// --- Script block {i} ---\n")
        f.write(s)
