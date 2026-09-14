#!/usr/bin/env python3
"""prostredi.py — co na stroji účastníka je a co chybí.

Publikum jsou marketéři na firemních noteboocích. Skript proto nikdy neklade
technické otázky: buď to umí spravit, nebo řekne jednou větou, co chtít po IT.
Jen standardní knihovna.
"""
import shutil
import subprocess

NASTROJE = ("python3", "git", "gh", "node", "npx")

# Každý správce pojmenovává balíčky jinak. Winget má vlastní identifikátory,
# apt jiné názvy než brew, a npx se neinstaluje zvlášť — přichází s Node.
_BALICKY = {
    "brew":   {"gh": "gh", "git": "git", "node": "node", "npx": "node", "python3": "python3"},
    "apt":    {"gh": "gh", "git": "git", "node": "nodejs", "npx": "npm", "python3": "python3"},
    # Winget nemá alias na nejnovější 3.x — každá minor verze je vlastní
    # identifikátor. Python 3.12 má podporu do roku 2028; potom povýšit.
    "winget": {"gh": "GitHub.cli", "git": "Git.Git", "node": "OpenJS.NodeJS",
               "npx": "OpenJS.NodeJS", "python3": "Python.Python.3.12"},
}

_SABLONY = {
    "brew": "brew install {b}",
    "apt": "sudo apt-get install -y {b}",
    "winget": "winget install -e --id {b}",
}


def _verze(nastroj: str):
    try:
        r = subprocess.run([nastroj, "--version"], capture_output=True, text=True, timeout=5)
        return (r.stdout or r.stderr).strip().splitlines()[0] if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def zkontroluj(hlas=None) -> dict:
    """`hlas` je volitelná funkce, které se po každém nástroji předá jeho výsledek."""
    vysledek = {}
    for n in NASTROJE:
        je = shutil.which(n) is not None
        zaznam = {"pritomen": je, "verze": _verze(n) if je else None}
        vysledek[n] = zaznam
        if hlas is not None:
            hlas(n, zaznam)
    return vysledek


def spravce_balicku():
    for s in ("brew", "apt", "winget"):
        if shutil.which(s):
            return s
    return None


def navrh_instalace(nastroj: str) -> str:
    spravce = spravce_balicku()
    if spravce is None:
        return (f"Nástroj {nastroj} tady chybí a nenašel jsem správce balíčků. "
                f"Napiš svému IT, ať ti doinstaluje {nastroj}.")
    balicek = _BALICKY[spravce].get(nastroj)
    if balicek is None:
        return (f"Nástroj {nastroj} tady chybí a přes {spravce} se neinstaluje jedním "
                f"příkazem. Napiš svému IT, ať ti doinstaluje {nastroj}.")
    prikaz = _SABLONY[spravce].format(b=balicek)
    if spravce == "winget":
        prikaz += "\nPo instalaci zavři terminál a otevři nové okno — mění se PATH a v původním okně nástroj nenajdeš."
    return prikaz


if __name__ == "__main__":
    def vypis(nastroj, zaznam):
        print(f"{nastroj}: {'ano' if zaznam['pritomen'] else 'CHYBÍ'} {zaznam['verze'] or ''}", flush=True)

    zkontroluj(hlas=vypis)
