# 16 — Reporty z více zdrojů a brandkit jako skill

Pravidelný report je nejčastější kandidát na automatizaci: stejné zdroje,
stejný tvar, jiná čísla. Postup má tři vrstvy a každá patří jinam.

## Tři vrstvy

| Vrstva | Kdo | Kam patří | Proč |
|---|---|---|---|
| Stáhnout a sečíst | skript | `scripts/` | stejný vstup, vždy stejný výstup; deset tisíc řádků skript nerozhodí; model dostane hotová čísla |
| Vyložit | model | tělo `SKILL.md` | příčiny, souvislosti, doporučení — na to je model, ne na aritmetiku |
| Vyrobit dokument | skill se značkou | samostatný skill | barvy, font, logo, pravidla — jednou napsané, celý tým používá totéž |

**Čísla počítá skript, model je vykládá.** Model aritmetiku odhaduje; u
čísel v reportu ke klientovi to nestačí. Proto mají pluginy re:LLMO složku
`scripts/` a model vidí až výsledek.

## Zdroje a jak se k nim dostat

| Zdroj | Cesta | Poznámka |
|---|---|---|
| Search Console | skript s přihlášením bez Cloud Console (návod 05) | dotazy, stránky, kliky, imprese |
| GA4 | MCP server nebo API přes servisní účet | chování na webu, konverze |
| Reklamní účty (Google Ads, Sklik, Meta) | MCP server, když existuje; jinak API | výdaje, konverze, CPC |
| Interní systém (CRM, e-shop) | API → vlastní MCP server nebo skript | když má API, stačí to (návod 03) |
| Cokoli bez API | export CSV/XLSX jako vstup skillu | nejlevnější cesta, když se report dělá jednou měsíčně |

Rozhodnutí MCP versus skript je v návodu 09. Pro pravidelný report obvykle
vyhraje skript: postup znáš, objem je velký, výsledek má být pokaždé stejný.

## Klíče

Klíč k API nikdy do skriptu ani do `SKILL.md`. Patří do proměnné prostředí
nebo do `.env`, který je v `.gitignore`. Skript ho čte z prostředí; kolega,
který skill dostane, si nastaví svůj. Podrobně v návodu 09.

## Brandkit jako skill

Skill, který zná firemní značku a umí v ní vyrobit dokument, je nejjednodušší
skill, jaký si postavíš — a použije ho každý report i prezentace. Co kam:

- **`SKILL.md`** — barvy (hex), název fontu, pár pravidel, která platí vždy
  („nikdy nepoužívej vykřičníky", „tykáme"). Krátké, čte se pokaždé.
- **`references/znacka.md`** — delší pravidla tónu, celý manuál. Načte se, až
  když se píše text ven.
- **`assets/`** — logo (SVG/PNG), šablona HTML, fonty. Binární věci, model
  je nečte, jen vloží.

Hotový tvar je ve vzorovém skillu v pluginu (`assets/vzorovy-skill/`).

Výstupem bývá **samostatná HTML stránka** — otevře se v prohlížeči, dá se v
ní hledat, a do mailu se převede na PDF (návod 12). Prezentace je totéž,
jen víc stránek. Word nebo PowerPoint jde taky, ale HTML je nejméně práce a
nejlíp se v něm drží značka.

## Jak to složit dohromady

1. Skill „report" spustí skript, který stáhne data a uloží `data.json` a
   krátký souhrn (pět řádků, ne tisíc).
2. Tělo skillu vyloží souhrn: co se změnilo, proč, co s tím.
3. Skill „report" požádá skill se značkou, ať z výkladu a čísel vyrobí
   dokument. Dva skilly, každý dělá jednu věc.

Jeden skill, který dělá všechno, se hůř ladí a hůř sdílí — až se změní
značka, přepisuješ i report. Proto dva.

## Sdílení v týmu

Skill se značkou zabal do pluginu a dej kolegům (návod 10 a 04). Změna
značky = nová verze pluginu, všichni ji dostanou při aktualizaci. Report,
který si každý staví sám nad svými zdroji, skill se značkou jen volá.

## Opakování

Report, který se dělá měsíčně, je kandidát na naplánovaný běh (návod 11).
Ale nejdřív ho třikrát pusť ručně — až je výstup pokaždé stejný a nikdo do
něj nemusí sahat, teprve pak ho nech běžet samotný.
