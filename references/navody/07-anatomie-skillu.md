# 07 — Anatomie skillu

Jak má vypadat skill, který se spouští, když má, a dělá, co má.

## Struktura složek

```
muj-skill/
├── SKILL.md          povinný, orchestrace, pod 500 řádků
├── references/       metodika a znalosti, načtou se na vyžádání
├── scripts/          deterministická práce: parsování, výpočty, zápis
└── assets/           šablony, ukázková data, obrázky
```

Když z toho děláš plugin, přibude `.claude-plugin/plugin.json` a `README.md`
v kořeni pluginu. **README nikdy nedávej dovnitř složky se skillem** — patří
do kořene.

## Pojmenování

Složky **kebab-case**, malými písmeny. Názvy souborů rozlišují velikost
písmen: `SKILL.md` přesně takhle, ne `Skill.md`.

| Správně | Vyhni se |
|---|---|
| `analyza-kanibalizace/` | `Analýza Kanibalizace`, `analyza_kanibalizace` |
| `SKILL.md` | `SKILL.MD`, `skill.md` |
| vlastní jméno | prefixy `claude-`, `anthropic-` (jsou rezervované) |

## Frontmatter

```yaml
---
name: analyza-kanibalizace
description: Najde dvojice stránek, které si konkurují na stejném dotazu…
license: LicenseRef-Firma-Interni
allowed-tools: Bash(python3:*), Read, Write, Edit
metadata:
  author: Jméno Příjmení
  version: 1.0.0
  category: marketing
---
```

`allowed-tools` **není bezpečnostní opatření.** Je to seznam toho, co se
nemusí odklikávat, ne omezení toho, co skill smí.

## Popis (`description`) je jediný spouštěč

Tohle je nejdůležitější řádek celého skillu. Model podle něj rozhoduje,
jestli skill spustit. **Není to shrnutí, je to rozhodovací věta.**

- Vejde se do 1 024 znaků. Ve výpisech je vidět zhruba prvních 250 —
  spouštěcí fráze musí být v nich.
- Osvědčená stavba: **co to dělá + kdy to použít + jak to lidi říkají**.
  Konkrétní věty, kterými o té práci mluví tvoji kolegové, fungují líp než
  obecný popis schopností.
- Kde hrozí záměna, přidej vylučovací větu: „Nepoužívej na …".

Špatně: *„Nástroj pro práci s klíčovými slovy."*
Lépe: *„Najde dvojice stránek, které si na stejném dotazu konkurují, a řekne,
kterou z nich posílit a kterou přesměrovat. Použij, když uživatel řekne
'kanibalizace', 'stránky si berou pozice' nebo 'proč mi kolísá pozice'."*

**Jak si to ověřit:** zeptej se Clauda „Kdy bys použil skill X?" Z odpovědi
poznáš, na co ten popis reálně zabírá.

## Styl těla: instrukce, ne role

Piš rozkazovací způsob, ne popis osobnosti.

| Anti-vzor | Lépe |
|---|---|
| „Jsi zkušený SEO konzultant…" | „Projdi dotazy po jednom a vyřaď brandové." |
| „Měl bys nejdřív načíst data." | „Nejdřív načti data." |

Popis role spustí hraní role. Rozkaz spustí postup.

## Tři vrstvy načítání

| Vrstva | Co se načte | Kdy |
|---|---|---|
| vždy | jen `name` a `description`, řádově sto tokenů na skill | při startu |
| při spuštění | celé tělo `SKILL.md` | když skill sedne |
| na vyžádání | `references/`, `scripts/`, `assets/` | když si o ně tělo řekne |

Proto můžeš mít sto skillů a model se nezahltí. A proto je délka `SKILL.md`
skutečný limit — načítá se celé.

Odkazy do `references/` drž **jednu úroveň hluboko**. Reference, která
odkazuje na další referenci, se nepřečte.

## Co kam patří

| Místo | Obsah |
|---|---|
| tělo `SKILL.md` | postup, rozhodování, co dělat v jakém pořadí |
| `references/` | metodika, doménové znalosti, tabulky, na které se odkazuje |
| `scripts/` | mechanická práce: parsování, výpočet, čtení a zápis souborů |
| `assets/` | šablony, ukázková data, loga, fonty |

Dvě pravidla, která se vyplatí: **výpočet nikdy v promptu** a **velké soubory
nikdy přes MCP**. Obojí patří do skriptu, jehož výsledek model teprve uvidí.

## Kolik volnosti dát

Podle toho, jak křehký ten úkol je:

- **Úzký most** — jedna správná cesta, krok za krokem, žádná volnost.
  Vhodné tam, kde odchylka znamená chybu (napojení přístupů, výpočet).
- **Široká cesta** — daný směr a mantinely, cesta na modelu. Většina
  analytických skillů.
- **Otevřené pole** — jen cíl a kritéria. Tvůrčí práce.

Špatně zvolená míra se pozná: příliš úzký skill se hádá se situací, kterou
autor nepředvídal; příliš volný pokaždé dopadne jinak.

## Špatný skill není neutrální

Skill, který se spouští, když nemá, aktivně škodí — přebíjí to, co by model
udělal správně sám. Když si nejsi jistý, jestli skill pomůže, zúž jeho popis,
ne rozšiř.
