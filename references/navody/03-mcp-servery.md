# 03 — MCP servery: co to je, kdy je chtít, jak je přidat

## Co MCP server je

Most mezi Claude Code a nějakou službou. Search Console, DataForSEO, GitHub,
Slack, tvoje CRM. Bez něj se Claude ke službě nedostane; s ním si o data
řekne sám, když je potřebuje.

Skill říká **co dělat**. MCP server dodává **s čím**.

## Kolik to stojí kontextu — co dnes platí

Delší dobu se mezi lidmi drží pravidlo „každý MCP server ti sežere desítky
tisíc tokenů, ještě než začneš pracovat". **Dnes to obecně neplatí.**
Claude Code má ve výchozím stavu zapnuté vyhledávání nástrojů (tool search) —
na začátku se načtou jen jména nástrojů a instrukce serveru, celé definice
se dotahují až ve chvíli, kdy jsou potřeba. Přidání dalšího serveru má na
kontextové okno malý vliv.

Stará poučka platí jen ve zvláštních případech: s vypnutým vyhledáváním
nástrojů (`ENABLE_TOOL_SEARCH=false`), s vlastní `ANTHROPIC_BASE_URL`,
u modelů starších než generace 4.5 v Google Cloud a přes Microsoft Foundry,
který vyhledávání nástrojů odmítá — Claude Code pak nástroje načte předem.

**Kde kontext opravdu bolí, je výstup.** Když si nástroj řekne o deset tisíc
řádků dat, projdou ti kontextovým oknem celé. Claude Code varuje nad
10 000 tokeny výstupu a výchozí strop je 25 000 tokenů (mění se proměnnou
`MAX_MCP_OUTPUT_TOKENS`); jednotlivý nástroj smí přes `anthropic/maxResultSizeChars`
dojít až na 500 000 znaků. Řešení není méně serverů, ale filtrovat dřív —
viz `09-mcp-nebo-skript.md`.

## Jak zjistit, co máš napojené

```bash
claude mcp list
```

U každého serveru uvidíš stav: připojeno, čeká na přihlášení, selhalo.

## Jak přidat server

Většina serverů má na svém webu hotový příkaz. Obecný tvar:

```bash
claude mcp add <nazev> -e KLIC=hodnota -- npx -y <balicek>
```

Server přes HTTP se přidává jinak:

```bash
claude mcp add --transport http <nazev> --scope user <url>
```

Po přidání **zavři a znovu spusť Claude Code.** Server se objeví mezi
nástroji až po restartu.

## Kdy MCP server nechtít

- **Když nástroj má běžné CLI** (`git`, `gh`, `aws`). Claude Code s ním umí
  pracovat rovnou.
- **Když z něj taháš velké objemy dat.** Skript je stáhne, zpracuje na disku
  a modelu vrátí pět řádků.
- **Když ho použiješ jednou za měsíc.** Přidej ho, až bude potřeba.

## Když server pro tvůj nástroj neexistuje

Stačí, aby ten nástroj měl API. Skill `mcp-builder` od Anthropicu z API
postaví MCP server: provede rešerší dokumentace, návrhem nástrojů, kódem
(Python nebo TypeScript) i testem. Je v pluginu `example-skills`:

```bash
claude plugin marketplace add anthropics/skills
claude plugin install example-skills@anthropic-agent-skills
```

Pak stačí říct „postav MCP server pro <nástroj>, dokumentace je na <adresa>". My jsme takhle udělali
server nad interním CRM — dokumentace API na vstupu, funkční server na
výstupu.

## Bezpečnost

MCP server je kód, který běží na tvém počítači a má přístup k tvým datům.
Než nějaký přidáš:

- Podívej se, kdo ho vydává. Oficiální server od výrobce služby má přednost
  před komunitním.
- Přístup dej co nejužší. Ke Search Console stačí čtecí oprávnění.
- Klíče nikdy nepiš do souboru, který může skončit na GitHubu. Jak na to,
  je v `09-mcp-nebo-skript.md`.
- Ve firmě se zeptej, jestli pro přidávání MCP serverů nemáte pravidlo. Bývá.
