import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Extract ffDocsData
ff_match = re.search(r'(const ffDocsData = \[.*?\];)', html, flags=re.DOTALL)
if ff_match:
    with open('ff_data.js', 'w', encoding='utf-8') as f:
        f.write(ff_match.group(1))
    html = html.replace(ff_match.group(1), '')

# 2. Extract excelDocsData
excel_match = re.search(r'(const excelDocsData = \[.*?\];)', html, flags=re.DOTALL)
if excel_match:
    with open('excel_data.js', 'w', encoding='utf-8') as f:
        f.write(excel_match.group(1))
    html = html.replace(excel_match.group(1), '')

# 3. Add script tags to index.html
script_tags = '\n    <script src="ff_data.js"></script>\n    <script src="excel_data.js"></script>\n'

# Find the first `<script>` tag inside body and insert before it
idx = html.find('<script>')
if idx != -1:
    html = html[:idx] + script_tags + html[idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Files extracted and index.html updated!")
