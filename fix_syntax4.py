with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('const excelDocsData =')
if idx != -1:
    print(repr(html[idx-100:idx+20]))
else:
    print("Not found")

