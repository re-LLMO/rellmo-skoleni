#!/usr/bin/env python3
"""pluginy.py — které pluginy Claude Code účastník má a které mu chybí.

Školení stojí na dvou pluginech z oficiální nabídky Anthropicu: superpowers
(nejdřív rozmyslet, pak dělat; psaní skillů) a skill-creator (druhý,
rovnocenný průvodce tvorbou skillu od Anthropicu). Skript je jen zjistí a
doinstaluje — nic neptá, nic nevysvětluje, to je práce skillu. Jen standardní
knihovna.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys

# Claude Code čte výstup jako UTF-8. Na Windows by Python psal do roury
# v kódování systému (cp1250) a znak, který v něm není (třeba ✘ z hlášky CLI),
# by shodil print. Platí i pro heredoc ve skillu, který tenhle modul importuje.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

POZADOVANE = (
    "superpowers@claude-plugins-official",
    "skill-creator@claude-plugins-official",
)

K_CEMU = {
    "superpowers@claude-plugins-official": "nejdřív rozmyslet, pak dělat — brainstorming, plán, psaní skillů",
    "skill-creator@claude-plugins-official": "druhý průvodce tvorbou vlastního skillu, od Anthropicu",
}

# Čistá instalace Claude Code má nakonfigurovaný jen vestavěný adresář
# `anthropic-plugin-directory`; stejné pluginy v něm vede pod svým jménem.
# Plugin z kterékoli z těchhle dvou marketplace se počítá jako přítomný — jinak
# by se nainstalovala druhá kopie. Instaluje se z `claude-plugins-official`,
# kterou CLI dohledá, i když v seznamu marketplace není.
OFICIALNI_MARKETPLACE = ("claude-plugins-official", "anthropic-plugin-directory")

_TIMEOUT_LIST = 60
_TIMEOUT_INSTALL = 300


def _claude() -> str | None:
    return shutil.which("claude")


def nainstalovane() -> set[str]:
    """Množina id nainstalovaných pluginů ve tvaru `nazev@marketplace`.

    Prázdná množina znamená i to, že `claude` na stroji není nebo výpis
    selhal — volající to rozliší přes `claude_dostupne()`.
    """
    cmd = _claude()
    if cmd is None:
        return set()
    try:
        r = subprocess.run([cmd, "plugin", "list", "--json"], capture_output=True,
                           encoding="utf-8", errors="replace", timeout=_TIMEOUT_LIST)
    except (OSError, subprocess.SubprocessError):
        return set()
    if r.returncode != 0:
        return set()
    try:
        data = json.loads(r.stdout or "[]")
    except json.JSONDecodeError:
        return set()
    if isinstance(data, dict):
        data = data.get("plugins", [])
    ids = set()
    for z in data:
        if isinstance(z, dict) and z.get("id"):
            ids.add(z["id"])
    return ids


def claude_dostupne() -> bool:
    return _claude() is not None


def _je_mezi(plugin_id: str, mam: set[str]) -> bool:
    nazev = plugin_id.split("@", 1)[0]
    return any(f"{nazev}@{m}" in mam for m in OFICIALNI_MARKETPLACE)


def chybejici() -> list[str]:
    mam = nainstalovane()
    return [p for p in POZADOVANE if not _je_mezi(p, mam)]


def nainstaluj(plugin_id: str) -> dict:
    """Spustí `claude plugin install <id>`. Vrátí {"vysledek", "zprava"}.

    `vysledek` je `ok` nebo `selhalo`. Oba požadované pluginy jsou v oficiální
    marketplace, kterou CLI dohledá i bez `claude plugin marketplace add` —
    chybějící marketplace tu proto není stav, se kterým se počítá.
    """
    cmd = _claude()
    if cmd is None:
        return {"vysledek": "selhalo", "zprava": "Claude Code (příkaz `claude`) na tomhle stroji není v PATH."}
    try:
        r = subprocess.run([cmd, "plugin", "install", plugin_id, "-y"], capture_output=True,
                           encoding="utf-8", errors="replace", timeout=_TIMEOUT_INSTALL)
    except subprocess.TimeoutExpired:
        return {"vysledek": "selhalo", "zprava": f"Instalace {plugin_id} nedoběhla do {_TIMEOUT_INSTALL} s (pomalá síť?)."}
    except (OSError, subprocess.SubprocessError) as e:
        return {"vysledek": "selhalo", "zprava": f"Instalaci {plugin_id} se nepodařilo spustit: {e}"}
    vystup = (r.stdout or "") + (r.stderr or "")
    if r.returncode == 0:
        return {"vysledek": "ok", "zprava": f"{plugin_id} nainstalován."}
    return {"vysledek": "selhalo", "zprava": f"Instalace {plugin_id} selhala: {vystup.strip()[:300]}"}


def prehled() -> dict:
    """Co je a co chybí — pro výpis na obrazovku a zápis do stavu."""
    mam = nainstalovane()
    return {
        "claude": claude_dostupne(),
        "pluginy": {p: {"pritomen": _je_mezi(p, mam), "k_cemu": K_CEMU[p]} for p in POZADOVANE},
    }


if __name__ == "__main__":
    p = prehled()
    if not p["claude"]:
        print("claude: příkaz nenalezen — Claude Code není v PATH")
    for pid, z in p["pluginy"].items():
        print(f"{'ok    ' if z['pritomen'] else 'CHYBÍ '} {pid} — {z['k_cemu']}")
