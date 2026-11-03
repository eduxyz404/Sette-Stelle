"""Foto di vetrina per i pezzi piccoli: la stessa foto, ingrandita sul gioiello per la scheda,
con il sigillo sempre nello stesso punto. La foto intera resta in img/CODICE.jpg (ingrandimento).
Lo zoom si legge dal campo `zoom:[scala, x%, y%]` del pezzo in index.html (via strumenti/pezzi.json).
Uso: node strumenti/estrai_pezzi.js && python3 strumenti/vetrina.py [CODICI...]   ->  img/CODICE-v.jpg"""
import sys, json, pathlib
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import foto, nitido
R = pathlib.Path(__file__).resolve().parent.parent
items = {p['code']: p for p in json.loads((R / 'strumenti' / 'pezzi.json').read_text())['ITEMS'] if p.get('zoom')}
codes = sys.argv[1:] or sorted(items)
for c in codes:
    s, ox, oy = items[c]['zoom']; ox /= 100; oy /= 100
    im = Image.open(R / 'originali' / f'{c}.jpg').convert('RGB')
    if im.width > im.height:
        w, h = im.size; cw = min(w, int(h * 1.05)); x0 = (w - cw) // 2; im = im.crop((x0, 0, x0 + cw, h))
    big = foto.fit_specchio(im) if abs(im.width / im.height - .75) > .005 else im
    w, h = big.size
    box = ((ox - ox / s) * w, (oy - oy / s) * h, (ox + (1 - ox) / s) * w, (oy + (1 - oy) / s) * h)
    v = big.crop(tuple(round(b) for b in box)).resize((foto.W, foto.H), Image.LANCZOS)
    P = R / 'img' / f'{c}-v.jpg'
    foto.stamp(v).save(P, quality=95)
    nitido.nitido(str(P))
    print(c, end=' ', flush=True)
print()
