with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's see the exact text causing the issue
idx = html.find('const excelDocsData')
print(html[idx-100:idx+20])

