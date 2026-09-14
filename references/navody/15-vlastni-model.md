# 15 — Vlastní model místo API

Většinu práce v Claude Code dělá velký model přes API a platí se za každý
dotaz. Pro jednu přesně vymezenou úlohu, která se opakuje ve velkém, se
vyplatí něco jiného: malý model natrénovaný jen na tu úlohu, který běží na
tvém počítači a za dotaz neúčtuje nic.

## Kdy se to vyplatí

Všechny čtyři podmínky naráz. Když chybí jedna, zůstaň u API.

1. **Úloha je úzká a dá se popsat jako štítek.** Dotaz → jedna z několika
   kategorií. Ne „napiš text", ne „rozhodni, co dělat".
2. **Objem je velký.** Tisíce až miliony položek, ne desítky.
3. **Opakuje se.** Stejná úloha každý týden nebo u každého klienta.
4. **Máš z čeho trénovat.** Reálná data z provozu, ne vymyšlené příklady.

Typické kandidáty u markeťáka: třídění vyhledávacích dotazů, štítkování
produktů, klasifikace zpětné vazby nebo dotazů zákazníků.

## Co jsme postavili

Klasifikátor záměru českých vyhledávacích dotazů. Každému dotazu přiřadí
jednu z osmi kategorií: vysvětlení, rychlá odpověď, výběr, nákup nebo
objednávka, navigace na web, lokální hledání, zákaznická podpora, nejasné.

| | |
|---|---|
| Základ | `Seznam/small-e-czech`, 14 milionů parametrů, český tokenizer |
| Trénovací data | 3,3 milionu reálných dotazů za 12 měsíců, po očištění 1,9 milionu českých |
| Nasazený tvar | ONNX, 54 MB, 2–3 ms na dotaz na běžném procesoru |
| Přesnost | 84,8 % na 883 dotazech z webů, které model při tréninku neviděl |
| Srovnání | DataForSEO 50,1 % (kategorii má u všeho); Ahrefs podobná přesnost, ale kategorii vrátí jen u 30 % českých dotazů |

Srovnání je proti sadě správných odpovědí, kterou jsme sestavili sami podle
vlastních kategorií. Není to neutrální benchmark a takhle se to neprodává.

Běží jako webová aplikace: https://rellmo.com/nastroje/klasifikator-zameru/
Ukázka běží rovnou, plný běh do 500 dotazů po zadání e-mailu.

## Jak vznikl — postup, který jde zopakovat

**Učitel a student.** Ruční štítkování desítek tisíc dotazů nepřipadá v úvahu.
Velké modely dotazy oštítkují, malý model se z výsledku naučí totéž levně a
rychle.

1. **Dva levní učitelé, nezávisle.** Lokální model (Qwen 3, zdarma) a levný
   API model (Haiku) dostali stejný manuál a oštítkovali stejných 40 000
   dotazů. Shodli se v 75,7 % případů.
2. **Drahý rozhodčí jen na spory.** Sporných 9 727 dotazů rozsoudil silnější
   model (Sonnet). Nemusel projít celý objem, jen čtvrtinu.
3. **Sjednocující průchod.** Hodnotitelé aplikují manuál na hraniční případy
   různě; po každé vlně je potřeba průchod, který sjednotí čtení stejného
   vzoru.
4. **Sedm modelů do srovnání.** Favorit (307 milionů parametrů, tisíc jazyků)
   prohrál s malým českým modelem o necelý bod — a ten je 22× menší,
   8× rychlejší a běží bez grafické karty.

## Co si z toho odnést i bez trénování

**Testovací sada je jediná kotva — a musí projít stejnou kontrolou jako to,
co měří.** Tři kola jsme optimalizovali proti chybě ve vlastní testovací
sadě: hodnotitelé považovali za značku cokoli, co znělo jako název, včetně
překlepů. Po opravě 45 ze 114 štítků se pořadí modelů obrátilo. Totéž platí
pro každý eval skillu nebo pluginu: než z něj vyvodíš rozhodnutí, ověř sadu,
proti které měříš.

**Všechno, co zabralo, přišlo z lepších dat nebo lepšího postupu.** Šest
pokusů o chytrou úpravu výstupu (kalibrace jistoty, destilace, syntetická
data) skončilo bez zlepšení. Průběžná čísla z tréninku neříkají, jak model
dopadne na datech, která nikdy neviděl.

**Odmítnutá zkratka.** Model dlouho chyboval na holých názvech značek.
Nabízelo se přebít výstup seznamem známých značek. Neudělali jsme to —
seznam by fungoval jen pro značky na něm a nástroj by tvrdil jistotu, kterou
nemá. Radši ukázat, že si model není jistý, než nejistotu schovat za ručně
napsané pravidlo.

## Co k tomu potřebuješ

- **Data z provozu** — u dotazů Search Console, u produktů feed, u zpětné
  vazby export z podpory. Anonymizované, za dost dlouhé období (sezónnost).
- **Manuál pro štítkování** — jedna stránka s kategoriemi a hraničními
  případy. Píše se dřív než cokoli jiného a upravuje po každé vlně.
- **Počítač s běžným procesorem** na provoz; na trénink malého modelu stačí
  běžná grafická karta nebo pronajatý stroj na pár hodin.
- **Claude Code** na všechno kolem: skripty na čištění dat, štítkování přes
  API, vyhodnocení, porovnání modelů. Trénink sám je jeden skript.

Kdy naopak ne: když úloha vyžaduje úsudek nad textem, když se kategorie mění
každý měsíc, nebo když objem nepřesáhne pár set položek — tam je API
levnější než týden práce.
