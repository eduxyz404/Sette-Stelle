# Bottega delle Sette Stelle · riassunto per riprendere il lavoro

## Chi e cosa
- Utente: Erika. **Rispondere sempre in italiano.** Nelle interfacce in inglese (GitHub ecc.) tradurre anche i pulsanti.
- Sito di una bottega per il gioco di ruolo **ExtremeLot**: *Bottega delle Sette Stelle* (nome elfico **Valacirca**), bottegaio **Elrohir** (il suo nome non è il nome della bottega). Aperta a tutte le razze.
- Classi per l'Universitas: **Monili, Tessuti, Oggettistica**. Niente cosmetici, **niente pelle/cuoio** (il bottegaio è vegetariano): cinture, fasce, trecce descritte come **cotone**; stivali/sandali sempre «non inclusi».

## Dove sta
- Sito pubblico: https://eduxyz404.github.io/Sette-Stelle/ (repo `eduxyz404/Sette-Stelle`, GitHub Pages). Push come Claude, con le righe di attribuzione.
- Anteprima su claude.ai (artifact): https://claude.ai/artifact/Cge1dy1uSoSp4gnhpSvB9G — per aggiornarla: `python3 strumenti/anteprima.py anteprima.html`, poi pubblicare quel file passando l'URL dell'artifact (prima leggerlo con l'azione read). Limite 16 MB.
- **La fonte è `index.html` nel repo.** Foto dei pezzi in `img/CODICE.jpg`; originali senza sigillo in `originali/CODICE.jpg`.

## Stile
- Blu notte e oro, titoli Cinzel Decorative; font Bellavoir Delight solo per il titolo di copertina e i titoli dei banner. Stella noldor a otto raggi (anche icona della scheda: `img/icona-stella.svg`, senza cerchio).
- **Nomi dei pezzi in quenya** (mai sindarin), con traduzione tra «».
- **Descrizioni brevissime**, una riga (~60 caratteri). Eventuale nota «… non inclusi» in oro. Negli abiti da cerimonia il tema è un'etichetta (`tema:"mare"` → «✦ TEMA MARE»).

## Ricette (regole ExtremeLot, semplici)
- Solo **cotone** (niente seta, niente lana), **1× Colori** per le tinte, **un metallo** (Oro o Argento) per ricami/fibbie.
- **Niente pietre preziose**: al loro posto **Cristallo** (+ Colori se è colorato).
- Esempi: abito da cerimonia 4× Cotone · 1× Colori · 1× Oro/Argento; abito semplice 3× Cotone · 1× Colori; anello senza pietra 1× Argento; bracciale 2× metallo + 1× altro (senza pietra 3× Argento); collana 2×+1×.

## Stanze (cat → stanza)
- **Per lui** · Monili: Anelli, Collane, Bracciali, Cerchi (diademi maschili: linee dritte, metallo brunito, niente pendenti; primo: Aran G54) · Tessuti: Mantelli, Completi, Toghe, Tuniche, Cerimonia, Accessori (cinture e borse di stoffa).
- **Per lei** · Monili: Diademi, Collane, Orecchini, Bracciali · Tessuti: Mantelli, Abiti, Completi, Accessori (borse di stoffa), Cerimonia.
- **Per la coppia** · Monili: Fedi (avorio: Veru G55, Melmë G56, Vanimelda G58 argento, Yúyo G59, Oialë G60 argento, Melda G65, Anarya G67, Anga G68 ferro brunito + oro; tolta Elenya G66, gemella d'argento di Anarya, foto ancora in originali/), Fedine (verde: Órë G57, Indis G61, Olassië G62, Rilya G63, Tintila G64, Angaina G69 ferro + argento); prezzi «la coppia». Nel sito si chiama **«Coppia»** (non «lui e lei»: vale per ogni coppia): voce nel menu in alto, colonna nel menu delle stanze e terza sala nell'elenco delle stanze (foto di Melmë). Indirizzi #coppia, #coppia-fedi, #coppia-fedine.
- Le stanze vuote non compaiono. «Fermagli per lui» è stato tolto. Tolti tutti i pezzi senza foto vera (disegni).
- Temi della Cerimonia: stelle, mare, bosco, aria, notte d'oriente, fuoco, tenebra, sposo. Elenwë (A74) è senza tema.
- Codici: A = tessuti (ultimo A104), G = monili (ultimo G69). A72 non esiste più.
- I mantelli (Kemen, Mornië, Calma) sono «trattati a cera: respingono l'acqua» (+1× Cera in ricetta).
- Regola dei Tessuti (ricettario): vietati abiti di taglio/stile moderno, cerniere, stampe moderne. Pezzi un po' a rischio: Yávië (A76), Verno (A67), Luinil (A77) — Erika li tiene per ora.

## Foto «indossato»
- Facoltativa, per ogni pezzo: salvare l'originale in `originali/CODICE-indossato.jpg`, `python3 strumenti/rifai_foto.py CODICE-indossato`, poi aggiungere `CODICE:"img/CODICE-indossato.jpg?v=…"` in `WORN` (subito sotto `PHOTOS`) dentro `index.html`. Nella scheda compare il pulsante «✦ indossato» che scambia la foto; l'ingrandimento mostra quella che si sta guardando.
- Attenzione: l'anteprima claude.ai ora supera i 16 MB (16,7): va ridotta (foto più piccole o qualità più bassa in `anteprima.py`) prima di ripubblicarla.

## Parure
- Oggetto `PARURE` in `index.html` (chiave → nome, descrizione, per chi). I pezzi con `parure:"chiave"` mostrano «✦ fa parte della Parure … · vedi tutti i pezzi» che porta a `#parure-chiave` (vista con i pezzi insieme e il prezzo totale; campi facoltativi `di:` per la frase «fa parte dei …» e `tipo:"collezione"` per l'etichetta; con `prezzo:` nella parure compare lo sconto, Silmë 5400 invece di 6000).

## Foto
- Formato 900×1200 (3:4), bordi riempiti **a specchio** (mai stirati), **sigillo** sempre nello stesso punto, poi un po' di **nitidezza**. **Nessuna levigatura**: a Erika le foto levigate sembrano rovinate/di cera.
- Luce più neutra (meno arancione) solo dove chiesto: Completi, Toghe, Mantelli, temi bosco/fuoco; correzione più forte sulla notte d'oriente.
- Strumento: `python3 strumenti/rifai_foto.py CODICE` rifà la foto da `originali/`. Per un pezzo nuovo: salvare l'originale in `originali/CODICE.jpg`, lanciare lo strumento, aggiungere la voce in `ITEMS` e la riga `CODICE:"img/CODICE.jpg?v=…"` in `PHOTOS` dentro `index.html`.
- Quasi tutte le foto degli abiti sono state rifatte **con Gemini** in versione realistica (elenco in `originali/realistiche.txt`: su queste non si applica la correzione della luce). Ne restano alcune originali per scelta (es. Carnil A31, Ilmen A32, Elenwë, Nessë, Lómëwen, Tindómiel, Morion, Vesta, Calion, Lómendil, Nárië, Nárwen, Ruinë, Úrion, Elenindis).
- Per sostituire una foto: salvare il nuovo originale in `originali/CODICE.jpg`, aggiungere il codice a `originali/realistiche.txt`, `python3 strumenti/rifai_foto.py CODICE`, aggiornare `?v=` del codice in `PHOTOS` dentro `index.html`.
- Trucchi per Gemini: una foto per richiesta, conversazione nuova ogni 4–5 immagini; chiedere «fotografia vera di un servizio di moda, reflex 85mm, niente effetti cinematografici, proporzioni corrette»; se ricopia l'originale senza cambiare, **cambiare ambientazione** (castello/chiostro di pietra con luce naturale, torre con telescopio…).

## Effetti del sito
- Quando si mette un pezzo nello scrigno parte una **stella cadente** con scia di polvere di stelle dal pulsante allo scrigno (funzione `stellaCadente`; disattivata con «riduci movimento»).
- Pulsante dello **scrigno** (in basso a destra): due scie di stella che girano intorno **solo a scrigno vuoto** e per ~2,6 s quando si aggiunge un pezzo (classe `gira`); con pezzi dentro restano ferme e invisibili, con un alone dorato; etichetta «Lo scrigno — metti da parte i pezzi che ti piacciono e copia l'ordine» che sparisce dopo il primo uso.
- **Ingresso**: due scie di stella che percorrono la cornice dell'arco (mosse da JavaScript, non solo CSS: in Brave l'animazione CSS non partiva). La «polvere di stelle» sul titolo è stata tolta (3/11): il titolo resta fermo.
- Icona della scheda: `img/icona-stella.svg` (stella senza cerchio).
- Anteprima claude.ai: `python3 strumenti/anteprima.py anteprima.html` (foto 540×720 per stare sotto 16 MB).
- Se GitHub Pages fallisce la pubblicazione (errore «Failed to get ID Token»), basta un nuovo commit/push.

## Certificati
- Ogni certificato porta la **firma di Elrohir** (font **Heleny**), piccola sotto il sigillo: `img/firma-elrohir-oro.png` sul blu, `img/firma-elrohir-scura.png` sull'avorio degli sposi, con la scritta «Elrohir · il bottegaio».
- Niente certificati nuziali: la bottega non celebra nozze, rilascia solo certificati di proprietà. Al loro posto c'è la **confezione degli sposi** (`img/confezione-nozze.jpg`): opzione `--nozze` di `certificato.py` (mette 1× Confezione in ricetta e mostra lo scrigno avorio «Agli Sposi»). Con --nozze il certificato è in versione avorio (colori chiari) con le fedi e il cartoncino della bottega in testa (`img/testata-sposi.jpg`). Esempio: `certificati/esempio-sposi.html`. Nel sito la sezione Coppia ha l'etichetta «unioni».
- `python3 strumenti/certificato.py --numero 001 --codice A01 --intestato "Nome PG" --anno XXV --mese 2 --giorno 10 [--confezione] [--dedica "…" --firma "…"]` (legge `strumenti/pezzi.json`, che si rigenera con `node strumenti/estrai_pezzi.js`). Registro in `certificati/registro.md`. I certificati li gestisce Erika tramite Claude.

## Da fare, quando lo chiede lei
- Gioielli per lei: Diademi, Collane, Orecchini. Prima parure: **Silmë** (G40 diadema, G41 Tintallë ciondolo, G42 Rossë orecchini, G43 Laurë bracciale), «alla maniera dei Silmarilli», foto su velluto blu al banco dell'orafo. Mancano anelli per lei. Diademi preziosi: Elentári (G44, oro, sette stelle di cristallo, tema stelle) e la sua versione sottile Tingilya (G53). Collezione **Diademi degli Elementi**: Nár G45 fuoco, Nén G46 acqua, Súlë G47 aria, Arda G48 terra (4000 l'uno, tutti insieme 14000 invece di 16000; ognuno ha il tema della Cerimonia abbinato). Versione sottile, collezione **Cerchietti degli Elementi**: Uryë G49, Sírë G50, Hwesta G51, Tasarë G52 (1200 l'uno, insieme 4200 invece di 4800).
- **Pelletteria**: Erika la vorrebbe. Su Lot esiste la classe «Articoli in Pelle» (borse, scarsella, sacca, otre, stivali, scarpe, guanti, cappello, cappuccio, gilet, coprispalle, manto, completi, cintola, falconeria); potrebbe sostituire «Oggettistica» (oggi vuota). Problema: Elrohir è vegetariano. Idee proposte: un **aiutante pellettiere** che lavora la pelle al posto suo; pelli solo «recuperate»; oppure «tela cerata» (cotone + Cera + Colori, da far approvare all'Universitas). Decisione ancora aperta.
- Classi: massimo 3 per bottega (ora Monili, Tessuti, Oggettistica).
- Eventuale ritaratura dei prezzi (ora 400–5200 monete).
- Lettera all'Universitas della Mercanzia (servono titolare, aiutante, sede).
