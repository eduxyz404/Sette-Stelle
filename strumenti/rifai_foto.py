"""Rifà tutte le foto dei pezzi dagli originali: colore, sfondo pulito, riempimento a specchio, sigillo, finitura."""
import json, sys
from PIL import Image, ImageEnhance
import foto, leviga, pulisci
S = '/tmp/claude-0/-home-claude/fbfb370e-b06d-58b8-a1f4-d4a74eaee141/scratchpad/'
A = '/mnt/user-data/attachments/fbfb370e-b06d-58b8-a1f4-d4a74eaee141/'
M = json.load(open(S + 'map-all.json'))
G = {'G17':'5f762357','G18':'5cec129d','G19':'e5203aae','G20':'428e52b3','G21':'96b25a13','G22':'81480c32','G23':'3ab3b613','G24':'11e79f5f','G25':'f1751c4d','G26':'fa4a1678','G27':'cb6a9807','G28':'f348ffdf','G29':'d33c9a24','G30':'93dc07cf','G31':'82d25971','G32':'80ed2c1d','G33':'4f078451','G34':'8ff6bb96','G35':'ff89bb0a','G36':'93a250e6'}
for c, f in G.items(): M[c] = A + f + '-image.png'
def forte(im):
    im = foto.neutral(im, 0.7); im = ImageEnhance.Color(im).enhance(1.12); im = ImageEnhance.Brightness(im).enhance(1.05); return ImageEnhance.Contrast(im).enhance(1.06)
VIVO = {'A07','A13','A34','A35','A36','A47','A49','A50','A58','A59','A60','A61'} | {f'A{n}' for n in range(14, 34)}
FORTE = {'A51','A52','A62'}
BALCONE = set()  # niente levigatura: foto il più possibile fedeli all'originale
codes = sys.argv[1:] or sorted(M)
for c in codes:
    src = M[c]
    if c in BALCONE:
        pulisci.pulisci(src, S + 'tmp-pul.png', (230, 40, 560, 1490), hp=3); src = S + 'tmp-pul.png'
    im = Image.open(src).convert('RGB')
    if c in VIVO: im = foto.neutro_vivo(im)
    if c in FORTE: im = forte(im)
    if im.width > im.height:
        w, h = im.size; cw = min(w, int(h * 1.05)); x0 = (w - cw) // 2; im = im.crop((x0, 0, x0 + cw, h))
    out = foto.stamp(foto.fit_specchio(im))
    P = f'/home/claude/sette-stelle/img/{c}.jpg'
    out.save(P, quality=92)
    if False: leviga.leviga(P)
    else: Image.open(P).save(P, quality=90, optimize=True, progressive=True)
    print(c, end=' ', flush=True)
