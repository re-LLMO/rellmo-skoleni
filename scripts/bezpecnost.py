#!/usr/bin/env python3
"""bezpecnost.py — ochrana dat účastníka.

Zakládá .gitignore dřív, než vznikne cokoli, co by se nemělo commitnout,
a maskuje tajemství ve všem, co jde na obrazovku. Jen standardní knihovna.
"""
import re
from pathlib import Path

RADKY_GITIGNORE = [
    ".skoleni/",
    ".env",
    ".env.*",
    "*.key",
    "*.pem",
    "*token*.json",
    "gsc_token.json",
    ".mcp.json",
    "*.duckdb",
    "*.seospider",
    "*.dbseospider",
    "*.csv",
    "opportunities.md",
    "curve.svg",
    "exporty/",
]

_KLIC = r"[A-Z_-]*(?:PASSWORD|HESLO|SECRET|TOKEN|APIKEY|API[_-]?KEY)[A-Z_-]*"

_VZORY = [
    # hodnota v uvozovkách za tajným klíčem — maskuje se vždy
    re.compile(rf"(?i)(\b{_KLIC}\b\"?\s*[=:]\s*\")([^\"]*)(\")"),
    # hodnota bez uvozovek — maskuje se, jen když vypadá jako tajemství
    re.compile(rf"(?i)(\b{_KLIC}\b\s*[=:]\s*)([^\s,;}}&]+)"),
    # autorizační hlavička — vždy
    re.compile(r"(?i)(\bAuthorization:\s*(?:Basic|Bearer)\s+)(\S+)"),
    # známé tvary tokenů i bez popisku
    re.compile(r"(sk-ant-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{20,})"),
]


# Hodnoty za tajným klíčem maskujeme ve výchozím stavu. Výjimkou jsou krátká
# a známá stavová slova — ta lektor potřebuje na obrazovce přečíst.
_BEZPECNA_SLOVA = {
    "ano", "ne", "yes", "no", "none", "null", "true", "false", "ok",
    "overeno", "ověřeno", "nastaven", "nastaveno", "nastavena",
    "chybi", "chybí", "prazdne", "prázdné", "neznamo", "neznámo",
    "platny", "platný", "neplatny", "neplatný", "aktivni", "aktivní",
    "expired", "missing", "unset", "empty",
}


def _vypada_jako_tajemstvi(hodnota: str) -> bool:
    """Maskujeme, dokud se neprokáže opak. Bezpečnostní funkce nemá hádat."""
    ocistena = hodnota.strip("\"'.,;:").lower()
    if len(ocistena) < 4:
        return False
    return ocistena not in _BEZPECNA_SLOVA


def zajisti_gitignore(slozka) -> dict:
    """Doplní chybějící řádky. Existující obsah nikdy nepřepisuje."""
    Path(slozka).mkdir(parents=True, exist_ok=True)
    p = Path(slozka) / ".gitignore"
    stavajici = p.read_text(encoding="utf-8").splitlines() if p.exists() else []
    chybi = [r for r in RADKY_GITIGNORE if r not in stavajici]
    if chybi:
        radky = stavajici + ([""] if stavajici and stavajici[-1] else [])
        radky += ["# školení re:LLMO — ať se ven nedostanou klíče ani exporty"] + chybi
        p.write_text("\n".join(radky) + "\n", encoding="utf-8")
    return {"doplneno": chybi, "cesta": str(p)}


def maskuj(text: str) -> str:
    """Nahradí hodnoty, které vypadají jako tajemství. Zbytek nechá být."""
    text = _VZORY[0].sub(lambda m: m.group(1) + "••••" + m.group(3), text)
    text = _VZORY[1].sub(
        lambda m: m.group(1) + ("••••" if _vypada_jako_tajemstvi(m.group(2)) else m.group(2)), text
    )
    text = _VZORY[2].sub(lambda m: m.group(1) + "••••", text)
    text = _VZORY[3].sub("••••", text)
    return text


def veta_o_odeslani(kam: str, co: str) -> str:
    return f"Chystám se poslat {co} službě {kam}. Můžu?"


if __name__ == "__main__":
    import sys
    print(maskuj(sys.stdin.read()))
