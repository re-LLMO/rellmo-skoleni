# 02 — Terminál a pracovní složka

Tenhle návod je pro člověka, který terminál nikdy nepoužíval. Nic se tu
nenaučíš navíc — jen to, bez čeho Claude Code nedává smysl.

## Jediná věc, kterou musíš pochopit

Terminál je **vždy v nějaké složce.** Když v něm spustíš Claude Code, bude
pracovat s tou složkou: tam bude soubory číst a tam je bude ukládat. Nic
mimo ni sám neotevře.

Proto platí: **pro každou práci vlastní složka.** Jedna složka na jeden web,
jeden projekt, jednu analýzu. Ne plocha, ne Stažené soubory.

## Tři příkazy, které stačí

```bash
pwd          # ve které složce zrovna jsem
ls           # co v ní je
cd nazev     # přejdi do složky "nazev"
```

`cd ..` tě posune o úroveň výš. `cd ~` tě vrátí do domovské složky.

## Založit pracovní složku a spustit v ní Claude Code

```bash
mkdir ~/muj-web
cd ~/muj-web
claude
```

Na Windows v PowerShellu to funguje stejně, jen domovská složka se píše bez
vlnovky: `cd $HOME\muj-web`.

## Jak se do složky dostat, když ji vidíš v okně

Nemusíš cestu psát. Napiš `cd `, mezeru — a **přetáhni složku myší do okna
terminálu.** Cesta se doplní sama. Funguje na macOS i na Windows.

## Co v pracovní složce vzniká

| Soubor nebo složka | Co to je |
|---|---|
| `CLAUDE.md` | Kontext, který si Claude Code načte pokaždé na začátku. |
| `.gitignore` | Seznam souborů, které se nikdy nemají dostat na GitHub. |
| `.claude/skills/` | Tvoje vlastní skilly platné jen v téhle složce. |
| `.skoleni/stav.json` | Stav průchodu školením. Nesahej do něj ručně. |
| reporty, exporty | Výstupy analýz. |

Složky začínající tečkou běžný správce souborů skrývá. Na macOS je v Finderu
zobrazíš klávesovou zkratkou Cmd+Shift+tečka.

## Kdy je potřeba restart

Claude Code načítá některé věci **jen při startu**. Když jsi právě založil
`.claude/skills/`, nainstaloval plugin nebo přidal MCP server, zavři ho
(`/exit`) a spusť znovu ve stejné složce. Není to chyba, je to způsob, jakým
to funguje.

## Kopírování textu

V terminálu často nefunguje Ctrl+C — to je historicky signál „přeruš, co
běží". Kopíruj myší s Cmd+C (macOS) nebo Ctrl+Shift+C (Windows a Linux).
