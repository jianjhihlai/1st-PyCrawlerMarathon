import importlib
from cupoyproject.spiders import newsparser

text = ''
with open('newsites/mamaclub.com_ex.html', 'r', encoding='UTF-8') as f:
    text = f.read()

parser = newsparser.NewsParser('mamaclub.com')
parsed = parser.parse(text)
print(parsed.author)
print(parsed.publish)