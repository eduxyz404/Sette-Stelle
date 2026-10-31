"""Aumenta la nitidezza delle foto dei pezzi (maschera di contrasto), sigillo escluso."""
import sys, numpy as np
from PIL import Image, ImageFilter
from leviga import mask
def nitido(path, src=None, r=1.6, p=90, t=2):
    im = Image.open(src or path).convert('RGB')
    sh = im.filter(ImageFilter.UnsharpMask(radius=r, percent=p, threshold=t))
    a = np.asarray(sh, np.float32) * (1 - mask) + np.asarray(im, np.float32) * mask
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path, quality=93, optimize=True, progressive=True)
if __name__ == '__main__':
    for f in sys.argv[1:]: nitido(f)
