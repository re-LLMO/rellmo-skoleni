import json
import subprocess

import pluginy as P


class _Vysledek:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _vypis(ids):
    return json.dumps([{"id": i, "version": "1", "scope": "user", "enabled": True} for i in ids])


def test_pozadovane_maji_vysvetleni():
    assert set(P.POZADOVANE) == set(P.K_CEMU)


def test_nainstalovane_cte_json_vypis(monkeypatch):
    monkeypatch.setattr(P, "_claude", lambda: "/usr/local/bin/claude")
    monkeypatch.setattr(P.subprocess, "run",
                        lambda *a, **k: _Vysledek(0, _vypis(["superpowers@claude-plugins-official"])))
    assert P.nainstalovane() == {"superpowers@claude-plugins-official"}


def test_nainstalovane_prezije_chybejici_claude(monkeypatch):
    monkeypatch.setattr(P, "_claude", lambda: None)
    assert P.nainstalovane() == set()
    assert P.claude_dostupne() is False


def test_nainstalovane_prezije_rozbity_vystup(monkeypatch):
    monkeypatch.setattr(P, "_claude", lambda: "/usr/local/bin/claude")
    monkeypatch.setattr(P.subprocess, "run", lambda *a, **k: _Vysledek(0, "{tohle není json"))
    assert P.nainstalovane() == set()


def test_chybejici_vraci_jen_co_chybi(monkeypatch):
    monkeypatch.setattr(P, "nainstalovane",
                        lambda: {"superpowers@claude-plugins-official"})
    assert P.chybejici() == ["skill-creator@claude-plugins-official"]


def test_nainstaluj_ok(monkeypatch):
    volane = {}

    def run(args, **k):
        volane["args"] = args
        return _Vysledek(0, "Installed")

    monkeypatch.setattr(P, "_claude", lambda: "/usr/local/bin/claude")
    monkeypatch.setattr(P.subprocess, "run", run)
    v = P.nainstaluj("skill-creator@claude-plugins-official")
    assert v["vysledek"] == "ok"
    assert volane["args"][1:4] == ["plugin", "install", "skill-creator@claude-plugins-official"]
    assert "-y" in volane["args"]


def test_pozadovane_jsou_jen_z_oficialni_marketplace():
    assert all(p.endswith("@claude-plugins-official") for p in P.POZADOVANE)


def test_nainstaluj_selhani_nese_zpravu_bez_pádu(monkeypatch):
    monkeypatch.setattr(P, "_claude", lambda: "/usr/local/bin/claude")
    monkeypatch.setattr(P.subprocess, "run",
                        lambda *a, **k: _Vysledek(1, "", "Error: network unreachable"))
    v = P.nainstaluj("superpowers@claude-plugins-official")
    assert v["vysledek"] == "selhalo"
    assert "network" in v["zprava"]


def test_nainstaluj_timeout(monkeypatch):
    def run(*a, **k):
        raise subprocess.TimeoutExpired(cmd="claude", timeout=1)

    monkeypatch.setattr(P, "_claude", lambda: "/usr/local/bin/claude")
    monkeypatch.setattr(P.subprocess, "run", run)
    assert P.nainstaluj("superpowers@claude-plugins-official")["vysledek"] == "selhalo"


def test_nainstaluj_bez_claude(monkeypatch):
    monkeypatch.setattr(P, "_claude", lambda: None)
    assert P.nainstaluj("superpowers@claude-plugins-official")["vysledek"] == "selhalo"


def test_prehled_ma_vsechny_pozadovane(monkeypatch):
    monkeypatch.setattr(P, "nainstalovane", lambda: set())
    monkeypatch.setattr(P, "claude_dostupne", lambda: True)
    p = P.prehled()
    assert set(p["pluginy"]) == set(P.POZADOVANE)
    assert all(z["pritomen"] is False for z in p["pluginy"].values())


def test_plugin_z_adresare_anthropicu_se_pocita_jako_pritomny(monkeypatch):
    """Čistá instalace Claude Code má jen vestavěnou `anthropic-plugin-directory`.
    Kdo si superpowers nainstaloval přes /plugin odtamtud, nesmí dostat druhou kopii."""
    monkeypatch.setattr(P, "nainstalovane", lambda: {
        "superpowers@anthropic-plugin-directory",
        "skill-creator@claude-plugins-official",
    })
    assert P.chybejici() == []
    monkeypatch.setattr(P, "claude_dostupne", lambda: True)
    assert all(z["pritomen"] for z in P.prehled()["pluginy"].values())


def test_plugin_z_ciziho_marketplace_se_nepocita(monkeypatch):
    monkeypatch.setattr(P, "nainstalovane", lambda: {"superpowers@superpowers-dev"})
    assert "superpowers@claude-plugins-official" in P.chybejici()


def test_vystup_claude_se_cte_jako_utf8(monkeypatch):
    """Na české Windows by `text=True` četl výstup CLI v cp1250 a na ň nebo Ř
    (třeba v cestě k profilu) spadl s UnicodeDecodeError."""
    volani = []

    def run(args, **k):
        volani.append(k)
        return _Vysledek(0, _vypis(["superpowers@claude-plugins-official"]))

    monkeypatch.setattr(P, "_claude", lambda: "/usr/local/bin/claude")
    monkeypatch.setattr(P.subprocess, "run", run)
    P.nainstalovane()
    P.nainstaluj("superpowers@claude-plugins-official")
    for k in volani:
        assert k.get("encoding") == "utf-8" and "text" not in k
