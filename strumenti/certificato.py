#!/usr/bin/env python3
"""Genera un Certificato di Proprietà della Bottega delle Sette Stelle.

Uso:
  python3 certificato.py --numero 001 --codice A01 --intestato "Nome PG" \
      --anno XXV --mese 2 --giorno 10 [--confezione] [--uscita percorso.html]

Il certificato riprende il modello di Lot: data nel calendario di Lot,
«Intestato a», immagine del pezzo, nome e codice, ricetta di creazione.
"""
import argparse, html, json, pathlib

BASE = pathlib.Path(__file__).resolve().parent
REPO = BASE.parent


def ricetta_testo(recipe, confezione):
    parti = [f"{q}x{m}" for q, m in recipe]
    if confezione:
        parti.append("1xConfezione")
    return parti


def pagina(numero, pezzo, info, intestato, anno, mese, giorno, confezione, esempio=False):
    e = html.escape
    nome_cat = info['name']
    per = {'lei': 'per lei', 'lui': 'per lui', 'coppia': 'per la coppia'}[info['who']]
    ricetta = ricetta_testo(pezzo['recipe'], confezione)
    abito = 'fabric' in pezzo
    if abito:
        dettagli = [("Tessuto", pezzo['fabric']), ("Colore", pezzo['colorName']), ("Ricami", pezzo['trimName'])]
    else:
        dettagli = [("Metallo", pezzo['metal']), ("Pietra", f"{pezzo['gem']}, taglio {pezzo['cut']}"), ("Peso", pezzo['ct'])]
    righe = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in dettagli)
    chips = "".join(f"<li>{e(r)}</li>" for r in ricetta)
    titolo = f"Certificato {numero} · {pezzo['name']}" if not esempio else f"Certificato di esempio · {pezzo['name']}"
    nota = '<p class="note">Esempio: il nome e la data verranno sostituiti con quelli del personaggio che acquista.</p>' if esempio else ''
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titolo)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cinzel:wght@400;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap">
<style>
:root{{--bg:#0a0f1f;--paper:#101934;--line:#5c4a26;--gold:#d9b468;--gold-b:#e6c27a;--fg:#ece6d6;--muted:#a9b2cc;
  --gild:linear-gradient(180deg,#fff1c8 0%,#e6c27a 45%,#a77a2c 100%);color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:"Cormorant Garamond",Georgia,serif;font-size:19px;line-height:1.5;
  padding:clamp(16px,4vw,40px) max(16px,env(safe-area-inset-left,0px));
  background-image:radial-gradient(1px 1px at 20% 30%,rgba(255,255,255,.22) 50%,transparent 51%),radial-gradient(1.5px 1.5px at 80% 70%,rgba(230,194,122,.3) 50%,transparent 51%);background-size:150px 150px}}
.cert{{position:relative;max-width:660px;margin:0 auto;background:var(--paper);border:1px solid var(--line);
  box-shadow:inset 0 0 0 6px var(--paper),inset 0 0 0 7px var(--line),0 30px 60px -30px rgba(0,0,0,.9);
  padding:clamp(28px,6vw,52px) clamp(20px,6vw,56px);text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px}}
.corner{{position:absolute;width:clamp(44px,9vw,70px);color:var(--gold)}}
.tl{{top:5px;left:5px}}.tr{{top:5px;right:5px;transform:scaleX(-1)}}.bl{{bottom:5px;left:5px;transform:scaleY(-1)}}.br{{bottom:5px;right:5px;transform:scale(-1,-1)}}
.seal{{width:64px;height:64px}}
.shop{{font-family:"Cinzel",Georgia,serif;letter-spacing:.18em;font-size:.82rem;text-transform:uppercase;color:var(--muted);margin:0}}
h1{{margin:4px 0 0;font-family:"Cinzel Decorative",Georgia,serif;font-weight:700;font-size:clamp(1.6rem,5.4vw,2.3rem);line-height:1.1;
  background:var(--gild);-webkit-background-clip:text;background-clip:text;color:transparent}}
.num{{font-family:"Cinzel",Georgia,serif;font-size:.86rem;letter-spacing:.2em;color:var(--gold)}}
.date{{margin:6px 0 0;font-family:"Cinzel",Georgia,serif;font-weight:600;font-size:1.02rem;letter-spacing:.06em}}
.to{{margin:0;font-size:1.25rem;font-style:italic}}
.to b{{font-style:normal;font-family:"Cinzel Decorative",Georgia,serif;font-weight:400;color:var(--gold-b)}}
.img{{width:min(100%,420px);height:auto;margin:10px 0 4px;border:1px solid var(--line);box-shadow:0 0 0 4px var(--paper),0 0 0 5px var(--line)}}
.item{{width:100%;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0;margin-top:6px}}
.item h2{{margin:0;font-family:"Cinzel Decorative",Georgia,serif;font-weight:400;font-size:1.5rem;color:#f1e6c8}}
.item .code{{font-family:"Cinzel",Georgia,serif;letter-spacing:.16em;font-size:.82rem;color:var(--gold)}}
.item .gl{{margin:2px 0 0;font-style:italic;color:var(--muted)}}
dl{{display:grid;grid-template-columns:auto 1fr;gap:3px 14px;text-align:left;margin:12px auto 0;max-width:440px}}
dt{{font-family:"Cinzel",Georgia,serif;font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-top:4px}}
dd{{margin:0}}
.desc{{margin:10px 0 0;font-style:italic;color:var(--muted)}}
.recipe h3{{margin:4px 0 6px;font-family:"Cinzel",Georgia,serif;font-weight:400;font-size:.8rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}}
.recipe small{{display:block;font-style:italic;color:var(--muted);margin-bottom:8px}}
.recipe ul{{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;justify-content:center;gap:6px}}
.recipe li{{border:1px solid var(--line);border-radius:999px;padding:2px 12px;font-family:"Cinzel",Georgia,serif;font-size:.86rem}}
.sign{{margin-top:12px;font-style:italic;color:var(--muted)}}
.sign b{{display:block;font-style:normal;font-family:"Cinzel Decorative",Georgia,serif;font-weight:400;color:var(--fg);font-size:1.1rem}}
.note{{margin:8px 0 0;font-size:.95rem;color:#e6c27a;font-style:italic}}
</style>
</head>
<body>
<main class="cert">
  {"".join(f'<svg class="corner {k}" viewBox="0 0 80 80" aria-hidden="true">{CORNER}</svg>' for k in ("tl","tr","bl","br"))}
  <svg class="seal" viewBox="0 0 120 120" aria-hidden="true">{STAR}</svg>
  <p class="shop">Bottega delle Sette Stelle · Valacirca</p>
  <h1>Certificato di Proprietà</h1>
  <span class="num">{'N° ' + e(numero) if not esempio else 'esempio'}</span>
  <p class="date">Anno {e(anno)} · Mese {e(str(mese))}° · Giorno {e(str(giorno))}°</p>
  <p class="to">Intestato a <b>{e(intestato)}</b></p>
  <img class="img" src="../img/{e(pezzo['code'])}.png" alt="{e(pezzo['name'])}, {e(nome_cat.lower())} {e(per)}">
  <section class="item">
    <h2>{e(pezzo['name'])}</h2>
    <span class="code">{e(nome_cat)} {e(per)} · Cod. {e(pezzo['code'])}</span>
    <p class="gl">«{e(pezzo['gloss'])}»</p>
    <dl>{righe}</dl>
    <p class="desc">{e(pezzo['desc'])}</p>
  </section>
  <section class="recipe">
    <h3>Ricetta di creazione</h3>
    <small>{e(pezzo['cls'])}</small>
    <ul>{chips}</ul>
  </section>
  <p class="sign">certificato rilasciato da<b>Bottega delle Sette Stelle</b></p>
  {nota}
</main>
</body>
</html>
"""


def _star():
    import math
    P = lambda r, t: f"{60 + r * math.sin(t):.1f},{60 - r * math.cos(t):.1f}"
    s = '<circle cx="60" cy="60" r="56" fill="none" stroke="#c9d2ea" stroke-width="1" opacity=".6"/><circle cx="60" cy="60" r="50" fill="none" stroke="#d9b468" stroke-width=".8" opacity=".6"/>'
    for k in range(8):
        a = k * math.pi / 4
        long = 46 if k % 2 == 0 else 32
        fill = "#c9d2ea" if k % 2 == 0 else "#d9b468"
        s += f'<polygon points="60,60 {P(10, a - math.pi / 8)} {P(long, a)} {P(10, a + math.pi / 8)}" fill="{fill}"/>'
    return s + '<circle cx="60" cy="60" r="5" fill="#d9b468"/>'


STAR = _star()
CORNER = ('<path d="M4 4 H70 M4 4 V70" stroke="currentColor" stroke-width="1.6" fill="none"/>'
          '<path d="M10 10 H46 M10 10 V46" stroke="currentColor" stroke-width=".9" fill="none" opacity=".7"/>'
          '<path d="M10 10 C30 12 40 22 38 34 C36 44 24 44 24 36 C24 30 31 29 32 34" stroke="currentColor" stroke-width="1.3" fill="none"/>'
          '<path d="M10 10 C12 30 22 40 34 38" stroke="currentColor" stroke-width="1.1" fill="none" opacity=".8"/>'
          '<path d="M54 4 C58 9 64 9 68 4 C64 -1 58 -1 54 4Z M4 54 C9 58 9 64 4 68 C-1 64 -1 58 4 54Z" fill="currentColor" opacity=".8"/>'
          '<path d="M10 2 L12.5 7.5 L18 10 L12.5 12.5 L10 18 L7.5 12.5 L2 10 L7.5 7.5Z" fill="currentColor"/>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--numero', required=True)
    ap.add_argument('--codice', required=True)
    ap.add_argument('--intestato', required=True)
    ap.add_argument('--anno', required=True)
    ap.add_argument('--mese', required=True)
    ap.add_argument('--giorno', required=True)
    ap.add_argument('--confezione', action='store_true')
    ap.add_argument('--esempio', action='store_true')
    ap.add_argument('--uscita')
    a = ap.parse_args()
    dati = json.loads((BASE / 'pezzi.json').read_text())
    pezzo = next(p for p in dati['ITEMS'] if p['code'] == a.codice)
    info = dati['CAT_INFO'][pezzo['cat']]
    out = pathlib.Path(a.uscita) if a.uscita else REPO / 'certificati' / f"{a.numero}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(pagina(a.numero, pezzo, info, a.intestato, a.anno, a.mese, a.giorno, a.confezione, a.esempio))
    print(out)


if __name__ == '__main__':
    main()
