"""Pulizia forte della grana a scaglie: sfondo molto levigato, figura poco (viso naturale)."""
import cv2, numpy as np
def pulisci(src, out, rect=(250, 50, 540, 1480), hp=5):
    im = cv2.imread(src); h, w = im.shape[:2]
    m = np.zeros((h, w), np.uint8); bg = np.zeros((1, 65)); fg = np.zeros((1, 65))
    cv2.grabCut(im, m, rect, bg, fg, 5, cv2.GC_INIT_WITH_RECT)
    pm = np.where((m == 1) | (m == 3), 1.0, 0.0).astype(np.float32)
    pm = cv2.morphologyEx(pm, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    pm = cv2.GaussianBlur(pm, (0, 0), 6)[..., None]
    person = cv2.fastNlMeansDenoisingColored(im, None, hp, hp, 7, 21)
    back = cv2.bilateralFilter(cv2.fastNlMeansDenoisingColored(im, None, 13, 13, 7, 25), 9, 35, 9)
    o = person * pm + back * (1 - pm)
    o = cv2.addWeighted(o, 1.25, cv2.GaussianBlur(o, (0, 0), 1.2), -0.25, 0)
    g = cv2.GaussianBlur(np.random.default_rng(2).normal(0, 3, (h, w)).astype(np.float32), (0, 0), 0.6)[..., None]
    cv2.imwrite(out, np.clip(o + g, 0, 255).astype(np.uint8))
