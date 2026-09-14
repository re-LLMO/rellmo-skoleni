# Řešení problémů

Sedm situací, které se pokazí nejčastěji. Každá má stejnou stavbu: **příznak,
příčina, co udělat, kde si ověřit, že to zabralo.**

Když tvůj příznak nesedí ani na jednu z nich, není to důvod k panice —
příručka není vyčerpávající seznam. Popiš, co vidíš, a řeš to jako každý
jiný problém.

---

## 1. Chybí doména ve stavu

**Příznak.** Skill ze školení se ptá na doménu pokaždé znovu, nebo běží nad
jinou, než čekáš.

**Příčina.** V `.skoleni/stav.json` není `domena` — buď jsi `/skoleni-start`
nedoběhl do konce, nebo sedíš v jiné pracovní složce než tehdy.

**Co udělat.**

```bash
pwd
cat .skoleni/stav.json
```

Když soubor neexistuje, jsi v jiné složce. Přejdi do té původní. Když
existuje a `domena` je `null`, pusť `/skoleni-start` znovu — doplní jen to,
co chybí, nic nepřepíše.

**Ověření.** `python3 -c "import json;print(json.load(open('.skoleni/stav.json'))['domena'])"`

---

## 2. Není přístup do Search Console

**Příznak.** V seznamu property tvoje doména není. Nebo tam je, ale každý
dotaz skončí chybou 403.

**Příčina.** Buď ti přístup nikdo nedal, nebo ho máš na úrovni
`siteUnverifiedUser` — ta je v seznamu vidět, ale data nevrací.

**Co udělat.**

1. Zkontroluj, kterým účtem jsi přihlášený. Přihlášení jde vyvolat znovu
   a nahradí předchozí token.
2. Napiš vlastníkovi property, ať tě přidá. Stačí úroveň omezeného
   uživatele, plný přístup není potřeba.
3. **Než ti přístup dá,** pracuj s tím, co máš — export z rozhraní Search
   Console (CSV) je pro většinu analýz dostačující vstup. Napojení bez Cloud
   Console popisuje `navody/05-search-console.md`.

**Ověření.** Property je v seznamu a testovací dotaz na posledních 7 dní
vrátí řádky.

---

## 3. Web blokuje crawl

**Příznak.** Kontrola přístupu AI robotů hlásí, že se na stránky nedostala.
Nebo crawl vrací samé 403 a 429.

**Příčina.** Ochrana proti botům na straně CDN nebo firewallu (Cloudflare
a podobné). U firemních webů je to spíš pravidlo než výjimka.

**Co udělat.**

1. Nesnaž se to obejít. Je to obrana tvého webu a funguje.
2. Zjisti, co jde zjistit nepřímo: `robots.txt`, XML sitemapy, hlavičky
   odpovědi na domovské stránce, indexové direktivy.
3. **Řekni o tom tomu, kdo web spravuje.** Že se k webu nedostane ani
   GPTBot nebo ClaudeBot, bývá pro firmu novinka — a je to rozhodnutí, které
   má někdo udělat vědomě.
4. Pro cvičení si vezmi jinou doménu, u které ochrana není.

**Ověření.** Report doběhne a v sekci o dostupnosti je uvedeno, který bot
narazil na co.

---

## 4. Chybí právo pushovat na GitHub

**Příznak.** `Permission denied` nebo `403` při `git push` nebo
`gh repo create`.

**Příčina.** Firemní organizace má zakládání repozitářů pod správou IT,
nebo nejsi přihlášený účtem, který do ní patří.

**Co udělat.**

```bash
gh auth status
```

1. Sedí účet? Když ne, přihlas se znovu.
2. Publikuj pod **vlastní osobní účet**. U skillu, ve kterém není nic
   firemního, se na principu nemění nic.
3. Když ani to nejde, projdi postup lokálně: `git init`, commit, větev,
   druhý commit, `git log --oneline`, `git diff <výchozí>..uprava-popisu`.
   Uvidíš historii i změnu, jen to nikam neodejde. Název výchozí větve
   zjistíš přes `git branch --show-current` — podle verze gitu `main`,
   nebo `master`.

**Ověření.** `gh repo view --web` otevře tvůj repozitář v prohlížeči.

---

## 5. Vyčerpaný limit předplatného

**Příznak.** Claude Code hlásí, že jsi vyčerpal limit, a odmítá pokračovat.

**Příčina.** Limity se počítají v okně; velké běhy je vyčerpají rychleji.

**Co udělat.**

1. `/usage` — ukáže, kolik zbývá a kdy se okno obnoví.
2. `/clear` mezi nesouvisejícími úkoly. Dlouhá konverzace stojí při každé
   odpovědi.
3. U velkých analýz vynech volitelné kroky, které jsou druhým průchodem přes
   stejná data (závěrečné redakční kontroly reportů).
4. Levnější model na mechanickou práci. Drahý model má cenu tam, kde se
   rozhoduje, ne tam, kde se přepisují data.

**Ověření.** `/usage` ukáže volnou kapacitu.

---

## 6. Poškozený soubor stavu

**Příznak.** Skill ze školení hlásí, že začíná s čistým stavem, přestože jsi
už kus dne prošel. Nebo spadne při čtení `.skoleni/stav.json`.

**Příčina.** Soubor se poškodil — nejčastěji tím, že do něj někdo sáhl ručně
nebo se zápis přerušil.

**Co udělat.** Nic dramatického. Plugin poškozený soubor pozná a založí
čistý; přijdeš jen o záznam postupu, ne o artefakty. Ty leží v pracovní
složce dál.

```bash
cat .skoleni/stav.json
```

Když to není platný JSON, smaž ho a pusť `/skoleni-start` znovu — projde jen
to, co chybí.

**Ověření.**

```bash
python3 <cesta-k-pluginu>/scripts/stav.py .
```

Vypíše jednu větu o stavu průchodu.

---

## 7. Nový MCP server nebo skill se neobjevil

**Příznak.** Přidal jsi MCP server nebo založil skill a Claude Code o něm neví.

**Příčina.** Obojí se načítá při startu. Změna udělaná za běhu se neprojeví.

**Co udělat.**

1. Ukonči Claude Code (`/exit`) a spusť ho **ve stejné složce** znovu.
2. Ověř, že to tam je:

```bash
claude mcp list        # MCP servery
claude plugin list     # pluginy
/help                  # dostupné příkazy včetně skillů
```

3. U skillu zkontroluj, že složka je na správném místě
   (`.claude/skills/<jmeno>/SKILL.md`) a že `name` ve frontmatteru odpovídá
   názvu složky.
4. Když se skill nespouští sám od sebe, není to o instalaci, ale o popisu
   (`description`). Viz `navody/08-testovani-skillu.md`.

**Ověření.** Server je v `claude mcp list` jako připojený; skill se objeví
v `/help` a spustí se napsáním `/<jmeno>`.
