# 01 — Instalace Claude Code a první spuštění

## Co potřebuješ mít

Předplatné Claude (Pro nebo vyšší) nebo přístup přes firemní organizaci.
Bez něj se Claude Code po instalaci nepřihlásí.

## Instalace

**macOS a Linux** — otevři aplikaci Terminál a vlož:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows** — otevři PowerShell a vlož:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Po instalaci **zavři terminál a otevři nové okno.** Ne novou záložku — nové
okno. Instalace mění systémovou proměnnou `PATH` a původní okno o změně neví;
`claude` by v něm hlásilo, že příkaz neexistuje.

## První spuštění

V novém okně napiš:

```
claude
```

Poprvé tě to pošle do prohlížeče se přihlásit. Přihlášení platí dál, příště
už se neptá.

## Co uvidíš

Textové okno s řádkem, do kterého se píše. Píše se **normálními větami
česky**, ne příkazy. Odpověď se vypisuje nad tím.

Užitečné hned na začátku:

| Napiš | Co to udělá |
|---|---|
| `/help` | Vypíše, co všechno umí. |
| `/usage` | Ukáže, kolik ti zbývá z limitu předplatného. |
| `/context` | Ukáže, čím je zaplněné kontextové okno. |
| `/clear` | Zahodí konverzaci a začne s čistým stolem. |
| `/exit` | Ukončí Claude Code. |

## Který terminál

Na macOS stačí vestavěný Terminál. Na Windows stačí PowerShell nebo Terminál
z Windows 11. Jestli chceš pohodlnější prostředí, existuje
[Warp](https://www.warp.dev) — hezčí okno, historie příkazů, nic víc; na
funkčnost Claude Code to nemá vliv.

## Když to nejde

| Co se děje | Co s tím |
|---|---|
| `claude: command not found` | Zavři terminál a otevři **nové okno**. |
| Instalační skript spadne na oprávnění | Firemní notebook s omezenými právy. Pošli IT odkaz na instalaci a řekni, že jde o CLI nástroj do uživatelského profilu. |
| Přihlášení se zacyklí | Zkus jiný prohlížeč. Odkaz nekopíruj z jednoho prohlížeče do druhého — Google i Anthropic ho vážou na konkrétní relaci. |
