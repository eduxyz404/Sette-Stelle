#!/usr/bin/env python3
"""Genera un Certificato di Proprietà della Bottega delle Sette Stelle.

Uso:
  node strumenti/estrai_pezzi.js
  python3 strumenti/certificato.py --numero 001 --codice A01 --intestato "Nome PG" \
      --anno XXV --mese 2 --giorno 10 [--confezione] [--uscita percorso.html]

Il certificato riprende il modello di Lot: data nel calendario di Lot,
«Intestato a», immagine del pezzo, nome e codice, ricetta di creazione.
"""
import argparse, html, json, math, pathlib

BASE = pathlib.Path(__file__).resolve().parent
REPO = BASE.parent

# Colore del campione accanto a ogni materiale della ricetta
SWATCH = {
    "Argento": "#d3dae6", "Oro": "#e6c27a", "Seta": "#ece4f6", "Lana": "#b8ae9c", "Cotone": "#f3efe6",
    "Pelle": "#8a5a3a", "Zaffiro": "#2b50b3", "Smeraldo Grezzo": "#1f8a5b", "Rubino Grezzo": "#a01c2e",
    "Topazio Grezzo": "#e3a03a", "Acquamarina Grezza": "#79c3d4", "Diamante Grezzo": "#eef3ff", "Opale": "#dfe6f4",
    "Ametista": "#8c4fb3", "Agata": "#2a2630", "Ematite": "#4a4d58", "Tormalina": "#7fae3e", "Cristallo": "#cfe8ff",
    "Confezione": "#b08a5a",
}
RAINBOW = "conic-gradient(#e04848,#e3a03a,#e6d24a,#5cb85c,#4a8fe0,#8c4fb3,#e04848)"


def ricetta(recipe, confezione):
    r = [(q, m) for q, m in recipe]
    if confezione:
        r.append((1, "Confezione"))
    return r


def _star(silver="#c9d2ea", gold="#d9b468", ring=True):
    P = lambda r, t: f"{60 + r * math.sin(t):.1f},{60 - r * math.cos(t):.1f}"
    s = (f'<circle cx="60" cy="60" r="56" fill="none" stroke="{silver}" stroke-width="1" opacity=".6"/>'
         f'<circle cx="60" cy="60" r="50" fill="none" stroke="{gold}" stroke-width=".8" opacity=".6"/>') if ring else ""
    for k in range(8):
        a = k * math.pi / 4
        s += (f'<polygon points="60,60 {P(10, a - math.pi / 8)} {P(46 if k % 2 == 0 else 32, a)} {P(10, a + math.pi / 8)}" '
              f'fill="{silver if k % 2 == 0 else gold}"/>')
    return s + f'<circle cx="60" cy="60" r="5" fill="{gold}"/>'


def _seal(numero):
    """Sigillo circolare con la scritta della bottega lungo il bordo."""
    return f"""<svg class="seal" viewBox="0 0 200 200" aria-hidden="true">
  <defs><path id="ring" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/>
    <radialGradient id="wax" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#f6dc9c"/><stop offset=".55" stop-color="#d9b468"/><stop offset="1" stop-color="#8a6420"/></radialGradient></defs>
  <circle cx="100" cy="100" r="96" fill="url(#wax)"/>
  <circle cx="100" cy="100" r="88" fill="none" stroke="#7a5518" stroke-width="1.4"/>
  <circle cx="100" cy="100" r="60" fill="none" stroke="#7a5518" stroke-width="1.2"/>
  <text font-family="Cinzel, Georgia, serif" font-size="13.5" letter-spacing="3.2" fill="#5a3c0c"><textPath href="#ring">BOTTEGA DELLE SETTE STELLE · VALACIRCA ·</textPath></text>
  <g transform="translate(55 47) scale(.75)">{_star("#5a3c0c", "#7a5518", False)}</g>
  <text x="100" y="152" text-anchor="middle" font-family="Cinzel, Georgia, serif" font-weight="600" font-size="12" letter-spacing="2" fill="#5a3c0c">{html.escape(numero.upper())}</text>
</svg>"""


VALACIRCA = """<svg class="dipper" viewBox="-8 -8 176 106" aria-hidden="true">
  <path d="M0 40 L35 30 L65 32 L95 40 L150 42 L150 78 L100 70 L95 40" fill="none" stroke="#e6c27a" stroke-width="1.2" stroke-opacity=".8" stroke-dasharray="3 3"/>
  <g fill="#fff6dc">""" + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(0, 40, 3), (35, 30, 3.2), (65, 32, 3.4), (95, 40, 2.6), (150, 42, 3.6), (150, 78, 3.2), (100, 70, 3)]
) + "</g></svg>"


def pagina(numero, pezzo, info, intestato, anno, mese, giorno, confezione, esempio=False):
    e = html.escape
    per = {'lei': 'per lei', 'lui': 'per lui', 'coppia': 'per la coppia'}[info['who']]
    abito = 'fabric' in pezzo
    if abito:
        dettagli = [("Tessuto", pezzo['fabric']), ("Colore", pezzo['colorName']), ("Ricami", pezzo['trimName'])]
    else:
        dettagli = [("Metallo", pezzo['metal']), ("Pietra", f"{pezzo['gem']}, taglio {pezzo['cut']}"), ("Peso", pezzo['ct'])]
    righe = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in dettagli)
    tokens = "".join(
        f'<li><span class="sw" style="background:{RAINBOW if m == "Colori" else SWATCH.get(m, "#9aa3b8")}"></span>'
        f'<b>{q}×</b>{e(m)}</li>' for q, m in ricetta(pezzo['recipe'], confezione))
    etichetta = "esempio" if esempio else f"N° {numero}"
    titolo = f"Certificato di esempio · {pezzo['name']}" if esempio else f"Certificato {numero} · {pezzo['name']}"
    nota = ('<p class="note">Questo è un esempio: nome e data saranno quelli del personaggio che acquista.</p>' if esempio else '')
    corners = "".join(f'<svg class="corner {k}" viewBox="0 0 80 80" aria-hidden="true">{CORNER}</svg>' for k in ("tl", "tr", "bl", "br"))
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titolo)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cinzel:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap">
<style>
/* Certificato «Regale»: foto della facciata in testa, nicchia ad arco per il pezzo, sigillo dorato */
:root{{--bg:#070b17;--paper:#0f1731;--paper-2:#131d3b;--line:#5c4a26;--gold:#d9b468;--gold-b:#e6c27a;--fg:#ece6d6;--muted:#a9b2cc;--silver:#c9d2ea;
  --gild:linear-gradient(180deg,#fff1c8 0%,#e6c27a 45%,#a77a2c 100%);color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;background:var(--bg);color:var(--fg);font-family:"Cormorant Garamond",Georgia,serif;font-size:19px;line-height:1.5;
  padding-block:clamp(16px,4vw,48px);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));
  background-image:radial-gradient(ellipse 70% 50% at 50% 0%,rgba(110,140,220,.16),transparent 70%),
    radial-gradient(1px 1px at 20% 30%,rgba(255,255,255,.25) 50%,transparent 51%),radial-gradient(1.5px 1.5px at 80% 70%,rgba(230,194,122,.35) 50%,transparent 51%),
    radial-gradient(1px 1px at 55% 15%,rgba(255,255,255,.2) 50%,transparent 51%);
  background-size:100% 100%,170px 170px,170px 170px,170px 170px}}
.cert{{position:relative;max-width:920px;margin:0 auto;border-radius:20px;overflow:hidden;
  background:linear-gradient(180deg,var(--paper-2),var(--paper));border:1px solid rgba(230,194,122,.55);
  box-shadow:inset 0 0 0 6px var(--paper),inset 0 0 0 7px rgba(230,194,122,.35),0 40px 80px -30px rgba(0,0,0,.95),0 0 60px -20px rgba(230,194,122,.25)}}
.corner{{position:absolute;z-index:3;width:clamp(44px,8vw,72px);color:var(--gold);pointer-events:none}}
.tl{{top:6px;left:6px}}.tr{{top:6px;right:6px;transform:scaleX(-1)}}.bl{{bottom:6px;left:6px;transform:scaleY(-1)}}.br{{bottom:6px;right:6px;transform:scale(-1,-1)}}

/* Testata con la foto */
.head{{position:relative;isolation:isolate;min-height:clamp(220px,32vw,300px);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
  text-align:center;padding:40px 20px 26px;border-bottom:1px solid rgba(230,194,122,.45)}}
.head::before{{content:"";position:absolute;inset:0;z-index:-2;background:url(../img/facciata.jpg) 45% 40%/cover}}
.head::after{{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(7,11,23,.15) 0%,rgba(10,16,34,.6) 50%,rgba(15,23,49,1) 100%)}}
.dipper{{position:absolute;top:22px;right:clamp(40px,10%,110px);width:clamp(90px,16vw,150px);filter:drop-shadow(0 0 6px rgba(255,220,150,.9))}}
.shop{{margin:0;font-family:"Cinzel",Georgia,serif;font-size:.8rem;letter-spacing:.26em;text-transform:uppercase;color:#d7deef;text-shadow:0 2px 8px #000}}
h1{{margin:6px 0 10px;font-family:"Cinzel Decorative",Georgia,serif;font-weight:700;font-size:clamp(1.8rem,5.6vw,3rem);line-height:1.05;
  background:var(--gild);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 3px 8px rgba(0,0,0,.8))}}
.pill{{font-family:"Cinzel",Georgia,serif;font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;color:var(--gold-b);
  border:1px solid rgba(230,194,122,.7);border-radius:999px;padding:4px 16px;background:rgba(7,11,23,.55)}}

/* Corpo: nicchia a sinistra, dati a destra */
.body{{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);gap:clamp(22px,4vw,44px);align-items:center;padding:clamp(26px,4.5vw,44px) clamp(22px,5vw,52px)}}
@media (max-width:720px){{.body{{grid-template-columns:1fr}}}}
.niche{{position:relative;margin:0;padding:10px;border-radius:999px 999px 8px 8px / 190px 190px 8px 8px;
  border:1px solid rgba(230,194,122,.6);box-shadow:0 0 0 5px var(--paper-2),0 0 0 6px rgba(230,194,122,.3),0 30px 50px -25px rgba(0,0,0,.9)}}
.niche img{{display:block;width:100%;height:auto;border-radius:999px 999px 4px 4px / 180px 180px 4px 4px}}
.niche figcaption{{position:absolute;left:50%;bottom:-14px;transform:translateX(-50%);white-space:nowrap;font-family:"Cinzel",Georgia,serif;font-size:.74rem;letter-spacing:.2em;
  color:var(--gold-b);background:var(--paper);border:1px solid rgba(230,194,122,.6);border-radius:999px;padding:3px 14px}}
.who{{display:flex;flex-direction:column;gap:2px;padding-bottom:16px;margin-bottom:16px;border-bottom:1px solid rgba(230,194,122,.3)}}
.lbl{{font-family:"Cinzel",Georgia,serif;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}}
.name{{font-family:"Cinzel Decorative",Georgia,serif;font-size:clamp(1.5rem,3.8vw,2.1rem);line-height:1.15;color:var(--gold-b);overflow-wrap:anywhere}}
.date{{font-family:"Cinzel",Georgia,serif;font-weight:500;font-size:1rem;letter-spacing:.06em;color:var(--fg)}}
.item h2{{margin:0;font-family:"Cinzel Decorative",Georgia,serif;font-weight:400;font-size:clamp(1.4rem,3.4vw,1.8rem);line-height:1.15;color:#f4ead0}}
.item .gl{{margin:0;font-style:italic;color:var(--muted)}}
.item .cat{{display:inline-block;margin-top:6px;font-family:"Cinzel",Georgia,serif;font-size:.74rem;letter-spacing:.16em;color:var(--gold)}}
dl{{margin:14px 0 0;display:flex;flex-direction:column;gap:6px}}
dl div{{display:grid;grid-template-columns:86px 1fr;gap:10px}}
dt{{font-family:"Cinzel",Georgia,serif;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-top:5px}}
dd{{margin:0;font-size:1.08rem}}
.desc{{margin:12px 0 0;font-style:italic;color:#c4cbe0}}

/* Ricetta e firma */
.foot{{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center;padding:24px clamp(22px,5vw,52px) clamp(28px,4vw,40px);
  border-top:1px solid rgba(230,194,122,.3);background:rgba(7,11,23,.35)}}
@media (max-width:620px){{.foot{{grid-template-columns:1fr;justify-items:center;text-align:center}}}}
.recipe h3{{margin:0 0 2px;font-family:"Cinzel",Georgia,serif;font-weight:500;font-size:.8rem;letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}}
.recipe small{{display:block;margin-bottom:10px;font-style:italic;font-size:1rem;color:var(--muted)}}
.recipe ul{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}}
@media (max-width:620px){{.recipe ul{{justify-content:center}}}}
.recipe li{{display:inline-flex;align-items:center;gap:8px;padding:5px 14px 5px 6px;border-radius:999px;border:1px solid rgba(230,194,122,.45);background:rgba(19,29,59,.9);font-size:1.05rem}}
.recipe li b{{font-family:"Cinzel",Georgia,serif;font-weight:600;font-size:.86rem;color:var(--gold-b)}}
.sw{{width:20px;height:20px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.35),0 0 0 1px rgba(0,0,0,.4)}}
.sign{{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}}
.seal{{width:118px;height:118px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.6));transform:rotate(-8deg)}}
.sign span{{font-family:"Cinzel",Georgia,serif;font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}}
.note{{margin:0;padding:14px 20px 22px;text-align:center;font-style:italic;color:var(--gold-b)}}
</style>
</head>
<body>
<main class="cert">
  {corners}
  <header class="head">
    {VALACIRCA}
    <p class="shop">Bottega delle Sette Stelle · Valacirca</p>
    <h1>Certificato di Proprietà</h1>
    <span class="pill">{e(etichetta)}</span>
  </header>

  <section class="body">
    <figure class="niche">
      <img src="../img/{e(pezzo['code'])}.png" alt="{e(pezzo['name'])}, {e(info['name'].lower())} {e(per)}">
      <figcaption>Cod. {e(pezzo['code'])}</figcaption>
    </figure>
    <div>
      <div class="who">
        <span class="lbl">Intestato a</span>
        <span class="name">{e(intestato)}</span>
        <span class="date">Anno {e(anno)} · Mese {e(str(mese))}° · Giorno {e(str(giorno))}°</span>
      </div>
      <div class="item">
        <h2>{e(pezzo['name'])}</h2>
        <p class="gl">«{e(pezzo['gloss'])}»</p>
        <span class="cat">{e(info['name'])} {e(per)}</span>
        <dl>{righe}</dl>
        <p class="desc">{e(pezzo['desc'])}</p>
      </div>
    </div>
  </section>

  <footer class="foot">
    <div class="recipe">
      <h3>Ricetta di creazione</h3>
      <small>{e(pezzo['cls'])}</small>
      <ul>{tokens}</ul>
    </div>
    <div class="sign">
      {_seal(etichetta)}
      <span>sigillo della bottega</span>
    </div>
  </footer>
  {nota}
</main>
</body>
</html>
"""


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
