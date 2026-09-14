# 13 — Vidět, kolik kontextu ti zbývá

## Proč to chtít

Nejčastější otázka lidí, kterým „přestal Claude Code fungovat", zní: proč
zpomalil nebo zapomněl, co jsme řešili. Skoro vždy je odpověď v naplněném
kontextovém okně. Když ho vidíš, poznáš to dřív, než to začne vadit.

## Zabudované příkazy

| Příkaz | Co ukáže |
|---|---|
| `/context` | Čím je zaplněné kontextové okno — po částech. |
| `/usage` (alias `/cost`) | Kolik ti zbývá z limitu předplatného. |
| `/compact` | Shrne dosavadní konverzaci a uvolní místo. |
| `/clear` | Zahodí konverzaci celou. Když začínáš jinou práci, tohle. |
| `/rewind` | Vrátí se o kus zpátky, když Claude odbočil. |

Praktické pravidlo: **`/clear` mezi dvěma nesouvisejícími úkoly.** Kontext
z předchozí práce nepomáhá, jen zabírá místo a mate.

## Trvalá lišta v terminálu

Pokud chceš mít stav pořád na očích, existuje `ccstatusline` — lišta, která
průběžně ukazuje spotřebu kontextu a další údaje.

```bash
npx -y ccstatusline@latest
```

Spouští se mimo Claude Code, jednou; nastavení se dělá v jejím vlastním menu.
Zdroj: `github.com/sirmalloc/ccstatusline`.

## Co kontext plní nejvíc

1. **Výstupy nástrojů.** Jeden nástroj, který vrátí deset tisíc řádků, spolkne
   víc než hodina povídání. Proto se velká data tahají skriptem a modelu se
   vrací jen výsledek.
2. **Dlouhé soubory načtené celé.** Když stačí kus, řekni si o kus.
3. **Historie konverzace.** Roste sama. Od toho je `/compact` a `/clear`.

Připojené MCP servery samy o sobě dnes velký problém nejsou — Claude Code
načítá jejich definice až při použití.
