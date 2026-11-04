"""Genera le due pagine dei certificati «istantanei», usabili senza Claude:
  certificati/c.html      mostra un certificato a partire dai dati nel link (#n=…&c=…&i=…)
  certificati/nuovo.html  modulo per la collaboratrice: sceglie il pezzo, scrive nome e data, ottiene il link
Stessa grafica di strumenti/certificato.py (CSS e fregi presi da lì). Rilanciare dopo aver cambiato certificato.py:
  python3 strumenti/modulo_certificati.py"""
import json, pathlib, sys
BASE = pathlib.Path(__file__).resolve().parent
REPO = BASE.parent
sys.path.insert(0, str(BASE))
import certificato as C

dati = json.loads((BASE / 'pezzi.json').read_text())
campione = next(p for p in dati['ITEMS'] if p['code'] == 'G56')
esempio = C.pagina('000', campione, dati['CAT_INFO'][campione['cat']], 'x', 'I', 1, 1, True, nozze=True, dedica='x', firma='x')
CSS = esempio[esempio.index('<style>') + 7:esempio.index('</style>')]
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Cinzel:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap">'

# Solo i dati che servono al certificato, dentro la pagina (niente file esterni da caricare)
CAMPI = ('code', 'cat', 'name', 'gloss', 'photo', 'metal', 'finish', 'gem', 'cut', 'ct', 'fabric', 'colorName', 'trimName', 'desc', 'excl', 'cls', 'recipe')
PEZZI = {p['code']: {k: p[k] for k in CAMPI if k in p} for p in dati['ITEMS']}
CATS = {k: {'name': v['name'], 'who': v['who']} for k, v in dati['CAT_INFO'].items()}
DATA_JS = 'const PEZZI = ' + json.dumps(PEZZI, ensure_ascii=False, separators=(',', ':')) + ';\nconst CATS = ' + \
          json.dumps(CATS, ensure_ascii=False, separators=(',', ':')) + ';'

RENDER_JS = r"""
const SWATCH = """ + json.dumps(C.SWATCH) + r""", RAINBOW = """ + json.dumps(C.RAINBOW) + r""";
const CORNER = """ + json.dumps(C.CORNER) + r""";
const esc = s => String(s ?? "").replace(/[&<>"']/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#x27;"}[ch]));
/* Dati del certificato -> HTML (stessa struttura di strumenti/certificato.py) */
function certificatoHTML(q){
  const p = PEZZI[q.c]; if(!p) return null;
  const info = CATS[p.cat], per = {lei:"per lei", lui:"per lui", coppia:"· unioni"}[info.who];
  const nozze = q.k === "s", conf = q.k === "c" || nozze, ded = (q.d || "").trim(), firma = (q.f || "").trim();
  const det = p.fabric ? [["Tessuto", p.fabric], ["Colore", p.colorName], ["Ricami", p.trimName]]
    : [["Metallo", p.metal]].concat(p.gem ? [["Pietra", `${p.gem}, taglio ${p.cut}`]].concat(p.ct ? [["Peso", p.ct]] : []) : [["Lavorazione", p.finish]]);
  const ric = p.recipe.concat(conf ? [[1, "Confezione"]] : []);
  const et = `N° ${q.n}`, chi = q.s === "m" ? ["Nériva (Madelyn)", "la bottegaia", "madelyn"] : ["Elrohir", "il bottegaio", "elrohir"];
  const extra = [];
  if(nozze) extra.push(`<div class="box"><img src="../img/confezione-nozze.jpg" alt="La confezione degli sposi: scrigno avorio con fregi e stelle d'oro, interno di velluto blu notte, nastro avorio e blu con sigillo d'oro e cartellino «Agli Sposi · Due cammini, una stessa luce»"><span class="lbl">Confezione degli sposi</span></div>`);
  else if(conf) extra.push(`<div class="box"><img src="../img/${ded ? "confezione.jpg" : "confezione-semplice.jpg"}" alt="La confezione della bottega: scatola color pergamena con fregi d'oro, nastro di velluto blu e sigillo d'oro"><span class="lbl">Confezione</span></div>`);
  if(ded){ const n = ded.length, fs = n <= 60 ? 5.6 : n <= 110 ? 4.7 : n <= 170 ? 3.9 : 3.3;
    extra.push(`<div class="tag" role="img" aria-label="Cartoncino della dedica"><div class="tag-text" style="--fs:${fs}cqw"><span class="lbl">Dedica</span><p class="msg">«${esc(ded)}»</p>${firma ? `<span class="from">${esc(firma)}</span>` : ""}</div></div>`); }
  const head = nozze
    ? `<div class="head nozze-head" role="img" aria-label="Le fedi sulla seta avorio, il sigillo d'oro sul nastro blu e il cartoncino della Bottega delle Sette Stelle"></div>`
    : `<div class="head" role="img" aria-label="La busta della Bottega delle Sette Stelle, chiusa da un nastro di velluto blu e dal sigillo d'oro con la stella"></div>`;
  const corners = ["tl","tr","bl","br"].map(k => `<svg class="corner ${k}" viewBox="0 0 80 80" aria-hidden="true">${CORNER}</svg>`).join("");
  return { titolo: `Certificato ${q.n} · ${p.name}`, cls: "cert" + (nozze ? " avorio" : ""), html: `${corners}${head}
  <header class="title"><h1>Certificato di Proprietà</h1><span class="pill">${esc(et)}</span></header>
  <section class="body">
    <figure class="niche photo"><img src="../img/${esc(p.code)}.jpg" alt="${esc(p.name)}, ${esc(info.name.toLowerCase())} ${per}"><figcaption>Cod. ${esc(p.code)}</figcaption></figure>
    <div>
      <div class="who"><span class="lbl">Intestato a</span><span class="name">${esc(q.i)}</span>
        <span class="date">Anno ${esc(q.a)} · Mese ${esc(q.m)}° · Giorno ${esc(q.g)}°</span></div>
      <div class="item"><h2>${esc(p.name)}</h2><p class="gl">«${esc(p.gloss)}»</p><span class="cat">${esc(info.name)} ${per}</span>
        <dl>${det.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join("")}</dl>
        <p class="desc">${esc(p.desc)}</p>${p.excl ? `<p class="excl">${esc(p.excl)}</p>` : ""}</div>
    </div>
  </section>
  ${extra.length ? `<section class="extras${extra.length === 1 ? " one" : ""}">${extra.join("")}</section>` : ""}
  <footer class="foot">
    <div class="recipe"><h3>Ricetta di creazione</h3><small>${esc(p.cls)}</small>
      <ul>${ric.map(([n, m]) => `<li><span class="sw" style="background:${m === "Colori" ? RAINBOW : (SWATCH[m] || "#9aa3b8")}"></span><b>${n}×</b>${esc(m)}</li>`).join("")}</ul></div>
    <div class="sign"><img class="seal" src="../img/sigillo-bottega.png" alt="Sigillo d'oro della Bottega delle Sette Stelle"><span class="seal-num">${esc(et)}</span>
      <div class="firma"><img src="../img/firma-${chi[2]}-${nozze ? "scura" : "oro"}.png" alt="Firma di ${chi[0]}"><span>${chi[0]} · ${chi[1]}</span></div></div>
  </footer>` };
}
const leggiLink = h => Object.fromEntries(new URLSearchParams(h.replace(/^#/, "")));
"""

C_HTML = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Certificato di Proprietà · Bottega delle Sette Stelle</title>
<link rel="icon" type="image/svg+xml" href="../img/icona-stella.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
<style>{CSS}
.vuoto{{padding:60px 24px;text-align:center;font-style:italic;color:var(--muted)}}
</style>
</head>
<body>
<main class="cert" id="cert"><p class="vuoto">Certificato non trovato: controlla di aver copiato tutto il link.</p></main>
<script>
{DATA_JS}
{RENDER_JS}
function mostra(){{
  const r = certificatoHTML(leggiLink(location.hash)); if(!r) return;
  const m = document.getElementById("cert"); m.className = r.cls; m.innerHTML = r.html; document.title = r.titolo;
}}
mostra(); addEventListener("hashchange", mostra);
</script>
</body>
</html>
"""

NUOVO_HTML = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Nuovo certificato · Bottega delle Sette Stelle</title>
<link rel="icon" type="image/svg+xml" href="../img/icona-stella.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
<style>
:root{{--bg:#070b17;--paper:#0f1731;--paper-2:#131d3b;--gold:#d9b468;--gold-b:#e6c27a;--fg:#ece6d6;--muted:#a9b2cc;--line:rgba(230,194,122,.45);color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;background:var(--bg);color:var(--fg);font-family:"Cormorant Garamond",Georgia,serif;font-size:19px;line-height:1.45;
  padding:clamp(16px,4vw,40px) max(16px,env(safe-area-inset-left,0px)) 60px}}
.wrap{{max-width:640px;margin:0 auto;display:flex;flex-direction:column;gap:22px}}
header{{text-align:center}}
header img{{width:54px;height:54px}}
.shop{{margin:6px 0 0;font-family:"Cinzel",Georgia,serif;font-size:.78rem;letter-spacing:.26em;text-transform:uppercase;color:var(--muted)}}
h1{{margin:2px 0 0;font-family:"Cinzel Decorative",Georgia,serif;font-size:clamp(1.5rem,5vw,2rem);color:var(--gold-b)}}
.intro{{margin:6px 0 0;font-style:italic;color:var(--muted)}}
form,.esito{{background:linear-gradient(180deg,var(--paper-2),var(--paper));border:1px solid var(--line);border-radius:18px;padding:clamp(18px,4vw,28px);display:flex;flex-direction:column;gap:16px}}
label,.campo{{display:flex;flex-direction:column;gap:6px}}
.lbl{{font-family:"Cinzel",Georgia,serif;font-size:.74rem;letter-spacing:.18em;text-transform:uppercase;color:var(--gold)}}
.aiuto{{font-size:.95rem;font-style:italic;color:var(--muted)}}
input,select,textarea{{font:inherit;font-size:1.1rem;color:var(--fg);background:#0a1024;border:1px solid var(--line);border-radius:10px;padding:10px 12px;width:100%}}
input:focus,select:focus,textarea:focus{{outline:2px solid var(--gold);outline-offset:1px}}
.riga{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}
.scelte{{display:flex;flex-direction:column;gap:8px}}
.scelte label{{flex-direction:row;align-items:center;gap:10px;font-size:1.1rem;cursor:pointer}}
.scelte input{{width:22px;height:22px;accent-color:var(--gold)}}
.pezzo-anteprima{{display:flex;gap:14px;align-items:center;padding:10px;border:1px dashed var(--line);border-radius:12px}}
.pezzo-anteprima img{{width:72px;height:96px;object-fit:cover;border-radius:999px 999px 6px 6px / 40px 40px 6px 6px;border:1px solid var(--line)}}
.pezzo-anteprima b{{font-family:"Cinzel Decorative",Georgia,serif;font-weight:400;color:#f4ead0}}
button{{font:inherit;font-family:"Cinzel",Georgia,serif;font-size:.9rem;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;border-radius:999px;padding:12px 20px;
  border:1px solid var(--gold);background:transparent;color:var(--gold-b)}}
button.primo{{background:linear-gradient(180deg,#f0d38f,#c99a45);color:#1a1205;border-color:#f0d38f;font-weight:600}}
button:focus-visible{{outline:2px solid #fff;outline-offset:2px}}
.errore{{margin:0;color:#ffb4a8;font-style:italic}}
.link{{word-break:break-all;font-size:.95rem;background:#0a1024;border:1px solid var(--line);border-radius:10px;padding:10px 12px;color:var(--muted)}}
.bottoni{{display:flex;flex-wrap:wrap;gap:10px}}
.msg-ok{{margin:0;color:#bfe3b0;font-style:italic;min-height:1.4em}}
iframe{{width:100%;height:760px;border:1px solid var(--line);border-radius:14px;background:var(--bg)}}
@media (max-width:520px){{.riga{{grid-template-columns:1fr 1fr 1fr;gap:8px}}iframe{{height:620px}}}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <img src="../img/icona-stella.svg" alt="">
    <p class="shop">Bottega delle Sette Stelle</p>
    <h1>Nuovo certificato</h1>
    <p class="intro">Compila, premi «Crea certificato» e manda il link all'acquirente.</p>
  </header>

  <form id="modulo" novalidate>
    <label><span class="lbl">Numero del certificato</span>
      <input id="numero" inputmode="numeric" autocomplete="off">
      <span class="aiuto">Si propone da solo il numero successivo all'ultimo creato da questo telefono o computer.</span></label>
    <div class="campo"><span class="lbl">Chi crea il certificato</span>
      <div class="scelte">
        <label><input type="radio" name="chi" value=""> Elrohir</label>
        <label><input type="radio" name="chi" value="m"> Nériva (Madelyn)</label>
      </div><span class="aiuto">Sotto il sigillo comparirà la sua firma.</span></div>
    <label><span class="lbl">Pezzo venduto</span>
      <select id="pezzo"></select></label>
    <div class="pezzo-anteprima" id="anteprima" hidden></div>
    <label><span class="lbl">Intestato a</span>
      <input id="intestato" autocomplete="off" placeholder="Nome del personaggio">
      <span class="aiuto">Per le fedi si possono scrivere due nomi: «Nome e Nome».</span></label>
    <div class="campo"><span class="lbl">Data di Lot</span>
      <div class="riga">
        <label><span class="aiuto">Anno</span><input id="anno" autocomplete="off" placeholder="XXV"></label>
        <label><span class="aiuto">Mese</span><input id="mese" inputmode="numeric" autocomplete="off"></label>
        <label><span class="aiuto">Giorno</span><input id="giorno" inputmode="numeric" autocomplete="off"></label>
      </div></div>
    <div class="campo"><span class="lbl">Confezione</span>
      <div class="scelte">
        <label><input type="radio" name="conf" value="" checked> Nessuna</label>
        <label><input type="radio" name="conf" value="c"> Confezione della bottega</label>
        <label><input type="radio" name="conf" value="s"> Confezione degli sposi (fedi e abiti nuziali)</label>
      </div></div>
    <label><span class="lbl">Dedica (facoltativa)</span>
      <textarea id="dedica" rows="2" placeholder="Lascia vuoto se non c'è"></textarea></label>
    <label><span class="lbl">Firma della dedica (facoltativa)</span>
      <input id="firma" autocomplete="off" placeholder="Chi regala"></label>
    <p class="errore" id="errore" role="alert"></p>
    <button class="primo" type="submit">✦ Crea certificato</button>
  </form>

  <section class="esito" id="esito" hidden>
    <span class="lbl">Ecco il link del certificato</span>
    <div class="link" id="link"></div>
    <div class="bottoni">
      <button type="button" class="primo" id="copia">Copia il link</button>
      <button type="button" id="apri">Apri il certificato</button>
    </div>
    <p class="msg-ok" id="ok" role="status"></p>
    <iframe id="vista" title="Anteprima del certificato"></iframe>
    <button type="button" id="altro">Crea un altro certificato</button>
  </section>
</div>
<script>
{DATA_JS}
const $ = id => document.getElementById(id);
const salva = (k, v) => {{ try {{ localStorage.setItem("ss-cert-" + k, v); }} catch(e) {{}} }};
const leggi = k => {{ try {{ return localStorage.getItem("ss-cert-" + k) || ""; }} catch(e) {{ return ""; }} }};
const tre = n => String(n).padStart(3, "0");
function prossimo(){{ const u = parseInt(leggi("ultimo"), 10); $("numero").value = tre(isNaN(u) ? 1 : u + 1); }}
// Elenco dei pezzi, raggruppati per stanza
const gruppi = {{}};
for(const p of Object.values(PEZZI)){{ const c = CATS[p.cat]; const g = c.name + " · " + (c.who === "coppia" ? "coppia" : "per " + c.who); (gruppi[g] = gruppi[g] || []).push(p); }}
$("pezzo").innerHTML = '<option value="">— scegli il pezzo —</option>' + Object.keys(gruppi).sort().map(g =>
  `<optgroup label="${{g}}">` + gruppi[g].map(p => `<option value="${{p.code}}">${{p.code}} · ${{p.name}}</option>`).join("") + "</optgroup>").join("");
$("pezzo").addEventListener("change", () => {{
  const p = PEZZI[$("pezzo").value], a = $("anteprima");
  if(!p){{ a.hidden = true; return; }}
  a.hidden = false; a.innerHTML = `<img src="../img/${{p.code}}.jpg" alt=""><div><b>${{p.name}}</b> <i>«${{p.gloss}}»</i><br><span class="aiuto">${{p.desc}}</span></div>`;
  if(CATS[p.cat].who === "coppia") document.querySelector('input[name=conf][value=s]').checked = true;
}});
function scegliChi(){{ const v = leggi("chi"); document.querySelector(`input[name=chi][value="${{v}}"]`).checked = true; }}
$("anno").value = leggi("anno"); scegliChi(); prossimo();
let ultimoLink = "", ultimo = null;
$("modulo").addEventListener("submit", ev => {{
  ev.preventDefault();
  const q = {{ n: tre(($("numero").value || "").replace(/\\D/g, "") || "0"), c: $("pezzo").value, i: $("intestato").value.trim(),
    a: $("anno").value.trim(), m: $("mese").value.trim(), g: $("giorno").value.trim(),
    k: document.querySelector("input[name=conf]:checked").value, d: $("dedica").value.trim(), f: $("firma").value.trim(), s: document.querySelector("input[name=chi]:checked").value }};
  const manca = [!q.c && "il pezzo", !q.i && "il nome", !(q.a && q.m && q.g) && "la data"].filter(Boolean);
  if(manca.length){{ $("errore").textContent = "Manca " + manca.join(", ") + "."; return; }}
  $("errore").textContent = "";
  const par = new URLSearchParams(); for(const [k, v] of Object.entries(q)) if(v) par.set(k, v);
  ultimoLink = new URL("c.html#" + par.toString(), location.href).href; ultimo = q;
  salva("ultimo", parseInt(q.n, 10)); salva("anno", q.a); salva("chi", q.s);
  $("link").textContent = ultimoLink; $("vista").src = ultimoLink; $("ok").textContent = "";
  $("modulo").hidden = true; $("esito").hidden = false; $("esito").scrollIntoView({{behavior: "smooth"}});
}});
$("copia").addEventListener("click", async () => {{
  try {{ await navigator.clipboard.writeText(ultimoLink); $("ok").textContent = "Link copiato: incollalo nel messaggio all'acquirente."; }}
  catch(e) {{ const r = document.createRange(); r.selectNodeContents($("link")); const s = getSelection(); s.removeAllRanges(); s.addRange(r); $("ok").textContent = "Il link è selezionato: copialo tenendoci il dito sopra (o Ctrl+C)."; }}
}});
$("apri").addEventListener("click", () => window.open(ultimoLink, "_blank"));
$("altro").addEventListener("click", () => {{
  $("modulo").reset(); $("anno").value = leggi("anno"); scegliChi(); prossimo(); $("anteprima").hidden = true;
  $("esito").hidden = true; $("modulo").hidden = false; scrollTo({{top: 0, behavior: "smooth"}});
}});
</script>
</body>
</html>
"""

(REPO / 'certificati' / 'c.html').write_text(C_HTML)
(REPO / 'certificati' / 'nuovo.html').write_text(NUOVO_HTML)
print('certificati/c.html', round(len(C_HTML) / 1024), 'KB · certificati/nuovo.html', round(len(NUOVO_HTML) / 1024), 'KB')
