# [Značka] — Barvy

> Podle **[název manuálu, verze, datum]**. Hlavní barvy: [výčet]. Která
> z nich musí v návrzích dominovat: [barva].

## Hlavní paleta (oficiální)

| Název | CSS proměnná | HEX | RGB | Použití |
|---|---|---|---|---|
| **[Název 1]** | `--color-primary` | `[#hex]` | `[r/g/b]` | [kde: cover, pozadí, zvýraznění] |
| **[Název 2]** | `--color-cta` | `[#hex]` | `[r/g/b]` | [např. výhradně tlačítka a výzvy k akci] |
| **Bílá** | `--color-white` | `#FFFFFF` | `255/255/255` | pozadí, text na tmavé ploše |

## Vedlejší paleta

> Napiš, k čemu vedlejší barvy JSOU a k čemu NEJSOU. Nejčastější chyba
> je použít odstín určený pro grafy jako akcent v rozhraní.

| Název | CSS proměnná | HEX | Použití |
|---|---|---|---|
| [Název] | `--color-secondary-1` | `[#hex]` | [jen segmenty grafů] |
| [Název] | `--color-secondary-2` | `[#hex]` | [jemné výplně] |

## Co NENÍ brand barva

- `[#hex]` — [kde se omylem objevuje a proč nepatří do palety]
- Žádné [zelené / oranžové / …] mimo data v grafech.
- Stavy v datech (růst / pokles) řeš [jak], ne novou barvou.

## Systémové barvy (rozhraní dokumentů)

| Kontext | Proměnná | Světlý režim | Tmavý režim |
|---|---|---|---|
| Pozadí | `--color-bg` | `[#hex]` | `[#hex]` |
| Text | `--color-text` | `[#hex]` | `[#hex]` |
| Tlumený text | `--color-muted` | `[#hex]` | `[#hex]` |
| Linka | `--color-border` | `[#hex]` | `[#hex]` |

## Pravidla použití (z manuálu)

- [Hlavní barva vyplňuje úvodní strany.]
- [CTA je vždy v barvě X, nikdy v hlavní.]
- [Text na hlavní barvě je vždy bílý.]
- [Barvy se nemíchají do gradientů, kromě: …]
