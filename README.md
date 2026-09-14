# rellmo-skoleni

Průvodce školením **Claude Code pro markeťáky** (re:LLMO). Provede účastníka
půldnem — od nastavení prostředí po vlastní automatizaci zabalenou pro
kolegy. Po školení zůstává jako příručka. Je stejný pro každý běh školení.

## Co plugin umí

| Příkaz | Co udělá |
|---|---|
| `/skoleni-start` | Založí pracovní složku, doinstaluje superpowers a skill-creator, ověří prostředí, zapíše nástroje účastníka |
| `/skoleni-automatizace` | Provede stavbou vlastní automatizace v osmi krocích, včetně zabalení do pluginu a sdílení |
| `/skoleni-napoveda` | Příručka: návody 01–18, prezentace, katalog automatizací, řešení problémů. Funguje i dlouho po školení |
| `/skoleni-shrnuti` | Inventura dne a návrh jednoho opakovaně běžícího procesu |

## Instalace

Plugin se instaluje jedním příkazem s licenčním klíčem, který přijde
e-mailem:

```
curl -fsSL "https://dist.rellmo.com/install/<KLÍČ>?lang=cs" | sh
```

Po instalaci restart Claude Code, pak `/skoleni-start`.

## Jak je postavený

Skilly jsou tenké, práci dělají skripty ve `scripts/`. Skript se do modelu
nenačítá — běží mimo a model vidí jen jeho výsledek. Stav průchodu drží
`.skoleni/stav.json` v pracovní složce účastníka.

| Složka | Co v ní je |
|---|---|
| `skills/` | Čtyři skilly |
| `scripts/` | `stav`, `bezpecnost`, `prostredi`, `pluginy` — jen standardní knihovna |
| `references/navody/` | Osmnáct návodů krok za krokem |
| `references/reseni-problemu.md` | Sedm situací, které se pokazí nejčastěji |
| `references/podklady/` | Katalog automatizací a prezentace ze školení |
| `assets/vzorovy-skill/` | Vzorový skill k rozkopírování |
| `tests/` | Testy skriptů a formální kontroly skillů |

Cesty do `scripts/`, `references/` a `assets/` se ve skillech píšou jako
`${CLAUDE_PLUGIN_ROOT}/…`. Claude Code je dosazuje do obsahu skillu inline;
**nečti je přes `os.environ`** — do prostředí volaného pythonu se
neexportují. Hlídá to test.

Plugin nenese žádná ukázková data — je malý a instaluje se rychle i na
společné wifi.

## Za běhu

Python 3.11+ a jeho standardní knihovna. `pytest` je potřeba jen pro vývoj.

## Vývoj

```
python3 -m pip install -r requirements-dev.txt
python3 -m pytest
```

## Licence

LicenseRef-Rellmo-Commercial
