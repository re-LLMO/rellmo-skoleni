import pytest
import bezpecnost as B


def test_zajisti_gitignore_zalozi_soubor(docasna_slozka):
    B.zajisti_gitignore(docasna_slozka)
    obsah = (docasna_slozka / ".gitignore").read_text()
    assert ".skoleni/" in obsah
    assert ".env" in obsah


def test_zajisti_gitignore_je_idempotentni(docasna_slozka):
    B.zajisti_gitignore(docasna_slozka)
    B.zajisti_gitignore(docasna_slozka)
    radky = (docasna_slozka / ".gitignore").read_text().splitlines()
    assert radky.count(".skoleni/") == 1


def test_zajisti_gitignore_zachova_existujici_radky(docasna_slozka):
    (docasna_slozka / ".gitignore").write_text("moje-slozka/\n")
    B.zajisti_gitignore(docasna_slozka)
    obsah = (docasna_slozka / ".gitignore").read_text()
    assert "moje-slozka/" in obsah
    assert ".skoleni/" in obsah


def test_maskuje_hodnotu_promenne_s_heslem():
    t = "DATAFORSEO_PASSWORD=4e88ae0aa8067da6 a pokracuje"
    assert "4e88ae0aa8067da6" not in B.maskuj(t)
    assert "pokracuje" in B.maskuj(t)


def test_maskuje_autorizacni_hlavicku():
    t = 'Authorization: Basic c2VvQGVmZmVjdGl4LmNvbTo0ZTg4YWU='
    assert "c2VvQGVmZmVjdGl4" not in B.maskuj(t)


def test_nemaskuje_bezny_text():
    t = "Nainstaloval jsem DataForSEO a spustil kontrolu."
    assert B.maskuj(t) == t


def test_veta_o_odeslani_jmenuje_kam_i_co():
    v = B.veta_o_odeslani("DataForSEO", "tvoji doménu")
    assert "DataForSEO" in v and "doménu" in v


@pytest.mark.parametrize("vstup,tajemstvi", [
    ('{"api_key": "sk-ant-api03-tajnyklic"}', "sk-ant-api03-tajnyklic"),
    ('{"password":"heslo123"}', "heslo123"),
    ("DATAFORSEO_PASSWORD=4e88ae0aa8067da6", "4e88ae0aa8067da6"),
    ("dataforseo_password: 4e88ae0aa8067da6", "4e88ae0aa8067da6"),
    ('Authorization: Basic c2VvQGVmZmVjdGl4', "c2VvQGVmZmVjdGl4"),
])
def test_maskuje_tajemstvi_v_ruznych_tvarech(vstup, tajemstvi):
    vysledek = B.maskuj(vstup)
    assert tajemstvi not in vysledek
    assert "••••" in vysledek


def test_maskovani_nechava_okolni_strukturu_citelnou():
    vysledek = B.maskuj('{"api_key": "sk-tajne", "region": "cz"}')
    assert "region" in vysledek and "cz" in vysledek


@pytest.mark.parametrize("vstup,tajemstvi", [
    ("PASSWORD=O'Brien123 a pokracuje", "Brien123"),
    ("Chyba: klíč sk-ant-api03-XXXXXXXXXXXXXXXX byl odmítnut.", "sk-ant-api03-XXXXXXXXXXXXXXXX"),
    ("Použil jsem ghp_1234567890abcdef1234567890abcdef1234 pro autentizaci.", "ghp_1234567890abcdef1234567890abcdef1234"),
    ("curl '...?key=AIzaSyD-abcdefghijklmnopqrstuvwx123'", "AIzaSyD-abcdefghijklmnopqrstuvwx123"),
])
def test_maskuje_i_bez_popisku_a_cele_heslo(vstup, tajemstvi):
    assert tajemstvi not in B.maskuj(vstup)


@pytest.mark.parametrize("vstup", [
    "GSC token: ověřeno",
    "Nastavil jsem Secret: ano",
    "Token nastaven",
])
def test_nemaskuje_stavova_slova(vstup):
    assert "••••" not in B.maskuj(vstup)


def test_maskovani_se_nerozlije_do_zbytku_dotazu():
    vysledek = B.maskuj("token=abc12345&region=cz&other=data")
    assert "abc12345" not in vysledek
    assert "region=cz" in vysledek and "other=data" in vysledek


def test_gitignore_pokryva_soubory_z_bloku_2():
    for vzor in ["analysis.duckdb", ".mcp.json", "items.csv", "opportunities.md", "curve.svg"]:
        assert any(
            vzor == r or (r.startswith("*") and vzor.endswith(r[1:]))
            for r in B.RADKY_GITIGNORE
        ), vzor


def test_zajisti_gitignore_zalozi_i_neexistujici_slozku(tmp_path):
    cil = tmp_path / "nova" / "hlubsi"
    B.zajisti_gitignore(cil)
    assert (cil / ".gitignore").exists()


@pytest.mark.parametrize("heslo", [
    "korelacni", "nazdarnazdar", "mojeheslo", "kooperativa", "abcdefgh",
])
def test_maskuje_i_heslo_ze_samych_malych_pismen(heslo):
    """Heslo k DataForSEO si volí uživatel — často bez číslic."""
    assert heslo not in B.maskuj(f"DATAFORSEO_PASSWORD={heslo}")


@pytest.mark.parametrize("stav", [
    "ověřeno", "ano", "none", "nastaveno", "false",
])
def test_nemaskuje_znama_stavova_slova(stav):
    vysledek = B.maskuj(f"GSC token: {stav}")
    assert stav in vysledek
    assert "••••" not in vysledek
