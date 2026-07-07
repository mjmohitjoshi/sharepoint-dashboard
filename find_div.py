from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.stack.append(self.getpos())
    
    def handle_endtag(self, tag):
        if tag == 'div':
            if len(self.stack) > 0:
                self.stack.pop()
            else:
                print("Extra closing div at:", self.getpos())

parser = MyHTMLParser()
with open('index.html', 'r', encoding='utf-8') as f:
    parser.feed(f.read())

if len(parser.stack) > 0:
    print("Unclosed divs at:", parser.stack)
