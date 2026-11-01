import pathlib
"""Finitura «fotografica» delle foto dei pezzi: levigatura leggera della grana a scaglie,
un filo di nitidezza e una grana fine da fotografia, così pelle e volti sembrano meno di plastica.
Il sigillo resta identico. Si applica sulle foto già preparate da foto.py (900x1200 con sigillo)."""
import sys, cv2, numpy as np
from PIL import Image
SEAL = Image.open(str(pathlib.Path(__file__).resolve().parent.parent / 'img' / 'sigillo-bottega.png')).convert('RGBA')
W, H, SW = 900, 1200, 144
sl = SEAL.resize((SW, round(SW * SEAL.height / SEAL.width)), Image.LANCZOS)
mask = np.zeros((H, W), np.float32)
a = np.asarray(sl.split()[3], np.float32) / 255
x0, y0 = W - SW - 45, H - sl.height - 45
mask[y0:y0 + sl.height, x0:x0 + SW] = np.clip(a * 1.6, 0, 1)
mask = cv2.GaussianBlur(mask, (5, 5), 0)[..., None]
def finitura(im, seed=1):
    d = cv2.fastNlMeansDenoisingColored(im, None, 2.5, 2.5, 7, 21)
    blur = cv2.GaussianBlur(d, (0, 0), 1.2)
    sh = cv2.addWeighted(d, 1.35, blur, -0.35, 0).astype(np.float32)
    g = np.random.default_rng(seed).normal(0, 3.2, sh.shape[:2]).astype(np.float32)
    g = cv2.GaussianBlur(g, (0, 0), 0.6)[..., None]
    return np.clip(sh + g, 0, 255)
def leviga(path, src=None):
    im = cv2.imread(src or path)
    if im.shape[:2] != (H, W): return False
    out = (finitura(im) * (1 - mask) + im.astype(np.float32) * mask).astype(np.uint8)
    Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).save(path, quality=90, optimize=True, progressive=True)
    return True
if __name__ == '__main__':
    for p in sys.argv[1:]: print(p, leviga(p))
