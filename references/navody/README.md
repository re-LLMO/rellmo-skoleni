# Návody ze školení Claude Code pro markeťáky

Osmnáct souborů, každý na jedno téma. Nemusíš je číst v pořadí — otevři ten,
který zrovna potřebuješ. Nebo se rovnou zeptej: `/skoleni-napoveda`.

| Soubor | Kdy ho otevřít |
|---|---|
| `01-instalace-a-prvni-spusteni.md` | Instaluješ Claude Code na další počítač. |
| `02-terminal-a-pracovni-slozka.md` | Nevíš, kde vlastně jsi a kam se ukládají soubory. |
| `03-mcp-servery.md` | Chceš napojit další nástroj — a nejdřív zjistit, jestli má smysl. |
| `04-pluginy-a-marketplace.md` | Instaluješ plugin nebo marketplace. |
| `05-search-console.md` | Napojuješ Search Console na jiném počítači nebo pro jinou doménu. |
| `06-slovnicek.md` | Pletou se ti pojmy skill, plugin, MCP server, subagent, hook. |
| `07-anatomie-skillu.md` | Píšeš vlastní skill a chceš, aby k něčemu byl. |
| `08-testovani-skillu.md` | Skill máš, ale nespouští se nebo dělá něco jiného. |
| `09-mcp-nebo-skript.md` | Rozhoduješ se, odkud si skill vezme data, a kam dát klíč. |
| `10-github.md` | Sdílíš skill s kolegou nebo si stahuješ cizí repozitář. |
| `11-opakovane-behy.md` | Chceš, aby se analýza spouštěla sama každý týden. |
| `12-html-do-pdf.md` | Máš HTML report a potřebuješ z něj PDF do mailu. |
| `13-status-line.md` | Chceš v terminálu vidět, kolik kontextu ti zbývá. |
| `14-superpowers.md` | Chceš pracovat metodicky: plan mode, nejdřív rozmyslet, pak dělat. |
| `15-vlastni-model.md` | Rozhoduješ se, jestli na úzkou úlohu vzít API, nebo vlastní model. |
| `16-reporty-z-vice-zdroju.md` | Skládáš pravidelný report z více zdrojů a chceš ho ve firemní značce. |
| `17-agentni-systemy.md` | Narazil jsi na Hermes, Paperclip a „agenty“ a chceš vědět, co to pro tebe znamená. |
| `18-postup-vlastni-automatizace.md` | Chceš si postavit další automatizaci a chceš postup, ne inspiraci. |

## Odkud to je

Většina textu vychází z interních návodů Effectixu (autoři Jakub Sinčák
a Lukáš Kostka, březen až červen 2026), přepsaných pro člověka mimo Effectix
a **prověřených k 14. 9. 2026**. Tři věci se oproti původním návodům změnily:

- Skilly se dnes instalují přes marketplace a `claude plugin install`,
  ne přes `npx skills add`.
- Příkazy `/ultraplan` a `/goal` v Claude Code neexistují; návod, který je
  popisoval, tady není.
- Tvrzení, že MCP server spotřebuje desítky tisíc tokenů, jen když se načte,
  dnes obecně neplatí — viz `03-mcp-servery.md`.
