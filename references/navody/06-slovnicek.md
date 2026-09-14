# 06 — Slovníček: skill, plugin, MCP server, subagent, hook

## Jak to do sebe zapadá

```
                  marketplace
                       │
                    PLUGIN   (.claude-plugin/plugin.json)
        ┌──────────┬────────┬────────┐
      skilly     agenti    hooky     MCP
        │
   ┌────┴─────┬──────────┐
references  scripts   assets
```

Plugin obaluje skilly. Skill obsahuje instrukce. Všechno ostatní je
volitelný doplněk.

## Skill — recept v markdownu

Složka se souborem `SKILL.md`. Říká **co dělat** a **kdy to dělat**. Nahoře
YAML frontmatter (metadata), pod ním tělo — instrukce, příklady, rozhodovací
stromy.

Doporučená délka **pod 500 řádků**. Co se tam nevejde, jde do `references/`
a načte se, až když je potřeba.

## Plugin — kuchařka s recepty

Obal pro rozdávání a verzování jednoho nebo více skillů. Má manifest
`plugin.json` s verzí a jménem.

- **Distribuce:** jeden příkaz `claude plugin install`.
- **Verzování:** `version: 1.2.0`, dá se aktualizovat.
- **Jmenný prostor:** `rellmo:cannibalization` — dva pluginy si můžou
  pojmenovat skill stejně a nekoliduje to.

## MCP server — dodavatel surovin

Skill je recept, MCP server dodává ingredience: data a nástroje z vnějších
služeb. DataForSEO, Search Console, GitHub, Slack, vlastní CRM.

Když má nástroj jméno, uváděj ho celé i se serverem (`dataforseo:serp_organic`).
Když běží víc serverů naráz, bez prefixu se model netrefí.

## Subagent — kolega s vlastním stolem

Samostatný agent s vlastním zadáním, vlastním omezeným seznamem nástrojů,
často levnějším modelem — a hlavně **s vlastním čistým kontextem**. Rodiči
vrátí jen shrnutí, ne celý průběh.

K čemu to je: hlavní agent zůstane dispečer. Když deset subagentů projde
deset stránek, hlavnímu kontextu se to nenaplní deseti stránkami HTML.

## Hook — automatická past na událost

Spustí se sám, když nastane událost: po zápisu souboru, po dokončení úkolu,
při startu relace. Hodí se na formátování, notifikace, načtení přístupů.

Hook má věci jen vylepšovat. Nikdy na něm nestav něco, bez čeho skill
nefunguje — nemusí se spustit všude.

## Slash command — zkratka `/<jmeno>`

Napíšeš `/skoleni-start` a spustí se skill toho jména.

**Skilly a slash commandy jsou dnes jedna věc.** Dřív to byly dva mechanismy
(`.claude/commands/x.md` a `.claude/skills/x/SKILL.md`); dnes obojí dělá
`/x`. Existující commandy fungují dál. Rozdíl je jen v tom, že ke skillu
můžeš přiložit soubory a skripty — a že si ho model může vyvolat sám, když
popis sedne na situaci.

## Tři typy skillů

| Typ | K čemu | Příklad |
|---|---|---|
| Tvorba dokumentů a výstupů | Konzistentní kvalitní výstup pokaždé | prezentace ve firemní značce, report do PDF |
| Automatizace postupu | Vícekrokový proces s metodikou | audit crawlu, rešerše ke článku |
| Nástavba nad MCP | Naučit Clauda používat existující server lépe | pravidla, jak číst data z tvého CRM |

## Hlavní princip

Když dvě cesty vedou ke stejnému výsledku, vyber tu s méně pohyblivými
součástkami a bližší tomu, jak to dělá většina. Vlastní vynálezy se za půl
roku neudržují.
