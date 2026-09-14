---
name: skoleni-napoveda
description: Příručka ze školení Claude Code pro markeťáky. Vysvětlí, jak nainstalovat plugin nebo MCP server, jak napsat vlastní skill a zabalit ho do pluginu, jak pracovat s GitHubem, jak naplánovat opakovaný běh, kdy se vyplatí vlastní model, jak skládat reporty z více zdrojů a co ověřit, když něco nefunguje. Použij ji po školení, když uživatel hledá materiály nebo se ptá „jak se to dělalo“, „kde to najdu“, „kde je prezentace“ nebo „tohle mi nefunguje“.
license: LicenseRef-Rellmo-Commercial
allowed-tools: Bash(python3:*), Read, Glob, Grep, AskUserQuestion
metadata:
  author: Rellmo
  version: 1.0.0
  category: prirucka
---

# skoleni-napoveda

Tento skill slouží po školení. Účastník si chce zopakovat postup bez pomoci
lektora. Nepředpokládej, že si pamatuje pojmy, a neodkazuj jej na to, co se
ukazovalo v sále. Nejprve zjisti konkrétní cíl a potom jej veď k ověřitelnému
výsledku.

## Co v pluginu hledat

Před odkazem na soubor ověř jeho existenci nástrojem `Glob`. Neoznačuj
plánovanou cestu za dostupný podklad.

| Cesta | Obsah, pokud soubor nebo složka existuje |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/navody/` | Návody krok za krokem (01–18) |
| `${CLAUDE_PLUGIN_ROOT}/references/reseni-problemu.md` | Řešení častých problémů |
| `${CLAUDE_PLUGIN_ROOT}/references/podklady/` | Katalog automatizací a prezentace |
| `${CLAUDE_PLUGIN_ROOT}/assets/vzorovy-skill/` | Vzorový skill k rozkopírování |

Soubory načítej až po určení tématu. Otevři jeden konkrétní soubor, ne celou
složku.

## Čtyři příkazy pluginu

| Příkaz | Kdy |
|---|---|
| `/skoleni-start` | nastavení složky, pluginů a prostředí; jde spustit znovu na dalším počítači |
| `/skoleni-automatizace` | stavba vlastní automatizace v osmi krocích; jde spustit znovu na další úkol |
| `/skoleni-napoveda` | tenhle skill |
| `/skoleni-shrnuti` | inventura toho, co ze školení vzniklo, a návrh opakovaného běhu |

## Nejdřív rozliš situaci

1. **„Něco mi nefunguje.“** → ověř chybový výstup a otevři odpovídající část
   `reseni-problemu.md`, pokud je soubor dostupný.
2. **„Chci zopakovat postup.“** → vyber jeden návod z rozcestníku.
3. **„Kde je soubor nebo prezentace?“** → ověř cestu v podkladech a uveď ji.
4. **„Chci si postavit další automatizaci.“** → návod 18, nebo rovnou
   `/skoleni-automatizace`.

Když z otázky není jasné, o kterou situaci jde, zeptej se jednou krátkou
větou. Nezačínej výpisem celého obsahu pluginu.

## Rozcestník — návody

Nejdřív pomocí `Glob` ověř, které soubory v
`${CLAUDE_PLUGIN_ROOT}/references/navody/` skutečně existují. Pro dostupné
soubory použij tuto mapu:

| Potřeba | Soubor |
|---|---|
| Nainstalovat Claude Code a poprvé jej spustit | `01-instalace-a-prvni-spusteni.md` |
| Zorientovat se v terminálu a pracovní složce | `02-terminal-a-pracovni-slozka.md` |
| Přidat MCP server a rozhodnout, kdy jej použít | `03-mcp-servery.md` |
| Nainstalovat plugin nebo marketplace | `04-pluginy-a-marketplace.md` |
| Napojit Search Console | `05-search-console.md` |
| Rozumět pojmům skill, plugin, MCP server, subagent a hook | `06-slovnicek.md` |
| Napsat vlastní skill | `07-anatomie-skillu.md` |
| Ověřit, že skill funguje | `08-testovani-skillu.md` |
| Volit MCP a skript, bezpečně předat klíče | `09-mcp-nebo-skript.md` |
| Pracovat s GitHubem | `10-github.md` |
| Naplánovat opakovaný běh | `11-opakovane-behy.md` |
| Převést HTML do PDF | `12-html-do-pdf.md` |
| Nastavit status line | `13-status-line.md` |
| Používat superpowers | `14-superpowers.md` |
| Rozhodnout, kdy se vyplatí vlastní model místo API | `15-vlastni-model.md` |
| Skládat reporty z více zdrojů a mít brandkit jako skill | `16-reporty-z-vice-zdroju.md` |
| Zorientovat se v agentních systémech (Hermes, Paperclip) | `17-agentni-systemy.md` |
| Postavit další vlastní automatizaci v osmi krocích | `18-postup-vlastni-automatizace.md` |
| Postavit brandkit — značku jako soubory pro model | `19-brandkit.md` |

Pokud požadovaný soubor neexistuje, řekni to přesně. Neodkazuj na něj jako na
dostupný návod a nenahrazuj chybějící obsah smyšleným postupem. Odpověz jen z
dostupných podkladů nebo nabídni, co lze ověřit příkazy.

Návod přečti a odpověz vlastními slovy podle konkrétní otázky. Nevypisuj celý
soubor zpět do chatu.

## Řešení problémů

Pokud existuje `references/reseni-problemu.md`, ověř v něm příznak, příčinu,
postup a kontrolu výsledku. Neodhaduj příčinu pouze z krátkého popisu.
Nejdřív si nech ukázat chybovou hlášku nebo výstup příkazu. Když příznak
nesedí na žádnou část dostupného souboru, řekni to a pokračuj běžnou
diagnostikou.

Než zobrazíš část chybového výstupu, zamaskuj možné tajné údaje. Pokud je
výstup uložený v souboru, použij funkci `maskuj` takto:

```bash
python3 - "<cesta k souboru s výstupem>" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import bezpecnost

print(bezpecnost.maskuj(Path(sys.argv[1]).read_text(encoding="utf-8")))
PY
```

Pokud výstup soubor nemá, neukládej jej kvůli citlivému obsahu do nového
trvalého souboru. Uveď jen bezpečnou parafrázi a tajné hodnoty neopakuj.

## Podklady

`references/podklady/` obsahuje dvě věci:

- `prezentace.html` — celá prezentace ze školení, jeden soubor. Otevírá se
  dvojklikem a funguje offline. Slidy označené jako **referenční** se v sále
  přeskakovaly a jsou tam právě kvůli pozdějšímu čtení.
- `katalog-automatizaci.md` — přehled toho, co umí pluginy re:LLMO, s cenami
  a s tím, co který potřebuje na vstupu.

Při otázce „kde je prezentace" **uveď cestu k souboru**, ne odkaz na web —
je to lokální soubor v pluginu. Kdyby některý podklad chyběl, řekni to
rovnou; nepředstírej, že tam je.

## Stav ze školení

Pokud v pracovní složce existuje `.skoleni/stav.json`, načti celý stav, ne jen
jednu souhrnnou větu ze skriptu `stav.py`:

```bash
python3 <<'PY'
import json
from pathlib import Path
import sys

root = Path("${CLAUDE_PROJECT_DIR}")
sys.path.insert(0, "${CLAUDE_PLUGIN_ROOT}/scripts")
import stav

stavova_cesta = root / ".skoleni" / "stav.json"
if stavova_cesta.exists():
    print(json.dumps(stav.nacti(str(root)), ensure_ascii=False, indent=2))
else:
    print(f"Stav školení neexistuje: {stavova_cesta}")
PY
```

Když soubor neexistuje, pokračuj bez něj. Nevytvářej nový stav jen proto, aby
bylo možné zobrazit prázdný výpis.

## Čeho se držet

- Česky, spisovně, v klidném tónu. Účastníkům tykej.
- Nepoužívej formulaci, která problém zlehčuje.
- Když si nejsi jistý, řekni to a nabídni konkrétní způsob ověření.
- Odpověď zakonči prvním úkonem, který má účastník provést.
