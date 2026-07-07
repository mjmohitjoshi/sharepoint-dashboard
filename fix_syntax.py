with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the trailing syntax error
html = html.replace('             renderFFPagination();\n        }\n    </script>', '    </script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed")
