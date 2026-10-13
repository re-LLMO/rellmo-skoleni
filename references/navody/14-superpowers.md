# 14 — Superpowers: nejdřív rozmyslet, pak dělat

## Co to je

Balíček skillů, který dává práci s Claude Code disciplínu: rozmysli → naplánuj
→ udělej → ověř. Bez něj má model tendenci začít psát hned; s ním se nejdřív
zeptá, co vlastně chceš.

Zdroj: `github.com/obra/superpowers`.

## Instalace

```bash
claude plugin install superpowers@claude-plugins-official
```

Oficiální marketplace Anthropicu Claude Code dohledá sám, přidávat ji není
potřeba. Repozitář `obra/superpowers` má i vlastní vývojovou marketplace
(`superpowers-dev`) — z té neinstaluj, vznikla by druhá kopie.

Po instalaci restartuj Claude Code.

## Co v balíčku najdeš

| Skill | K čemu |
|---|---|
| `brainstorming` | Průzkum zadání dřív, než se začne dělat. Pusť to **před** jakoukoli tvůrčí prací. |
| `writing-plans` | Z rozmyšleného zadání udělá plán po krocích. |
| `executing-plans` | Provede plán s kontrolními body. |
| `writing-skills` | Tvorba a úprava skillů — hlavní cesta, jak si napsat vlastní automatizaci (viz návod 18). |
| `systematic-debugging` | Postup, když něco nefunguje a není jasné proč. |
| `test-driven-development` | Nejdřív test, který padá, pak oprava. |
| `verification-before-completion` | Ověření, že to opravdu funguje, než to prohlásíš za hotové. |
| `using-git-worktrees` | Dva úkoly naráz, každý ve vlastní kopii, bez kolizí. |

## Kde je to nejvíc znát

**Daň za špatné zadání.** Pět minut ušetřených na zadání se vrací jako hodina
oprav. `brainstorming` tomu předchází tím, že se model ptá, dokud zadání
nedrží pohromadě.

**Sokratovská metoda.** Místo abys popisoval, co chceš, nech model klást
otázky. Odpovídat na konkrétní otázku je snazší než formulovat úplné zadání
dopředu — a výsledek bývá přesnější.

## Plan mode — totéž, ale zabudované v Claude Code

Než sáhneš po pluginu, vyzkoušej režim, který v Claude Code už je.

**Plan mode** znamená, že si Claude přečte, co potřebuje, prozkoumá projekt
a **napíše, co chce udělat — ale nic nezmění**, dokud plán neschválíš.

Zapneš ho dvěma způsoby:

```
Shift+Tab          přepíná režimy dokola; dole ve stavovém řádku
                   uvidíš „⏸ plan mode on"
/plan <zadání>     jednorázově, jen pro tenhle jeden prompt
```

Hodí se pokaždé, když nevíš, co Claude udělá — a to je u nové práce skoro
vždycky. `brainstorming` jde o úroveň dál: ptá se tebe, dokud zadání nedrží
pohromadě. Plan mode ukáže, co model pochopil.

## Praktický postup na vlastní skill

1. `brainstorming` — co ten skill má umět a kdy se má spustit.
2. `writing-skills` — napsat `SKILL.md` a strukturu složek.
3. Vyzkoušet v čerstvém okně (`/clear`), jestli se spouští, když má.
4. Doladit popis (`description`), ne tělo — spouštění řídí popis.

## Kdy to nepoužívat

Na krátký jednorázový dotaz ne. Metodika má smysl tam, kde se práce vrací —
u skillu, který budeš používat každý týden, nebo u analýzy, kterou budeš
opakovat.
