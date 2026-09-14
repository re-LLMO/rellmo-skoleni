# [Značka] — Logo

> Podle **[název manuálu, strany]**.

## Rodiny značek

| Značka | Co to je | Kdy |
|---|---|---|
| Logo | [celé slovo / symbol + slovo] | hlavička dokumentu, titulní strana, patička |
| Logotyp / symbol | [zkrácená verze] | profilové fotky, favicon, malé plochy |
| Odvozené prvky | [uvozovky, linka, vzor] | [k čemu] |

## Soubory v `logo/`

| Soubor | Varianta | Pozadí |
|---|---|---|
| `logo-[barva].svg` | [hlavní barva] | bílé |
| `logo-white.svg` | bílá | [hlavní barva, tmavé] |
| `logo-black.svg` | černá | světlé, tisk černobíle |
| `mark-[barva].svg` | symbol | [kde] |

SVG vždy, když existuje. PNG jen tam, kde SVG nejde vložit (některé
e-mailové klienty, prezentace v cizím nástroji).

## Rozhodovací strom — kterou variantu použít

1. Na bílém pozadí → `[hlavní barva]`.
2. Na ploše v hlavní barvě → `bílá`.
3. Na fotografii → `bílá` s [tmavým překryvem], nikdy barevná.
4. Černobílý tisk → `černá`.
5. Plocha menší než [40 px / 5 mm] → symbol, ne celé logo.

## Minimální velikosti

- Logo: [5 mm tisk / 40 px web]
- Symbol: [3 mm tisk / 26 px web]

## Ochranná zóna

[Např. výška písmene „x" v logu na všech stranách; do zóny nepatří žádný
grafický prvek ani text.]

## Zakázané úpravy

- deformace (roztažení, stlačení)
- otáčení
- obrys místo výplně
- jiná než oficiální barva
- stín, přechod, průhlednost
- logo na nedostatečně kontrastním pozadí
- [další z manuálu]

## HTML implementace

```html
<!-- hlavička dokumentu, bílé pozadí -->
<img src="logo/logo-[barva].svg" alt="[Značka]" height="[32]">

<!-- titulní strana v hlavní barvě -->
<img src="logo/logo-white.svg" alt="[Značka]" height="[40]">
```

## Náhrada textem — kdy je v pořádku

Jen tam, kde nejde vložit obrázek (prostý text, předmět e-mailu). Tvar:
`[značka]` [malými písmeny / jak píše manuál].
