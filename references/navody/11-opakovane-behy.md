# 11 — Z jednorázové analýzy opakovaný proces

Analýza, kterou uděláš jednou, zastará. Analýza, která běží sama, drží web
v kondici i ve chvíli, kdy máš jinou práci.

## Nejdřív rozhodni tři věci

1. **Co se hlídá a jak často.**
   Týdně to, co se mění po každém nasazení — kanibalizace klíčových slov,
   technické chyby z crawlu. Měsíčně to, co se mění pomalu — příležitosti
   ze Search Console, viditelnost v AI chatbotech, sitemapy.
2. **Kdy má přijít zpráva.**
   Ne po každém běhu. „Dej vědět, jen když přibude nová dvojice stránek,
   které si konkurují." Report, který chodí pokaždé, se po třech týdnech
   přestane číst.
3. **Kam.**
   Do souboru v repozitáři, do Slacku, mailem. Tam, kam se reálně díváš.

Bez těchhle tří vět je naplánovaný běh jen další zdroj šumu.

## Naplánovaný běh v Claude Code

Claude Code umí naplánované agenty (routines) běžící na cronu v cloudu.
Nastavují se příkazem:

```
/schedule
```

Průvodce se zeptá, co se má spouštět, jak často a co se stane s výsledkem.
Zadání pro naplánovaný běh musí být **soběstačné** — příští běh nebude mít
tenhle rozhovor. Piš tedy plné zadání: doména, property, co porovnat s čím,
kam uložit výsledek, kdy mlčet.

Existující plány se stejným příkazem vypisují a mění.

**Než na tom něco postavíš, ověř jednu věc.** Routines běží v cloudu, takže
záleží na tom, co je pro tvůj účet a verzi Claude Code zapnuté — a hlavně:
**MCP servery přidané lokálně přes `claude mcp add` se do cloudového běhu
nepřenášejí samy.** Když analýza stojí na napojeném serveru nebo na tokenu
uloženém ve tvé domovské složce, naplánuj nejdřív jeden zkušební běh a
podívej se, jestli doběhl. Když ne, jdi cestou níž.

## Když to má běžet na tvém počítači

Když se má analýza pouštět lokálně (třeba proto, že sahá na data, která
z firmy nesmí), použij plánovač operačního systému:

- **macOS a Linux:** `crontab -e`, jeden řádek na úlohu.
- **Windows:** Plánovač úloh (Task Scheduler), akce „spustit program".

V obou případech spouštíš skript, ne Claude Code interaktivně. Skript
připraví data a výsledek uloží; interpretaci si pak vyžádáš, když se na
to díváš.

## Vzory, ze kterých se dá vyjít

| Situace | Co hlídat | Jak často | Kdy dát vědět |
|---|---|---|---|
| E-shop s velkým katalogem | kanibalizace klíčových slov | týdně | jen při nové dvojici |
| Web pod regulací, pomalý vývoj | čitelnost pro AI boty, technický audit | měsíčně | při zhoršení oproti minule |
| Redakční provoz | příležitosti ze Search Console | měsíčně | vždy, jako podklad k plánu obsahu |
| Po migraci nebo redesignu | technický audit z crawlu | denně první týden | při každé nové chybě |

## Na co narazíš

- **Přihlášení vyprší.** Token do Search Console se obnovuje sám, ale když
  ho někdo odvolá, běh začne tiše selhávat. Ať zpráva chodí i při chybě,
  ne jen při nálezu.
- **Porovnání potřebuje minulý běh.** Ukládej výstupy tak, aby šly srovnat —
  jeden soubor na běh, v názvu datum.
- **Placené API stojí peníze i na pozadí.** U běhů nad DataForSEO si nastav
  limit a kontroluj kredit.
