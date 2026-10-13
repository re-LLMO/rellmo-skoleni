import json
import pytest
import stav as S


def test_vychozi_stav_ma_vsechny_kroky_nezacate():
    s = S.vychozi_stav()
    assert set(s["kroky"]) == set(S.KROKY)
    assert all(k["stav"] == "nezacato" for k in s["kroky"].values())


def test_nacti_zalozi_vychozi_kdyz_soubor_chybi(docasna_slozka):
    s = S.nacti(docasna_slozka)
    assert s["kroky"]["start"]["stav"] == "nezacato"


def test_nacti_opravi_poskozeny_soubor(docasna_slozka):
    cesta = docasna_slozka / ".skoleni"
    cesta.mkdir()
    (cesta / "stav.json").write_text("{tohle není json", encoding="utf-8")
    s = S.nacti(docasna_slozka)
    assert s["kroky"]["start"]["stav"] == "nezacato"
    assert "poškozen" in s["poznamky"][0].lower()


def test_zapis_a_nacti_zachova_data(docasna_slozka):
    s = S.vychozi_stav()
    s["domena"] = "priklad.cz"
    S.zapis(s, docasna_slozka)
    assert S.nacti(docasna_slozka)["domena"] == "priklad.cz"


def test_nastav_krok_odmitne_neznamy_krok():
    with pytest.raises(ValueError):
        S.nastav_krok(S.vychozi_stav(), "neexistuje", "hotovo")


def test_nastav_krok_odmitne_neznamy_stav():
    with pytest.raises(ValueError):
        S.nastav_krok(S.vychozi_stav(), "start", "skoro-hotovo")


def test_veta_hlasi_pocet_a_duvod_zablokovani():
    s = S.vychozi_stav()
    S.nastav_krok(s, "start", "hotovo")
    S.nastav_krok(s, "automatizace", "ceka-na-prihlaseni", "GitHub")
    v = S.veta(s)
    assert "1 z 4" in v
    assert "GitHub" in v


@pytest.mark.parametrize("obsah", [
    '[1, 2, 3]',
    'null',
    '"jen retezec"',
    '{"kroky": ["a", "b"]}',
    '{"kroky": {"start": "hotovo"}}',
    '{"kroky": null}',
])
def test_nacti_prezije_strukturalne_poskozeny_soubor(docasna_slozka, obsah):
    cesta = docasna_slozka / ".skoleni"
    cesta.mkdir()
    (cesta / "stav.json").write_text(obsah, encoding="utf-8")
    s = S.nacti(docasna_slozka)
    assert set(s["kroky"]) == set(S.KROKY)
    assert s["kroky"]["start"]["stav"] == "nezacato"


def test_nacti_sklada_kroky_v_kanonickem_poradi(docasna_slozka):
    cesta = docasna_slozka / ".skoleni"
    cesta.mkdir()
    prohazene = {
        "verze": 1,
        "kroky": {
            "shrnuti": {"stav": "hotovo", "poznamka": "", "artefakty": []},
            "start": {"stav": "hotovo", "poznamka": "", "artefakty": []},
        },
    }
    (cesta / "stav.json").write_text(json.dumps(prohazene), encoding="utf-8")
    nacteny = S.nacti(docasna_slozka)
    assert list(nacteny["kroky"]) == list(S.KROKY)
    assert nacteny["kroky"]["start"]["stav"] == "hotovo"
    assert nacteny["kroky"]["shrnuti"]["stav"] == "hotovo"
    assert nacteny["kroky"]["automatizace"]["stav"] == "nezacato"


def test_heredoc_s_importem_tiskne_utf8_i_v_cp1250(docasna_slozka):
    """Skilly tisknou stav z heredocu (`import stav` a `print`). Na české
    Windows jde výstup do roury v cp1250 a poznámka se šipkou by print shodila."""
    import os
    import subprocess
    import sys
    from pathlib import Path

    kod = (
        "import sys; sys.path.insert(0, sys.argv[1]); import stav;"
        "s = stav.nacti(sys.argv[2]);"
        "stav.nastav_krok(s, 'start', 'blokovano', 'git → chybí, řeší IT');"
        "print(stav.veta(s))"
    )
    r = subprocess.run([sys.executable, "-c", kod, str(Path(S.__file__).parent), str(docasna_slozka)],
                       capture_output=True, env={**os.environ, "PYTHONIOENCODING": "cp1250"})
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    assert "git → chybí, řeší IT" in r.stdout.decode("utf-8")
