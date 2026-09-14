---
name: skoleni-start
description: Nastaví prostředí pro školení Claude Code pro markeťáky. Založí pracovní složku s CLAUDE.md a .gitignore, zeptá se na úroveň a doménu, doinstaluje pluginy superpowers a skill-creator, ověří python, git, gh a node a zapíše, jaké nástroje účastník v práci používá. Použij na začátku školení nebo když se k němu uživatel vrací a chce navázat. Spouštěj i opakovaně — dělá jen to, co chybí. Spouští se příkazem /skoleni-start nebo když účastník řekne "začínáme", "spusť školení", "kde jsem skončil", "chci pokračovat" nebo se ptá, co má udělat jako první.
license: LicenseRef-Rellmo-Commercial
allowed-tools: Bash(python3:*), Bash(brew:*), Bash(apt-get:*), Bash(winget:*), Read, Write, Edit, AskUserQuestion, WebSearch
metadata:
  author: Rellmo
  version: 1.0.0
  category: onboarding
---

# skoleni-start

První skill, který účastník spustí — a ten, na kterém stojí celé ráno. Malá
skupina markeťáků na firemních noteboocích, jedna wifi, různá zkušenost s
Claude Code. Nikdo neprogramuje. Tenhle skill musí odjet nastavení sám, u
každého kroku říct, co udělal a proč, a nikdy se nezaseknout na technickém
dotazu, který markeťák neumí zodpovědět.

## Pořadí kroků je závazné

1. Bezpečnost — `.gitignore`, `.claude/skills/`, `CLAUDE.md`.
2. Úroveň a doména.
3. Pluginy — superpowers a skill-creator.
4. Prostředí — python, git, gh, node, npx.
5. Nástroje účastníka.

Nepřehazuj to. Krok 1 je první, aby nic citlivého nevzniklo dřív než
`.gitignore`. Krok 3 je před krokem 4 schválně: pluginy jsou to, s čím se
během dne pracuje, chybějící `gh` nikoho nezdrží dřív než odpoledne.

## Jak mluvit

- Česky, tykání, klidně. Publikum jsou markeťáci, ne vývojáři — bez
  nadšeneckého tónu a bez dramatizování toho, co se právě děje.
- Nikdy neklaď technické otázky ("máš nainstalovaný Homebrew?", "jakou máš verzi
  Pythonu?"). Buď to zjisti a sprav sám, nebo řekni jednou větou, co má člověk
  udělat (typicky: napsat IT).
- U každého kroku řekni, co jsi udělal a kam jsi to zapsal. Práci děláš za
  účastníka, ale on musí vidět co — to je princip celého pluginu. Ruční postup
  pro zopakování doma je v návodech (`/skoleni-napoveda`), tenhle skill ho
  nevysvětluje.
- Nikdy nevypisuj tokeny ani hesla — ani v chatu, ani v souborech. Cokoli, co
  by mohlo nést tajemství (chybové hlášky, výpisy příkazů), protáhni přes
  `bezpecnost.maskuj()` dřív, než to účastník uvidí.

## Skripty a jak je volat

Práci dělají skripty ve `scripts/`, skill je jen řídí. **Volej je vždy absolutní
cestou přes `${CLAUDE_PLUGIN_ROOT}/scripts/…`, nikdy relativně a nikdy přes `cd`
do adresáře pluginu** — na Windows leží plugin pod uživatelským profilem a
relativní cesta vyvolá dotaz na citlivý soubor při každém zápisu. Pracovní
složku účastníka předávej jako `${CLAUDE_PROJECT_DIR}`, ne `.` a ne odhadem.

| Skript | Co z něj tenhle skill volá |
|---|---|
| `bezpecnost.py` | `zajisti_gitignore(slozka)`, `maskuj(text)` |
| `stav.py` | `nacti(slozka)`, `zapis(stav, slozka)`, `nastav_krok(stav, krok, novy, poznamka)`, `pridej_artefakt(stav, krok, cesta)`, `veta(stav)` |
| `pluginy.py` | `prehled()`, `chybejici()`, `nainstaluj(plugin_id)` (spustitelné rovnou jako skript) |
| `prostredi.py` | `zkontroluj(hlas=…)` (spustitelné rovnou jako skript), `navrh_instalace(nastroj)` |

`pluginy.py`, `prostredi.py` a `stav.py` jde spustit přímo — vypíšou přesně
to, co tenhle skill potřebuje:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/pluginy.py"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/prostredi.py"
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/stav.py" "${CLAUDE_PROJECT_DIR}"
```

Funkce z nich volej přes heredoc, vždy v jednom uzavřeném volání pythonu
(mezi dvěma voláními Bashe se nic nepamatuje, takže se vždy znovu načte stav,
upraví a hned zapíše):

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
# ... uprav s ...
stav.zapis(s, "${CLAUDE_PROJECT_DIR}")
PY
```

## Stav a navázání

Na úplném začátku vždy načti stav (`stav.nacti("${CLAUDE_PROJECT_DIR}")`) a
podívej se, kde je krok `start`:

- **`hotovo`** — start už proběhl. Řekni to (úroveň, doména, které pluginy
  jsou nainstalované) a zeptej se, jestli chce projet znovu (třeba nová
  doména), nebo pokračovat dál ve školení. Ber to jako signál, ne jako
  blokaci — nikdy neodmítej spustit se znovu.
- **cokoli jiného** — naváž přesně tam, kde se přestalo. Nezačínej od nuly:
  - úroveň/doména už ve stavu → přeskoč **otázky** v kroku 2 a řekni, že je to
    už zapsané. I tak zkontroluj `CLAUDE.md`: pokud v něm ještě je placeholder
    `<TODO — doplní krok 2, až bude známá doména účastníka>`, doplň ho stejným
    postupem jako v kroku 2 — může zůstat z běhu, který se přerušil mezi
    krokem 1 a 2.
  - `.gitignore` — `zajisti_gitignore` je sama o sobě idempotentní (doplňuje
    jen chybějící řádky), volej ji vždy, i podruhé, a řekni, jestli něco přibylo.
  - pluginy — `pluginy.chybejici()` vrátí jen to, co skutečně chybí; co je,
    se neinstaluje znovu.
  - `stav["nastroje"]` — pokud už není prázdné, ukaž, co tam je, a zeptej se,
    jestli přibyl další nástroj, místo aby ses ptal od začátku.

Na konci každého běhu (dokončeného i částečného) zapiš stav kroku `start`:
`hotovo`, pokud doběhlo všech pět kroků; `blokovano`, pokud něco nejde
spravit bez IT (chybějící nástroj, selhaná instalace pluginu). Do `poznamka`
napiš konkrétně na co — `stav.veta()` z toho pak lektorovi řekne, koho jít
zachránit.

## Krok 1 — Bezpečnost první

Dřív, než vznikne cokoli dalšího:

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import bezpecnost
print(bezpecnost.zajisti_gitignore("${CLAUDE_PROJECT_DIR}"))
PY
```

Řekni účastníkovi jednou větou, co se stalo: buď "založil jsem `.gitignore`,
ať ti sem žádný klíč ani export omylem nespadne do gitu", nebo (při druhém
spuštění) "gitignore už měl všechno, nic jsem nepřidával".

Ve stejném kroku založ i prázdnou složku na budoucí skilly účastníka —
odpoledne do ní ukládá `skoleni-automatizace`:

```bash
python3 -c "
import os
p = os.path.join('${CLAUDE_PROJECT_DIR}', '.claude', 'skills')
existovala = os.path.isdir(p)
os.makedirs(p, exist_ok=True)
print('existovala' if existovala else 'nova')
"
```

Pokud výstup je `nova`, řekni účastníkovi: "Zakládám i prázdnou složku
`.claude/skills/`, kam si odpoledne uložíš vlastní skill. Claude Code
sleduje jen složky, které existovaly při startu — proto ji vytvářím teď a
na konci tohohle bloku tě poprosím o restart. Ušetří ti to přerušení
uprostřed práce." Pokud je výstup `existovala`, nic z toho neříkej.

Ve stejném kroku založ i krátký `CLAUDE.md` — ručně psaný rozsahem, ne
vygenerovaný, ať je sám ukázkou toho, co odpoledne učíme (krátce, říkej kde,
ne co). V tuhle chvíli ještě neznáš doménu účastníka, takže do něj patří jen
to, co platí už teď — zbytek doplní krok 2:

```bash
python3 -c "
import os
print('existuje' if os.path.isfile(os.path.join('${CLAUDE_PROJECT_DIR}', 'CLAUDE.md')) else 'neexistuje')
"
```

Pokud výstup je `neexistuje`, zapiš (nástrojem Write) přesně tohle, beze
změny — je to pod dvacet řádků, nic nepřidávej:

```markdown
# Pracovní složka — školení Claude Code pro markeťáky

Tohle je pracovní složka ze školení Claude Code pro markeťáky (re:LLMO).

## Stav průchodu
Stav dnešního postupu je v `.skoleni/stav.json` — nesahej do něj ručně,
zapisuje a čte ho jen plugin `rellmo-skoleni`.

## Bezpečnost
Klíče, tokeny a datové exporty jsou v `.gitignore` — nemají co dělat ve
veřejném repozitáři.

## Web
<TODO — doplní krok 2, až bude známá doména účastníka>
```

Řekni účastníkovi jednou větou, co je tenhle soubor a proč vzniká: "Založil
jsem i `CLAUDE.md` — krátký kontext o týhle složce, který si Claude Code
načte pokaždé na začátku. Odpoledne na něj navážeme, až budeš psát ten samý
typ souboru pro vlastní skill." Pokud `CLAUDE.md` už existuje (druhé
spuštění), nic nepřepisuj a jen řekni, že tam už je z dřívějška.

## Krok 2 — Úroveň a doména

Jedno `AskUserQuestion` se dvěma otázkami najednou:

1. **Úroveň** — "Začátečník" / "Pokročilý" (ovlivňuje tempo a hloubku ve
   zbytku dne, ne tenhle skill).
2. **Doména** — webu, se kterým bude dnes účastník pracovat (vlastní nebo
   klientský). Nech to jako volnou odpověď, ne výběr z předvyplněných
   příkladů — každý má jinou doménu. Kdo dnes žádný web řešit nechce, může
   nechat prázdné; pak se doména do stavu nezapisuje a `CLAUDE.md` dostane
   větu "Dnes bez konkrétního webu."

Zapiš rovnou do stavu:

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
s["uroven"] = "zacatecnik"   # nebo "pokrocily", podle odpovědi
s["domena"] = "priklad.cz"   # doména z odpovědi, bez https:// a bez lomítka; None, když žádná
stav.zapis(s, "${CLAUDE_PROJECT_DIR}")
PY
```

Dopiš doménu i do `CLAUDE.md` z kroku 1 — nahraď `<TODO — doplní krok 2, až
bude známá doména účastníka>` (nástrojem Edit) větou "Web, se kterým dnes
pracujeme: `<domena>`." Pokud `CLAUDE.md` tenhle placeholder už nemá (druhé
spuštění), nic neměň.

Řekni, že sis to zapsal a že to bude platit i pro zbytek dne.

## Krok 3 — Pluginy

Nejdřív vypiš, co je a co chybí — nech výstup na obrazovce, ať účastník vidí
obě položky a k čemu jsou:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/pluginy.py"
```

Pak u každého chybějícího pluginu řekni jednou větou, k čemu dnes bude, a
rovnou ho nainstaluj, bez ptaní:

- **superpowers** — "Nejdřív rozmyslet, pak dělat. Dnes ho použijeme na
  zadání vlastní automatizace (brainstorming) i na psaní skillu."
- **skill-creator** — "Druhý průvodce tvorbou skillu, od Anthropicu.
  Odpoledne si vybereš, který ti sedí víc."

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import pluginy
for p in pluginy.chybejici():
    v = pluginy.nainstaluj(p)
    print(p, "-", v["vysledek"], "-", v["zprava"])
PY
```

Instalace trvá desítky sekund na plugin — řekni to předem, ať nikdo nemyslí,
že se to zaseklo. Po úspěšné instalaci se nové skilly objeví až po restartu
Claude Code; restart se dělá jednou, na konci tohohle skillu (viz "Na
konci"), ne teď.

**Když instalace selže** (síť, oprávnění), nezkoušej to znovu. Chybovou
hlášku protáhni přes `bezpecnost.maskuj()`, řekni jednou větou, co se stalo,
zapiš do stavu `blokovano` s názvem pluginu a pokračuj — zbytek rána bez
pluginů funguje, odpoledne je doinstaluje lektor ručně.

## Krok 4 — Prostředí

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/prostredi.py"
```

Tohle samo vypisuje průběžně, nástroj po nástroji — nech to běžet na
obrazovce. Pro každý nástroj, co chybí (`pritomen: false`), zjisti návrh a
rovnou ho proveď, bez ptaní:

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import prostredi
print(prostredi.navrh_instalace("git"))
PY
```

Vrátí buď příkaz (`brew install git`, `winget install -e --id Git.Git`, …) —
ten spusť sám přes Bash a řekni, co jsi doinstaloval. Nebo (když správce
balíčků chybí úplně) jednu větu, co má účastník napsat svému IT — tu jen
přečti a jdi dál, nečekej na odpověď a nezkoušej to obejít.

Po instalaci přes `winget` je potřeba nové okno terminálu (mění se PATH) —
pokud k tomu dojde, řekni to účastníkovi rovnou.

**Když instalační příkaz selže** (typicky oprávnění nebo firewall na
firemním notebooku), nezkoušej to znovu a neřeš proč. Zapiš do stavu, který
nástroj chybí, řekni jednou větou, co má účastník poslat svému IT, a
pokračuj — většina dne funguje i bez něj. Co konkrétně bez toho nástroje
nepůjde, řekni rovnou (bez `gh` nepůjde odpoledne sdílet skill přes GitHub;
bez `python3` nepoběží skripty ve vlastní automatizaci):

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
stav.nastav_krok(s, "start", "blokovano", "git se nepodařilo doinstalovat (selhalo oprávnění) — chybí IT")
stav.zapis(s, "${CLAUDE_PROJECT_DIR}")
PY
```

## Krok 5 — Nástroje účastníka

Zeptej se (běžnou větou, ne technicky): "Jaké nástroje nebo systémy dnes v
práci používáš?" (Search Console, GA4, Shoptet, WordPress, Mergado, reklamní
účty, konkrétní CRM, cokoli.) Pro každý nástroj to levně dohledej — jedno
`WebSearch` na "`<nástroj>` MCP server" stačí:

- **Existuje** → zapiš to a řekni, že napojení je krok pro odpoledne, až
  bude jasné, jestli ho vlastní automatizace vůbec potřebuje (návod 03).
- **Neexistuje** → zapiš to a řekni jednou větou, že stačí, aby nástroj měl
  API — server nad ním jde postavit (návod 03 a 09).

Nic dnes ráno neinstaluj — jen zapisuj a doporučuj. Search Console má
vlastní cestu bez Cloud Console (návod 05), zmiň to jen tomu, kdo ji uvede.

Zapiš výsledek do `stav["nastroje"]` — čte to `skoleni-automatizace`:

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
s["nastroje"].append({
    "nazev": "Shoptet",
    "ma_mcp": False,
    "nainstalovano": False,
    "poznamka": "MCP server nenalezen, jde postavit nad API",
})
stav.zapis(s, "${CLAUDE_PROJECT_DIR}")
PY
```

Každý nástroj = jeden záznam s klíči `nazev`, `ma_mcp`, `nainstalovano`,
`poznamka`. Drž se přesně těchhle klíčů — jiné skilly to pole čtou.

## Na konci

Ulož finální stav kroku `start` (viz "Stav a navázání" výše) a vypiš větu:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/stav.py" "${CLAUDE_PROJECT_DIR}"
```

Řekni účastníkovi přesně tohle: "Tohle je věta pro lektora — pokud v ní je
'zaseklo se', přečti ji nahlas, ať ví, koho jít zachránit."

Pak jednou větou, bez dramatu: "Zavři a znovu otevři Claude Code ve stejné
složce — načtou se nové pluginy a složka pro tvoje skilly. Je to jediný
restart dne." Restart je potřeba vždy, když se v kroku 3 něco instalovalo
nebo v kroku 1 vznikla `nova` složka; když ani jedno, řekni, že restart
tentokrát není potřeba. Po restartu je účastník připravený na výklad; další
skill (`/skoleni-automatizace`) přijde až v bloku o vlastní automatizaci.
