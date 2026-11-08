#!/usr/bin/env python3
"""Arma la app a partir de src/.

- index.html        → con src/powers_data.js (versión pública: nombres y páginas, sin el texto del libro).
- index.local.html  → sólo si existe fuentes/powers_data_full.js (con las descripciones completas).
                      Está en .gitignore: nunca se sube.
"""
from pathlib import Path
root = Path(__file__).resolve().parent
t = (root / 'src' / 'template.html').read_text(encoding='utf-8')
assert '/*DATA*/' in t, 'falta el marcador /*DATA*/ en src/template.html'

def build(data_file, out):
    (root / out).write_text(t.replace('/*DATA*/', data_file.read_text(encoding='utf-8')), encoding='utf-8')
    print(f'{out} listo')

build(root / 'src' / 'powers_data.js', 'index.html')
full = root / 'fuentes' / 'powers_data_full.js'
if full.exists():
    build(full, 'index.local.html')
else:
    print('(sin fuentes/powers_data_full.js: no se arma index.local.html)')
