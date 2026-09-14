# 17 — Agentní systémy: Hermes, Paperclip a co s tím

Na školení používáš Claude Code tak, že sedíš u něj a zadáváš práci.
Agentní systémy jsou vrstva nad tím: Claude Code (nebo jiný agent) dostává
úkoly odjinud, plní je sám a výsledek vrací tam, odkud úkol přišel. Tenhle
návod je výhled, ne doporučení k nasazení.

## Dva pojmy, na které narazíš

**Hermes Agent** — open source „brána" pro agenty. Umí přijímat úkoly ze
Slacku nebo jiného kanálu, držet profily (kdo smí co), plánovat opakované
běhy, pamatovat si kontext a předávat práci exekutorovi — třeba Claude Code
spuštěnému bez obrazovky (`claude -p`). Když by se Claude Code na něco
zeptal (oprávnění, upřesnění), otázka jde přes Hermes do Slacku a odpověď
zpátky.

**Paperclip** (`github.com/paperclipai/paperclip`) — open source orchestrační
vrstva nad Claude Code, hostovaná u sebe. Modeluje firmu: organizační schéma,
role, cíle, rozpočty, schvalovací brány, stropy nákladů. Agenti berou úkoly z
fronty podle rozvrhu, člověk schvaluje z dashboardu.

Rozdíl: Hermes je brána a dispečink pro jeden tým, Paperclip je „firma
z agentů". Oba stojí na tom, co už umíš — na skillech a pluginech, které
agent spouští.

## Náš pilot (Effectix, od září 2026)

Interní agent pro SEO tým:

1. Úkol vznikne ve Slacku (zpráva v kanálu nebo DM) nebo v interním systému
   pro řízení práce (Allfred), kde je přiřazený uživateli „Hermes".
2. Hermes ho přijme a předá Claude Code s našimi pluginy — v pilotu jen dvěma,
   které nepotřebují klientské přístupy (kontrola přístupu AI robotů, audit
   XML sitemap).
3. Claude Code plugin spustí; když by se ptal, otázka jde přes Hermes do
   Slacku a čeká na člověka.
4. Výsledek (report, shrnutí, spotřeba, čas běhu) se zapíše zpět do vlákna
   nebo k úkolu.

Pravidla pilotu: žádný zápis do klientských systémů bez schválení ve Slacku;
u každého úkolu zapsaná spotřeba; po čtyřech týdnech vyhodnocení podle toho,
kolik úkolů prošlo bez zásahu a kolik výstupů kolegové použili bez
přepracování.

Rozhodnutí, která stojí za zmínku: Claude Code jako exekutor běží pod
předplatným (Max), ne přes API klíč — pluginy jsou jeden zdroj pro lidi i
pro agenta. Běží to na běžném firemním počítači, ne na pronajatém serveru.

## Kdy to dává smysl

- Máš **hotové, ověřené pluginy**, které běží bez zásahu — agent je jen
  spouští. Bez nich není co orchestrovat.
- Úkoly **přicházejí odjinud** než od tebe: kolegové, ticketing, kalendář.
- Potřebuješ **stopy**: kdo co zadal, kolik to stálo, co vzniklo.
- Jsi ochotný **nastavit pravidla** — co se smí bez schválení a co ne.

## Kdy ne

- Když jsi jediný, kdo úkoly zadává. Naplánovaný běh (návod 11) je
  jednodušší a stačí.
- Když pluginy ještě nejsou stabilní. Agent chyby neopraví, jen je
  zmnoží.
- Když nemáš, kdo by to provozoval. Je to další systém s aktualizacemi,
  přístupy a výpadky.

## Co se nemění

Tři věci, které se učíš na školení, platí v každém agentním systému: popsat
práci v krocích, které jde předat dál; dodat kontext a data, ne jen zadání;
zabalit jednorázovou práci tak, aby ji spustil někdo jiný. Mění se názvy a
příkazy, způsob přemýšlení zůstává.
