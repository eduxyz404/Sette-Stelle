"""Prepara le foto dei pezzi: 900x1200 (3:4, come la cornice), figura intera, sigillo sempre nello stesso punto."""
import io, base64
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
SEAL = Image.open('/home/claude/sette-stelle/img/sigillo-bottega.png').convert('RGBA')
W, H = 900, 1200
SW = 144                      # larghezza sigillo, fissa
SX, SY = W - SW - 45, H - 0   # angolo: 45 px da destra; il fondo viene calcolato sotto
def fit(src):
    w, h = src.size; r = w / h
    if abs(r - 0.75) < 0.005: return src.resize((W, H), Image.LANCZOS)
    c = Image.new('RGB', (W, H))
    if r < 0.75:
        fig = src.resize((round(w * H / h), H), Image.LANCZOS); x0 = (W - fig.width) // 2
        c.paste(fig.crop((0, 0, 10, H)).resize((x0 + 12, H)).filter(ImageFilter.GaussianBlur(3)), (0, 0))
        c.paste(fig.crop((fig.width - 10, 0, fig.width, H)).resize((W - x0 - fig.width + 12, H)).filter(ImageFilter.GaussianBlur(3)), (x0 + fig.width - 12, 0))
        m = Image.new('L', fig.size, 0); ImageDraw.Draw(m).rectangle((6, 0, fig.width - 6, fig.height), fill=255)
        c.paste(fig, (x0, 0), m.filter(ImageFilter.GaussianBlur(4)))
    else:
        fig = src.resize((W, round(h * W / w)), Image.LANCZOS); y0 = (H - fig.height) // 2
        c.paste(fig.crop((0, 0, W, 10)).resize((W, y0 + 12)).filter(ImageFilter.GaussianBlur(3)), (0, 0))
        c.paste(fig.crop((0, fig.height - 10, W, fig.height)).resize((W, H - y0 - fig.height + 12)).filter(ImageFilter.GaussianBlur(3)), (0, y0 + fig.height - 12))
        m = Image.new('L', fig.size, 0); ImageDraw.Draw(m).rectangle((0, 6, fig.width, fig.height - 6), fill=255)
        c.paste(fig, (0, y0), m.filter(ImageFilter.GaussianBlur(4)))
    return c
def stamp(im):
    im = im.convert('RGBA')
    sl = SEAL.resize((SW, round(SW * SEAL.height / SEAL.width)), Image.LANCZOS)
    sl.putalpha(sl.split()[3].point(lambda v: int(v * 0.78)))
    im.alpha_composite(sl, (W - SW - 45, H - sl.height - 45))
    return im.convert('RGB')
def neutral(im, k=0.7):
    """Luce più neutra: toglie il 70% della dominante calda (bilanciamento sul grigio medio, in luce lineare)."""
    lin = (np.asarray(im.convert('RGB'), float) / 255) ** 2.2
    m = lin.reshape(-1, 3).mean(0); g = (m.mean() / m) ** k
    return Image.fromarray((np.clip(lin * g, 0, 1) ** (1 / 2.2) * 255 + .5).astype('uint8'))
def build(path, out_jpg, neutro=False):  # neutro=True solo per i Completi per lui
    im = Image.open(path).convert('RGB')
    im = stamp(fit(neutral(im) if neutro else im))
    im.save(out_jpg, quality=86, optimize=True, progressive=True)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
