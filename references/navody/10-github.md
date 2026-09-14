# 10 — GitHub pro člověka, který ho nikdy nepoužíval

## Čtyři pojmy

| Pojem | Věta, která stačí |
|---|---|
| **repozitář** | Složka na GitHubu, která si pamatuje každou verzi toho, co v ní je. |
| **commit** | Uložený stav se jmenovkou. |
| **větev** | Kopie, ve které zkoušíš změnu, aniž bys sáhl na to, co funguje. |
| **pull request** | Žádost „koukni na to a vezmi si to k sobě". Místo, kde proběhne kontrola. |

Víc nepotřebuješ. Claude Code obsluhu zvládne sám; tyhle čtyři pojmy
potřebuješ jen k tomu, abys věděl, o čem mluví.

## `gh` a MCP server nejsou dvě varianty téhož

| | GitHub CLI (`gh`) | GitHub MCP server |
|---|---|---|
| Co to je | Program na tvém počítači | Most na GitHub API |
| Pracuje se soubory na disku | ano | ne |
| Stáhne repozitář k tobě | **ano** | ne |
| Pošle tvoje změny | **ano** | jen jednotlivé soubory |
| Přečte soubor bez stahování | ano | ano |
| Založí issue, otevře pull request | ano | ano |

**`gh` potřebuješ vždycky.** Bez něj si Claude nestáhne repozitář na disk
a nemůže na něm pracovat. MCP server je doplněk pro rychlé nahlédnutí.

## Instalace `gh`

**Windows:**

```
winget install -e --id GitHub.cli
```

Pak **zavři terminál a otevři nové okno.** Ne novou záložku — mění se `PATH`
a v původním okně `gh` nenajdeš. (Pozor: `winget install gh` bez `-e --id`
nainstaluje něco jiného.)

**macOS** — přes Homebrew. Většina lidí ho nemá, takže nejdřív on:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Instalátor se ptá: potvrdíš klávesou Return a zadáš heslo k počítači. Až
doběhne, přidej Homebrew do cesty — na Apple Silicon se to samo nestane:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Teprve pak:

```bash
brew install gh
```

**Linux:**

```bash
sudo apt-get install -y gh
```

## Přihlášení

```bash
gh auth login
```

Průchod: **GitHub.com → HTTPS → Login with a web browser → opsat jednorázový
kód.** Otevře se prohlížeč, vložíš kód, potvrdíš.

Ověření:

```bash
gh auth status
```

## Publikace vlastního skillu

```bash
cd <složka se skillem>
git init
git add .
git commit -m "první verze skillu"
gh repo create <nazev> --private --source=. --push
```

**Než poprvé commitneš, zkontroluj, co v tom commitu bude:**

```bash
git status --porcelain --untracked-files=all
```

Hledej cokoli s `token`, `secret`, `key`, `.env`, `.csv`, `.duckdb`.
Když tam něco takového je, doplň to do `.gitignore` a zkontroluj znovu.
Jednou commitnutý klíč zůstane v historii repozitáře i po smazání souboru.

## Změna přes větev a pull request

```bash
git checkout -b uprava-popisu
# … úprava souboru …
git add . && git commit -m "přesnější popis"
git push -u origin uprava-popisu
gh pr create --fill
gh pr view --web
```

Na záložce se změnami uvidíš zeleně přidané a červeně odebrané řádky. To je
celý smysl pull requestu: změna je vidět dřív, než se použije.

Sloučení:

```bash
gh pr merge --squash --delete-branch
```

## Instalace cizího skillu

```bash
gh repo clone <ucet>/<nazev> ~/.claude/skills/<nazev>
```

Po stažení **restart Claude Code**. Nová složka ve `.claude/skills/` se načte
až při startu.

## Když nemáš práva

Firemní GitHub bývá pod správou IT s vypnutým zakládáním repozitářů. Pořadí,
co zkusit:

1. Vlastní osobní účet. Na principu se nemění nic.
2. Registrace osobního účtu na `github.com`, když ho nemáš.
3. Když ani to nejde, projdi celý postup lokálně: `git init`, commit, větev,
   druhý commit, `git log --oneline`, `git diff <výchozí>..uprava-popisu`.
   Uvidíš historii i změnu, jen to nikam neodejde. Doma pak stačí
   `gh auth login` a poslední dva příkazy.

   Jak se výchozí větev jmenuje, zjistíš hned po prvním commitu přes
   `git branch --show-current` — podle verze gitu je to `main`, nebo
   `master`. Nedomýšlej si to; s nesprávným názvem `git diff` skončí chybou.

## Když se něco nepovede

| Co se děje | Co s tím |
|---|---|
| `gh: command not found` | Zavři terminál, otevři **nové okno**. |
| `brew: command not found` | Chybí ty dva řádky s `~/.zprofile` výš. |
| `Permission denied` při push | Nemáš právo do toho repozitáře. Publikuj pod vlastní účet. |
| Kolega repozitář nevidí | Je privátní. Přidej ho jako spolupracovníka, nebo přepni na veřejný — ale jen když v něm není nic firemního. |
