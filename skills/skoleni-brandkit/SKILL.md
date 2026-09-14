---
name: skoleni-brandkit
description: Postaví účastníkovi školení brandkit — značku jako složku souborů, kterou umí číst model. Vytěží logo, barvy a písma z webu skriptem, doplní je z brand manuálu (PDF), každou hodnotu ověří s účastníkem a rozdíly zapíše, vyrobí tokens.css, ukázkový report a skill se značkou, který na brandkit odkazuje. Použij, když účastník řekne "chci brandkit", "naše značka pro Claude", "skill v našich barvách", "vytáhni barvy a logo z webu", nebo když v /skoleni-automatizace padne dokument ve firemní značce.
license: LicenseRef-Rellmo-Commercial
allowed-tools: Bash(python3:*), Bash(mkdir:*), Bash(cp:*), Read, Write, Edit, AskUserQuestion, Skill
metadata:
  author: Rellmo
  version: 1.0.0
  category: stavba
---

# skoleni-brandkit

Zhruba 30 minut u klávesnice, jde spustit i doma. Výsledkem je složka
`brandkit/` (barvy, písmo, loga, pravidla, `tokens.css`, `corrections.md`),
jeden ukázkový report v HTML a skill se značkou, který na brandkit jen
odkazuje. Cíl není jen ten brandkit — je to **postup, jak značku dostat do
souborů tak, aby ji model používal stejně jako člověk.**

Dvě zásady, které se neříkají nahlas, jen se podle nich jedná:

- **Hodnoty rozhoduje člověk, ne model.** Skript umí spočítat, která barva je
  na webu nejčastější; jestli je to brand barva, ví jen účastník. Každá
  hodnota v brandkitu má zdroj (strana manuálu, CSS proměnná na webu, nebo
  „řekl účastník") a bez odsouhlasení se nezapíše jako pravidlo.
- **Skončit s polotovarem je selhání skillu.** Když dochází čas, zúží se
  rozsah (viz Hlídání času), ale `tokens.css` a odsouhlasené barvy a písmo
  musí existovat vždycky.

## Kroky

0. Stav a navázání.
1. **Zdroje.** Doména, manuál (PDF), reálné výstupy, kdo značku hlídá.
2. **Vytěžení webu** skriptem `web_znacka.py` — loga, barvy, písma s četností.
3. **Vytěžení manuálu** — když je; každá hodnota se stranou.
4. **Ověření s účastníkem** po skupinách; rozdíly do `corrections.md`.
5. **Soubory brandkitu** — vyplnit vzor, `tokens.css`, `fonts.css`, loga.
6. **Ukázkový výstup** — jednostránkový HTML report, porovnat, opravit soubory.
7. **Skill se značkou** — kopie vzoru, odkazy místo opisování, zkouška naostro.
8. Zapsat stav, nabídnout sdílení.

## Hlídání času

Skill neví, kolik času z bloku uteklo — zeptej se po kroku 4. Když zbývá
méně než čtvrtina (zhruba osm minut): přeskoč krok 6, v kroku 7 jen zkopíruj
vzor a přepiš odkazy bez zkoušky naostro, a řekni na rovinu, co zůstává na
doma (návod 19 to vede stejným postupem). Kroky 4 a 5 nikdy nepřeskakuj.

## Jak mluvit

- Česky, tykání, klidně. Publikum jsou markeťáci; neptej se na „RGB versus
  HSL", ptej se „je tahle fialová vaše hlavní barva, nebo jen tlačítko".
- U každé hodnoty říkej zdroj: „z webu, CSS proměnná `--brand`", „manuál
  strana 5", „tvoje slovo". Bez zdroje nic nezapisuj jako pravidlo.
- Ukazuj, ne popisuj: barvy vypiš s hex kódem, loga otevři (cesta k souboru),
  písmo pojmenuj i s náhradou.
- Chybové hlášky (ze skriptu, ze sítě) protáhni přes `bezpecnost.maskuj()`.

## Skripty a jak je volat

Vždy absolutní cestou přes `${CLAUDE_PLUGIN_ROOT}/scripts/…`, pracovní složku
přes `${CLAUDE_PROJECT_DIR}`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/web_znacka.py" "<domena>" --out "${CLAUDE_PROJECT_DIR}/brandkit/_web"
```

Stav stejným vzorem jako ostatní skilly pluginu:

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

## Krok 0 — Stav a navázání

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
print(s["domena"], "|", s["uroven"])
print(s["kroky"]["brandkit"]["stav"], "|", s["kroky"]["brandkit"]["artefakty"])
PY
```

- **`hotovo`** — brandkit existuje. Ukaž cestu a zeptej se, jestli chce
  projít další kolo ověření (přišel manuál), přidat výstup do `examples/`,
  nebo jít dál. Neodmítej.
- **cokoli jiného** — podívej se, jestli `${CLAUDE_PROJECT_DIR}/brandkit/`
  už existuje. Pokud ano, přečti `README.md` a `corrections.md`, řekni, co
  je vyplněné, a pokračuj od prvního souboru s nevyplněnými závorkami.
  Druhý běh nepřepisuje, co účastník odsouhlasil poprvé.

## Krok 1 — Zdroje

Jedno `AskUserQuestion`, čtyři otázky najednou (u `zacatecnik` po jedné):

1. **Doména** — předvyplň `stav["domena"]`, nech potvrdit nebo změnit.
2. **Brand manuál** — má PDF? Ať napíše cestu k souboru. Bez manuálu jde
   postup dál, brandkit bude označený jako *odvozený z webu*.
3. **Reálné výstupy** — jedna až dvě prezentace nebo PDF, které značku
   drží správně (cesty). Volitelné.
4. **Kdo značku hlídá** — jméno nebo role; a tři odpovědi: nejčastější
   chyba, co nikdy, co je nedotknutelné. Když to účastník neví, nech
   prázdné a zapiš jako otevřenou otázku.

Založ složku ze vzoru a hned řekni, co v ní je (devět částí, jednou větou
každá — viz `README.md` vzoru):

```bash
mkdir -p "${CLAUDE_PROJECT_DIR}/brandkit"
cp -R "${CLAUDE_PLUGIN_ROOT}/assets/vzorovy-brandkit/." "${CLAUDE_PROJECT_DIR}/brandkit/"
```

## Krok 2 — Vytěžení webu

Spusť skript a nech výstup běžet na obrazovce:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/web_znacka.py" "<domena>" --out "${CLAUDE_PROJECT_DIR}/brandkit/_web"
```

Skript stáhne domovskou stránku a její CSS a vypíše: nejčastější barvy
(bez šedých a bílé), CSS proměnné s barvou, písma (použitá, `@font-face`,
Google Fonts) a kandidáty na logo, které stáhl do `brandkit/_web/loga/`.
Podrobný nález je v `brandkit/_web/nalez.json`.

Co s tím říct nahlas, dřív než se cokoli zapíše:

- **Četnost není důležitost.** Nejčastější barva bývá brand barva, ale ne
  vždy — šablony (Bootstrap, Tailwind) do CSS přinesou celou paletu, která
  se na webu vůbec nepoužívá. Když vidíš proměnné jako `--blue`, `--indigo`,
  `--pink` vedle sebe, je to paleta frameworku, ne značky. Řekni to.
- **Pojmenované proměnné jsou silnější signál než četnost.** `--brand`,
  `--c-primary`, `--color-purple` vyhrávají nad `#xxxxxx ×157`.
- **Kandidáti na logo** mají skóre: obrázek s „logo" v atributech v hlavičce
  je nejjistější, `og:image` nejméně. Otevři nejvýš tři nejlepší (cesta
  k souboru) a nech účastníka ukázat, který je ten pravý.
- **Písma**: `@font-face` a Google Fonts říkají, co web opravdu načítá;
  `font-family` v CSS říká, co se používá. Když se liší, ptej se.

Když skript skončí chybou (web blokuje roboty, přesměrování jinam, přes
3 MB), neopakuj to. Řekni to jednou větou a pokračuj: barvy, písmo a logo
si vyžádáš od účastníka v kroku 4 (hex kódy, název písma, soubor s logem).
Zapiš do poznámky stavu, že web nešel vytěžit.

## Krok 3 — Vytěžení manuálu

Jen když má účastník PDF. Přečti ho (nástrojem Read) a vypiš tabulku:
**hodnota · kde v manuálu (strana) · co na webu (z kroku 2) · shoda/rozdíl**.
Skupiny: barvy, písmo, logo (varianty, ochranná zóna, minimální velikost,
zakázané úpravy), tón a claim, vzory stran.

Co v manuálu není a web to má, označ „jen web". Co má manuál a web ne,
označ „jen manuál" — to je obvykle pravidlo, které se na webu porušuje, a
patří do `corrections.md` jako poznámka pro toho, kdo web spravuje.

Bez manuálu tenhle krok přeskoč a do `README.md` brandkitu napiš první
větu: *„Odvozeno z webu `<domena>` dne `<datum>`; oficiální manuál nebyl
k dispozici."*

## Krok 4 — Ověření s účastníkem

Jádro skillu. Projdi čtyři skupiny, každou jedním `AskUserQuestion` (u
`zacatecnik` po jedné hodnotě, u `pokrocily` celou skupinu naráz):

1. **Barvy** — navrhni hlavní barvu, barvu pro akci (CTA) a nejvýš dvě
   vedlejší, každou se zdrojem. Zeptej se, co z toho sedí, co chybí, a
   výslovně: *„Je něco, co na webu je, ale brand barva to NENÍ?"* Odpověď
   patří do oddílu „Co NENÍ brand barva".
2. **Písmo** — název, řezy, náhrada. Zeptej se na licenci: smí soubory
   písma do repozitáře, nebo jen odkaz?
3. **Logo** — který kandidát je logo, jaké varianty existují (barevná,
   bílá, černá, symbol), jak se logo jmenuje v manuálu. Když má účastník
   vlastní soubory, ať napíše cestu; zkopíruj je do `brandkit/logo/` a
   pojmenuj podle `logo.md`.
4. **Tón a pravidla** — tykání/vykání, co nikdy, claim. Tři odpovědi z
   kroku 1 sem patří jako první tři pravidla.

Každý rozdíl mezi tím, co našel skript nebo manuál, a tím, co řekl
účastník, zapiš do `brandkit/corrections.md` (co, před, po, důvod, zdroj).
Ne až na konci — hned, jak padne rozhodnutí. Prázdný `corrections.md`
znamená, že ověření neproběhlo.

## Krok 5 — Soubory brandkitu

Vyplň (nástrojem Edit) `colors.md`, `typography.md`, `logo.md`,
`brand-identity.md` a `README.md` z odsouhlasených hodnot. Pravidla:

- Každá hodnota má za sebou zdroj v závorce: *(manuál s. 5)*, *(web,
  `--c-primary`)*, *(účastník)*.
- Co zůstalo neodsouhlasené, nech v hranatých závorkách a sepiš na konec
  `README.md` jako „Otevřené otázky".
- Sekce, které pro značku nedávají smysl (tmavý režim, sociální sítě),
  smaž — prázdná sekce je horší než žádná.

Pak `tokens.css`: dosaď hex kódy, název písma, náhradu a řádkování; nech
jen proměnné, které mají hodnotu. `fonts/fonts.css`: jeden `@font-face` na
odsouhlasený řez; soubory písma zkopíruj jen se souhlasem k licenci, jinak
napiš do komentáře, odkud si je má každý doplnit. Loga v `brandkit/logo/`
pojmenuj podle `logo.md`, složku `_web/` smaž nebo nech jako pracovní
(řekni, že do repozitáře nepatří — přidej ji do `.gitignore` účastníka).

Krátce zopakuj, co kam šlo a proč: krátké a vždy potřebné do `README.md`
a `tokens.css`, dlouhé a občasné do `brand-identity.md`, binární do
`logo/` a `fonts/`.

## Krok 6 — Ukázkový výstup

Vyrob (nástrojem Write) `brandkit/examples/report.html`: samostatná
stránka, která načítá `../tokens.css`, má logo v hlavičce, nadpis, dva
odstavce, jednu tabulku a jeden blok s výzvou k akci v barvě CTA. Žádný
externí zdroj kromě `tokens.css` a `fonts/`. Otevři ji účastníkovi (cesta)
a zeptej se: sedí to na manuál nebo na váš poslední dokument?

Opravy dělej **v souborech brandkitu**, ne v reportu — pak report znovu
otevři. Tohle je test, že brandkit drží: co se musí opravit v reportu
ručně, chybí v pravidlech.

## Krok 7 — Skill se značkou

Zkopíruj vzorový skill a přepiš ho tak, aby na brandkit odkazoval:

```bash
mkdir -p "${CLAUDE_PROJECT_DIR}/.claude/skills"
cp -R "${CLAUDE_PLUGIN_ROOT}/assets/vzorovy-skill" "${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>-znacka"
```

V `SKILL.md` (nástrojem Edit): `name` na `<jmeno>-znacka`; `description`
napíše účastník sám jako rozhodovací větu (stejná tři pravidla jako
v `/skoleni-automatizace`: začíná situací, obsahuje slovo, které by sám
napsal, neopakuje postup); tělo: *barvy a písmo podle `brandkit/tokens.css`,
logo z `brandkit/logo/`, pravidla tónu v `brandkit/brand-identity.md`, vzor
výstupu `brandkit/examples/report.html`*. `references/znacka.md` a
`assets/` vzoru smaž — brandkit je nahrazuje.

Zkouška naostro: účastník napíše běžnou žádost („udělej jednostránkovou
nabídku v naší značce pro …"). Když se skill nespustí, vyvolej ho jménem;
když ho Claude Code nenajde, restart ve stejné složce. Výstup polož vedle
`examples/report.html` — mají vypadat jako ze stejné ruky.

## Krok 8 — Stav a sdílení

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
stav.pridej_artefakt(s, "brandkit", "${CLAUDE_PROJECT_DIR}/brandkit/tokens.css")
stav.pridej_artefakt(s, "brandkit", "${CLAUDE_PROJECT_DIR}/brandkit/examples/report.html")
stav.pridej_artefakt(s, "brandkit", "${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>-znacka/SKILL.md")
stav.nastav_krok(s, "brandkit", "hotovo", "")
stav.zapis(s, "${CLAUDE_PROJECT_DIR}")
print(stav.veta(s))
PY
```

`hotovo` jen když existuje `tokens.css`, `corrections.md` není prázdný a
skill prošel zkouškou; jinak nech stav, jak byl, a do poznámky napiš, co
zůstává na doma (typicky manuál, licence písma, kolo ověření).

Na konci jedna věta o sdílení: brandkit patří do vlastního repozitáře
(návod 10), skill se značkou do pluginu (`/skoleni-automatizace`, krok 8).
Změna značky = nová verze a řádek v `corrections.md`. Nic z toho teď
nespouštěj, pokud o to účastník výslovně nepožádá.
