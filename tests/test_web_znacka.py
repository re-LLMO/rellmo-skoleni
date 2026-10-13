"""test_web_znacka.py — vytěžení značky z webu bez sítě (mock stahování)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import web_znacka  # noqa: E402

HTML = """<!doctype html><html><head><title>Firma s.r.o. — domů</title>
<meta property="og:site_name" content="Firma">
<meta name="theme-color" content="#9B36F7">
<link rel="stylesheet" href="/static/main.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Inter">
<link rel="apple-touch-icon" href="/apple.png">
<style>:root{--brand:#9b36f7;--cta:#140328} h1{color:#9B36F7;font-family:'Poppins',sans-serif}</style>
</head><body>
<header class="site-header"><a href="/"><img src="/img/logo-fialove.svg" alt="Firma logo" class="logo"></a>
<svg class="brand-mark" viewBox="0 0 10 10"><rect width="10" height="10"/></svg></header>
<main style="color:#333333"><img src="/img/hero.jpg" alt="hero"></main>
</body></html>"""

CSS = """@font-face{font-family:"Poppins";font-weight:600;src:url(/fonts/p-600.woff2) format('woff2')}
body{font-family:Poppins,Arial,sans-serif;background:#ffffff;color:#1a1a1a}
.btn{background:#140328;color:#fff} .btn:hover{background:rgb(155, 54, 247)}
.card{border:1px solid #eeeeee} .accent{color:#9B36F7} .accent2{color:#9b36f7}"""


def _mock_stahni(url, limit, binarni=False, duvod=None):
    if url.endswith("main.css"):
        return CSS, url, "text/css"
    if url.endswith((".svg", ".png", ".jpg")):
        return (b"<svg/>" if url.endswith(".svg") else b"\x89PNG"), url, ("image/svg+xml" if url.endswith(".svg") else "image/png")
    return HTML, url, "text/html; charset=utf-8"


def test_analyza_bez_site(monkeypatch, tmp_path):
    monkeypatch.setattr(web_znacka, "stahni", _mock_stahni)
    n = web_znacka.analyzuj("priklad.cz", str(tmp_path))
    assert n["url"] == "https://priklad.cz"
    assert n["nazev"] == "Firma"
    assert n["theme_color"] == "#9B36F7"
    assert n["css_soubory"] == ["https://priklad.cz/static/main.css"]

    top = {b["hex"]: b for b in n["barvy"]["top"]}
    assert top["#9b36f7"]["pocet"] >= 5          # hex velké/malé + rgb() + inline styl
    assert top["#9b36f7"]["neutralni"] is False
    assert top["#ffffff"]["neutralni"] is True
    promenne = {p["promenna"]: p["hex"] for p in n["barvy"]["promenne"]}
    assert promenne == {"--brand": "#9b36f7", "--cta": "#140328"}

    pouzite = {f["nazev"] for f in n["fonty"]["pouzite"]}
    assert pouzite == {"Poppins"}                 # Arial a sans-serif jsou generické
    assert n["fonty"]["google"] == ["Inter", "Poppins"]
    assert n["fonty"]["font_face"][0]["nazev"] == "Poppins"

    duvody = [k["duvod"] for k in n["loga"]]
    assert any("logo" in d for d in duvody)
    assert n["loga"][0]["skore"] >= 6            # img s logem v hlavičce, nebo inline svg s logo
    ulozene = sorted(p.name for p in (tmp_path / "loga").iterdir())
    assert any(s.endswith(".svg") for s in ulozene)
    assert (tmp_path / "nalez.json").exists() and (tmp_path / "styly.css").exists()


def test_chyba_stazeni(monkeypatch):
    monkeypatch.setattr(web_znacka, "stahni", lambda *a, **k: None)
    n = web_znacka.analyzuj("https://nedostupne.example")
    assert "chyba" in n
    assert "nedostupne.example" in web_znacka.shrnuti(n)


def test_shrnuti_je_citelne(monkeypatch):
    monkeypatch.setattr(web_znacka, "stahni", _mock_stahni)
    n = web_znacka.analyzuj("priklad.cz")
    s = web_znacka.shrnuti(n)
    assert "#9b36f7" in s and "Poppins" in s and "Kandidáti na logo" in s
    assert "_markup" not in s


def test_norm_hex():
    assert web_znacka._norm_hex("abc") == "#aabbcc"
    assert web_znacka._norm_hex("AABBCCDD") == "#aabbcc"
    assert web_znacka._norm_hex("abcde") is None


SVG_HTML = """<html><head><title>X</title></head><body><header>
<svg class="logo" viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g"><stop offset="0"/><stop offset="1"/></linearGradient></defs>
<path d="M0 0h10v10z" fill="url(#g)"/><rect width="1" height="1"></rect>
</svg></header></body></html>"""


def test_inline_svg_je_platne_xml(monkeypatch, tmp_path):
    import xml.dom.minidom as m
    monkeypatch.setattr(web_znacka, "stahni", lambda url, limit, binarni=False, duvod=None: (SVG_HTML, url, "text/html"))
    n = web_znacka.analyzuj("priklad.cz", str(tmp_path))
    soubory = [k["soubor"] for k in n["loga"] if k.get("soubor", "").endswith("inline.svg")]
    assert soubory, "inline SVG z hlavičky se nezachytilo"
    text = open(soubory[0], encoding="utf-8").read()
    assert "</path>" not in text and "</stop>" not in text          # samouzavírací zůstanou samouzavírací
    assert "</linearGradient>" in text and "</lineargradient>" not in text
    m.parseString(text)                                              # platné XML


def test_chyba_stazeni_rika_duvod(monkeypatch):
    """Na firemní síti je rozdíl mezi blokací webu a proxy s podvrženým
    certifikátem — lektor to musí poznat z jedné věty."""
    def stahni(url, limit, binarni=False, duvod=None):
        duvod.append("URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]>")
        return None

    monkeypatch.setattr(web_znacka, "stahni", stahni)
    assert "CERTIFICATE_VERIFY_FAILED" in web_znacka.analyzuj("priklad.cz")["chyba"]


def test_vypis_prezije_vystup_v_cp1250():
    """Na české Windows jde výstup do roury v cp1250; šipka ve shrnutí v něm
    není a print by spadl až po stažení celého webu."""
    import os
    import subprocess

    kod = (
        "import sys; sys.path.insert(0, sys.argv[1]); import web_znacka as w;"
        "w.analyzuj = lambda url, out: {'url': url, 'nazev': 'Firma ✓', 'theme_color': None,"
        "'css_soubory': [], 'barvy': {'top': [], 'promenne': []},"
        "'fonty': {'pouzite': [], 'font_face': [], 'google': []},"
        "'loga': [{'skore': 5, 'duvod': 'img s logem', 'url': 'https://priklad.cz/logo.svg'}]};"
        "sys.exit(w.main(['priklad.cz']))"
    )
    r = subprocess.run([sys.executable, "-c", kod, str(Path(web_znacka.__file__).parent)],
                       capture_output=True, env={**os.environ, "PYTHONIOENCODING": "cp1250"})
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    assert "→ https://priklad.cz/logo.svg" in r.stdout.decode("utf-8")
