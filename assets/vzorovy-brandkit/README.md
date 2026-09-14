# [Značka] — Brandkit

Brandkit je složka souborů, ve které je značka popsaná tak, aby ji uměl použít
člověk i model: barvy, písmo, logo, pravidla a hotové CSS proměnné. Skill se
značkou (viz `assets/vzorovy-skill/`) na tuhle složku jen odkazuje — nic
z ní neopisuje. Když se značka změní, mění se jeden soubor tady.

Všechno v hranatých závorkách je k doplnění. Soubory, které pro tvou značku
nedávají smysl, smaž — prázdný soubor je horší než žádný.

## Obsah

| Soubor | Co v něm je |
|---|---|
| `colors.md` | paleta, co je hlavní a co vedlejší, co značka NENÍ |
| `typography.md` | písmo, řezy, poměry velikostí, řádkování |
| `logo.md` | varianty loga, kdy kterou, ochranná zóna, zakázané úpravy |
| `brand-identity.md` | claim, hodnoty, tón, vizuální systém (cover, obsah, karty, CTA) |
| `tokens.css` | totéž jako CSS proměnné — HTML dokumenty je jen načtou |
| `corrections.md` | co se změnilo po ověření proti manuálu |
| `fonts/` | písmo k self-hostingu + `fonts.css` |
| `logo/` | soubory loga (SVG/PNG) ve všech oficiálních variantách |
| `examples/` | jeden až dva hotové výstupy, podle kterých se pozná „správně" |

## Odkud se plní

1. **Oficiální brand manuál** (PDF od grafika). Zdroj pravdy. Když něco
   v manuálu není, do brandkitu to nepatří jako pravidlo, nanejvýš jako
   poznámka „používá se, ale manuál to neřeší".
2. **Reálné výstupy** (master prezentace, web, poslední tři nabídky).
   Ukazují, jak se manuál používá v praxi — a kde se od něj odchyluje.
3. **Lidé**, kteří značku hlídají. Tři otázky: co je nejčastější chyba,
   co nikdy, co je nedotknutelné.

Postup krok za krokem je v návodu 19 pluginu školení.

## Rychlý přehled

Vyplň, až budou hotové ostatní soubory — je to souhrn, ne zdroj.

- **Hlavní barva:** `[#hex]` — [kde musí dominovat]
- **Barva pro akci (CTA):** `[#hex]` — [pravidlo]
- **Písmo:** [název] (náhrada [název]), řezy [rozsah]
- **Řádkování:** [hodnota]
- **Logo:** [tvar, počet oficiálních variant]
- **Claim:** „[claim]"
- **Tón:** [dvě slova]
- **Jazyk výstupů:** [čeština]
