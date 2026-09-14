# 08 — Testování skillu

Skill je hotový teprve tehdy, když se spustí ve správnou chvíli a jeho výstup
sedí. Obojí se dá ověřit.

## Tři věci, které se testují

| Co | Otázka | Jak |
|---|---|---|
| **Spouštění** | Spustí se, když má? A nespustí, když nemá? | Tři až pět vět, na které **má** zabrat, a dvě až tři, na které **nemá**. |
| **Výsledek** | Je výstup správný? | Znám vstup, znám správný výstup. Pusť a porovnej. |
| **Přínos** | Je to se skillem lepší než bez něj? | Stejné zadání se skillem a bez něj, porovnej výsledek. |

## Čerstvá instance ukáže pravdu

Nejčastější omyl při testování: zkoušíš skill v tom samém rozhovoru, ve
kterém jsi ho psal. Tam ale model zná celý kontext z konverzace a doplní si,
co ve skillu chybí.

Otevři nové okno (`/clear` nebo nový terminál) a zadej úkol tak, jak by ho
zadal kolega. Teprve co projde tam, je hotové.

## Nejdřív test, který padá

Než změníš cokoli v hotovém skillu:

1. Řekni si, jaké chování chceš změnit.
2. Napiš zadání, na kterém současný skill **selže**.
3. Pusť ho a ověř, že fakt selhal.
4. Teprve pak uprav `SKILL.md`.
5. Pusť znovu — musí projít.

Test, který projde i proti té staré, vadné verzi, nehlídá nic. Tohle je
nejčastější tichá chyba: napíšeš kontrolu, ona zeleně projde, a přitom by
prošla vždycky.

## Co sledovat v běžném provozu

| Příznak | Co to znamená | Co s tím |
|---|---|---|
| Model čte soubory v podivném pořadí | Struktura mu nedává smysl | Přejmenuj nebo přeuspořádej. |
| Ignoruje odkaz na referenci | Odkaz není dost výrazný | Napiš přímo „Než uděláš X, přečti si Y." |
| Pořád dokola čte tentýž soubor | Patří to do těla | Přesuň obsah do `SKILL.md`. |
| Přiložený soubor nikdy neotevře | Není potřeba | Smaž ho. |

## Když se skill nespouští

Skoro vždy je to popis (`description`), ne tělo.

1. Existuje složka a je na správném místě? (`.claude/skills/` v pracovní
   složce, nebo `~/.claude/skills/` globálně)
2. Restartoval jsi Claude Code po vytvoření složky?
3. Zeptej se přímo: „Kdy bys použil skill *jméno*?" Odpověď ti řekne,
   na co popis zabírá.
4. Doplň do popisu věty, kterými o té práci mluvíš ty a tvoji kolegové.
