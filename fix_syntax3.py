with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the broken string
html = html.replace("document.getElementById(tab + '-view')const excelDocsData", "document.getElementById(tab + '-view').style.display = 'block';\n        }\n\n        const excelDocsData")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed again")
