# rellmo-skoleni

Průvodce školením **Claude Code pro markeťáky** (re:LLMO). Provede účastníka
půldnem — od nastavení prostředí po vlastní automatizaci zabalenou pro
kolegy. Po školení zůstává jako příručka. Je stejný pro každý běh školení.

## Co plugin umí

| Příkaz | Co udělá |
|---|---|
| `/skoleni-start` | Založí pracovní složku, doinstaluje superpowers a skill-creator, ověří prostředí, zapíše nástroje účastníka |
| `/skoleni-automatizace` | Provede stavbou vlastní automatizace v osmi krocích, včetně zabalení do pluginu a sdílení |
| `/skoleni-brandkit` | Postaví brandkit: vytěží logo, barvy a písma z webu a manuálu, ověří je s účastníkem, vyrobí tokens.css, ukázkový report a skill se značkou |
| `/skoleni-napoveda` | Příručka: návody 01–19, prezentace, katalog automatizací, řešení problémů. Funguje i dlouho po školení |
| `/skoleni-shrnuti` | Inventura dne a návrh jednoho opakovaně běžícího procesu |

## Instalace

Repozitář je veřejný a sám je marketplace, takže stačí dva kroky.

V aplikaci Claude: tlačítko + vedle pole pro zprávu → Plugins → přidat
marketplace `re-LLMO/rellmo-skoleni` a z něj nainstalovat `rellmo-skoleni`.

V terminálu:

```
claude plugin marketplace add re-LLMO/rellmo-skoleni
claude plugin install rellmo-skoleni@rellmo-skoleni
```

Po instalaci restart Claude Code (nebo `/reload-plugins`), pak
`/skoleni-start`. Novou verzi stáhne `claude plugin marketplace update
rellmo-skoleni` a `claude plugin update rellmo-skoleni@rellmo-skoleni`.

## Jak je postavený

Skilly jsou tenké, práci dělají skripty ve `scripts/`. Skript se do modelu
nenačítá — běží mimo a model vidí jen jeho výsledek. Stav průchodu drží
`.skoleni/stav.json` v pracovní složce účastníka.

| Složka | Co v ní je |
|---|---|
| `skills/` | Pět skillů |
| `scripts/` | `stav`, `bezpecnost`, `prostredi`, `pluginy`, `web_znacka` — jen standardní knihovna |
| `references/navody/` | Devatenáct návodů krok za krokem |
| `references/reseni-problemu.md` | Osm situací, které se pokazí nejčastěji |
| `references/podklady/` | Katalog automatizací a prezentace ze školení |
| `assets/vzorovy-skill/` | Vzorový skill k rozkopírování |
| `assets/vzorovy-brandkit/` | Vzorový brandkit pro `/skoleni-brandkit` |
| `tests/` | Testy skriptů a formální kontroly skillů |

Cesty do `scripts/`, `references/` a `assets/` se ve skillech píšou jako
`${CLAUDE_PLUGIN_ROOT}/…`. Claude Code je dosazuje do obsahu skillu inline;
**nečti je přes `os.environ`** — do prostředí volaného pythonu se
neexportují. Hlídá to test.

Plugin nenese žádná ukázková data — je malý a instaluje se rychle i na
společné wifi.

## Za běhu

Python 3.9+ a jeho standardní knihovna (na macOS stačí ten z Command Line
Tools). Na Windows se Python často spouští jako `py` nebo `python` — `python3`
tam bývá jen odkaz do Microsoft Storu; skilly s tím počítají. `pytest` je
potřeba jen pro vývoj.

## Vývoj

```
python3 -m pip install -r requirements-dev.txt
python3 -m pytest
```

## Licence

LicenseRef-Rellmo-Commercial
