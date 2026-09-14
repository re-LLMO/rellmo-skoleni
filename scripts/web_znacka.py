#!/usr/bin/env python3
"""web_znacka.py — co jde o značce vyčíst z webu: loga, barvy, písma.

Stáhne domovskou stránku a její CSS, spočítá barvy, najde názvy písem a
kandidáty na logo, ty stáhne do složky. Nic neinterpretuje — vrátí četnosti
a zdroje, rozhodnutí je na člověku ve skillu. Jen standardní knihovna.

Použití:
    python3 web_znacka.py https://priklad.cz --out brandkit/_web
Vypíše shrnutí a zapíše `nalez.json` + stažená loga do `--out`.
"""
import argparse
import colorsys
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
MAX_HTML = 3_000_000
MAX_CSS = 2_000_000
MAX_LOGO = 2_000_000
MAX_CSS_SOUBORU = 12
MAX_LOG = 8
TIMEOUT = 15

GENERICKA_PISMA = {
    "sans-serif", "serif", "monospace", "system-ui", "inherit", "initial", "unset",
    "-apple-system", "blinkmacsystemfont", "segoe ui", "ui-sans-serif", "ui-serif",
    "ui-monospace", "cursive", "fantasy", "emoji", "math", "fangsong", "helvetica neue",
    "helvetica", "arial", "apple color emoji", "segoe ui emoji", "segoe ui symbol",
    "noto color emoji", "var(--font-sans)", "revert",
}


def stahni(url: str, limit: int, binarni: bool = False):
    """Vrátí (bytes|str, finální URL, content-type). Chyby vrací jako None."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "cs,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = r.read(limit + 1)
            ct = r.headers.get("Content-Type", "")
            fin = r.geturl()
    except Exception:
        return None
    if len(data) > limit:
        return None
    if binarni:
        return data, fin, ct
    m = re.search(r"charset=([\w-]+)", ct or "")
    for enc in ([m.group(1)] if m else []) + ["utf-8", "cp1250", "latin-1"]:
        try:
            return data.decode(enc), fin, ct
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", errors="ignore"), fin, ct


class _Parser(HTMLParser):
    """Sbírá odkazy na CSS, inline styly, meta, obrázky a inline SVG."""

    def __init__(self):
        super().__init__()
        self.css_odkazy = []
        self.inline_css = []
        self.google_fonts = []
        self.meta = {}
        self.obrazky = []          # (src, alt, class, id, v_hlavicce)
        self.svg = []              # (markup, class, v_hlavicce)
        self.ikony = []            # (rel, href)
        self.title = ""
        self._v_style = False
        self._v_title = False
        self._hloubka_header = 0
        self._svg_buf = None
        self._svg_attrs = None
        self._svg_stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "header" or (tag in ("div", "nav") and re.search(r"header|navbar|topbar", (a.get("class") or "") + " " + (a.get("id") or ""), re.I)):
            self._hloubka_header += 1
        if tag == "link":
            rel = (a.get("rel") or "").lower()
            href = a.get("href") or ""
            if "stylesheet" in rel and href:
                if "fonts.googleapis.com" in href:
                    self.google_fonts.append(href)
                else:
                    self.css_odkazy.append(href)
            if "icon" in rel and href:
                self.ikony.append((rel, href))
        elif tag == "style":
            self._v_style = True
        elif tag == "title":
            self._v_title = True
        elif tag == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if n in ("theme-color", "og:site_name", "og:image", "application-name"):
                self.meta[n] = a.get("content") or ""
        elif tag == "img":
            self.obrazky.append((a.get("src") or a.get("data-src") or "", a.get("alt") or "",
                                 a.get("class") or "", a.get("id") or "", self._hloubka_header > 0))
        elif tag == "svg" and self._svg_buf is None:
            self._svg_buf = [self.get_starttag_text()]
            self._svg_stack = ["svg"]
            self._svg_attrs = (a.get("class") or "", self._hloubka_header > 0, a.get("aria-label") or "")
        elif self._svg_buf is not None:
            raw = self.get_starttag_text()
            self._svg_buf.append(raw)
            # HTMLParser názvy značek zmenšuje; SVG je XML a `linearGradient`
            # potřebuje stejnou velikost písmen i v uzavírací značce.
            m = re.match(r"<\s*([\w:.-]+)", raw)
            if not raw.rstrip().endswith("/>"):
                self._svg_stack.append(m.group(1) if m else tag)
        if tag == "style" and a.get("style"):
            pass
        if a.get("style"):
            self.inline_css.append(a["style"])

    def handle_endtag(self, tag):
        if tag == "header" and self._hloubka_header:
            self._hloubka_header -= 1
        if tag == "style":
            self._v_style = False
        if tag == "title":
            self._v_title = False
        if self._svg_buf is not None:
            raw = self._svg_stack.pop() if self._svg_stack else tag
            self._svg_buf.append(f"</{raw}>")
            if tag == "svg" and not self._svg_stack:
                cls, v_hl, label = self._svg_attrs
                self.svg.append(("".join(self._svg_buf), cls, v_hl, label))
                self._svg_buf = None

    def handle_startendtag(self, tag, attrs):
        # Samouzavírací značka (`<path …/>`): uvnitř SVG se zapíše jen jednou,
        # bez dodatečného `</path>` — jinak by výsledek nebyl platné XML.
        if self._svg_buf is not None and tag != "svg":
            self._svg_buf.append(self.get_starttag_text())
            return
        self.handle_starttag(tag, attrs)
        if tag not in ("link", "meta", "img"):
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self._v_style:
            self.inline_css.append(data)
        if self._v_title:
            self.title += data
        if self._svg_buf is not None:
            self._svg_buf.append(data)


# ---------- barvy ----------

def _norm_hex(h: str):
    h = h.lstrip("#").lower()
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    elif len(h) == 8:
        h = h[:6]
    elif len(h) != 6:
        return None
    return "#" + h


def _neutralni(hexa: str) -> bool:
    r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return s < 0.12 or l > 0.96 or l < 0.06


def barvy(css: str) -> dict:
    """Četnost barev v CSS + pojmenované CSS proměnné s barvou."""
    pocty = Counter()
    for m in re.finditer(r"#([0-9a-fA-F]{3,8})\b", css):
        n = _norm_hex(m.group(1))
        if n:
            pocty[n] += 1
    for m in re.finditer(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", css):
        r, g, b = (min(255, int(x)) for x in m.groups())
        pocty[f"#{r:02x}{g:02x}{b:02x}"] += 1
    promenne = []
    for m in re.finditer(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))", css):
        val = m.group(2)
        if val.startswith("#"):
            n = _norm_hex(val)
        else:
            mm = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", val)
            n = f"#{int(mm.group(1)):02x}{int(mm.group(2)):02x}{int(mm.group(3)):02x}" if mm else None
        if n:
            promenne.append({"promenna": m.group(1), "hex": n})
    videne = set()
    promenne = [p for p in promenne if not (p["promenna"], p["hex"]) in videne and not videne.add((p["promenna"], p["hex"]))]
    top = [{"hex": h, "pocet": c, "neutralni": _neutralni(h)} for h, c in pocty.most_common(40)]
    return {"promenne": promenne[:40], "top": top}


# ---------- písma ----------

def _rodina(hodnota: str):
    prvni = hodnota.split(",")[0].strip().strip("'\"").strip()
    if not prvni or prvni.lower() in GENERICKA_PISMA or prvni.startswith("var("):
        return None
    return prvni


def fonty(css: str, google_odkazy) -> dict:
    pouzite = Counter()
    for m in re.finditer(r"font-family\s*:\s*([^;}{]+)", css, re.I):
        r = _rodina(m.group(1))
        if r:
            pouzite[r] += 1
    face = []
    for blok in re.finditer(r"@font-face\s*{([^}]*)}", css, re.I | re.S):
        t = blok.group(1)
        fam = re.search(r"font-family\s*:\s*([^;]+)", t, re.I)
        src = re.findall(r"url\(([^)]+)\)", t)
        w = re.search(r"font-weight\s*:\s*([^;]+)", t, re.I)
        if fam:
            face.append({"nazev": fam.group(1).strip().strip("'\""), "rez": (w.group(1).strip() if w else ""),
                         "src": [s.strip("'\" ") for s in src][:2]})
    google = []
    for href in google_odkazy:
        q = urllib.parse.urlparse(href).query
        for fam in re.findall(r"family=([^&]+)", q):
            google.append(urllib.parse.unquote(fam).split(":")[0].replace("+", " "))
    return {"pouzite": [{"nazev": n, "pocet": c} for n, c in pouzite.most_common(12)],
            "font_face": face[:20], "google": sorted(set(google))}


# ---------- loga ----------

def kandidati_loga(p: _Parser, base: str) -> list:
    out = []

    def pridej(url, duvod, skore):
        if not url or url.startswith("data:"):
            return
        absu = urllib.parse.urljoin(base, url)
        if any(k["url"] == absu for k in out):
            return
        out.append({"url": absu, "duvod": duvod, "skore": skore, "soubor": None})

    for src, alt, cls, iid, v_hl in p.obrazky:
        text = " ".join([src, alt, cls, iid]).lower()
        if "logo" in text:
            pridej(src, "img s „logo“ v atributech" + (" v hlavičce" if v_hl else ""), 5 + (2 if v_hl else 0))
        elif v_hl and src.lower().endswith((".svg", ".png")):
            pridej(src, "obrázek v hlavičce", 3)
    for rel, href in p.ikony:
        pridej(href, f"ikona ({rel})", 2 if "apple" in rel else 1)
    if p.meta.get("og:image"):
        pridej(p.meta["og:image"], "og:image (často logo nebo cover)", 1)
    for i, (markup, cls, v_hl, label) in enumerate(p.svg):
        text = (cls + " " + label).lower()
        if "logo" in text or v_hl:
            out.append({"url": None, "duvod": "inline SVG" + (" s „logo“" if "logo" in text else " v hlavičce"),
                        "skore": 6 if "logo" in text else 3, "soubor": None, "_markup": markup, "_i": i})
    out.sort(key=lambda k: -k["skore"])
    return out[:MAX_LOG]


def _pripona(url: str, ct: str) -> str:
    cesta = urllib.parse.urlparse(url).path.lower()
    for e in (".svg", ".png", ".jpg", ".jpeg", ".webp", ".ico", ".gif"):
        if cesta.endswith(e):
            return e
    ct = (ct or "").lower()
    if "svg" in ct:
        return ".svg"
    if "png" in ct:
        return ".png"
    if "jpeg" in ct or "jpg" in ct:
        return ".jpg"
    if "webp" in ct:
        return ".webp"
    return ".bin"


def stahni_loga(kandidati: list, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for i, k in enumerate(kandidati, 1):
        if k.get("_markup"):
            cesta = out / f"logo-{i:02d}-inline.svg"
            markup = k.pop("_markup")
            if "xmlns" not in markup[:200]:
                markup = markup.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
            cesta.write_text(markup, encoding="utf-8")
            k["soubor"] = str(cesta)
            k.pop("_i", None)
            continue
        r = stahni(k["url"], MAX_LOGO, binarni=True)
        if not r:
            k["chyba"] = "nestaženo (chyba, nebo přes 2 MB)"
            continue
        data, fin, ct = r
        cesta = out / f"logo-{i:02d}{_pripona(fin, ct)}"
        cesta.write_bytes(data)
        k["soubor"] = str(cesta)
        k["velikost_b"] = len(data)


# ---------- orchestrace ----------

def analyzuj(url: str, out_dir: str | None = None) -> dict:
    if not re.match(r"^https?://", url):
        url = "https://" + url
    r = stahni(url, MAX_HTML)
    if not r:
        return {"chyba": f"Nepodařilo se stáhnout {url} (blokace, přesměrování mimo web, nebo přes 3 MB)."}
    html, fin, _ = r
    p = _Parser()
    p.feed(html)
    css_text = "\n".join(p.inline_css)
    css_soubory = []
    for href in p.css_odkazy[:MAX_CSS_SOUBORU]:
        absu = urllib.parse.urljoin(fin, href)
        rr = stahni(absu, MAX_CSS)
        if rr:
            css_text += "\n" + rr[0]
            css_soubory.append(absu)
    nalez = {
        "url": fin,
        "nazev": (p.meta.get("og:site_name") or p.meta.get("application-name") or p.title.strip()[:120]),
        "title": p.title.strip()[:200],
        "theme_color": p.meta.get("theme-color"),
        "css_soubory": css_soubory,
        "barvy": barvy(css_text),
        "fonty": fonty(css_text, p.google_fonts),
        "loga": kandidati_loga(p, fin),
    }
    if out_dir:
        out = Path(out_dir)
        stahni_loga(nalez["loga"], out / "loga")
        (out / "styly.css").write_text(css_text, encoding="utf-8")
        (out / "nalez.json").write_text(json.dumps(nalez, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        for k in nalez["loga"]:
            k.pop("_markup", None)
            k.pop("_i", None)
    return nalez


def shrnuti(n: dict) -> str:
    if "chyba" in n:
        return n["chyba"]
    radky = [f"Web: {n['url']}  ·  název: {n['nazev'] or '—'}  ·  theme-color: {n['theme_color'] or '—'}",
             f"CSS souborů: {len(n['css_soubory'])}", "", "Barvy (nejčastější, bez šedých a bílé):"]
    barevne = [b for b in n["barvy"]["top"] if not b["neutralni"]][:8]
    for b in barevne:
        radky.append(f"  {b['hex']}  ×{b['pocet']}")
    if n["barvy"]["promenne"]:
        radky.append("CSS proměnné s barvou (prvních 12):")
        for pr in n["barvy"]["promenne"][:12]:
            radky.append(f"  {pr['promenna']}: {pr['hex']}")
    radky.append("")
    radky.append("Písma:")
    for f in n["fonty"]["pouzite"][:6]:
        radky.append(f"  {f['nazev']}  ×{f['pocet']}")
    if n["fonty"]["font_face"]:
        radky.append("  @font-face: " + ", ".join(sorted({f['nazev'] for f in n['fonty']['font_face']})))
    if n["fonty"]["google"]:
        radky.append("  Google Fonts: " + ", ".join(n["fonty"]["google"]))
    radky.append("")
    radky.append("Kandidáti na logo:")
    for k in n["loga"]:
        kde = k.get("soubor") or k.get("url") or "inline SVG"
        radky.append(f"  [{k['skore']}] {k['duvod']} → {kde}" + (f"  ({k['chyba']})" if k.get("chyba") else ""))
    if not n["loga"]:
        radky.append("  nic — logo si vyžádej od účastníka")
    return "\n".join(radky)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url")
    ap.add_argument("--out", help="složka pro nalez.json, styly.css a stažená loga")
    ap.add_argument("--json", action="store_true", help="vypsat celý nález jako JSON")
    a = ap.parse_args(argv)
    n = analyzuj(a.url, a.out)
    print(json.dumps(n, ensure_ascii=False, indent=2) if a.json else shrnuti(n))
    return 1 if "chyba" in n else 0


if __name__ == "__main__":
    sys.exit(main())
