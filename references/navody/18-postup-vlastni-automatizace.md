# 18 — Postup vlastní automatizace v osmi krocích

Stejný postup, jakým tě na školení vedl `/skoleni-automatizace`. Tady je
samostatně, aby šel zopakovat doma na další úkol — s otázkami, které si má
člověk v každém kroku položit. Když chceš, ať tě vede Claude Code, spusť
`/skoleni-automatizace`; skill naváže i na rozdělanou práci.

## 1. Pojmenuj opakovaný úkol

Co děláš každý týden nebo měsíc ručně a pokaždé stejně?

Dobrý kandidát: **opakuje se**, **postup znáš zpaměti**, **vstup je pokaždé
podobný** (jiná data, stejný tvar). Špatný kandidát: jednorázová věc, nebo
úkol, u kterého pokaždé rozhoduješ jinak.

Otázky: Kolikrát za měsíc to dělám? Kolik minut to trvá? Dělá to ještě někdo
další stejně?

## 2. Zadání

Co je vstup, co je výstup a podle čeho poznám, že je to správně?

Pět minut ušetřených na zadání se vrací jako hodina oprav. Nech se
vyptávat: v Claude Code spusť skill `brainstorming` ze superpowers (návod
14) nebo zapni plan mode a popiš úkol. Odpovídat na konkrétní otázky je
snazší než napsat úplné zadání dopředu.

Výsledek jsou čtyři věty: **vstup**, **výstup**, **hotovo, když**, **co se
liší mezi běhy**.

## 3. Zúžení zadání

Je v zadání „a" mezi dvěma různými úkoly?

„Stáhne data, napíše k nim komentář a rozešle to týmu" jsou tři skilly, ne
jeden. Rozsah je to, na čem skilly nejčastěji selhávají — ne chybějící
znalost nástroje. Jeden skill = **jeden vstup, jeden výstup**.

Otázka, která pomáhá: *Kdybych to musel spustit hned teď, na jeden vstup, co
by vzniklo jako první?* To stavíš. Zbytek si zapiš jako „na příště".

## 4. Data: MCP, skript, nebo žádná

Odkud si skill vezme data — a potřebuje vůbec nějaká?

| Situace | Volba |
|---|---|
| Nevíš přesně, co v datech hledáš; zkoumáš | **MCP** — model se rozhoduje za běhu |
| Postup znáš, stahuješ objem, opakuje se | **skript** — deterministické, model dostane výsledek, ne deset tisíc řádků |
| Vstupem je text, obrázek, dokument | **žádná** — není co stahovat |

Obvyklý vývoj: prozkoumáš přes MCP, postup se ustálí, převedeš ho na skript.
Podrobně v návodu 09; klíče k API do proměnné prostředí, nikdy do skillu.

## 5. Kostra

Co patří do `SKILL.md`, co do `references/`, `assets/` a `scripts/`?

- **`SKILL.md`** — jediné, co model čte pokaždé. Krátké, jen to, co je
  potřeba vždy.
- **`references/`** — delší text čtený jen občas (pravidla, metodika).
- **`assets/`** — soubory, které model nečte, jen použije (logo, šablona).
- **`scripts/`** — mechanická práce s daty; běží mimo model.

Kostru nemusíš psát ručně. Dvě rovnocenné cesty: skill `writing-skills` ze
superpowers, nebo `skill-creator` od Anthropicu. Obojí máš nainstalované ze
školení. Když chceš jen vidět hotový tvar, zkopíruj vzorový skill z pluginu
(`assets/vzorovy-skill/`). Anatomie skillu do detailu: návod 07.

Tělo piš jako **konkrétní pokyny**, ne popis role: ne „analyzuje data", ale
„spusť `scripts/stahni.py` s adresami ze vstupu, z `podklad.md` vytáhni…".
Nástroje, které tělo používá, zapiš do `allowed-tools`.

## 6. Popis (`description`) jako rozhodovací věta

Podle čeho Claude Code pozná, že má skill spustit?

Popis není shrnutí toho, co skill dělá. Je to jediná věta, kterou Claude
Code čte, když se rozhoduje, jestli skill vůbec otevřít. Tři kontroly:

1. Začíná situací, kdy se má spustit („Použij, když…"), ne funkcí.
2. Obsahuje slova, která bys sám napsal do chatu.
3. Neopakuje celý postup — jinak si model myslí, že už ví, co dělat, a tělo
   nečte.

## 7. Zkouška naostro

Funguje to na jednom malém vstupu?

Jedna adresa, jeden soubor, pět položek. Napiš žádost tak, jak bys ji napsal
kolegovi. Když se skill nespustí sám, vyvolej ho jménem — zúží to problém na
popis. Když ho Claude Code nenajde ani jménem, restart ve stejné složce a
kontrola, že `name` sedí se jménem složky (návod 08).

Když spadne: **nezkoušej to opakovaně**. Jedno selhání stačí k rozhodnutí.
Zúž rozsah na nejmenší verzi, která projde, a tu zkus znovu. Bez jediného
úspěšného běhu skill není hotový.

## 8. Zabalení a sdílení

Spustí to kolega bez tebe?

Skill v `.claude/skills/` funguje jen v té složce a jen tobě. Plugin je totéž
zabalené k instalaci jedním příkazem: složka s `.claude-plugin/plugin.json`
(název, verze, popis) a `skills/<jmeno>/`. Před sdílením zkontroluj obsah —
žádné klíče, exporty, zákaznická data (`.gitignore` a kontrola souborů).

Sdílení přes GitHub: repozitář, commit, kolega si přidá marketplace a
nainstaluje plugin (návody 10 a 04). GitHub je nadstavba — plugin jde poslat
i jako složka. Verzi zvedni pokaždé, když má kolega dostat změnu.

## A pak

Až skill třikrát proběhne bez zásahu, je kandidát na naplánovaný běh (návod
11). A další úkol začíná zase krokem 1.
