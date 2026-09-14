---
name: vzorovy-skill
description: Vzorový skill ze školení Claude Code pro SEO. Ukazuje, co patří do SKILL.md, co do references/ a co do assets/ — na příkladu skillu, který zná firemní značku a umí v ní vyrobit dokument. Zkopíruj si ho, přejmenuj a přepiš obsah svým. Použij, když si stavíš první vlastní skill a chceš vidět hotový tvar.
license: LicenseRef-Rellmo-Commercial
allowed-tools: Read, Write, Edit
metadata:
  author: Rellmo
  version: 0.1.0
  category: vzor
---

# vzorový skill

> **Tohle je šablona, ne funkční nástroj.** Zkopíruj složku k sobě, přejmenuj
> ji, přepiš `name` a `description` a nahraď obsah svým. Všechno v hranatých
> závorkách je k doplnění.

## Než začneš přepisovat

Nejdůležitější řádek celého souboru je `description`. Podle něj se model
rozhoduje, jestli skill spustit. **Není to shrnutí, je to rozhodovací věta.**
Napiš do něj věty, kterými o té práci mluvíš ty a tvoji kolegové.

Zbytek souboru čte model až ve chvíli, kdy se skill spustí. Tam patří postup,
ne popis, co skill umí.

## Co skill dělá

[Jednou větou: co je na vstupu, co je na výstupu.]

## Postup

1. **Zjisti vstup.** [Co potřebuješ vědět, než začneš. Když to chybí, zeptej
   se — jednou otázkou, ne dotazníkem.]
2. **Načti kontext.** Pravidla značky jsou v `references/znacka.md`, logo a
   barvy v `assets/`. Načti jen to, co pro tenhle výstup potřebuješ.
3. **Vyrob výstup.** [Formát, kam se ukládá, jak se jmenuje.]
4. **Řekni, co vzniklo.** Cesta k souboru a jedna věta o tom, co v něm je.

## Pravidla, která platí vždycky

- [Věc, kterou model dělá špatně, dokud mu to neřekneš. Tady je od toho
  místo — a je to nejcennější část celého skillu.]
- [Například: „Nikdy nepiš do nadpisu název firmy, je v logu."]

## Když něco chybí

| Chybí | Co udělat |
|---|---|
| [vstup] | [náhradní postup, ne odmítnutí] |
| [přístup] | [na koho se obrátit, co jde udělat mezitím] |

## Co do tohohle souboru nepatří

- **Dlouhé tabulky a metodika** → `references/`. Načtou se, až budou potřeba.
- **Loga, fonty, šablony** → `assets/`.
- **Mechanická práce s daty** → `scripts/`. Skript se do modelu nenačítá,
  běží mimo a model vidí jen jeho výsledek.

Tělo `SKILL.md` drž pod pěti sty řádky. Načítá se celé, pokaždé.
