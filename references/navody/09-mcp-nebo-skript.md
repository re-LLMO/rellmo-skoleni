# 09 — MCP server, nebo skript? A kam s klíči

## Rozhodnutí, které vypadá technicky a není

Když skill potřebuje data zvenčí, má dvě cesty: **říct si o ně MCP serverem**,
nebo **stáhnout je skriptem**. Rozdíl není v tom, co je modernější, ale
v tom, kudy ta data protečou.

- **MCP nástroj** — odpověď přijde do rozhovoru. Model ji vidí celou.
- **Skript** — běží mimo, výsledek si uloží na disk, modelu vrátí, co si
  vyžádá. Do rozhovoru jde pět řádků místo deseti tisíc.

## Kdy co

| Situace | Volba | Proč |
|---|---|---|
| Model se za běhu rozhoduje, co dál | **MCP** | Potřebuje ta data vidět, aby se rozhodl. |
| Znám postup a stahuju velký objem | **skript** | Determinismus a průtok. Model to nemusí vidět celé. |
| Výstup přesahuje pár tisíc řádků | **skript** | MCP naráží na strop výstupu. |
| Nástroj má běžné CLI (`git`, `gh`) | **CLI** | Claude s ním umí pracovat rovnou. |
| Nástroj nemá CLI (Figma, CRM) | **MCP** | Jiná cesta není. |
| Stejný nástroj používá pět skillů | **MCP** | Přihlášení se řeší jednou pro všechny. |
| Máš obojí | **kombinace** | Skriptem naber a ulož, MCP nebo model se pak ptá lokálních dat. |

## Kombinovaný vzor

Tenhle vzor stojí za většinou našich analytických pluginů:

```
skript stáhne data              →  soubory na disku
skript je zpracuje              →  lokální databáze
model se ptá databáze           →  dostane výsledky, ne surová data
```

Na crawlu o statisících řádků je rozdíl mezi „model to vidí celé" a „model
vidí odpověď na dotaz" řádový. Zásada: **výpočet nikdy v promptu, práce se
soubory nikdy přes MCP.**

## Co dnes o kontextové ceně MCP platí

Starší materiály tvrdí, že každý připojený MCP server ukousne desítky tisíc
tokenů, ještě než začneš pracovat. **Dnes to obecně neplatí** — Claude Code
má ve výchozím stavu zapnuté vyhledávání nástrojů a definice se načítají až
při použití.

Argument pro skript proto nestojí na tom, kolik stojí připojení serveru,
ale na **objemu výstupu, determinismu a průtoku**.

## Kam s klíči

Klíč nikdy nepiš přímo do `SKILL.md`, do skriptu ani do souboru, který může
skončit na GitHubu.

**V pluginu** se to řeší přes `userConfig` v manifestu:

```json
"userConfig": {
  "dataforseo_password": {
    "type": "string",
    "title": "DataForSEO API password",
    "sensitive": true,
    "required": true
  }
}
```

Claude Code se při instalaci zeptá, `sensitive: true` uloží hodnotu do
systémové klíčenky (ne do `settings.json`) a skript ji čte z proměnné
prostředí:

```python
os.environ["CLAUDE_PLUGIN_OPTION_DATAFORSEO_PASSWORD"]
```

**U MCP serveru** se přihlašovací údaje předávají při přidání:

```bash
claude mcp add dataforseo -e DATAFORSEO_USERNAME=… -e DATAFORSEO_PASSWORD=… -- npx -y dataforseo-mcp-server
```

**Ve vlastní pracovní složce** stačí soubor `.env` a řádek `.env`
v `.gitignore`. Pravidlo: než poprvé cokoli commitneš, zkontroluj
`git status --porcelain -uall` a projdi, co v tom seznamu je.

## Než něco odešleš

Chybové hlášky a výpisy stavu často obsahují token. Než je někam zkopíruješ
nebo vložíš do issue, přečti si je. V pluginu ze školení je na to funkce
`bezpecnost.maskuj()`.
