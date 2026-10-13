# 04 — Pluginy a marketplace

## Tři pojmy

- **Skill** — složka se souborem `SKILL.md`. Návod pro Clauda: co dělat a
  kdy to dělat.
- **Plugin** — obal kolem jednoho nebo více skillů, s manifestem a verzí.
  Slouží k tomu, aby se skill dal rozdat a aktualizovat.
- **Marketplace** — seznam pluginů. Přidáš ho jednou a pak z něj instaluješ.

## Instalace marketplace a pluginu

```bash
claude plugin marketplace add <organizace>/<repozitar>
claude plugin marketplace list
claude plugin install <nazev-pluginu>@<nazev-marketplace>
```

Název marketplace vypíše `claude plugin marketplace list` — nemusí se
shodovat s názvem repozitáře.

Po instalaci **restart Claude Code**, nebo v běžící relaci `/reload-plugins`.
Slash commandy z pluginu se objeví až potom.

Ověření, že to sedlo:

```bash
claude plugin list
```

## Pozor na zastaralý postup

Pokud někde narazíš na `npx skills add …`, je to starší cesta. Dnešní
nativní postup je marketplace a `claude plugin install`.

## Automatizace re:LLMO

Instalují se install příkazem z e-mailu po objednání na rellmo.com (jeden
příkaz přidá marketplace `rellmo` a nainstaluje vše, na co máš nárok). Spouštějí
se tím, že o ně požádáš normální větou — nemusíš si pamatovat názvy příkazů.
Ceny a vstupy jsou v `podklady/katalog-automatizaci.md`.

| Plugin | Co dělá | Co k tomu potřebuje |
|---|---|---|
| kontrola přístupu AI robotů | Ověří, jestli se k tvému webu dostanou GPTBot, ClaudeBot a spol. — robots.txt po jednotlivých botech, HTTP sondy, detekce ochrany proti botům, direktivy v indexu. | jen doménu |
| kanibalizace klíčových slov | Najde dvojice stránek, které si na stejném dotazu konkurují, a řekne, co s nimi. | Search Console |
| příležitosti ze Search Console | Dotazy a stránky, kde je nejblíž k dalším proklikům. Vlastní CTR křivka podle tvého webu. | Search Console |
| analýza crawlu (sf-analysis) | Technický audit z hotového crawlu ze Screaming Frogu. | crawl nebo CSV exporty |


## Když se plugin nechce načíst

1. Restartoval jsi Claude Code po instalaci?
2. `claude plugin list` — je v seznamu?
3. Sedí název? Slash command vzniká z názvu skillu, ne z názvu pluginu.
4. `/help` vypíše všechny dostupné příkazy včetně těch z pluginů.

## Vzorový skill

V pluginu ze školení leží `assets/vzorovy-skill/` — hotový skill k
rozkopírování, když stavíš vlastní. Postup je v návodu 18.

## Bezpečnost

Plugin je spustitelný kód. Instaluj jen to, u čeho víš, kdo to napsal.
U cizích pluginů z veřejných zdrojů platí obvyklá opatrnost: podívej se do
repozitáře, kdo ho udržuje a kdy naposledy. Když si nejsi jistý, neinstaluj.
