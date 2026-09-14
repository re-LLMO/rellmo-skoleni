#!/usr/bin/env python3
"""stav.py — průchod účastníka školením.

Jediné místo, které sahá na .skoleni/stav.json. Stav slouží třem věcem:
účastník ví, kde je; lektor pozná, koho jít zachránit; a při návratu domů
plugin naváže tam, kde se přestalo. Jen standardní knihovna.
"""
import json
from pathlib import Path

KROKY = ("start", "automatizace", "shrnuti")
STAVY = ("nezacato", "hotovo", "ceka-na-prihlaseni",
         "jede-na-ukazkovych-datech", "blokovano", "preskoceno")

POPIS_KROKU = {
    "start": "nastavení, pluginy a první report",
    "automatizace": "vlastní automatizace",
    "shrnuti": "shrnutí dne",
}


def vychozi_stav() -> dict:
    return {
        "verze": 1,
        "uroven": None,
        "domena": None,
        "nastroje": [],
        "kroky": {k: {"stav": "nezacato", "poznamka": "", "artefakty": []} for k in KROKY},
        "poznamky": [],
    }


def _cesta(slozka) -> Path:
    return Path(slozka) / ".skoleni" / "stav.json"


def _ma_platny_tvar(nacteny) -> bool:
    """Soubor může být platný JSON a přesto mít tvar, se kterým se nedá pracovat."""
    if not isinstance(nacteny, dict):
        return False
    if "kroky" not in nacteny:
        return True
    kroky = nacteny["kroky"]
    if not isinstance(kroky, dict):
        return False
    return all(isinstance(v, dict) and "stav" in v for v in kroky.values())


def nacti(slozka) -> dict:
    p = _cesta(slozka)
    if not p.exists():
        return vychozi_stav()
    try:
        nacteny = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        nacteny = None
    if nacteny is None or not _ma_platny_tvar(nacteny):
        s = vychozi_stav()
        s["poznamky"].append("Soubor stavu byl poškozený, začínáme s čistým.")
        return s
    zaklad = vychozi_stav()
    zaklad.update({k: v for k, v in nacteny.items() if k in zaklad and k != "kroky"})
    nactene_kroky = nacteny.get("kroky", {})
    zaklad["kroky"] = {
        k: nactene_kroky.get(k, {"stav": "nezacato", "poznamka": "", "artefakty": []})
        for k in KROKY
    }
    return zaklad


def zapis(stav: dict, slozka) -> None:
    p = _cesta(slozka)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(stav, ensure_ascii=False, indent=2), encoding="utf-8")


def nastav_krok(stav: dict, krok: str, novy: str, poznamka: str = "") -> dict:
    if krok not in KROKY:
        raise ValueError(f"neznámý krok: {krok}")
    if novy not in STAVY:
        raise ValueError(f"neznámý stav: {novy}")
    stav["kroky"][krok]["stav"] = novy
    stav["kroky"][krok]["poznamka"] = poznamka
    return stav


def pridej_artefakt(stav: dict, krok: str, cesta: str) -> dict:
    if krok not in KROKY:
        raise ValueError(f"neznámý krok: {krok}")
    if cesta not in stav["kroky"][krok]["artefakty"]:
        stav["kroky"][krok]["artefakty"].append(cesta)
    return stav


def veta(stav: dict) -> str:
    """Jedna řádka, kterou účastník přečte nahlas, aby lektor věděl, co řešit."""
    hotovo = sum(1 for k in stav["kroky"].values() if k["stav"] == "hotovo")
    celkem = len(KROKY)
    zadrhel = [
        (k, v) for k, v in stav["kroky"].items()
        if v["stav"] in ("ceka-na-prihlaseni", "blokovano", "jede-na-ukazkovych-datech")
    ]
    zaklad = f"Hotovo {hotovo} z {celkem}"
    if not zadrhel:
        return zaklad + "."
    krok, info = zadrhel[0]
    duvod = info["poznamka"] or POPIS_KROKU[krok]
    slovy = {
        "ceka-na-prihlaseni": "čekám na přihlášení",
        "blokovano": "zaseklo se",
        "jede-na-ukazkovych-datech": "jedu na ukázkových datech",
    }[info["stav"]]
    return f"{zaklad} · {slovy}: {duvod}"


if __name__ == "__main__":
    import sys
    print(veta(nacti(sys.argv[1] if len(sys.argv) > 1 else ".")))
