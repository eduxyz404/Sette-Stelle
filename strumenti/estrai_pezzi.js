// Estrae ITEMS e CAT_INFO dal sito e li salva in JSON per i certificati
const fs = require('fs');
const s = fs.readFileSync(require('path').join(__dirname, '..', 'index.html'), 'utf8');
const js = s.slice(s.indexOf('const ITEMS = ['), s.indexOf('const KINDS = {'));
const out = new Function(js + '; return {ITEMS, CAT_INFO};')();
fs.writeFileSync(require('path').join(__dirname, 'pezzi.json'), JSON.stringify(out, null, 1));
console.log(out.ITEMS.length, 'pezzi');
