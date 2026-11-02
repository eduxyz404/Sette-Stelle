"""Rifà le foto dei pezzi da originali/CODICE.jpg: correzione luce dove serve, bordi a specchio, sigillo, nitidezza.
Uso: python3 strumenti/rifai_foto.py A73 G25 ...   (senza codici: tutte)"""
import sys, pathlib
from PIL import Image, ImageEnhance
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import foto, nitido
R = pathlib.Path(__file__).resolve().parent.parent
def forte(im):
    im = foto.neutral(im, 0.7); im = ImageEnhance.Color(im).enhance(1.12); im = ImageEnhance.Brightness(im).enhance(1.05); return ImageEnhance.Contrast(im).enhance(1.06)
VIVO = {'A07','A13','A34','A35','A36','A47','A49','A50','A58','A59','A60','A61'} | {f'A{n}' for n in range(14, 34)}  # luce meno arancione
FORTE = {'A51','A52','A62'}  # notte d'oriente: correzione più forte
REAL = set((R / 'originali' / 'realistiche.txt').read_text().split()) if (R / 'originali' / 'realistiche.txt').exists() else set()  # foto rifatte (Gemini): niente correzione colore
codes = sys.argv[1:] or sorted(p.stem for p in (R / 'originali').glob('*.jpg'))
for c in codes:
    im = Image.open(R / 'originali' / f'{c}.jpg').convert('RGB')
    if c in VIVO and c not in REAL: im = foto.neutro_vivo(im)
    if c in FORTE and c not in REAL: im = forte(im)
    if im.width > im.height:  # gioielli: foto orizzontali, ritaglio centrale quasi quadrato
        w, h = im.size; cw = min(w, int(h * 1.05)); x0 = (w - cw) // 2; im = im.crop((x0, 0, x0 + cw, h))
    P = R / 'img' / f'{c}.jpg'
    foto.stamp(foto.fit_specchio(im)).save(P, quality=95)
    nitido.nitido(str(P))
    print(c, end=' ', flush=True)
print()
