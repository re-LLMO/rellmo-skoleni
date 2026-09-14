# Katalog automatizací re:LLMO

Co je hotové, co to stojí a co to potřebuje na vstupu.

Ze školení ti zůstává **jeden plugin z tohohle katalogu zdarma podle vlastního
výběru** a **10 % sleva na ostatní**. Kontrola přístupu AI robotů je zdarma
pro všechny. Každý plugin se instaluje install příkazem, který přijde
e-mailem po objednání na rellmo.com — jeden příkaz přidá marketplace re:LLMO
a nainstaluje všechno, na co máš nárok. Co přesně máš nainstalované, vypíše
`claude plugin list`.

Spouštějí se tím, že o ně požádáš normální větou. Názvy příkazů si pamatovat
nemusíš.

Ceny jsou jednorázové, bez DPH, podle stavu na rellmo.com v září 2026.

---

## Web a technika

### Kontrola přístupu AI robotů · *zdarma*

Ověří, jestli se k tvému webu vůbec dostanou GPTBot, ClaudeBot, PerplexityBot,
Google-Extended a další. Rozebere `robots.txt` po jednotlivých botech, zkusí
HTTP přístup za každého z nich proti kontrolnímu prohlížeči, pozná blokaci na
CDN nebo firewallu, najde obsah dostupný až po vykreslení JavaScriptem,
projde vzorek typových stránek ze sitemapy a napíše HTML report.

**Potřebuje:** doménu. Nic víc, žádný účet.

**Kdy to sáhne nejhlouběji:** když server vrací 200 a `robots.txt` je v
pořádku, a přesto bot vidí skoro nic — protože se obsah načítá až
JavaScriptem. Tohle je nejčastější tichá závada, kterou běžný audit nevidí.

### Analýza crawlu (sf-analysis) · *2 000 Kč*

Z hotového crawlu ze Screaming Frogu udělá technický audit: pět analytických
okruhů naráz, výsledky do lokální databáze, report s tříděním podle
závažnosti. Umí i porovnání dvou crawlů — vhodné jako kontrola po migraci.

**Potřebuje:** crawl (`.seospider`, `.dbseospider`), nebo CSV exporty
z crawlu. Export z crawlu vyžaduje licencovaný Screaming Frog; **s hotovými
CSV exporty licenci nepotřebuješ.**

### Audit XML sitemap

Projde sitemapy a indexy sitemap, ověří strukturu a živý stav uvedených URL:
kód odpovědi, přesměrování, kanonizace, indexovatelnost.

**Potřebuje:** doménu nebo adresu sitemapy.

---

## Obsah a klíčová slova

### Kanibalizace klíčových slov · *1 000 Kč*

Najde dvojice stránek, které si na stejném dotazu konkurují. Porovnává denní
maximum dotazu s pokrytím po stránkách den po dni, takže jednorázové
prostřídání stránek ani dominanci jedné stránky nevyhodnotí jako
kanibalizaci. Potvrzené případy seskupí a ke každému navrhne řešení.

**Potřebuje:** Search Console, přibližně 90 dní dat.

### Příležitosti ze Search Console · *1 500 Kč*

Najde stránky a dotazy s největším prostorem k růstu. Vlastní CTR křivku
podle pozic si dopočítá z tvých dat (bez brandových dotazů), pak označí
propady prokliku oproti očekávání a dotazy těsně za hranicí viditelnosti.
Odhady uvádí jako dolní meze, ne jako sliby.

**Potřebuje:** Search Console, přibližně 90 dní dat.
**Nedělá:** rešerši nových klíčových slov. Optimalizuje, co už rankuje.

### Klasifikátor záměru vyhledávání · *webová aplikace, zdarma*

Ke každému českému vyhledávacímu dotazu přiřadí typ obsahu, který na něj má
odpovídat (vysvětlení, rychlá odpověď, výběr, nákup, navigace, lokální,
podpora). Vlastní model, běží bez API a bez kreditů za dotaz. Ukázka běží
rovnou, plný běh do 500 dotazů po zadání e-mailu:
https://rellmo.com/nastroje/klasifikator-zameru/

**Potřebuje:** seznam dotazů, jeden na řádek.

### Rozpad obsahu (content decay)

Najde stránky, jejichž výkon klesá, a k jednotlivým URL navrhne, co
aktualizovat.

**Potřebuje:** Search Console.

### Interní prolinkování

Audit interního prolinkování s návrhy odkazů: metriky odkazového grafu,
významové shlukování stránek, návrhy textů odkazů podle dat ze Search Console.

**Potřebuje:** crawl a Search Console.

---

## Odkazy a viditelnost

### Odkazové příležitosti · *2 000 Kč*

Najde a prověří domény, kam má smysl získat odkaz: mezera oproti konkurenci,
relevance, indexovanost, kontakt. Výstup je setříděný seznam s hodnocením
ano / možná / ne.

**Potřebuje:** DataForSEO.

### Audit viditelnosti v AI chatbotech

Zjistí, co o značce říká pět nástrojů (ChatGPT, Perplexity, Gemini, Google AI
Mode, Bing Copilot). Sbírá odpovědi na dvojice otázek — jednou směrem od
tématu, jednou směrem od značky — a rozděluje citované zdroje na vlastní
a získané. K tomu spolu-zmínky konkurence a tón odpovědí.

**Potřebuje:** placený přístup ke sběru dat.

---

## Co si postavíš sám

Nejčastější případ, na který nikdo hotový plugin nemá: tvoje vlastní data
v tvém vlastním systému. Když ten systém má API, stačí to.

- Postup v osmi krocích je v `navody/18-postup-vlastni-automatizace.md`, nebo
  rovnou `/skoleni-automatizace`.
- Anatomie skillu: `navody/07-anatomie-skillu.md`.
- MCP server nad vlastním API: `navody/03-mcp-servery.md`.

## Jak z toho udělat trvalý proces

Většina těchhle analýz dává smysl opakovaně, ne jednou. Postup je
v `navody/11-opakovane-behy.md`.
