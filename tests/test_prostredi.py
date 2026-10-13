import prostredi as P


def test_seznam_nastroju_obsahuje_npx():
    assert "npx" in P.NASTROJE
    assert "python3" in P.NASTROJE


def test_zkontroluj_vrati_zaznam_ke_kazdemu_nastroji(monkeypatch):
    monkeypatch.setattr(P.shutil, "which", lambda n: "/usr/bin/" + n)
    monkeypatch.setattr(P, "_verze", lambda n: "1.0")
    v = P.zkontroluj()
    assert set(v) == set(P.NASTROJE)
    assert v["git"]["pritomen"] is True


def test_zkontroluj_pozna_chybejici_nastroj(monkeypatch):
    monkeypatch.setattr(P.shutil, "which", lambda n: None if n == "gh" else "/usr/bin/" + n)
    monkeypatch.setattr(P, "_verze", lambda n: "1.0")
    v = P.zkontroluj()
    assert v["gh"]["pritomen"] is False
    assert v["gh"]["verze"] is None


def test_spravce_balicku_vrati_brew_kdyz_existuje(monkeypatch):
    monkeypatch.setattr(P.shutil, "which", lambda n: "/opt/homebrew/bin/brew" if n == "brew" else None)
    assert P.spravce_balicku() == "brew"


def test_spravce_balicku_vrati_none_kdyz_zadny(monkeypatch):
    monkeypatch.setattr(P.shutil, "which", lambda n: None)
    assert P.spravce_balicku() is None


def test_navrh_instalace_pro_brew_obsahuje_nazev(monkeypatch):
    monkeypatch.setattr(P, "spravce_balicku", lambda: "brew")
    assert "gh" in P.navrh_instalace("gh")


def test_navrh_instalace_bez_spravce_vrati_srozumitelnou_vetu(monkeypatch):
    monkeypatch.setattr(P, "spravce_balicku", lambda: None)
    v = P.navrh_instalace("gh")
    assert "IT" in v or "ručně" in v


def test_navrh_instalace_pouziva_winget_identifikator(monkeypatch):
    monkeypatch.setattr(P, "spravce_balicku", lambda: "winget")
    navrh = P.navrh_instalace("gh")
    assert "GitHub.cli" in navrh
    assert "winget install gh" not in navrh


def test_navrh_instalace_pro_winget_upozorni_na_nove_okno(monkeypatch):
    monkeypatch.setattr(P, "spravce_balicku", lambda: "winget")
    assert "nové okno" in P.navrh_instalace("git")


def test_navrh_instalace_zna_balicek_pro_kazdy_nastroj(monkeypatch):
    for spravce in ("brew", "apt", "winget"):
        monkeypatch.setattr(P, "spravce_balicku", lambda s=spravce: s)
        for nastroj in P.NASTROJE:
            navrh = P.navrh_instalace(nastroj)
            assert navrh and (nastroj in navrh or "IT" in navrh or "install" in navrh)


def test_zkontroluj_hlasi_prubeh(monkeypatch):
    monkeypatch.setattr(P.shutil, "which", lambda n: "/usr/bin/" + n)
    monkeypatch.setattr(P, "_verze", lambda n: "1.0")
    videno = []
    P.zkontroluj(hlas=lambda n, z: videno.append(n))
    assert videno == list(P.NASTROJE)


def test_zkontroluj_funguje_i_bez_hlasu(monkeypatch):
    monkeypatch.setattr(P.shutil, "which", lambda n: "/usr/bin/" + n)
    monkeypatch.setattr(P, "_verze", lambda n: "1.0")
    assert set(P.zkontroluj()) == set(P.NASTROJE)


def test_apt_umi_nainstalovat_gh(monkeypatch):
    """gh je v Debian main i Ubuntu universe od 22.04 — nemá se posílat za IT."""
    monkeypatch.setattr(P, "spravce_balicku", lambda: "apt")
    navrh = P.navrh_instalace("gh")
    assert "apt-get install -y gh" in navrh
    assert "IT" not in navrh


def test_python_je_pritomen_i_kdyz_python3_neni_v_path(monkeypatch):
    """Na Windows se Python spouští jako `py` nebo `python` a `python3` chybí
    nebo je jen odkaz do Microsoft Storu. Skript sám v Pythonu běží, takže
    nesmí hlásit chybějící Python a posílat účastníka ho instalovat znovu."""
    monkeypatch.setattr(P.shutil, "which", lambda n: None)
    v = P.zkontroluj()
    assert v["python3"]["pritomen"] is True
    assert v["python3"]["verze"].startswith("Python 3.")
    assert v["git"]["pritomen"] is False


def test_verze_se_zjistuje_z_plne_cesty(monkeypatch):
    """Na Windows je `npx` soubor `npx.cmd` — spustit jde jen přes plnou cestu."""
    monkeypatch.setattr(P.shutil, "which", lambda n: rf"C:\Program Files\nodejs\{n}.cmd")
    volane = []
    monkeypatch.setattr(P, "_verze", lambda cesta: volane.append(cesta) or "1.0")
    P.zkontroluj()
    assert r"C:\Program Files\nodejs\npx.cmd" in volane
