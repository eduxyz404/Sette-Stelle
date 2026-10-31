"""Leviga la grana «a scaglie» delle foto dei pezzi, lasciando nitido il sigillo."""
import sys, cv2, numpy as np
from PIL import Image
SEAL = Image.open('/home/claude/sette-stelle/img/sigillo-bottega.png').convert('RGBA')
W, H, SW = 900, 1200, 144
sl = SEAL.resize((SW, round(SW * SEAL.height / SEAL.width)), Image.LANCZOS)
mask = np.zeros((H, W), float)
a = np.asarray(sl.split()[3], float) / 255
x0, y0 = W - SW - 45, H - sl.height - 45
mask[y0:y0 + sl.height, x0:x0 + SW] = np.clip(a * 1.6, 0, 1)
mask = cv2.GaussianBlur(mask, (5, 5), 0)[..., None]
def leviga(path, h=5):
    im = cv2.imread(path)
    if im.shape[:2] != (H, W): return False
    d = cv2.fastNlMeansDenoisingColored(im, None, h, h, 7, 21)
    out = (d * (1 - mask) + im * mask).astype(np.uint8)
    Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).save(path, quality=88, optimize=True, progressive=True)
    return True
if __name__ == '__main__':
    for p in sys.argv[1:]: print(p, leviga(p))
