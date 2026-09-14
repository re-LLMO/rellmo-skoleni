# 12 — Z HTML reportu PDF

Většina výstupů z pluginů re:LLMO je HTML — otevře se v prohlížeči, dá se
v něm hledat a klikat. Do mailu ale často potřebuješ PDF.

## Postup

1. **Řekni Claudovi rovnou při tvorbě**, že to má být i na tisk: formát A4,
   okraje, zalomení stránek (`page-break-before`, `break-inside: avoid`),
   tiskové CSS (`@media print`). Když to řekneš až potom, přesazuje se to
   znovu.
2. Otevři HTML v prohlížeči (Chrome, Edge, Safari).
3. Tisk — Cmd+P nebo Ctrl+P.
4. V dialogu vyber **Cíl → Uložit jako PDF**.

Vznikne soubor, který se dá poslat mailem. Žádný hosting není potřeba.

## Kdy to nedělat

- Když potřebuješ interaktivní výstup — filtrování, řazení, rozklikávací
  detaily. To se do PDF nepřenese; pošli rovnou HTML soubor.
- Když report obsahuje data, která nemají opustit firmu. HTML s klientskými
  daty nikam nenahrávej; pošli ho jako přílohu.

## Drobnosti, které to zlepší

- Řekni si o **hlavičku a patičku s číslem stránky** — v tiskovém CSS to jde.
- Grafy vykreslené na plátně (canvas) se někdy netisknou. Když se to stane,
  nech si je vygenerovat jako SVG.
- Barevná pozadí prohlížeč ve výchozím stavu netiskne. V tiskovém dialogu
  je potřeba zapnout „tisknout pozadí".
