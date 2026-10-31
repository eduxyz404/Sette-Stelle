# Bottega delle Sette Stelle (Valacirca)

Vetrina della bottega di gioielli e abiti in stile elfico noldor, per il gioco di ruolo Extremelot.

Il sito è tutto in `index.html`, con le immagini già incluse.

## Certificati di proprietà

Per ogni vendita si genera una pagina in `certificati/` con:

    node strumenti/estrai_pezzi.js
    python3 strumenti/certificato.py --numero 001 --codice A01 --intestato "Nome PG" --anno XXV --mese 2 --giorno 10 [--confezione]

e si aggiunge una riga a `certificati/registro.md`. Le immagini dei pezzi sono in `img/`, una per codice.
