---
name: skoleni-shrnuti
description: Uzavře den školení Claude Code pro markeťáky — ze stavu vyjmenuje, co si účastník za den vyrobil, ukáže k tomu skutečné cesty k souborům, řekne, co mu zůstává nainstalované, a navrhne jeden opakovaně běžící proces přizpůsobený jeho práci a datům. Použij na konci školení, spouští se příkazem /skoleni-shrnuti nebo když účastník řekne "co jsme dnes udělali", "co si odnáším", "shrň mi to" nebo se ptá, co s tím vším teď.
license: LicenseRef-Rellmo-Commercial
allowed-tools: Bash(python3:*), Bash(py:*), Bash(python:*), Read, AskUserQuestion
metadata:
  author: Rellmo
  version: 1.0.0
  category: zaver
---

# skoleni-shrnuti

Závěr trvá přibližně čtyři minuty na účastníka. Projdi pět položek a u
každé uveď skutečnou cestu nebo pravdivě řekni, že nevznikla.

Používej stejná podstatná jména jako v ranním programu. Nevymýšlej artefakty,
které ve stavu nebo na disku nejsou.

## Pět položek

1. **Připravené prostředí** — pracovní složka s `CLAUDE.md` a `.gitignore`,
   pluginy superpowers a skill-creator.
2. **Vlastní automatizace** — skill (`SKILL.md`), případně zabalený plugin a
   odkaz na GitHub.
3. **Brandkit a skill se značkou** — složka `brandkit/` s `tokens.css`,
   ukázkový report, skill, který na ni odkazuje (jen když účastník šel touhle
   cestou; jinak řekni, že je to na doma podle návodu 19).
4. **Návrh procesu**, který se bude spouštět opakovaně.
5. **Co zůstává** — plugin školení s příručkou, superpowers a skill-creator,
   jeden plugin z katalogu re:LLMO zdarma podle vlastního výběru a 10 % na
   ostatní.

Položka 4 vznikne až v kroku 3. Položky 1 až 3 hledej ve stavu (brandkit v
`kroky["brandkit"]`). Položka 5 je
pevný seznam; u pluginů řekni jen to, co dnešní průchod prokázal
(`stav["kroky"]["start"]`), a plugin z katalogu neoznačuj jako
nainstalovaný — vybírá si ho účastník sám po školení.

## Pořadí kroků

1. Přečíst stav a ověřit artefakty na disku.
2. Projít seznam nahlas s cestami.
3. Navrhnout jeden opakovaně běžící proces.
4. Uložit návrh, zapsat stav a uzavřít den.

## Jak mluvit

- Česky, spisovně, v klidném tónu. Účastníkům tykej.
- Nehodnoť výkon a nepoužívej oslavné fráze. Je to inventura.
- U chybějící položky řekni, co přesně chybí a jaký je další krok.
- Cesty vypisuj tak, jak existují na disku. Relativní cestu vždy vztáhni k
  `${CLAUDE_PROJECT_DIR}`.

## Krok 1 — Přečíst stav a ověřit artefakty

`${CLAUDE_PLUGIN_ROOT}` a `${CLAUDE_PROJECT_DIR}` dosazuje Claude Code do
textu skillu dřív, než ho čte model — platí tedy i uvnitř uzavřeného heredocu.
Na Windows: když `python3` nespustí Python (bývá to jen odkaz do Microsoft
Storu), použij místo něj `py`, případně `python`. Cesty v kódu pythonu nech
jako `r"…"` — na Windows je Claude Code dosazuje se zpětnými lomítky.

```bash
python3 <<'PY'
import json
from pathlib import Path
import sys

root = Path(r"${CLAUDE_PROJECT_DIR}")
sys.path.insert(0, r"${CLAUDE_PLUGIN_ROOT}/scripts")
import stav

stavova_cesta = root / ".skoleni" / "stav.json"
if not stavova_cesta.exists():
    print(f"Stav školení neexistuje: {stavova_cesta}")
    raise SystemExit(1)
s = stav.nacti(str(root))
print(json.dumps(s, ensure_ascii=False, indent=2))
print("\nKontrola artefaktů:")
for krok, info in s["kroky"].items():
    for artefakt in info.get("artefakty", []):
        if str(artefakt).startswith(("http://", "https://")):
            print(f"{krok}: {artefakt} (odkaz)")
            continue
        cesta = Path(artefakt)
        if not cesta.is_absolute():
            cesta = root / cesta
        print(f"{krok}: {cesta} ({'existuje' if cesta.exists() else 'CHYBÍ'})")
for soubor in ("CLAUDE.md", ".gitignore"):
    print(f"{soubor}: {'existuje' if (root / soubor).exists() else 'CHYBÍ'}")
PY
```

Spáruj položky takto:

| Položka | Kde ji hledat |
|---|---|
| Připravené prostředí | `CLAUDE.md` a `.gitignore` na disku; `kroky["start"]["stav"]` a poznámka |
| Vlastní automatizace | `kroky["automatizace"]["artefakty"]` — cesta na `SKILL.md`, případně složka pluginu a odkaz |
| Návrh procesu | vznikne v kroku 3 |
| Co zůstává | pevný seznam výše |

## Krok 2 — Projít seznam

Projdi všechny čtyři položky v pořadí. U každé řekni jednou větou, co vzniklo
a kde to leží. U chybějících položek použij přesný stav:

- `blokovano` — uveď chybějící nástroj, právo nebo přihlášení a co s tím
  (typicky návod 01 nebo 10, nebo IT);
- `preskoceno` — řekni, jak lze krok později doplnit (`/skoleni-automatizace`
  jde spustit znovu, naváže na rozdělanou práci);
- `nezacato` — řekni to bez hodnocení a odkaž na příslušný příkaz.

## Krok 3 — Návrh opakovaně běžícího procesu

Cílem je jeden konkrétní proces, ne seznam možností. Zeptej se přes
`AskUserQuestion`, co z dneška by účastník chtěl mít hotové pokaždé, bez
sebe: vlastní automatizaci z kroku 2, nebo něco z toho, co viděl na plátně.

Návrh sestav ze tří vět:

1. Co se kontroluje a jak často.
2. Při jaké změně má přijít zpráva.
3. Kam se zpráva uloží nebo odešle.

`routine` je cloudové plánování v Claude Code. Příkaz `/schedule` vyžaduje
přihlášení claude.ai a dostupné Claude Code on the web; organizace může
routine také zakázat. Routines pracují s repozitáři na GitHubu a připojenými
connectors. Lokální MCP server přidaný příkazem `claude mcp add` ani lokální
soubor do routine automaticky nepřejdou. Pokud proces závisí na místních
souborech nebo místním MCP serveru, navrhni naplánovaný běh na stroji.
`/schedule` nenastavuj v tomto kroku; odkaž na návod 11 a `/skoleni-napoveda`.

Vyber jeden vzor podle toho, co účastník dělá:

- **Pravidelný přehled z jednoho zdroje:** týdenní nebo měsíční report
  (Search Console, GA4, reklamní účet), zpráva jen když se něco pohne mimo
  obvyklé rozmezí.
- **Kontrola webu nebo obsahu:** měsíční průchod podle pravidel, která si
  účastník hlídá ručně, zpráva při zhoršení oproti minule.
- **Podklad, který se dělá pořád dokola:** dokument ve značce z podobných
  vstupů, spouštěný na vyžádání kolegou přes sdílený plugin.

Napiš schválený návrh do souboru. Protože `Write` není v `allowed-tools`,
proveď zápis přes povolený `python3` a dosaď skutečné tři věty:

```bash
python3 - "${CLAUDE_PROJECT_DIR}/navrh-procesu.md" <<'PY'
from pathlib import Path
import sys

soubor = Path(sys.argv[1])
obsah = """<tři schválené věty návrhu procesu>"""
soubor.write_text(obsah.rstrip() + "\n", encoding="utf-8")
print(soubor)
PY
```

Příkaz výše není spustitelný s doslovným placeholderem. Nahraď jej skutečným
návrhem. Bez vzniklého souboru krok 4 neoznačuj jako hotový.

## Krok 4 — Zapsat stav

Artefakt zapiš jako absolutní cestu, aby jej další běh našel i z jiné složky:

```bash
python3 <<'PY'
from pathlib import Path
import sys

sys.path.insert(0, r"${CLAUDE_PLUGIN_ROOT}/scripts")
import stav

s = stav.nacti(r"${CLAUDE_PROJECT_DIR}")
s["kroky"]["shrnuti"].setdefault("artefakty", [])
stav.pridej_artefakt(s, "shrnuti", r"${CLAUDE_PROJECT_DIR}/navrh-procesu.md")
stav.nastav_krok(s, "shrnuti", "hotovo", "")
stav.zapis(s, r"${CLAUDE_PROJECT_DIR}")
print(stav.veta(s))
PY
```

Na závěr řekni, že plugin zůstává nainstalovaný, `/skoleni-napoveda` je
dostupný i po školení a `/skoleni-automatizace` jde pustit znovu na další
úkol. Plugin z katalogu si účastník vybere sám — kde, říká
`references/podklady/katalog-automatizaci.md`. Pokud některé podklady nebo
návody chybějí, uveď to otevřeně.
