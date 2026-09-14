# [Značka] — Typografie

> Podle **[název manuálu]**. Písmo [název], náhrada [název]. Řádkování
> [hodnota] je závazné.

## Rodina písma

| Role | Písmo | Řezy | Odkud |
|---|---|---|---|
| Nadpisy a text | [název] | [200–800] | [`fonts/`, licence: …] |
| Náhrada | [Arial / system-ui] | — | když písmo není k dispozici |
| Kód, čísla v tabulkách (volitelné) | [název] | [400] | [odkud] |

### Font stack

```css
--font-sans: '[název]', [náhrada], sans-serif;
```

### Self-hosting

Pro dokumenty ke klientovi písmo vždy z `fonts/fonts.css` (soubory ve složce
`fonts/`), ne z veřejného CDN. Důvod: dokument funguje offline a neposílá
data třetí straně.

## Závazná pravidla z manuálu

### 1. Poměry velikostí

| Dvojice | Poměr | Příklad |
|---|---|---|
| nadpis : text | [5:2] | [40 px : 16 px] |
| podnadpis : text | [3:2] | [24 px : 16 px] |

### 2. Řádkování

- Text: [1,5]
- Nadpisy: [1,1–1,2]

### 3. Hierarchie kontrastem řezů

- Dvojice pro nadpis / text: [Bold / Regular] nebo [SemiBold / Light].
- Nikdy [dva podobné řezy vedle sebe].

## Velikostní škála pro HTML dokumenty

| Úroveň | Velikost | Řez | Řádkování |
|---|---|---|---|
| H1 | [px] | [700] | [1,1] |
| H2 | [px] | [600] | [1,2] |
| H3 | [px] | [600] | [1,3] |
| Text | [px] | [400] | [1,5] |
| Popisek | [px] | [400] | [1,4] |

## Tracking (letter-spacing)

- Nadpisy: [−0,02em]
- Verzálky (štítky): [+0,08em]

## Vzory

### Titulní strana

[Jak vypadá titul: velikost nadpisu, barva, umístění, co pod ním.]

### Obsahová strana

[Nadpis, perex, tělo; kolik textu na stranu maximálně.]
