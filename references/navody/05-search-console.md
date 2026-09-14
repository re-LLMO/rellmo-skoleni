# 05 — Napojení Search Console

## Proč to nejde přes běžný MCP server

Většina MCP serverů pro Search Console chce servisní účet založený v Google
Cloud Console. To je pro marketéra na firemním notebooku další kolo IT
ticketů — a hlavně je to zbytečné.

Pluginy re:LLMO, které se Search Console ptají (kanibalizace klíčových slov,
příležitosti), si nesou vlastní přihlášení přes OAuth: jedno kliknutí
v prohlížeči, čtecí oprávnění, žádná Cloud Console.

## Jak se přihlásit

Řekni Claudovi, že chceš spustit analýzu příležitostí nebo kanibalizace nad
svou doménou. Přihlášení proběhne v prvním kroku samo. Pokud si chceš proces
vyvolat zvlášť, běží pod skriptem `gsc_auth.py login` uvnitř toho pluginu.

Přihlašovací odkaz se ti vypíše do terminálu:

- **Otevři ho v libovolném prohlížeči.** Nemusí to být ten, který se sám
  otevřel.
- **Nekopíruj URL z adresního řádku otevřeného prohlížeče do jiného.**
  Google ji přepíše na adresu vázanou na konkrétní relaci a jinde nebude
  fungovat. Kopíruj vždycky ten odkaz z terminálu.

Token se uloží do domovské složky (`~/.rellmo/gsc_token.json`) a platí dál.
Přihlašuješ se jednou, ne před každou analýzou.

## Které property uvidíš

Ty, ke kterým má přihlášený účet přístup. Tři úrovně oprávnění se chovají
různě:

| Úroveň | Co to znamená |
|---|---|
| `siteOwner`, `siteFullUser` | Data se čtou bez omezení. |
| `siteRestrictedUser` | Data se čtou. |
| `siteUnverifiedUser` | Property je vidět v seznamu, ale **každý dotaz vrátí 403.** Vyber jinou. |

Doménová property (`sc-domain:priklad.cz`) pokrývá všechny subdomény
i protokoly. URL property (`https://www.priklad.cz/`) jen tu jednu variantu.
Když máš obojí, ber doménovou.

## Přihlášení jiným účtem

Spusť přihlášení znovu. Nový token nahradí starý. Když potřebuješ střídat
dva účty pravidelně, počítej s tím, že se pokaždé přihlašuješ znovu.

## Když ti přístup chybí

Search Console dává přístupy vlastník property. Napiš mu, ať tě přidá —
stačí úroveň „omezený uživatel", plný přístup není potřeba.

Než ti ho dá, pracuj s exportem z rozhraní Search Console (CSV) — pro
většinu analýz je to dostačující vstup. Podrobněji v `reseni-problemu.md`,
sekce o chybějícím přístupu.

## Kolik dat se tahá a proč to trvá

Pull jde přímo proti API Search Console, ne přes MCP — vrací až 25 000 řádků
na dotaz a ukládá je na disk, mimo kontextové okno. U větších webů běží
minuty. To je v pořádku; kdyby ta data tekla přes model, stálo by to řádově
statisíce tokenů a nešlo by to.

Okno je zhruba 90 dní (`T-92d` až `T-3d`). Poslední tři dny se vynechávají,
protože je Search Console ještě dopočítává.
