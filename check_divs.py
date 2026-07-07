with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

div_open = html.count('<div')
div_close = html.count('</div')
print(f"Open: {div_open}, Close: {div_close}")
