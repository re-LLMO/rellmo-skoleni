# 19 — Brandkit: značka jako soubory, které umí číst model

## Co to je

Brandkit je složka souborů, ve které je značka popsaná tak, aby ji uměl
použít člověk i model: barvy, písmo, logo, pravidla, hotové CSS proměnné.
Není to skill. Skill se značkou (návod 16) na brandkit odkazuje a nic z něj
neopisuje. Když se změní logo, mění se jeden soubor v brandkitu a všechny
skilly, reporty a prezentace to převezmou.

Vzor se strukturou a vyplňovacími místy je v pluginu:
`assets/vzorovy-brandkit/`. Skládá se z devíti částí:

| Soubor | Co v něm je |
|---|---|
| `README.md` | obsah, odkud se plní, rychlý přehled |
| `colors.md` | paleta, hlavní a vedlejší, co značka NENÍ |
| `typography.md` | písmo, řezy, poměry velikostí, řádkování |
| `logo.md` | varianty, rozhodovací strom, ochranná zóna, zakázané úpravy |
| `brand-identity.md` | claim, hodnoty, tón, vzory stran |
| `tokens.css` | totéž jako CSS proměnné pro HTML dokumenty |
| `corrections.md` | co se změnilo po ověření proti manuálu |
| `fonts/`, `logo/` | písmo k self-hostingu, soubory loga |
| `examples/` | jeden až dva schválené výstupy |

## Postup

### 1. Shromáždi zdroje

Tři druhy, v tomhle pořadí důležitosti:

1. **Oficiální brand manuál** (PDF od grafika). Zdroj pravdy.
2. **Reálné výstupy**: master prezentace, web, poslední tři nabídky nebo
   reporty. Ukazují, jak se manuál používá, a kde se od něj odchyluje.
3. **Lidé, kteří značku hlídají.** Tři otázky: nejčastější chyba, co nikdy,
   co je nedotknutelné.

Když manuál nemáš, začni z výstupů a do `README.md` napiš, že brandkit je
odvozený, ne oficiální. Až manuál přijde, projde kolem 3.

### 2. Nech model vytěžit zdroje do souborů

Zkopíruj vzor do vlastní složky a dej modelu manuál (PDF umí přečíst) plus
odkaz na vzor:

> Vyplň soubory v `brandkit/` podle `manual.pdf`. Ke každé hodnotě napiš
> stranu manuálu, odkud je. Co v manuálu není, nech v hranatých závorkách
> a napiš to do seznamu otevřených otázek na konec `README.md`.

Trvej na odkazu na stranu. Bez něj se do brandkitu dostanou hodnoty, které
model odhadl z prezentace, a v kole 3 je nejde dohledat.

### 3. Ověř proti manuálu a zapiš rozdíly

Tohle je krok, který se přeskakuje nejčastěji, a je nejdůležitější. První
extrakce má vždycky chyby: barva z ukázkových dat v prezentaci se zapíše
jako brand akcent, náhradní písmo se odhadne, řádkování se nechá volné.

Projdi soubory vedle manuálu, stranu po straně, a každý rozdíl zapiš do
`corrections.md`: co, před, po, důvod, strana. Tenhle soubor je pojistka,
aby se stará verze nevrátila z něčí paměti nebo ze starého dokumentu.

Ověřuje člověk, ne model. Model může připravit tabulku rozdílů, rozhodnout
musí ten, kdo značku hlídá.

### 4. Doplň písmo a loga

- `fonts/`: soubory písma (woff2) a `fonts.css` s `@font-face` na každý
  řez. Nejdřív ověř licenci; komerční písmo často nesmí do repozitáře, pak
  sem patří jen `fonts.css` a soubory si každý doplní ze svého účtu.
- `logo/`: všechny oficiální varianty jako SVG, pojmenované podle
  `logo.md`. Nic neupravuj ručně, varianty od grafika nebo z manuálu.
- `tokens.css`: zkontroluj, že hodnoty sedí s `colors.md` a
  `typography.md`. Když se liší, platí manuál.

### 5. Přidej ukázkový výstup

Vyrob jeden dokument (report, jedna strana) s `tokens.css`, nech ho
schválit tím, kdo značku hlídá, a ulož do `examples/`. Skill se značkou pak
říká: „vyrob to jako `examples/report.html`, jen s jiným obsahem". Vzor
drží konzistenci líp než seznam pravidel.

### 6. Napoj skill se značkou

Ve skillu (vzor `assets/vzorovy-skill/`) nahraď vlastní pravidla odkazem:

- v `SKILL.md` jen to, co model potřebuje pokaždé: cesta k brandkitu, tři
  nejdůležitější pravidla, cesta k ukázce;
- `references/znacka.md` → místo něj odkaz na `brandkit/brand-identity.md`
  a `colors.md`, načítají se až při psaní;
- `assets/` → logo bere z `brandkit/logo/`, CSS z `brandkit/tokens.css`.

Brandkit může ležet vedle skillu, nebo jako samostatný repozitář, který si
skill naklonuje. Samostatný repozitář se vyplatí, jakmile ho používá víc
než jeden skill.

### 7. Sdílej a verzuj

Brandkit patří do repozitáře (návod 10) s vlastní verzí. Změna značky =
nová verze + řádek v `corrections.md`. Kolegové aktualizují jedním
příkazem, nikdo neopisuje hex kódy z e-mailu.

## Kontrola, že to funguje

1. Vyrob dva různé dokumenty (report a nabídka) dvěma různými skilly, které
   oba odkazují na brandkit.
2. Polož je vedle sebe a vedle `examples/`. Když se liší v barvě, písmu
   nebo logu, chyba je v brandkitu (nedostatečně jednoznačné pravidlo), ne
   ve skillu.
3. Změň jednu hodnotu v `tokens.css` a vyrob dokument znovu. Změna se musí
   propsat bez zásahu do skillu.

## Časté chyby

- **Barva z dat v grafu jako brand barva.** Do `colors.md` patří i oddíl
  „co NENÍ brand barva".
- **Písmo z CDN v dokumentu ke klientovi.** Self-hosting, viz `fonts/`.
- **Pravidla bez zdroje.** Každá hodnota má stranu manuálu, nebo je
  označená jako odvozená.
- **Brandkit opsaný do každého skillu.** Pak se mění na pěti místech.
  Odkazuj, neopisuj.
