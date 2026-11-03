#!/usr/bin/env python3
"""Genera il Certificato Nuziale della Bottega delle Sette Stelle:
un unico certificato per gli sposi, con le fedi e gli abiti nuziali acquistati.

Uso:
  node strumenti/estrai_pezzi.js
  python3 strumenti/certificato_nozze.py --numero N001 --sposi "Nome uno" "Nome due" \
      --codici G56 A41 A67 --anno XXV --mese 6 --giorno 21 \
      [--luogo "Giardino di ..."] [--testimoni "Nome" "Nome"] [--dedica "..." --firma "..."] [--esempio] [--uscita percorso.html]
"""
import argparse, html, json, math, pathlib

BASE = pathlib.Path(__file__).resolve().parent
REPO = BASE.parent
SWATCH = {"Argento": "#c9cfda", "Oro": "#d9b468", "Ferro": "#55575e", "Rame": "#b8743f", "Cotone": "#efe8da",
          "Cristallo": "#d6ecff", "Cera": "#e8d9a8", "Confezione": "#b08a5a"}
RAINBOW = "conic-gradient(#e04848,#e3a03a,#e6d24a,#5cb85c,#4a8fe0,#8c4fb3,#e04848)"
FRASE = ("Elen síla lúmenn' omentielvo", "una stella brilla sull'ora del nostro incontro")


def stella(cx, cy, R, r, fill, rot=0.0):
    pts = []
    for k in range(16):
        a = rot + k * math.pi / 8
        rr = R if k % 4 == 0 else (R * .62 if k % 2 == 0 else r)
        pts.append(f"{cx + rr * math.sin(a):.1f},{cy - rr * math.cos(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def due_stelle():
    """Due stelle a otto raggi intrecciate, d'oro e d'argento, dentro due anelli che si incrociano."""
    return (f'<svg class="stars" viewBox="0 0 200 110" aria-hidden="true">'
            f'<circle cx="78" cy="55" r="44" fill="none" stroke="#b8892f" stroke-width="1.4"/>'
            f'<circle cx="122" cy="55" r="44" fill="none" stroke="#8d95a6" stroke-width="1.4"/>'
            + stella(78, 55, 30, 8, "#c9a04a") + stella(122, 55, 30, 8, "#a9b1c2", math.pi / 8)
            + '<circle cx="78" cy="55" r="3.2" fill="#fff8e6"/><circle cx="122" cy="55" r="3.2" fill="#fff8e6"/></svg>')


CORNER = ('<path d="M4 4 H70 M4 4 V70" stroke="currentColor" stroke-width="1.6" fill="none"/>'
          '<path d="M10 10 H46 M10 10 V46" stroke="currentColor" stroke-width=".9" fill="none" opacity=".7"/>'
          '<path d="M10 10 C30 12 40 22 38 34 C36 44 24 44 24 36 C24 30 31 29 32 34" stroke="currentColor" stroke-width="1.3" fill="none"/>'
          '<path d="M10 10 C12 30 22 40 34 38" stroke="currentColor" stroke-width="1.1" fill="none" opacity=".8"/>'
          '<path d="M10 2 L12.5 7.5 L18 10 L12.5 12.5 L10 18 L7.5 12.5 L2 10 L7.5 7.5Z" fill="currentColor"/>')


def pagina(numero, sposi, pezzi, cat_info, anno, mese, giorno, luogo=None, testimoni=None, dedica=None, firma=None, esempio=False):
    e = html.escape
    per = {'lei': 'per lei', 'lui': 'per lui', 'coppia': 'per la coppia'}
    etichetta = "esempio" if esempio else f"N° {numero}"
    titolo = ("Certificato nuziale di esempio" if esempio else f"Certificato nuziale {numero}") + f" · {sposi[0]} e {sposi[1]}"
    righe = []
    for p in pezzi:
        info = cat_info[p['cat']]
        chips = "".join(f'<li><span class="sw" style="background:{RAINBOW if m == "Colori" else SWATCH.get(m, "#b9b2a2")}"></span><b>{q}×</b>{e(m)}</li>'
                        for q, m in p['recipe'])
        prezzo_unit = f" {p['unit']}" if p.get('unit') else ""
        righe.append(f"""<li class="piece">
        <img src="../img/{e(p['code'])}.jpg" alt="{e(p['name'])}">
        <div>
          <span class="cat">{e(info['name'])} {e(per[info['who']])} · Cod. {e(p['code'])}</span>
          <h3>{e(p['name'])} <i>«{e(p['gloss'])}»</i></h3>
          <p>{e(p['desc'])}</p>
          <small>{e(p['cls'])}</small>
          <ul class="chips">{chips}</ul>
        </div>
      </li>""")
    extra = []
    if luogo:
        extra.append(f'<div><span class="lbl">Luogo</span><span>{e(luogo)}</span></div>')
    if testimoni:
        extra.append(f'<div><span class="lbl">Testimoni</span><span>{e(" e ".join(testimoni))}</span></div>')
    extra_html = f'<div class="facts">{"".join(extra)}</div>' if extra else ''
    ded = (f'<section class="dedica"><span class="lbl">Dedica</span><p>«{e(dedica)}»</p>'
           + (f'<span class="from">{e(firma)}</span>' if firma else '') + '</section>') if dedica else ''
    nota = '<p class="note">Questo è un esempio: nomi, data e pezzi saranno quelli delle nozze vere.</p>' if esempio else ''
    corners = "".join(f'<svg class="corner {k}" viewBox="0 0 80 80" aria-hidden="true">{CORNER}</svg>' for k in ("tl", "tr", "bl", "br"))
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titolo)}</title>
<link rel="icon" type="image/svg+xml" href="../img/icona-stella.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cinzel:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap">
<style>
/* Certificato nuziale: pergamena avorio con fregi d'oro, due stelle intrecciate */
:root{{--bg:#070b17;--paper:#f7f1e4;--paper-2:#efe5cf;--ink:#3b2a10;--muted:#7d6a4c;--gold:#b8892f;--gold-b:#9a6f1e;
  --gild:linear-gradient(180deg,#d9b468 0%,#b8892f 55%,#7a5518 100%);color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;background:var(--bg);color:var(--ink);font-family:"Cormorant Garamond",Georgia,serif;font-size:19px;line-height:1.5;
  padding-block:clamp(16px,4vw,48px);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));
  background-image:radial-gradient(ellipse 70% 50% at 50% 0%,rgba(230,194,122,.14),transparent 70%),
    radial-gradient(1px 1px at 20% 30%,rgba(255,255,255,.25) 50%,transparent 51%),radial-gradient(1.5px 1.5px at 80% 70%,rgba(230,194,122,.35) 50%,transparent 51%);
  background-size:100% 100%,170px 170px,170px 170px}}
.cert{{position:relative;max-width:920px;margin:0 auto;border-radius:20px;overflow:hidden;
  background:radial-gradient(ellipse 90% 60% at 50% 0%,#fffaf0,var(--paper) 60%,var(--paper-2));border:1px solid var(--gold);
  box-shadow:inset 0 0 0 6px var(--paper),inset 0 0 0 7px rgba(184,137,47,.45),0 40px 80px -30px rgba(0,0,0,.95),0 0 60px -20px rgba(230,194,122,.35)}}
.corner{{position:absolute;z-index:3;width:clamp(44px,8vw,72px);color:var(--gold);pointer-events:none}}
.tl{{top:6px;left:6px}}.tr{{top:6px;right:6px;transform:scaleX(-1)}}.bl{{bottom:6px;left:6px;transform:scaleY(-1)}}.br{{bottom:6px;right:6px;transform:scale(-1,-1)}}
.head{{display:flex;flex-direction:column;align-items:center;text-align:center;padding:clamp(34px,6vw,56px) 24px 18px}}
.stars{{width:clamp(130px,24vw,190px);height:auto;filter:drop-shadow(0 2px 4px rgba(122,85,24,.25))}}
.shop{{margin:10px 0 0;font-family:"Cinzel",Georgia,serif;font-size:.78rem;letter-spacing:.26em;text-transform:uppercase;color:var(--muted)}}
h1{{margin:4px 0 2px;font-family:"Cinzel Decorative",Georgia,serif;font-weight:700;font-size:clamp(1.5rem,4.4vw,2.2rem);line-height:1.15;
  background:var(--gild);-webkit-background-clip:text;background-clip:text;color:transparent}}
.quenya{{margin:6px 0 0;font-style:italic;font-size:1.25rem;color:var(--gold-b)}}
.quenya small{{display:block;font-size:1rem;color:var(--muted)}}
.pill{{margin-top:14px;font-family:"Cinzel",Georgia,serif;font-size:.76rem;letter-spacing:.22em;text-transform:uppercase;color:var(--gold-b);
  border:1px solid rgba(184,137,47,.7);border-radius:999px;padding:4px 16px}}
.couple{{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;padding:22px clamp(22px,5vw,52px) 26px;
  border-top:1px solid rgba(184,137,47,.45);border-bottom:1px solid rgba(184,137,47,.45);margin:0 clamp(22px,5vw,52px)}}
.lbl{{font-family:"Cinzel",Georgia,serif;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}}
.names{{display:flex;flex-wrap:wrap;justify-content:center;align-items:baseline;gap:.2em .5em;font-family:"Cinzel Decorative",Georgia,serif;
  font-size:clamp(1.6rem,4.6vw,2.4rem);line-height:1.15;color:var(--ink)}}
.names .e{{font-family:"Cormorant Garamond",Georgia,serif;font-style:italic;font-size:.8em;color:var(--gold)}}
.date{{font-family:"Cinzel",Georgia,serif;font-weight:500;font-size:1rem;letter-spacing:.06em}}
.facts{{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 28px;margin-top:8px}}
.facts div{{display:flex;flex-direction:column;align-items:center}}
.pieces{{padding:26px clamp(22px,5vw,52px) 8px}}
.pieces h2{{margin:0 0 14px;text-align:center;font-family:"Cinzel",Georgia,serif;font-weight:500;font-size:.82rem;letter-spacing:.24em;text-transform:uppercase;color:var(--gold-b)}}
.pieces ol{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:18px}}
.piece{{display:grid;grid-template-columns:110px minmax(0,1fr);gap:18px;align-items:center;padding:14px;border-radius:14px;
  background:rgba(255,255,255,.45);border:1px solid rgba(184,137,47,.35)}}
@media (max-width:520px){{.piece{{grid-template-columns:84px minmax(0,1fr);gap:12px}}}}
.piece img{{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:999px 999px 6px 6px / 70px 70px 6px 6px;border:1px solid rgba(184,137,47,.6)}}
.piece .cat{{font-family:"Cinzel",Georgia,serif;font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-b)}}
.piece h3{{margin:2px 0 0;font-family:"Cinzel Decorative",Georgia,serif;font-weight:400;font-size:1.3rem;line-height:1.2}}
.piece h3 i{{font-family:"Cormorant Garamond",Georgia,serif;font-size:.85em;color:var(--muted)}}
.piece p{{margin:4px 0 0;font-style:italic}}
.piece small{{display:block;margin-top:6px;color:var(--muted)}}
.chips{{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px}}
.chips li{{display:inline-flex;align-items:center;gap:6px;padding:2px 10px 2px 4px;border-radius:999px;border:1px solid rgba(184,137,47,.45);background:#fffaf0;font-size:.95rem}}
.chips b{{font-family:"Cinzel",Georgia,serif;font-size:.78rem;color:var(--gold-b)}}
.sw{{width:16px;height:16px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)}}
.dedica{{margin:22px clamp(22px,5vw,52px) 0;padding:18px 22px;text-align:center;border:1px dashed rgba(184,137,47,.6);border-radius:14px;background:rgba(255,255,255,.4)}}
.dedica p{{margin:4px 0;font-style:italic;font-size:1.3rem}}
.dedica .from{{font-family:"Cinzel Decorative",Georgia,serif;color:var(--gold-b)}}
.foot{{display:flex;flex-direction:column;align-items:center;gap:6px;padding:26px 24px clamp(30px,5vw,44px)}}
.seal{{width:140px;height:auto;filter:drop-shadow(0 8px 12px rgba(80,50,10,.45));transform:rotate(-6deg)}}
.foot span{{font-family:"Cinzel",Georgia,serif;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}}
.foot .num{{font-weight:600;font-size:.84rem;color:var(--gold-b)}}
.note{{margin:0;padding:0 20px 24px;text-align:center;font-style:italic;color:var(--gold-b)}}
</style>
</head>
<body>
<main class="cert">
  {corners}
  <header class="head">
    {due_stelle()}
    <p class="shop">Bottega delle Sette Stelle</p>
    <h1>Certificato Nuziale</h1>
    <p class="quenya">«{e(FRASE[0])}»<small>{e(FRASE[1])}</small></p>
    <span class="pill">{e(etichetta)}</span>
  </header>
  <section class="couple">
    <span class="lbl">Uniti in nozze</span>
    <div class="names"><span>{e(sposi[0])}</span><span class="e">e</span><span>{e(sposi[1])}</span></div>
    <span class="date">Anno {e(anno)} · Mese {e(str(mese))}° · Giorno {e(str(giorno))}°</span>
    {extra_html}
  </section>
  <section class="pieces">
    <h2>I doni delle nozze</h2>
    <ol>{"".join(righe)}</ol>
  </section>
  {ded}
  <footer class="foot">
    <img class="seal" src="../img/sigillo-bottega.png" alt="Sigillo d'oro della Bottega delle Sette Stelle">
    <span class="num">{e(etichetta)}</span>
    <span>sigillo della bottega</span>
  </footer>
  {nota}
</main>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--numero', required=True)
    ap.add_argument('--sposi', nargs=2, required=True)
    ap.add_argument('--codici', nargs='+', required=True)
    ap.add_argument('--anno', required=True)
    ap.add_argument('--mese', required=True)
    ap.add_argument('--giorno', required=True)
    ap.add_argument('--luogo')
    ap.add_argument('--testimoni', nargs='+')
    ap.add_argument('--dedica')
    ap.add_argument('--firma')
    ap.add_argument('--esempio', action='store_true')
    ap.add_argument('--uscita')
    a = ap.parse_args()
    dati = json.loads((BASE / 'pezzi.json').read_text())
    pezzi = [next(p for p in dati['ITEMS'] if p['code'] == c) for c in a.codici]
    out = pathlib.Path(a.uscita) if a.uscita else REPO / 'certificati' / f"{a.numero}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(pagina(a.numero, a.sposi, pezzi, dati['CAT_INFO'], a.anno, a.mese, a.giorno, a.luogo, a.testimoni, a.dedica, a.firma, a.esempio))
    print(out)


if __name__ == '__main__':
    main()
