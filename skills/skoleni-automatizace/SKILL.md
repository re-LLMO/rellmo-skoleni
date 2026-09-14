---
name: skoleni-automatizace
description: Provede účastníka školení stavbou vlastní automatizace v Claude Code v osmi krocích — od pojmenování opakovaného úkolu přes zadání, zúžení, volbu dat, kostru skillu a popis až po zkoušku naostro a zabalení do pluginu, který si nainstaluje kolega. U každého kroku říká proč, oponuje širokému zadání a vždy dotáhne skill do funkčního stavu, i kdyby se rozsah musel zúžit. Použij v bloku o vlastní automatizaci, spouští se příkazem /skoleni-automatizace nebo když účastník řekne "chci si postavit vlastní automatizaci", "chci si to zautomatizovat", "postav mi skill", "jak se dělá skill" nebo se ptá, co si může postavit sám.
license: LicenseRef-Rellmo-Commercial
allowed-tools: Bash(python3:*), Bash(mkdir:*), Bash(cp:*), Bash(git:*), Bash(gh:*), Read, Write, Edit, AskUserQuestion, Skill
metadata:
  author: Rellmo
  version: 1.0.0
  category: stavba
---

# skoleni-automatizace

Blok o vlastní automatizaci, zhruba 25 minut u klávesnice. Účastník má za
sebou ranní `skoleni-start` (složka, `.claude/skills/`, superpowers a
skill-creator) a dopolední výklad o tom, z čeho se skill skládá. Teď si
jeden postaví. Cíl bloku není ten konkrétní skill — je to **postup, který
umí zopakovat doma na další úkol**. Proto u každého kroku říkej proč, ne
jen co.

Osm kroků je stejných v prezentaci, v tomhle skillu i v návodu
`references/navody/18-postup-vlastni-automatizace.md`. Účastník si má odnést
těch osm otázek, ne tvůj výstup.

Platí i druhá půlka, která se neříká nahlas, jen se podle ní jedná:
**skončit s polotovarem je selhání tohohle skillu, ne účastníka.** Když
dochází čas, je na tobě zúžit rozsah a dotáhnout menší, ale funkční verzi —
ne nechat účastníka odejít s rozepsaným `SKILL.md`, který nikdy nic nevyrobil.

## Osm kroků

0. Stav a navázání.
1. **Pojmenuj opakovaný úkol.** Co děláš každý týden ručně.
2. **Zadání.** Brainstorming, dokud není jasný vstup, výstup a „hotovo, když".
3. **Zúžení zadání.** Jeden vstup, jeden výstup.
4. **Data.** MCP, skript, nebo žádná.
5. **Kostra.** Superpowers `writing-skills` nebo skill-creator, jinak vzorový skill.
6. **Popis (`description`)** jako rozhodovací věta.
7. **Zkouška naostro** na malém vstupu.
8. **Zabalení a sdílení.**
9. Zapsat stav.

Kroky 1–4 se v praxi prolínají — rozsah se ukáže širší, až když se probírá
první nápad, a rozhodnutí o datech padá spolu s tím, co skill vlastně dělá.
Drž se pořadí jako kostry rozhovoru, ne jako rigidního checklistu. Ale kroky
6 a 7 nikdy nepřeskakuj: bez popisu se skill nespustí a bez zkoušky nikdo
neví, jestli funguje.

## Hlídání času

Tenhle skill nemá jak sám zjistit, kolik reálného času z bloku uteklo —
zeptej se přímo, v přirozeném okamžiku: nejpozději po kroku 4, ať víš, kolik
má stavba a testování ještě prostoru.

Když zbývá **méně než čtvrtina bloku** (zhruba šest minut) a skill ještě
neběžel naostro: zastav rozšiřování, řekni to na rovinu ("zbývá nám asi šest
minut, škrtneme tohle a dotáhneme zbytek do funkčního stavu") a jdi rovnou na
nejmenší verzi, která projde krokem 7. Krok 8 pak zredukuj na `plugin.json`
a jednu větu o tom, jak se sdílí — GitHub je nadstavba, ne podmínka.

## Jak mluvit

- Česky, tykání, klidně. Žádné technické otázky ("chceš to synchronně nebo
  přes frontu") — publikum jsou markeťáci, ne vývojáři.
- Ptej se a oponuj, ale nenech účastníka bloudit. Vedeš rozhovor (otázky,
  protiotázky, návrhy k výběru), jen nepředžvýkáváš řešení. Kostru
  `SKILL.md`, volání `stav.py` a skript (pokud vznikne) piš ty nástrojem
  Write/Edit — šetří se na tom, CO se tam napíše, ne na psaní samotném.
- Tempo podle `stav["uroven"]`: `zacatecnik` — jedna otázka po druhé, počkej
  na odpověď. `pokrocily` — otázky klidně slouč a rovnou řekni, co jde
  přeskočit.
- Chybové hlášky (ze zkoušky naostro, ze skriptu, z gitu) protáhni přes
  `bezpecnost.maskuj()`, než je ukážeš.
- Restart kvůli `.claude/skills/` má účastník za sebou z rána — v kroku 7 ho
  zmiň jen jako záchranu, ne jako první podezření.

## Skripty a jak je volat

Vlastní skripty tohohle pluginu (`stav.py`, `bezpecnost.py`) vždy absolutní
cestou přes `${CLAUDE_PLUGIN_ROOT}/scripts/…`:

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

Skill, který účastník staví, vzniká v jeho pracovní složce, ne v tomhle
pluginu — vždy v `${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>/`. Skript,
který si případně postaví v kroku 4, leží tamtéž; volej ho přes
`${CLAUDE_PROJECT_DIR}`, nikdy relativně:

```bash
SKRIPT="${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>/scripts/<nazev>.py"
python3 "$SKRIPT" <argumenty>
```

## Krok 0 — Stav a navázání

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
print(s["uroven"], "|", s["domena"])
print(s["nastroje"])
print(s["kroky"]["automatizace"]["stav"], "|", s["kroky"]["automatizace"]["artefakty"])
PY
```

- **`hotovo`** — skill už existuje a byl vyzkoušený naostro. Ukaž cestu k
  němu a zeptej se, jestli chce rozšířit rozsah, postavit druhý, nebo jít na
  zabalení a sdílení (krok 8), pokud se ráno nestihlo. Neodmítej upravit ho
  znovu.
- **cokoli jiného** — než se začneš ptát, zkontroluj, jestli
  `${CLAUDE_PROJECT_DIR}/.claude/skills/` už obsahuje rozdělanou práci (cesta
  v `artefakty`, nebo nová podsložka od dřívějšího běhu). Pokud ano, přečti
  `SKILL.md` a podívej se, které `<TODO` ještě zbývají — doplněné části
  nevracej, jen řekni, co už tam je, a pokračuj od prvního nedoplněného místa.
  Druhý běh nikdy nepřepíše, co účastník napsal poprvé.

## Krok 1 — Pojmenuj opakovaný úkol

Zeptej se přímo: "Co děláš každý týden nebo měsíc ručně a pokaždé stejně?"
Nech chvíli prostor pro vlastní nápad — většina ho má. Dobrý kandidát má tři
znaky, řekni je nahlas: **opakuje se**, **postup znáš zpaměti**, **vstup je
pokaždé podobný** (jiná data, stejný tvar).

**Když nápad nemá**, nenabízej obecný seznam. Sáhni do `stav["nastroje"]` a
nabídni tři návrhy šité na to, s čím účastník pracuje, přes
`AskUserQuestion` spolu s volbou "mám vlastní nápad":

- nástroj s `ma_mcp: true` → automatizace, která ho skutečně použije
  (pravidelný přehled z jednoho zdroje: co se změnilo od minula);
- kontrola webu nebo obsahu podle pravidel, která si účastník hlídá ručně;
- dokument ve firemní značce (report, prezentace, podklad), který se dělá
  pořád dokola z podobných vstupů.

Návrhy odvozuj z toho, co je ve stavu, ne z odhadu oboru. Nástroj bez MCP a
bez API přeskoč — není zatím na co navázat.

## Krok 2 — Zadání

Tohle je učební moment: **pět minut ušetřených na zadání se vrací jako
hodina oprav.** Řekni to.

Pokud je nainstalovaný plugin superpowers, vyvolej skill
`superpowers:brainstorming` (nástrojem Skill) s tím, co účastník řekl v kroku
1 — ať se ptá, dokud zadání nedrží pohromadě. Když superpowers chybí, ptej se
sám podle stejných zásad, jedna otázka po druhé:

1. Co je **vstup** — soubor, adresa, seznam, nic?
2. Co je **výstup** — soubor, tabulka, text v chatu, dokument?
3. **Hotovo, když** — podle čeho účastník pozná, že výsledek je správně?
4. Co se **liší mezi běhy** a co je pokaždé stejné?

Výsledek zadání shrň do čtyř vět a nech ho účastníkem odsouhlasit. Bez
odsouhlasení nepokračuj — je to jeho zadání, ne tvoje.

## Krok 3 — Zúžení zadání

Řekni nahlas: **rozsah je to, na čem skilly nejčastěji selhávají** — ne
chybějící znalost nástroje. Široké zadání se pozná podle dvou věcí:

- je v něm **"a" mezi dvěma různými úkoly** ("stáhne data, napíše k nim
  komentář a rozešle to týmu") — to jsou dva nebo tři skilly, ne jeden;
- nemá **jeden jasný vstup a jeden jasný výstup**.

Když zadání takhle vypadá, řekni to a nech účastníka zúžit sám — nezužuj za
něj. Pomáhá jedna konkrétní otázka: "Kdybys tohle musel spustit hned teď, na
jeden vstup, co by z toho vzniklo jako první?" Tenhle jeden výstup je to, co
dnes stavíte; zbytek je nápad na příště, ne škrtnutá práce. Zapiš si ho
k zadání jako "na příště".

Zúžení kvůli rozsahu **není totéž** co zúžení kvůli času z "Hlídání času" —
tady škrtáš zadání, které bylo široké už na vstupu.

## Krok 4 — Data: MCP, skript, nebo žádná

Tahle otázka padá jen tam, kde skill skutečně stahuje nebo zpracovává data.
Pokud jde jen o text nebo dokument bez datového zdroje, řekni to, zapiš
"žádná data" a přeskoč na krok 5.

Připomeň krátce princip z dopoledne: **skript se do modelu nenačítá, běží
mimo a model vidí jen výsledek**; přímé volání MCP nástroje zůstává v
rozhovoru a model výsledek vidí celý. Z toho plyne rozhodnutí:

| Situace | Volba | Proč |
|---|---|---|
| Nevíš přesně, co v datech hledáš, zkoumáš | **MCP** | model se rozhoduje za běhu, úsudek nad každým krokem |
| Postup znáš, stahuješ objem, opakuje se | **skript** | deterministické, model dostane pět řádků, ne deset tisíc |
| Vstupem je text, obrázek, dokument | **žádná** | není co stahovat |

Obvyklý vývoj: prozkoumáš přes MCP, postup se ustálí, převedeš ho na skript.

**Když padne skript**, napiš ho (nástrojem Write) do
`.claude/skills/<jmeno>/scripts/` v pracovní složce účastníka, pod jménem,
které říká, co dělá. Pravidla: bere vstup jako argumenty; na síť sahá jen
přes standardní knihovnu (`urllib.request`) — žádná závislost, kterou by bylo
potřeba instalovat uprostřed školení; plný výstup uloží do souboru vedle, na
obrazovku napíše jen krátké shrnutí. Základní tvar (uprav podle skutečného
zadání, neopisuj mechanicky):

```python
#!/usr/bin/env python3
"""stahni.py — stáhne zadané adresy a uloží z nich viditelný text.

Bere URL adresy jako argumenty. Plný text každé stránky uloží do souboru,
na výstup napíše jen jednu řádku za adresu — ať se do kontextu modelu
nenačítá dlouhý text.
"""
import re
import sys
import urllib.request

def stahni(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="ignore")

def na_text(html: str) -> str:
    bez_skriptu = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    bez_znacek = re.sub(r"(?s)<[^>]+>", " ", bez_skriptu)
    return re.sub(r"\s+", " ", bez_znacek).strip()

if __name__ == "__main__":
    vystup = []
    for url in sys.argv[1:]:
        try:
            text = na_text(stahni(url))
        except Exception as e:
            print(f"{url}: nepodařilo se stáhnout ({e})")
            continue
        vystup.append(f"## {url}\n\n{text[:4000]}\n")
        print(f"{url}: {len(text)} znaků textu")
    with open("podklad.md", "w", encoding="utf-8") as f:
        f.write("\n".join(vystup))
```

Pro jiné zdroje (CSV export, API s klíčem) platí totéž pravidlo: mechanické
a objemné do skriptu, úsudek nad výsledkem do těla skillu. Klíč k API nikdy
do skriptu ani do `SKILL.md` — do proměnné prostředí (návod 09).

**Když padne MCP** a server ještě není napojený (`stav["nastroje"]` bez
`nainstalovano: true`), řekni to na rovinu: napojení stojí čas, který teď
nemusí zbýt. Nabídni buď napojit teď podle návodu 03 (a zkrátit zbytek
bloku), nebo postavit skill tak, aby data dostal jako soubor, a MCP doplnit
doma.

## Krok 5 — Kostra

Nejdřív řekni ve třech větách, k čemu je která část — tohle si má účastník
odnést, ne technický popis:

- **`SKILL.md`** — to jediné, co model přečte pokaždé, když se skill spustí.
  Patří sem jen to, co je potřeba vždycky a je to krátké.
- **`references/`** — delší text, který se hodí jen občas (pravidla, celý
  manuál, metodika). Model si ho dotáhne, až ho potřebuje — ne pokaždé.
- **`assets/`** — soubory, které model nečte jako text, ale použije ve
  výstupu: logo, šablona, cokoli binárního.
- **`scripts/`** — mechanická práce s daty. Skript se do modelu nenačítá,
  běží mimo a model vidí jen jeho výsledek.

Pak nabídni přes `AskUserQuestion` dvě rovnocenné cesty, superpowers první:

1. **`superpowers:writing-skills`** — vede strukturou, popisem i testem;
   stejná sada, ze které přišel ranní brainstorming.
2. **`skill-creator`** — oficiální průvodce od Anthropicu, od nápadu po
   hotovou složku.

Vyvolej zvolený skill nástrojem Skill se zadáním z kroků 2–4 (vstup, výstup,
hotovo když, volba dat). Když ani jeden není nainstalovaný, nebo se účastník
chce jen podívat na hotový tvar, sáhni po vzoru:

```bash
cp -R "${CLAUDE_PLUGIN_ROOT}/assets/vzorovy-skill" "${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>"
```

Když je zadáním **dokument ve firemní značce** (report, prezentace,
nabídka), ukaž ještě `${CLAUDE_PLUGIN_ROOT}/assets/vzorovy-brandkit/`:
značka nepatří do skillu, ale do samostatné složky souborů (barvy, písmo,
loga, `tokens.css`), na kterou skill jen odkazuje. Dnes stačí vyplnit
`colors.md` a `typography.md` z toho, co má účastník v hlavě; zbytek podle
návodu 19 doma, z manuálu. Skill pak říká „barvy a písmo viz
`brandkit/tokens.css`", ne hex kódy v těle.

Pak přejmenuj `name`, vyprázdni `description` na `<TODO>` (napíše ho sám v
kroku 6) a nahraď tělo. Reference a assety značky, které ve vzoru zůstaly,
smaž, pokud je skill nepotřebuje — jinak si bude tahat kontext, který k
práci nepotřebuje.

Jméno skillu znormalizuj na platný tvar (malá písmena, spojovníky místo mezer
a diakritiky, nic jiného) — přesně tohle vyžaduje `name` ve frontmatteru:

```bash
python3 -c "
import re, unicodedata
s = 'Týdenní report'  # odpověď účastníka
s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
print(s)
"
```

Ať kostra vznikla kteroukoli cestou, na konci kroku musí platit: složka
`${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>/` existuje, `SKILL.md` má
`name`, tělo psané jako **konkrétní, spustitelné pokyny** (ne "analyzuje
data", ale "spusť `scripts/stahni.py` s adresami ze vstupu, z `podklad.md`
vytáhni …"), a `description` je zatím `<TODO>`. Když tělo zmiňuje nástroj
nebo příkaz, zapiš ho i do `allowed-tools` — jinak se uprostřed běhu objeví
dotaz na oprávnění, na který účastník neumí odpovědět.

## Krok 6 — Popis (`description`) jako rozhodovací věta

Vysvětli rozdíl, dřív než účastník cokoli napíše: **popis není shrnutí toho,
co skill dělá — je to jediná věta, podle které se Claude Code rozhoduje,
jestli skill vůbec spustit.** Nikdo nečte celý `SKILL.md` předem; čte se
popis, a teprve když sedí, načte se zbytek. Kontrast:

- Slabé: *"Vyrábí týdenní reporty."* (popisuje CO dělá, ne KDY se má spustit)
- Silnější: *"Použij, když někdo chce týdenní přehled ze Search Console —
  pozná se to podle slov 'týdenní report', 'co se změnilo', 'přehled za
  týden'."*

Nech účastníka napsat vlastní verzi bez pomoci. Pak dej zpětnou vazbu na tři
věci, konkrétně na jeho větě: (1) začíná situací, kdy se má spustit, ne
funkcí; (2) obsahuje aspoň jedno slovo, které by účastník sám napsal do
chatu; (3) neopakuje celý postup skillu — to je past, kvůli které si Claude
Code může myslet, že už ví, co dělat, a tělo dál nečte. Doplň finální verzi
do `SKILL.md` (nástrojem Edit) místo `<TODO>`.

## Krok 7 — Zkouška naostro

Bez tohohle kroku blok není hotový, ať je zbytek sebelepší.

**Testuj na malém vstupu.** Jedna adresa, jeden soubor, tři až pět položek —
ne celý seznam. Šetří to čas i limity předplatného, které musí vystačit na
zbytek dne.

1. Nech účastníka napsat běžnou žádost tak, jak by ji napsal kolegovi —
   přesně na tohle popis z kroku 6 cílí.
2. Pokud se skill sám nespustí, vyvolej ho výslovně jménem (nástrojem Skill)
   — zúží to problém na popis, nebo na to, že ho Claude Code vůbec nenašel.
3. **Když ho Claude Code nenajde ani na jméno:** nejčastější důvod je
   nestihnutý ranní restart — zavři a znovu otevři Claude Code ve stejné
   složce. Pokud problém přetrvá, zkontroluj, jestli `name` ve frontmatteru
   sedí se jménem složky.
4. Když skill nebo skript spadne, **nezkoušej to opakovaně** — jedno selhání
   stačí k rozhodnutí. Zapiš, co se stalo (hlášku přes `bezpecnost.maskuj()`),
   zúž rozsah na nejmenší verzi, která projde, a tu zkus znovu. Skončit bez
   jediného úspěšného běhu je jediný skutečně nedokončený stav tohohle bloku.
5. Když výstup vznikne, projděte ho spolu krátce — sedí na "hotovo, když" z
   kroku 2? Zapiš cestu k výstupu i k `SKILL.md` jako artefakty.

## Krok 8 — Zabalení a sdílení

Řekni, proč se to dělá: skill ve složce `.claude/skills/` funguje jen v
téhle složce a jen účastníkovi. **Plugin** je totéž zabalené tak, aby se
dalo nainstalovat jedním příkazem, verzovat a aktualizovat — i u kolegy.

**Jádro (vždy):** vedle pracovní složky založ složku pluginu a přesuň do ní
skill:

```bash
mkdir -p "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin/.claude-plugin" "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin/skills"
cp -R "${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>" "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin/skills/<jmeno>"
```

Zapiš (nástrojem Write) `.claude-plugin/plugin.json` — název, verze, popis
jednou větou, autor. Verzi začni na `0.1.0` a řekni, že se zvedá při každé
změně, kterou má kolega dostat. Pak pluginu založ `.gitignore` a
zkontroluj obsah, **než** ho pošleš kamkoli ven:

```bash
python3 - "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import bezpecnost
koren = Path(sys.argv[1]).resolve()
print(bezpecnost.zajisti_gitignore(str(koren)))
for cesta in sorted(koren.rglob("*")):
    if cesta.is_file() and ".git" not in cesta.relative_to(koren).parts:
        print(cesta.relative_to(koren))
PY
```

Projdi seznam i obsah textových souborů: přihlašovací údaje, tokeny, klíče,
interní adresy, datové exporty, zákaznická data. Když něco najdeš, nahraď to
názvem proměnné prostředí a tajnou hodnotu v chatu neopakuj.

**Nadstavba (jen když je čas a `gh` přihlášené):** sdílení přes GitHub.
Čtyři pojmy, každý jednou větou, až když na ně přijde řada — repozitář
(složka na GitHubu, která uchovává verze), commit (uložený stav s popisem),
větev (oddělená pracovní verze), pull request (žádost o kontrolu a převzetí
změny). Nic víc nevysvětluj.

```bash
gh auth status --hostname github.com
git -C "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin" init -b main
git -C "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin" add .
git -C "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin" status --short
git -C "${CLAUDE_PROJECT_DIR}/<jmeno>-plugin" commit -m "první verze pluginu"
gh api user --jq .login
gh repo create "<účet>/<jmeno>-plugin" --private --source="${CLAUDE_PROJECT_DIR}/<jmeno>-plugin" --remote=origin --push
```

Do příkazů vždy dosaď skutečnou cestu, účet a název — zástupné hodnoty
nikdy nespouštěj doslova. Před `commit` ukaž `status --short` a ověř, že v
seznamu není nic z kontroly výše. Když `gh` chybí nebo účet není přihlášený
(`gh auth login --hostname github.com --web`), sdílení odlož: řekni, že
plugin je hotový a přenositelný jako složka, a že GitHub je krok na doma
podle návodu 10. Neblokuj tím konec bloku.

Kolega si plugin nainstaluje dvěma příkazy (u soukromého repozitáře po
pozvání v Settings → Collaborators):

```
claude plugin marketplace add <účet>/<jmeno>-plugin
claude plugin install <jmeno>@<jmeno>-plugin
```

Řekni to jako větu, ne jako úkol na teď — kolega v sále nesedí.

## Krok 9 — Zapsat stav

```bash
python3 <<'PY'
import sys
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav
s = stav.nacti("${CLAUDE_PROJECT_DIR}")
stav.pridej_artefakt(s, "automatizace", "${CLAUDE_PROJECT_DIR}/.claude/skills/<jmeno>/SKILL.md")
# když vznikl plugin, přidej i jeho složku; když repozitář, i odkaz
stav.nastav_krok(s, "automatizace", "hotovo", "")
stav.zapis(s, "${CLAUDE_PROJECT_DIR}")
print(stav.veta(s))
PY
```

Stav vol podle skutečnosti: `hotovo`, pokud skill má popis a prošel krokem 7;
`blokovano`, pokud krok 7 opakovaně selhal a nejde to opravit; jinak nech,
jak byl. Do poznámky napiš, co se nestihlo (plugin, GitHub) — `skoleni-shrnuti`
to pak řekne správně.

## Na konci

Řekni, co vzniklo — jméno skillu, co umí, jestli běžel na plném, nebo
zúženém rozsahu, jestli je zabalený a jestli je na GitHubu. Pak jednu větu o
tom, co si má odnést: osm kroků z návodu 18 funguje na jakýkoli další úkol,
tenhle skill byl jen první.
