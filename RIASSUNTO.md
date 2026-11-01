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
- **Per lui** · Monili: Anelli, Collane, Bracciali · Tessuti: Mantelli, Completi, Toghe, Cerimonia, Accessori (cinture).
- **Per lei** · Tessuti: Mantelli, Abiti, Completi, Cerimonia. (Per lei non ci sono ancora gioielli.)
- Le stanze vuote non compaiono. «Fermagli per lui» e «Coppie» sono stati tolti. Tolti tutti i pezzi senza foto vera (disegni).
- Temi della Cerimonia: stelle, mare, bosco, aria, notte d'oriente, fuoco, tenebra, sposo. Elenwë (A74) è senza tema.
- Codici: A = tessuti (ultimo A80), G = monili (ultimo G36). A72 non esiste più.

## Foto
- Formato 900×1200 (3:4), bordi riempiti **a specchio** (mai stirati), **sigillo** sempre nello stesso punto, poi un po' di **nitidezza**. **Nessuna levigatura**: a Erika le foto levigate sembrano rovinate/di cera.
- Luce più neutra (meno arancione) solo dove chiesto: Completi, Toghe, Mantelli, temi bosco/fuoco; correzione più forte sulla notte d'oriente.
- Strumento: `python3 strumenti/rifai_foto.py CODICE` rifà la foto da `originali/`. Per un pezzo nuovo: salvare l'originale in `originali/CODICE.jpg`, lanciare lo strumento, aggiungere la voce in `ITEMS` e la riga `CODICE:"img/CODICE.jpg?v=…"` in `PHOTOS` dentro `index.html`.
- In corso: Erika rifà con ChatGPT 31 foto che sembrano disegni/3D (A13–A23, A58–A70, A71–A80), per renderle realistiche. Quando le manda con il codice, vanno messe al posto delle vecchie (stesso nome, stesso testo).

## Certificati
- `python3 strumenti/certificato.py --numero 001 --codice A01 --intestato "Nome PG" --anno XXV --mese 2 --giorno 10 [--confezione] [--dedica "…" --firma "…"]` (legge `strumenti/pezzi.json`, che si rigenera con `node strumenti/estrai_pezzi.js`). Registro in `certificati/registro.md`. I certificati li gestisce Erika tramite Claude.

## Da fare, quando lo chiede lei
- Gioielli per lei e coppie (servono foto).
- Eventuale ritaratura dei prezzi (ora 400–5200 monete).
- Lettera all'Universitas della Mercanzia (servono titolare, aiutante, sede).
