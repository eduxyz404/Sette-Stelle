"""Crea l'anteprima a file unico (per l'artifact su claude.ai) partendo da index.html:
le foto dei pezzi vengono incorporate in piccolo (600x800) dentro la pagina.
Uso: python3 strumenti/anteprima.py  ->  anteprima.html (non va nel sito)"""
import re, io, base64, pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parent.parent
s = (R / 'index.html').read_text()
def emb(m):
    im = Image.open(R / 'img' / f'{m.group(2)}.jpg').convert('RGB').resize((540, 720), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=80, optimize=True, progressive=True)
    return f'{m.group(1)}"data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}"'
for blocco in ('const PHOTOS = {', 'const WORN = {'):
    if blocco not in s: continue
    i = s.index(blocco); j = s.index('\n};', i)
    s = s[:i] + re.sub(r'(\n\s*\w+:)"img/([\w-]+)\.jpg[^"]*"', lambda m: emb(m), s[i:j]) + s[j:]
svg = (R / 'img' / 'icona-stella.svg').read_text()
import urllib.parse
s = re.sub(r'<link rel="icon"[^>]*>', '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,' + urllib.parse.quote(svg) + '">', s, count=1)
s = re.sub(r'<link rel="apple-touch-icon"[^>]*>\n?', '', s)
out = pathlib.Path('/tmp/anteprima.html') if len(__import__('sys').argv) < 2 else pathlib.Path(__import__('sys').argv[1])
out.write_text(s); print(out, round(len(s) / 1e6, 1), 'MB')
