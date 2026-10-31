"""Costruisce sito/index.html dal file principale: sul sito le foto dei pezzi si caricano da img/CODICE.jpg (qualità piena)."""
import re, pathlib, time
V = time.strftime('%Y%m%d%H%M')
s = open('/home/claude/bottega-lunargento.html').read()
i = s.index('const PHOTOS = {'); j = s.index('\n};', i)
body = re.sub(r'(\n\s*(\w+):)"data:image/jpeg;base64,[^"]*"', lambda m: f'{m.group(1)}"img/{m.group(2)}.jpg?v={V}"', s[i:j])
for code in re.findall(r'img/(\w+)\.jpg', body):
    assert pathlib.Path(f'/home/claude/sette-stelle/img/{code}.jpg').exists(), code
s = s[:i] + body + s[j:]
s = __import__('re').sub(r'<link rel="icon"[^>]*>', '<link rel="icon" type="image/svg+xml" href="img/icona-stella.svg?v=3">\n<link rel="apple-touch-icon" href="img/icona-stella-180.png?v=3">', s, count=1)
head = '''<!doctype html>\n<html lang="it">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>html{color-scheme:dark}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'''
k = s.index('<div class="wrap">')
open('/home/claude/sito/index.html', 'w').write(head + s[:k] + '</head>\n<body>\n' + s[k:] + '\n</body>\n</html>\n')
print('sito/index.html', round(len(s) / 1e6, 2), 'MB')
